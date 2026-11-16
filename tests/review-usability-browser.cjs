// Full browser interactions on synthetic fixtures; refuses the production service.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {chromium}=require('playwright');
const args=process.argv.slice(2),arg=n=>args[args.indexOf(n)+1],config=JSON.parse(fs.readFileSync(arg('--config'),'utf8'));
assert.ok(new URL(config.url).hostname.startsWith('schematica-review-validation.'));
const fixtureRoot=arg('--fixtures'),fixtures=JSON.parse(fs.readFileSync(path.join(fixtureRoot,'fixtures.json'),'utf8')),output=arg('--output');
fs.mkdirSync(output,{recursive:true});
(async()=>{
  const browser=await chromium.launch({headless:true,channel:'chrome'}),checks=[],errors=[];
  const check=(ok,message)=>{assert.ok(ok,message);checks.push(message);};
  async function session(viewport){const context=await browser.newContext({viewport});
    const login=await context.request.post(config.url+'/review/login',{headers:{Origin:config.url},data:{password:config.password}});assert.equal(login.status(),200);
    if(args.includes('--local'))await context.route('**/*',route=>{const url=new URL(route.request().url()),files={'/review':'app/review/index.html','/review/review-app.js':'app/review/review-app.js','/review/review.css':'app/review/review.css','/review/review-tools.js':'app/review/review-tools.js','/review/review-workflow.js':'app/review/review-workflow.js','/preview-coordinates.js':'app/viewer/preview-coordinates.js'};return url.origin===config.url&&files[url.pathname]?route.fulfill({path:path.resolve(files[url.pathname])}):route.continue();});
    const page=await context.newPage();page.on('pageerror',e=>errors.push(e.stack));await page.goto(config.url+'/review');await page.locator('.symbol-top h2').waitFor();return {context,page};}
  const {context,page}=await session({width:1440,height:1000});
  const state=async(p=page)=>(await p.request.get(config.url+'/api/review/state')).json();
  const userAction=async(action,value,p=page)=>{const r=await p.request.post(config.url+'/api/review/actions/'+action,{headers:{Origin:config.url,'Idempotency-Key':crypto.randomUUID()},data:value});assert.equal(r.status(),200,await r.text());return r.json();};
  async function choose(key){if(await page.locator('.mobile-top').isVisible())await page.locator('[data-action=queue]').click();await page.locator('#batch').selectOption('all');
    const response=page.waitForResponse(r=>r.url().endsWith('/actions/cursor')&&r.request().method()==='POST'&&r.status()===200&&r.request().postDataJSON().symbol===fixtures[key].symbol);await page.locator(`[data-action=select][data-value="${fixtures[key].symbol}"]`).click();await response;await page.locator('.drawing-canvas image').waitFor();}
  // Reset only these three synthetic decisions, retaining their history.
  for(const key of ['fast-a','fast-b','fast-c']){const s=(await state()).symbols[fixtures[key].symbol];if(s.selected)await userAction('unverify',{symbol:s.id,expected:s.selected,previous:null});if(s.discarded)await userAction('restore',{symbols:[s.id]});}
  for(const key of ['image-a','image-b']){const s=(await state()).symbols[fixtures[key].symbol];if(s.discarded)await userAction('restore',{symbols:[s.id]});}
  await page.reload();await page.locator('.symbol-top h2').waitFor();await choose('fast-a');await page.locator('#batch').selectOption('Usability navigation');await page.setViewportSize({width:390,height:844});
  await page.locator('.symbol-top').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(output,'phone.png')});
  for(const [index,key] of ['fast-a','fast-b','fast-c'].entries()){
    const response=page.waitForResponse(r=>r.url().endsWith('/actions/verify')&&r.status()===200);
    await page.locator('.phone-action-bar [data-action=verify-next]').click();assert.equal((await response).status(),200);
    await page.waitForFunction(({next,last})=>!busy&&(last?local.queueComplete:local.selected===next)&&!!current(),{next:index<2?fixtures[['fast-b','fast-c'][index]].symbol:null,last:index===2});
    await page.evaluate(async()=>{await new Promise(requestAnimationFrame);await new Promise(requestAnimationFrame);});
    assert.equal((await state()).symbols[fixtures[key].symbol].selected,fixtures[key].revision);
    const canvas=await page.locator('.drawing-canvas').boundingBox(),bar=await page.locator('.phone-action-bar').boundingBox();
    if(!canvas||!bar)throw Error(JSON.stringify({canvas,bar,errors,ui:await page.evaluate(()=>({body:document.body.className,selected:local.selected,feedback:local.feedback,busy,html:document.querySelector('.phone-action-bar')?.outerHTML}))}));
    check(canvas.y>=0&&canvas.y+canvas.height<=bar.y+1,`Consecutive phone review ${index+1} keeps the drawing above its actions`);
    check(!await page.locator('#r-toast').isVisible(),'Successful verification needs no popup dismissal');
  }
  check(await page.locator('.queue-complete').isVisible(),'Queue completion is compact and visible');
  await page.locator('#phone-undo').click();await page.waitForFunction(()=>!busy);check((await state()).symbols[fixtures['fast-c'].symbol].selected===null,'Phone Undo restores the exact previous choice');
  for(const key of ['fast-a','fast-b'])await userAction('unverify',{symbol:fixtures[key].symbol,expected:fixtures[key].revision,previous:null});
  await page.setViewportSize({width:1440,height:1000});await choose('image-a');
  const text='Shorten only the top bar to 70% of its current width. Keep both other bars and the lead unchanged. Inspect the attached reference and record its visible number in your image observations. Synthetic browser check '+crypto.randomUUID();
  await page.locator('[data-setting=size][data-value=small]').click();await page.locator('[data-setting=stroke][data-value=thick]').click();await page.locator('#this-config').check();
  const target=await page.evaluate(()=>({symbol:local.selected,revision:local.revision,configurations:[config().key]}));
  await page.evaluate(()=>{const prepare=ReviewTools.prepareImage;ReviewTools.prepareImage=async file=>{await new Promise(resolve=>window.releaseImage=resolve);return prepare(file);};});
  await page.locator('#comment').fill(text);await page.locator('#image-picker').setInputFiles(path.join(fixtureRoot,'reference.png'));
  check(await page.locator('[data-action=save-comment]').isDisabled(),'Saving waits until image preparation finishes');
  await page.evaluate(()=>window.releaseImage());await page.locator('#image-drafts img').waitFor();
  await page.route('**/api/review/images',route=>route.abort());await page.locator('[data-action=save-comment-next]').click();await page.waitForFunction(()=>local.save.includes('failed'));
  check(await page.locator('#comment').inputValue()===text&&await page.locator('#image-drafts img').count()===1,'Upload failure retains text and image');
  check(await page.evaluate(()=>local.selected)===fixtures['image-a'].symbol,'Upload failure does not advance the drawing');
  await page.reload();await page.locator('#image-drafts img').waitFor();check(await page.locator('#comment').inputValue()===text,'Image and text drafts survive reload');
  check(await page.locator('#this-config').isChecked(),'Configuration-only targeting survives upload failure and reload');
  await page.unroute('**/api/review/images');await page.route('**/api/review/actions/comment',route=>route.abort());await page.locator('[data-action=save-comment-next]').click();await page.waitForFunction(()=>local.save.includes('failed'));
  check(await page.locator('#comment').inputValue()===text&&await page.locator('#image-drafts img').count()===1,'Comment failure after upload retains the complete draft');
  await page.unroute('**/api/review/actions/comment');await page.route('**/api/review/state',route=>route.abort());await page.locator('[data-action=save-comment]').click();await page.waitForFunction(()=>local.save==='Saved'&&!busy);
  check(await page.locator('#r-toast').innerText().then(t=>t.includes('Saved on the server')),'A failed refresh after acknowledgement does not misreport a failed save');await page.unroute('**/api/review/state');await page.evaluate(()=>refresh());
  check(await page.evaluate(()=>!local.refreshNeeded),'Normal polling recovers an acknowledged save after reconnection');
  const saved=(await state()).comments,comment=Object.values(saved).find(c=>c.text===text&&c.targets[0].symbol===fixtures['image-a'].symbol);
  check(comment?.attachments.length===1,'Saved comment links its private image to the exact target');
  assert.deepEqual(comment.targets,[target]);check(true,'Retry preserves the exact revision and original Small/Thick target');
  check(await page.evaluate(()=>local.selected)===fixtures['image-a'].symbol,'Save comment stays on the current drawing');
  const second=await session({width:390,height:844}),other=await state(second.page);check(other.comments[comment.id].attachments[0].hash===comment.attachments[0].hash,'An independent session retrieves the same image comment');
  const imageResponse=await second.page.request.get(config.url+'/review/images/'+comment.attachments[0].hash),imageBytes=await imageResponse.body();
  check(crypto.createHash('sha256').update(imageBytes).digest('hex')===comment.attachments[0].hash,'Private image bytes remain exact across sessions');
  await page.locator('.comment-card [data-action=image]').first().click();check(await page.locator('#image-dialog .enlarged-image').isVisible(),'Saved images enlarge on tap');await page.locator('[data-action=close-image]').click();
  await choose('image-b');const encoded=fs.readFileSync(path.join(fixtureRoot,'reference.png')).toString('base64');
  for(const kind of ['paste','drop']){
    await page.locator('#comment').evaluate((node,{encoded,kind})=>{const transfer=new DataTransfer();transfer.items.add(new File([Uint8Array.from(atob(encoded),c=>c.charCodeAt(0))],'clipboard.png',{type:'image/png'}));node.dispatchEvent(kind==='paste'?new ClipboardEvent('paste',{clipboardData:transfer,bubbles:true,cancelable:true}):new DragEvent('drop',{dataTransfer:transfer,bubbles:true,cancelable:true}));},{encoded,kind});
    await page.locator('#image-drafts img').waitFor();check(true,`Desktop ${kind} accepts an image`);await page.locator('#image-drafts [data-action=remove-image]').click();await page.locator('#image-drafts img').waitFor({state:'detached'});check(true,'Pending image can be removed before submission');
  }
  await page.locator('#comment').fill('Shorten only the top bar to 80% of its current width. Preserve the other bars and lead.');
  await page.locator('[data-action=save-comment-next]').click();await page.waitForFunction(id=>!busy&&local.selected!==id,fixtures['image-b'].symbol);check(true,'Save comment & next advances only after saving');
  await choose('fast-a');await page.locator('#review-description summary').click();await page.waitForFunction(()=>localStorage.getItem('schematica-review-description')==='open');await page.reload();await page.locator('#review-description[open]').waitFor();check(true,'Description expansion survives reload');
  await page.locator('#updates-button').click();await page.getByRole('heading',{name:'Working / queued',exact:true}).waitFor();check(true,'Updates groups ready drawings, working jobs and attention');await page.locator('[data-action=close-dialog]').click();
  await page.screenshot({path:path.join(output,'desktop.png')});
  await page.setViewportSize({width:390,height:844});await page.locator('.phone-action-bar [data-action=comment]').click();await page.locator('#comment').focus();
  check(!await page.locator('.phone-action-bar').isVisible(),'Phone comment editor hides the bottom navigation while typing');
  await page.locator('[data-action=close-feedback]').click();check(await page.locator('.phone-action-bar').isVisible(),'Bottom navigation returns after closing feedback');
  check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Phone layout has no horizontal overflow');
  assert.deepEqual(errors,[]);fs.writeFileSync(path.join(output,'results.json'),JSON.stringify({checks,passed:checks.length,productionWrites:0,physicalPhone:false},null,2));
  console.log(JSON.stringify({passed:checks.length,productionWrites:0,physicalPhone:false}));await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
