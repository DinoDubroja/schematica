// Actual Review UI, read-only production data. No comments/decisions/cursor writes.
// NODE_PATH may point to an existing Playwright installation. Credentials stay private.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const args=process.argv.slice(2),arg=name=>args[args.indexOf(name)+1];
const connection=JSON.parse(fs.readFileSync(arg('--config'),'utf8'));
const output=path.resolve(arg('--output')),repo=path.resolve(__dirname,'..');
const before=args.includes('--before'),localFiles=args.includes('--local');
fs.mkdirSync(output,{recursive:true});
(async()=>{
  const context=await chromium.launchPersistentContext('',{headless:true,channel:'chrome',viewport:{width:1440,height:1000},extraHTTPHeaders:{Authorization:'Bearer '+connection.token}});
  let preventedWrites=0;
  await context.route('**/*',async route=>{
    const request=route.request(),url=new URL(request.url());
    if(url.origin!==new URL(connection.url).origin)return route.abort();
    if(!['GET','HEAD'].includes(request.method())){preventedWrites++;return route.abort();}
    const files={'/review':'app/review/index.html','/review/review-app.js':'app/review/review-app.js','/review/review-tools.js':'app/review/review-tools.js','/review/review-workflow.js':'app/review/review-workflow.js','/review/review.css':'app/review/review.css','/preview-coordinates.js':'app/viewer/preview-coordinates.js','/':'app/viewer/index.html','/app.js':'app/viewer/app.js'};
    if(localFiles&&files[url.pathname])return route.fulfill({path:path.join(repo,files[url.pathname])});
    return route.continue();
  });
  const page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(connection.url+'/review');await page.locator('.symbol-top h2').waitFor();
  async function show(id,choice){
    // Published-only symbols can be inspected without submitting a fake candidate.
    await page.evaluate(async({id,choice})=>{
      const entry=data.symbols[id];local.selected=id;local.revision=entry.latest;
      await loadRevision(local.revision);local.tab='drawing';local.queue=false;local.pins=true;
      local.size=choice?.size||'medium';local.stroke=choice?.stroke||'medium';local.options=choice?.options||{};render();
      await new Promise(requestAnimationFrame);await new Promise(requestAnimationFrame);
      const image=document.querySelector('.drawing-canvas image');
      await new Promise((resolve,reject)=>{const img=new Image();img.onload=resolve;img.onerror=reject;img.src=image.href.baseVal;});
    },{id,choice});
  }
  const measure=()=>page.evaluate(async()=>{
            const c=config(),svg=document.querySelector('.drawing-canvas>svg'),pattern=svg.querySelector('pattern'),matrix=svg.getScreenCTM();
            // SVGRect rounds to float32; read the exact authored viewport for
            // the resize assertion, then test actual screen transforms below.
            const canvas=svg.parentElement,box=svg.getAttribute('viewBox').trim().split(/\s+/).map(Number);
            if(Math.abs(box[2]/box[3]-canvas.clientWidth/canvas.clientHeight)>1e-7)throw Error('Resize left a stale grid viewport: '+JSON.stringify({symbol:current().symbol.id,key:c.key,box,canvas:[canvas.clientWidth,canvas.clientHeight]}));
            if(pattern.getAttribute('patternUnits')!=='userSpaceOnUse'||+pattern.getAttribute('width')!==1||+pattern.getAttribute('height')!==1)throw Error('Grid is not one millimetre');
            const dot=pattern.querySelector('circle');
            if(+pattern.getAttribute('x')+ +dot.getAttribute('cx')!==0||+pattern.getAttribute('y')+ +dot.getAttribute('cy')!==0)throw Error('Grid origin differs from terminals');
            if(Math.abs(matrix.a-matrix.d)>1e-8||matrix.b||matrix.c)throw Error('Preview scales axes differently');
            const source=await(await fetch('/review/assets/'+c.sha256)).text();
            const raw=new DOMParser().parseFromString(source,'image/svg+xml').documentElement;
            raw.style.cssText='position:absolute;left:0;top:0;visibility:hidden;pointer-events:none';document.body.append(raw);
            const rawBox=raw.viewBox.baseVal,image=svg.querySelector('image'),imageMatrix=image.getScreenCTM();
            let maximum=0;const defects=[];
            for(const pin of current().symbol.pins){
              const marker=svg.querySelector(`[data-pin="${pin.id}"]`),point=new DOMPoint(+marker.getAttribute('cx'),+marker.getAttribute('cy')).matrixTransform(matrix);
              const lead=raw.querySelector(`[data-part="${pin.lead_part}"]`),endpoints=[];
              for(const node of lead.querySelectorAll('path,line,polyline')){
                const length=node.getTotalLength();
                for(const t of [0,length]){
                  const rawPoint=node.getPointAtLength(t).matrixTransform(node.getScreenCTM()).matrixTransform(raw.getScreenCTM().inverse());
                  // Map the actual saved path endpoint through the displayed image bounds.
                  const p=new DOMPoint(image.x.baseVal.value+(rawPoint.x-rawBox.x)*image.width.baseVal.value/rawBox.width,
                    image.y.baseVal.value+(rawPoint.y-rawBox.y)*image.height.baseVal.value/rawBox.height).matrixTransform(imageMatrix);
                  endpoints.push(Math.hypot(p.x-point.x,p.y-point.y));
                }
              }
              const distance=Math.min(...endpoints);maximum=Math.max(maximum,distance);
              if(distance>0.03)defects.push({pin:pin.id,pixels:distance});
              if(Math.abs(+marker.getAttribute('cx')-Math.round(+marker.getAttribute('cx')))>1e-8||Math.abs(+marker.getAttribute('cy')-Math.round(+marker.getAttribute('cy')))>1e-8)throw Error('Terminal is off the physical grid');
            }
            raw.remove();
            return {key:c.key,width:innerWidth,gridPixels:matrix.a,maximumEndpointErrorPixels:maximum,defects,
              overflow:document.documentElement.scrollWidth>innerWidth};
          });
  await show('adc-differential-n-bit');
  await page.screenshot({path:path.join(output,'desktop.png')});
  await page.locator('.drawing-canvas').screenshot({path:path.join(output,'canvas.png')});
  const detail=await page.locator('.inspector').boundingBox();
  await page.screenshot({path:path.join(output,'detail.png'),clip:{...detail,height:Math.min(detail.height,760)}});
  await page.setViewportSize({width:390,height:844});await show('adc-differential-n-bit');
  await page.screenshot({path:path.join(output,'phone.png')});
  const results=[];
  if(!before&&!args.includes('--zoom-only')){
    for(const id of ['resistor-eu','resistor-variable-eu','transistor-pnp','adc-differential-n-bit','multiplexer-4to1','relay-dpdt','filter-band-pass-tunable']){
      await show(id);
      const choices=await page.evaluate(()=>current().symbol.configurations.map(c=>({size:c.size,stroke:c.stroke,options:c.options})));
      for(const viewport of [{width:1440,height:1000},{width:860,height:900},{width:390,height:844}]){
        await page.setViewportSize(viewport);
        for(const choice of choices){
          await show(id,choice);
          const result=await measure();
          results.push(result);assert.equal(result.overflow,false,JSON.stringify(result));
        }
      }
    }
  }
  const resizeResults=[];
  if(!before){
    await show('adc-differential-n-bit');
    await page.evaluate(()=>window.resizeProbe=document.querySelector('.drawing-canvas>svg'));
    for(const viewport of [{width:1440,height:1000},{width:390,height:844},{width:860,height:900},{width:1440,height:1000}]){
      await page.setViewportSize(viewport);
      await page.evaluate(async()=>{await new Promise(requestAnimationFrame);await new Promise(requestAnimationFrame);if(window.resizeProbe!==document.querySelector('.drawing-canvas>svg'))throw Error('Resize unexpectedly recreated the drawing');});
      resizeResults.push(await measure());
    }
    await page.getByRole('checkbox',{name:'Connections',exact:true}).uncheck();
    assert.equal(await page.locator('.drawing-canvas .pin-dot').count(),0);
    assert.equal(await page.locator('.drawing-canvas .mm-grid').count(),1);
    await page.getByRole('checkbox',{name:'Connections',exact:true}).check();
    assert.equal(await page.locator('.drawing-canvas .pin-dot').count(),3);
  }
  const zoomResults=[];
  if(!before||args.includes('--zoom-only')){
    // Chrome's own zoom setting in this disposable test profile: this is browser
    // zoom, not CSS zoom or device-scale emulation. The user's profile is unused.
    const settings=await context.newPage();await settings.goto('chrome://settings/appearance');
    for(const viewport of [{width:1440,height:1000},{width:390,height:844}]){
      await page.setViewportSize(viewport);
      for(const zoom of [.8,1.25,2]){
        await settings.evaluate(z=>new Promise(done=>chrome.settingsPrivate.setDefaultZoom(z,done)),zoom);
        for(const id of ['resistor-eu','transistor-pnp','adc-differential-n-bit','multiplexer-4to1']){
          await show(id,{size:'small',stroke:'thick'});
          const dpr=await page.evaluate(()=>devicePixelRatio);assert.ok(Math.abs(dpr-zoom)<1e-6);
          const result=before?await page.evaluate(()=>({width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth,maximumEndpointErrorPixels:0,defects:[]})):await measure();
          zoomResults.push({...result,zoom,devicePixelRatio:dpr});
        }
      }
    }
    await settings.evaluate(()=>new Promise(done=>chrome.settingsPrivate.setDefaultZoom(1,done)));await settings.close();
  }
  let librarySmoke=false;
  if(!before){
    await page.setViewportSize({width:1440,height:1000});await page.goto(connection.url+'/');
    await page.locator('button[data-symbol="resistor-eu"]').click();
    await page.locator('#canvas .pin-markers circle').first().waitFor();
    assert.equal(await page.locator('#canvas .pin-markers circle').count(),2);
    assert.equal(await page.locator('#canvas .grid-lines path').count(),63);
    librarySmoke=true;
  }
  assert.deepEqual(errors,[]);assert.equal(preventedWrites,0);
  const receipt={source:localFiles?'local fix against live read-only data':'hosted Review',before,configurations:results.length,
    maximumEndpointErrorPixels:Math.max(0,...[...results,...zoomResults,...resizeResults].map(r=>r.maximumEndpointErrorPixels)),defects:[...results,...zoomResults,...resizeResults].filter(r=>r.defects.length),serviceWrites:0,librarySmoke,zoomChecks:zoomResults.length,resizeChecks:resizeResults.length,resizeResults,zoomResults,results};
  fs.writeFileSync(path.join(output,'results.json'),JSON.stringify(receipt,null,2));
  assert.deepEqual(receipt.defects,[],'Drawn lead endpoints must coincide with terminal markers');
  console.log(JSON.stringify({...receipt,results:undefined,zoomResults:undefined,resizeResults:undefined,defects:receipt.defects.slice(0,8)}));
  await context.close();
})().catch(e=>{console.error(e);process.exit(1);});
