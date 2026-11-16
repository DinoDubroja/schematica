import test from 'node:test';
import assert from 'node:assert/strict';
import {initial,transition,processingSummary,commentProgress,commentToken,stale} from '../app/review/domain.mjs';
let serial=0;
const step=(state,action,input={},actor='user')=>transition(state,action,input,{actor,now:'2026-11-16T15:00:00Z',id:`action-${++serial}`});
const revision=(id,number=1,parent=null)=>({id:`${id}-${number}`,parent,symbol:{id,name:id,revision:number},change:{why:'Synthetic correction'}});
const target=(id,number=1)=>({symbol:id,revision:`${id}-${number}`,configurations:[]});
async function fixture(){let s=initial();for(const id of ['npn','pnp','other'])s=(await step(s,'upload',{revision:revision(id)},'desktop')).state;return s;}
async function comment(s,ids=['npn','pnp']){return step(s,'comment',{text:'Keep the lead; change only the arrow.',targets:ids.map(id=>target(id)),attachments:[{hash:'a'.repeat(64),mime:'image/png',bytes:100,name:'reference.png'}]});}
async function confirm(s,plan,included){plan??=await processingSummary(s);included??=[...plan.corrections,...plan.publications].map(t=>t.key);return step(s,'process',{snapshot:plan.snapshot,included});}
async function claim(s){return step(s,'claim',{protocol:2},'desktop');}
async function finish(s,job){s=(await step(s,'upload',{job:job.id,lease:job.lease,revision:revision(job.corrections[0].symbol,2,job.corrections[0].revision)},'desktop')).state;return (await step(s,'complete',{job:job.id,lease:job.lease},'desktop')).state;}

test('preparing a summary never queues work; only exact confirmed included choices execute',async()=>{
  let s=(await comment(await fixture())).state;s=(await step(s,'verify',{symbol:'other',revision:'other-1'})).state;
  const copy=structuredClone(s),plan=await processingSummary(s);assert.deepEqual(s,copy);assert.equal(plan.corrections.length,2);assert.equal(plan.publications.length,1);
  await assert.rejects(step(s,'process',{}),/summary/);
  const result=await confirm(s,plan,[plan.corrections[0].key]);assert.equal(Object.keys(result.state.jobs).length,1);assert.equal(result.state.symbols.other.published,null);
  assert.equal(result.state.comments[Object.keys(s.comments)[0]].targets.length,2,'Excluding the second symbol does not delete its feedback');
  await assert.rejects(confirm(result.state,plan,[plan.corrections[0].key]),/changed/);
  assert.equal((await processingSummary(result.state)).corrections.length,1,'Newly queued work is excluded from a fresh summary');
});

test('new arrivals, comment edits, images and verification changes invalidate prepared summaries',async()=>{
  const s=(await comment(await fixture(),['npn'])).state,plan=await processingSummary(s),c=Object.values(s.comments)[0];
  const changes=[
    ['comment',{text:'Additional request',targets:[target('other')]}],
    ['comment',{comment:c.id,expected:c.edit,text:c.text,targets:c.targets,attachments:[{...c.attachments[0],hash:'b'.repeat(64)}]}],
    ['verify',{symbol:'npn',revision:'npn-1'}],
    ['upload',{revision:revision('npn',2,'npn-1')},'desktop'],
  ];
  for(const [action,input,actor] of changes){const next=(await step(s,action,input,actor)).state;await assert.rejects(confirm(next,plan),/changed/);assert.equal(Object.keys(next.jobs).length,0);}
});

test('adding PNP to a processed NPN comment retains its independent completed result',async()=>{
  let saved=await comment(await fixture(),['npn']),s=saved.state,c=s.comments[saved.result.id];
  s=(await confirm(s)).state;const claimed=await claim(s);s=await finish(claimed.state,claimed.result.job);
  const original=commentToken(c,target('npn'));
  s=(await step(s,'comment-extend',{comment:c.id,expected:c.edit,targets:[target('pnp')]})).state;c=s.comments[c.id];
  assert.equal(commentToken(c,target('npn')),original);assert.equal(commentProgress(s,c,target('npn')).status,'Updated');assert.equal(commentProgress(s,c,target('pnp')).status,'Pending');
  assert.deepEqual((await processingSummary(s)).corrections.map(t=>t.symbol),['pnp']);
  s=(await confirm(s)).state;assert.equal((await claim(s)).result.job.corrections[0].symbol,'pnp');
  assert.equal(s.symbols.npn.revisions.length,2);assert.equal(s.symbols.npn.selected,null);
});

test('adding a target while NPN is working does not invalidate that independent job',async()=>{
  let saved=await comment(await fixture(),['npn']),s=saved.state,c=s.comments[saved.result.id];s=(await confirm(s)).state;
  const claimed=await claim(s);s=claimed.state;const job=claimed.result.job;
  s=(await step(s,'comment-extend',{comment:c.id,expected:c.edit,targets:[target('pnp')]})).state;
  assert.equal(await stale(s,s.jobs[job.id]),false);assert.deepEqual((await processingSummary(s)).corrections.map(t=>t.symbol),['pnp']);
});

test('one failure retries independently while successful shared feedback stays completed',async()=>{
  let saved=await comment(await fixture()),s=(await confirm(saved.state)).state;
  let claimed=await claim(s);s=await finish(claimed.state,claimed.result.job);
  claimed=await claim(s);s=(await step(claimed.state,'fail',{job:claimed.result.job.id,lease:claimed.result.job.lease,error:'Synthetic failure'},'desktop')).state;
  const c=s.comments[saved.result.id];assert.equal(commentProgress(s,c,target('npn')).status,'Updated');assert.equal(commentProgress(s,c,target('pnp')).status,'Failed');
  const plan=await processingSummary(s);assert.deepEqual(plan.corrections.map(t=>t.symbol),['pnp']);
  const retried=await confirm(s,plan);assert.equal(Object.keys(retried.state.jobs).length,2);assert.deepEqual(retried.result.existing,[claimed.result.job.id]);
  assert.equal((await claim(retried.state)).result.job.corrections[0].symbol,'pnp');
});

test('text edits preserve original targets and only an explicit new target change gets a new token',async()=>{
  let saved=await comment(await fixture()),s=saved.state,c=s.comments[saved.result.id],token=commentToken(c,target('npn'));
  s=(await step(s,'comment',{comment:c.id,expected:c.edit,text:c.text,targets:c.targets})).state;c=s.comments[c.id];assert.equal(commentToken(c,target('npn')),token);
  s=(await step(s,'comment',{comment:c.id,expected:c.edit,text:'A new requested change',targets:c.targets})).state;c=s.comments[c.id];assert.notEqual(commentToken(c,target('npn')),token);assert.equal(c.originalTargets.length,2);
});

test('feedback can reopen a published-only symbol while its exact approval and publication remain intact',async()=>{
  let s=await fixture();Object.assign(s.symbols.npn,{candidate:false,selected:'npn-1',published:'npn-1',confirmed:true});
  s=(await comment(s,['npn'])).state;assert.equal(s.symbols.npn.candidate,true);
  assert.equal(s.symbols.npn.selected,'npn-1');assert.equal(s.symbols.npn.published,'npn-1');
  const plan=await processingSummary(s);assert.equal(plan.publications.length,0);assert.equal(plan.corrections.length,1);
  s=(await confirm(s,plan)).state;const claimed=await claim(s);s=await finish(claimed.state,claimed.result.job);
  assert.equal(s.symbols.npn.latest,'npn-2');assert.equal(s.symbols.npn.selected,'npn-1');assert.equal(s.symbols.npn.published,'npn-1');assert.equal(s.symbols.npn.confirmed,true);
});
