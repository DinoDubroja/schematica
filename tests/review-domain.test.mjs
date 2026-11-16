import test from 'node:test';
import assert from 'node:assert/strict';
import {initial,transition,signature,stale} from '../app/review/domain.mjs';
import {validateSVG} from '../app/review/worker.mjs';
let serial=0;
const now='2026-11-15T23:00:00Z';
const change=(s,a,i={},actor='user',at=now)=>transition(s,a,a==='claim'?{protocol:2,...i}:i,{actor,now:at,id:`event-${++serial}`});
const rev=(id,parent=null,migration=false)=>({id,parent,migration,fingerprint:'test',symbol:{id:'fixture',name:'Fixture',family:'Tests'},batch:'Validation'});
async function fixture(){return (await change(initial(),'upload',{revision:rev('r1')},'desktop')).state;}
test('new uploads preserve exact older verification and published predecessor',async()=>{
  let s=(await change(initial(),'upload',{revision:rev('r1',null,true)},'desktop')).state;
  s=(await change(s,'upload',{revision:rev('r2','r1')},'desktop')).state;
  assert.equal(s.symbols.fixture.published,'r1');assert.equal(s.symbols.fixture.selected,'r1');
  s=(await change(s,'verify',{symbol:'fixture',revision:'r1'})).state;
  assert.equal(s.symbols.fixture.selected,'r1');assert.equal(s.symbols.fixture.latest,'r2');
});
test('discard and restore preserve assets and publication',async()=>{
  let s=(await change(initial(),'upload',{revision:rev('r1',null,true)},'desktop')).state;
  s=(await change(s,'discard',{symbols:['fixture']})).state;assert.equal(s.symbols.fixture.published,'r1');
  await assert.rejects(change(s,'verify',{symbol:'fixture',revision:'r1'}),/Restore/);
  s=(await change(s,'restore',{symbols:['fixture']})).state;assert.equal(s.symbols.fixture.discarded,false);
});
test('comment edits preserve original text and targets and reject stale edits',async()=>{
  let s=await fixture();const first=await change(s,'comment',{text:'Shorten bars',targets:[{symbol:'fixture',revision:'r1',configurations:['small-thick']}]});s=first.state;
  const id=first.result.id,old=s.comments[id];s=(await change(s,'comment',{comment:id,expected:old.edit,text:'Shorten only outer bars',targets:old.targets})).state;
  assert.equal(s.comments[id].originalText,'Shorten bars');assert.deepEqual(s.comments[id].originalTargets,old.targets);
  await assert.rejects(change(s,'comment',{comment:id,expected:old.edit,text:'Stale edit',targets:old.targets}),/changed/);
});
test('shared targets are explicit, unique and tied to saved revisions',async()=>{
  const s=await fixture();await assert.rejects(change(s,'comment',{text:'x',targets:[]}),/targets/);
  await assert.rejects(change(s,'comment',{text:'x',targets:[{symbol:'fixture',revision:'r9'}]}),/Revision/);
  await assert.rejects(change(s,'comment',{text:'x',targets:[{symbol:'fixture',revision:'r1'},{symbol:'fixture',revision:'r1'}]}),/Duplicate/);
});
async function proposal(){let s=await fixture();s=(await change(s,'comment',{text:'Shorten bars',targets:[{symbol:'fixture',revision:'r1'}]})).state;
  const queued=await change(s,'process');s=queued.state;const job=s.jobs[queued.result.id];
  // A preserved legacy proposal which was already being prepared before upgrade.
  delete job.workflow;delete job.authorized;job.phase='prepare';job.status='Working';job.lease='legacy';job.until='2026-11-15T23:03:00Z';
  s=(await change(s,'proposal',{job:job.id,lease:job.lease,changes:[{symbol:'fixture',revision:'r1',intent:'Shorten outer bars only'}]},'desktop')).state;return {s,id:job.id};}
test('Process Review leaves uncommented and discarded candidates unchanged',async()=>{
  const s=await fixture();await assert.rejects(change(s,'process'),/Nothing/);
  const {s:p,id}=await proposal();assert.equal(p.jobs[id].status,'Waiting for approval');assert.equal(p.symbols.fixture.latest,'r1');
  assert.equal((await change(p,'claim',{},'desktop')).result.job,null,'Old pending proposals must not execute');
});
test('feedback changes make proposal stale before approval',async()=>{
  let {s,id}=await proposal();s=(await change(s,'comment',{text:'Keep outer bars',targets:[{symbol:'fixture',revision:'r1'}]})).state;
  assert.equal(await stale(s,s.jobs[id]),true);
  await assert.rejects(change(s,'approve',{job:id,proposal:s.jobs[id].proposal.id}),/stale/);
});
test('approved exact correction returns unverified and can resume after its upload',async()=>{
  let {s,id}=await proposal();s=(await change(s,'approve',{job:id,proposal:s.jobs[id].proposal.id})).state;
  let claimed=await change(s,'claim',{},'desktop');s=claimed.state;const job=claimed.result.job;
  s=(await change(s,'upload',{job:id,lease:job.lease,revision:rev('r2','r1')},'desktop')).state;
  assert.equal(s.symbols.fixture.selected,null);assert.equal(await stale(s,s.jobs[id]),false);
  claimed=await change(s,'claim',{},'desktop','2026-11-15T23:04:00Z');s=claimed.state;
  assert.equal(claimed.result.job.results[0].revision,'r2');
  s=(await change(s,'complete',{job:id,lease:claimed.result.job.lease},'desktop','2026-11-15T23:04:01Z')).state;
  assert.equal(s.jobs[id].status,'Ready to review');
});
test('job lease prevents parallel execution and expires recoverably',async()=>{
  let s=await fixture();s=(await change(s,'verify',{symbol:'fixture',revision:'r1'})).state;s=(await change(s,'process')).state;
  const a=await change(s,'claim',{},'desktop');s=a.state;assert.equal((await change(s,'claim',{},'desktop')).result.job,null);
  const b=await change(s,'claim',{},'desktop','2026-11-15T23:04:00Z');assert.notEqual(a.result.job.lease,b.result.job.lease);
  await assert.rejects(change(b.state,'publication',{job:a.result.job.id,lease:a.result.job.lease,symbol:'fixture',revision:'r1'},'desktop','2026-11-15T23:04:00Z'),/lease/);
});
test('Verify does not publish; processing pins exact revision, then confirmation is separate',async()=>{
  let s=await fixture();s=(await change(s,'verify',{symbol:'fixture',revision:'r1'})).state;assert.equal(s.symbols.fixture.published,null);
  s=(await change(s,'process')).state;const c=await change(s,'claim',{},'desktop');s=c.state;const job=c.result.job;
  await assert.rejects(change(s,'publication',{job:job.id,lease:job.lease,symbol:'fixture',revision:'other'},'desktop'),/outside/);
  s=(await change(s,'publication',{job:job.id,lease:job.lease,symbol:'fixture',revision:'r1'},'desktop')).state;assert.equal(s.symbols.fixture.confirmed,false);
  s=(await change(s,'published',{job:job.id,lease:job.lease,symbol:'fixture',revision:'r1',proof:{catalog:'r1',assets:['hash']}},'desktop')).state;
  assert.equal(s.symbols.fixture.confirmed,true);
});
test('browser cannot impersonate desktop and desktop cannot approve',async()=>{
  const s=await fixture();await assert.rejects(change(s,'claim',{},'user'),/Desktop/);
  await assert.rejects(change(s,'verify',{symbol:'fixture',revision:'r1'},'desktop'),/Browser/);
});
test('SVG payloads reject active content and remote references',()=>{
  for(const svg of ['<svg><script>x</script></svg>','<svg onload="x"/>','<svg><image href="https://x"/></svg>','<svg><use href="https://x"/></svg>','<svg><path style="fill:url(https://x)"/></svg>','<!DOCTYPE svg><svg/>'])assert.throws(()=>validateSVG(svg));
  assert.doesNotThrow(()=>validateSVG('<svg xmlns="http://www.w3.org/2000/svg"><defs><path id="a"/></defs><use href="#a"/></svg>'));
});
