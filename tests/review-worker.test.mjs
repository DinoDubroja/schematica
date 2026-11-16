import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../app/review/worker.mjs';
import {hash} from '../app/review/domain.mjs';

test('private document replaces public asset CSP so local image drafts render without relaxing scripts',async()=>{
  const env={DESKTOP_TOKEN_HASH:await hash('fixture-token'),ASSETS:{fetch:async()=>new Response('<html>Review</html>',{headers:{'Content-Security-Policy':"default-src 'self'; img-src 'self'",'Cache-Control':'public,max-age=86400'}})}};
  const response=await worker.fetch(new Request('https://example.test/review',{headers:{Authorization:'Bearer fixture-token'}}),env),policy=response.headers.get('content-security-policy');
  assert.equal(response.status,200);assert.equal(policy.split('default-src').length,2);
  assert.match(policy,/img-src 'self' data: blob:/);assert.match(policy,/script-src 'self';/);
  assert.equal(response.headers.get('cache-control'),'private, no-store');
});

test('public Library review.js remains a public script while private Review assets require login', async()=>{
  const calls=[];
  const env={ASSETS:{fetch:async request=>{calls.push(new URL(request.url).pathname);return new Response('public script',{headers:{'Content-Type':'text/javascript'}});}}};
  const publicScript=await worker.fetch(new Request('https://example.test/review.js'),env);
  assert.equal(publicScript.status,200);
  assert.equal(await publicScript.text(),'public script');
  assert.deepEqual(calls,['/review.js']);
  for(const path of ['/review/review-app.js','/review/review.css','/review/review-tools.js','/review/review-workflow.js','/api/review/state','/api/review/candidate-previews','/api/review/processing-summary','/api/review/timeline/test','/review/images/'+'a'.repeat(64),'/api/review/images']) {
    const response=await worker.fetch(new Request('https://example.test'+path),env);
    assert.equal(response.status,401,path);
  }
  assert.deepEqual(calls,['/review.js']);
});
