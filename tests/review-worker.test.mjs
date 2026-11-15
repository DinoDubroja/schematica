import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../app/review/worker.mjs';

test('public Library review.js remains a public script while private Review assets require login', async()=>{
  const calls=[];
  const env={ASSETS:{fetch:async request=>{calls.push(new URL(request.url).pathname);return new Response('public script',{headers:{'Content-Type':'text/javascript'}});}}};
  const publicScript=await worker.fetch(new Request('https://example.test/review.js'),env);
  assert.equal(publicScript.status,200);
  assert.equal(await publicScript.text(),'public script');
  assert.deepEqual(calls,['/review.js']);
  for(const path of ['/review/review-app.js','/review/review.css','/api/review/state']) {
    const response=await worker.fetch(new Request('https://example.test'+path),env);
    assert.equal(response.status,401,path);
  }
  assert.deepEqual(calls,['/review.js']);
});
