import test from 'node:test';
import assert from 'node:assert/strict';
import {initial,transition,signature} from '../app/review/domain.mjs';
import {validateImage} from '../app/review/images.mjs';
let serial=0;
const at='2026-11-16T12:00:00Z';
const act=(s,a,v={},actor='user',now=at)=>transition(s,a,v,{actor,now,id:`event-${++serial}`});
const rev=(symbol,id,parent=null)=>({id,parent,fingerprint:'test',symbol:{id:symbol,name:symbol},change:{why:'Shortened the top bar'}});
async function fixture(){let s=initial();for(const id of ['one','two','three'])s=(await act(s,'upload',{revision:rev(id,id+'-1')},'desktop')).state;return s;}
const comment=(s,id,text='Shorten the top bar',attachments=[])=>act(s,'comment',{text,attachments,targets:[{symbol:id,revision:id+'-1'}]});
test('Process Review directly authorizes separate jobs and suppresses duplicate submissions',async()=>{
  let s=await fixture();s=(await comment(s,'one')).state;s=(await comment(s,'two')).state;
  let queued=await act(s,'process');s=queued.state;assert.equal(queued.result.ids.length,2);
  assert.ok(queued.result.ids.every(id=>!/[<>:"/\\|?*]/.test(id)),'Job IDs must be safe on Windows');
  assert.ok(queued.result.ids.every(id=>s.jobs[id].workflow===2&&s.jobs[id].authorized&&s.jobs[id].phase==='correct'));
  assert.equal((await act(s,'process')).result.ids.length,0);
  assert.equal((await act(s,'claim',{},'desktop')).result.job,null,'Old desktop cannot claim the new protocol');
  let claim=await act(s,'claim',{protocol:2},'desktop');s=claim.state;let job=claim.result.job;
  s=(await act(s,'upload',{job:job.id,lease:job.lease,revision:rev('one','one-2','one-1')},'desktop')).state;
  assert.equal(s.symbols.one.selected,null);assert.equal(s.symbols.one.published,null);
  s=(await act(s,'complete',{job:job.id,lease:job.lease},'desktop')).state;
  assert.equal(s.jobs[job.id].status,'Ready to review');
  claim=await act(s,'claim',{protocol:2},'desktop');assert.equal(claim.result.job.corrections[0].symbol,'two');
});
test('one clarification does not block independent work; the answer resumes only that exact source',async()=>{
  let s=await fixture();s=(await comment(s,'one')).state;s=(await comment(s,'two')).state;s=(await act(s,'process')).state;
  let claim=await act(s,'claim',{protocol:2},'desktop');s=claim.state;const job=claim.result.job;
  s=(await act(s,'question',{job:job.id,lease:job.lease,question:'Which bar should be shortened?'},'desktop')).state;
  assert.equal(s.jobs[job.id].status,'Needs your answer');
  claim=await act(s,'claim',{protocol:2},'desktop');s=claim.state;assert.equal(claim.result.job.corrections[0].symbol,'two');
  const q=s.jobs[job.id].question.id;s=(await act(s,'answer',{job:job.id,question:q,text:'Only the top bar.'})).state;
  assert.equal(s.jobs[job.id].status,'Waiting for desktop');assert.equal(s.jobs[job.id].corrections[0].comments.length,2);
  await assert.rejects(act(s,'answer',{job:job.id,question:q,text:'Late answer'}),/Question changed/);
});
test('image edits invalidate work; stale work cannot overwrite a new source or stop other jobs',async()=>{
  let s=await fixture();const image={hash:'a'.repeat(64),mime:'image/png',bytes:120,name:'reference.png'};
  s=(await comment(s,'one','',[image])).state;s=(await comment(s,'two')).state;
  const before=await signature(s,'one','one-1');s=(await act(s,'process')).state;
  let claim=await act(s,'claim',{protocol:2},'desktop');s=claim.state;const job=claim.result.job;
  const c=Object.values(s.comments).find(c=>c.targets[0].symbol==='one');
  s=(await act(s,'comment',{comment:c.id,expected:c.edit,text:'Use this instead',attachments:[{...image,hash:'b'.repeat(64)}],targets:c.targets})).state;
  assert.notEqual(await signature(s,'one','one-1'),before);assert.deepEqual(s.comments[c.id].originalAttachments,[image]);
  await assert.rejects(act(s,'upload',{job:job.id,lease:job.lease,revision:rev('one','one-2','one-1')},'desktop'),/stale/);
  claim=await act(s,'claim',{protocol:2},'desktop','2026-11-16T12:04:00Z');
  assert.equal(claim.result.job.corrections[0].symbol,'two');assert.equal(claim.state.jobs[job.id].status,'Stale');
});
test('seen updates persist separately from verification and old publication',async()=>{
  let s=await fixture();s.symbols.one.selected='one-1';s.symbols.one.published='one-1';
  s=(await act(s,'upload',{revision:rev('one','one-2','one-1')},'desktop')).state;
  s=(await act(s,'seen',{symbol:'one',revision:'one-2'})).state;
  assert.equal(s.symbols.one.seenRevision,'one-2');assert.equal(s.symbols.one.updateRevision,'one-2');
  assert.equal(s.symbols.one.selected,'one-1');assert.equal(s.symbols.one.published,'one-1');
});
test('failures stay retryable, while old queued proposals remain inert',async()=>{
  let s=await fixture();s=(await comment(s,'one')).state;s=(await act(s,'process')).state;
  let claim=await act(s,'claim',{protocol:2},'desktop');s=claim.state;const j=claim.result.job;
  s=(await act(s,'fail',{job:j.id,lease:j.lease,error:'Temporary renderer failure'},'desktop')).state;
  assert.equal((await act(s,'process')).result.ids.length,0);
  s=(await act(s,'retry',{job:j.id})).state;assert.equal(s.jobs[j.id].status,'Waiting for desktop');
  delete s.jobs[j.id].workflow;delete s.jobs[j.id].authorized;s.jobs[j.id].phase='prepare';
  assert.equal((await act(s,'claim',{protocol:2},'desktop')).result.job,null);
});
test('image validation rejects active formats, oversize data, forged metadata and dimensions',async()=>{
  const raw=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=','base64');
  const hash=Buffer.from(await crypto.subtle.digest('SHA-256',raw)).toString('hex');
  const input={hash,mime:'image/png',body:raw.toString('base64')};
  assert.equal((await validateImage(input)).width,1);
  const full=Buffer.alloc(1048576);raw.copy(full);
  assert.equal((await validateImage({mime:'image/png',body:full.toString('base64'),hash:Buffer.from(await crypto.subtle.digest('SHA-256',full)).toString('hex')})).bytes,1048576);
  await assert.rejects(validateImage({...input,mime:'image/svg+xml'}),/Choose/);
  await assert.rejects(validateImage({...input,hash:'a'.repeat(64)}),/checksum/);
  await assert.rejects(validateImage({...input,body:'A'.repeat(1500000)}),/exceeds/);
  const large=Buffer.from(raw);large.writeUInt32BE(100000,16);
  await assert.rejects(validateImage({...input,body:large.toString('base64')}),/dimensions/);
});
