const test=require('node:test'),assert=require('node:assert/strict');
const {needsReview,nextCandidate,updates}=require('../app/review/review-tools.js');
const fixture=()=>({symbols:Object.fromEntries(['a','b','c','d'].map(id=>[id,{id,name:id,candidate:true,latest:id+'2',selected:null,updateRevision:id+'2'}])),comments:{},jobs:{}});
test('quick review skips verified, commented and discarded candidates, then completes',()=>{
  const s=fixture(),pool=Object.values(s.symbols);s.symbols.b.selected='b2';s.symbols.c.discarded=true;
  assert.equal(nextCandidate(s,pool,'a'),'d');s.comments.comment={targets:[{symbol:'d',revision:'d2'}]};
  assert.equal(nextCandidate(s,pool,'a'),null);assert.equal(needsReview(s,s.symbols.a),true);
});
test('an old approval or old-revision feedback never approves a new candidate',()=>{
  const s=fixture();s.symbols.a.selected='a1';s.comments.old={targets:[{symbol:'a',revision:'a1'}]};
  assert.equal(needsReview(s,s.symbols.a),true);assert.equal(updates(s).ready.length,4);
});
test('Updates counts symbols once, retains seen status and separates action from logs',()=>{
  const s=fixture();s.symbols.a.seenRevision='a2';
  s.jobs.done={id:'done',status:'Ready to review',results:[{symbol:'a',revision:'a2'}]};
  s.jobs.duplicate={...s.jobs.done,id:'duplicate'};
  s.jobs.work={id:'work',workflow:2,status:'Working',results:[]};
  s.jobs.question={id:'question',workflow:2,status:'Needs your answer',results:[]};
  let u=updates(s);assert.equal(u.ready.length,4);assert.equal(u.ready[0].seen,true);assert.equal(u.working.length,1);assert.equal(u.attention.length,1);
  s.symbols.a.selected='a2';u=updates(s);assert.equal(u.ready.length,3);
  s.jobs.legacy={id:'legacy',status:'Waiting for desktop',approved:{at:'earlier'},results:[]};
  assert.equal(updates(s).working.length,2,'An explicitly approved legacy job remains visible while queued');
});
