// Hosted synthetic revisions only. Never publishes or runs a correction.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {chromium}=require('playwright');
const args=process.argv.slice(2),arg=n=>args[args.indexOf(n)+1],config=JSON.parse(fs.readFileSync(arg('--config'),'utf8'));
assert.ok(new URL(config.url).hostname.startsWith('schematica-review-validation.'));
const fixtures=JSON.parse(fs.readFileSync(arg('--fixtures'),'utf8')),output=arg('--output');fs.mkdirSync(output,{recursive:true});
(async()=>{
  const browser=await chromium.launch({headless:true,channel:'chrome'}),checks=[],errors=[];
  const check=(condition,name)=>{assert.ok(condition,name);checks.push(name);};
  async function session(){const context=await browser.newContext({viewport:{width:1440,height:1000}});
    assert.equal((await context.request.post(config.url+'/review/login',{headers:{Origin:config.url},data:{password:config.password}})).status(),200);
    if(args.includes('--local'))await context.route('**/*',route=>{const url=new URL(route.request().url()),files={'/review':'app/review/index.html','/review/review-app.js':'app/review/review-app.js','/review/review.css':'app/review/review.css','/review/review-tools.js':'app/review/review-tools.js'};return url.origin===config.url&&files[url.pathname]?route.fulfill({path:path.resolve(files[url.pathname])}):route.continue();});
    const page=await context.newPage();page.on('pageerror',e=>errors.push(e.stack));await page.goto(config.url+'/review');await page.locator('.symbol-top h2').waitFor();return {page,context};}
  const {page}=await session(),state=async(p=page)=>(await p.request.get(config.url+'/api/review/state')).json();
  async function action(name,value){const r=await page.request.post(config.url+'/api/review/actions/'+name,{headers:{Origin:config.url,'Idempotency-Key':crypto.randomUUID()},data:value});assert.equal(r.status(),200,await r.text());return r.json();}
  async function clickSave(selector,name){const response=page.waitForResponse(r=>r.url().endsWith('/actions/'+name)&&r.status()===200);await page.locator(selector).click();await response.catch(async e=>{throw Error(e.message+' '+await page.locator('#r-toast').innerText());});await page.waitForFunction(()=>!busy);}
  for(const key of ['image-a','image-b','question']){const s=(await state()).symbols[fixtures[key].symbol];if(s.discarded)await action('restore',{symbols:[s.id]});}
  const before=await state(),id=fixtures['image-a'].symbol,idB=fixtures['image-b'].symbol,latest=before.symbols[id].latest;
  async function updates(){await page.locator('#updates-button').click();await page.getByRole('heading',{name:'Ready to review',exact:false}).waitFor();}
  const expected=await page.evaluate(()=>ReviewTools.updates(data).ready.length);check(expected>=2,'Two independent completed corrections await review');
  await updates();check(await page.locator('[data-action=open-update]').count()===expected,'Badge counts revised symbols, not job events');
  await page.locator(`[data-action=open-update][data-value="${id}"]`).click();await page.waitForFunction(({id,rev})=>local.selected===id&&local.revision===rev,{id,rev:latest});
  await page.waitForResponse(r=>r.url().endsWith('/actions/seen')&&r.status()===200);
  check((await state()).symbols[id].selected!==latest,'Opening an update does not verify it');
  await page.reload();await page.locator('.symbol-top h2').waitFor();await updates();
  check((await page.locator(`[data-action=open-update][data-value="${id}"]`).locator('..').innerText()).includes('Seen · still needs review'),'Seen status survives reload and keeps the update');
  const second=await session();check((await state(second.page)).symbols[id].seenRevision===latest,'Seen status is shared with another device');
  await page.locator('[data-action=close-dialog]').click();
  await page.evaluate(async id=>{await select(id);await cursorSave;},id);
  await clickSave('.desktop-review-actions [data-action=discard]','discard');
  check((await state()).symbols[id].discarded,'Discard is saved');await clickSave('#r-undo','restore');
  check(!(await state()).symbols[id].discarded,'Undo restores a discarded correction');
  await clickSave('.desktop-review-actions [data-action=verify-next]','verify');await page.waitForFunction(()=>!busy&&!!undo);
  check((await state()).symbols[id].selected===latest,'Verify selects the exact returned revision');await clickSave('#r-undo','unverify');await page.waitForFunction(()=>!busy&&!undo);
  check((await state()).symbols[id].selected===before.symbols[id].selected,'Undo restores the previous exact verification');
  // Edit an old synthetic image comment; the original raster must remain in history.
  const comment=Object.values((await state()).comments).find(c=>c.targets.some(t=>t.symbol===id&&t.revision===fixtures['image-a'].revision)&&c.attachments?.length);
  assert.ok(comment);await action('comment',{comment:comment.id,expected:comment.edit,text:comment.text+' (synthetic history edit)',attachments:[],targets:comment.targets});
  await page.evaluate(async id=>{await refresh(true);await select(id);},id);await page.locator('[data-action=tab][data-value=history]').click();
  await page.locator('#history-list [data-action=comment-history]').first().click();await page.getByRole('heading',{name:'Comment history',exact:true}).waitFor();
  check(await page.locator('#dialog .comment-image img').count()>0,'Earlier comment edits retain their private images');
  await page.locator('#dialog [data-action=image]').first().click();check(await page.locator('#image-dialog img').isVisible(),'A removed historical attachment still enlarges');await page.locator('[data-action=close-image]').click();await page.locator('[data-action=close-dialog]').click();
  const question=Object.values((await state()).jobs).find(j=>j.status==='Needs your answer'&&j.corrections[0]?.symbol===fixtures.question.symbol);assert.ok(question);
  await updates();await page.locator(`[data-action=answer][data-value="${question.id}"]`).click();await page.locator('#question-answer').fill('For this synthetic fixture, shorten only the top bar to 75%. Keep the lower bars and lead unchanged.');
  await clickSave('[data-action=save-answer]','answer');await page.waitForFunction(()=>!busy&&modal==='updates');
  const answered=(await state()).jobs[question.id];check(answered.status==='Waiting for desktop'&&answered.answers.length===1,'A focused answer resumes the same authorized job without a plan gate');
  const failure=Object.values((await state()).jobs).find(j=>j.status==='Failed'&&j.corrections[0]?.symbol===fixtures.failure.symbol);assert.ok(failure);
  await clickSave(`[data-action=retry][data-value="${failure.id}"]`,'retry');check((await state()).jobs[failure.id].status==='Waiting for desktop','Failed correction is retryable from Updates');
  await page.locator('[data-action=close-dialog]').click();
  // Deliver a real saved revision through polling after temporarily withholding it.
  const actual=await state(),earlier=structuredClone(actual);earlier.version--;earlier.symbols[idB].latest=fixtures['image-b'].revision;delete earlier.symbols[idB].updateRevision;
  for(const job of Object.values(earlier.jobs))job.results=job.results.filter(r=>r.symbol!==idB);
  let arrived=false;await page.route('**/api/review/state',route=>route.fulfill({json:arrived?actual:earlier}));
  await page.evaluate(async id=>{await refresh(true);await select(id);},id);await page.locator('#comment').fill('Unfinished local draft during a new arrival');await page.locator('#comment').focus();
  const position=await page.evaluate(()=>{window.testEditor=document.querySelector('#comment');window.scrollTo(0,180);return {x:scrollX,y:scrollY,revision:local.revision};});
  arrived=true;await page.evaluate(()=>refresh());
  check(await page.evaluate(p=>local.revision===p.revision&&document.querySelector('#comment')===window.testEditor&&document.activeElement===window.testEditor&&scrollX===p.x&&scrollY===p.y&&window.testEditor.value==='Unfinished local draft during a new arrival',position),'New arrivals preserve the exact drawing, editor, draft, focus and scroll');
  await page.unroute('**/api/review/state');await page.locator('#comment').fill('');await page.locator('#comment').blur();await updates();await page.screenshot({path:path.join(output,'updates-desktop.png')});
  assert.deepEqual(errors,[]);fs.writeFileSync(path.join(output,'results.json'),JSON.stringify({passed:checks.length,checks,productionWrites:0,publications:0},null,2));console.log(JSON.stringify({passed:checks.length}));await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
