'use strict';
const $=s=>document.querySelector(s), esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const local={selected:null,revision:null,tab:'drawing',size:'medium',stroke:'medium',options:{},filter:'all',batch:'all',search:'',selection:[],selecting:false,queue:false,feedback:false,arrivals:[],drafts:{},save:'Saved',pins:true};
try{local.drafts=JSON.parse(localStorage.getItem('schematica-review-drafts')||'{}');}catch{}
const draftImages={},draftRequests={},draftTargets={};let imagesReady=false,imageError='',descriptionOpen=false,preparingImages=0;
const historicImages=new Map();
try{descriptionOpen=localStorage.getItem('schematica-review-description')==='open';Object.assign(draftRequests,JSON.parse(localStorage.getItem('schematica-review-requests')||'{}'));Object.assign(draftTargets,JSON.parse(localStorage.getItem('schematica-review-targets')||'{}'));}catch{}
let data=null,revisions=new Map(),undo=null,busy=false,modal=null,editing=null,selectionSerial=0,refreshPending=null,cursorSave=Promise.resolve();
let artSerial=0;
const canvasObserver=new ResizeObserver(()=>fitDrawing());
function remember(){try{localStorage.setItem('schematica-review-drafts',JSON.stringify(local.drafts));localStorage.setItem('schematica-review-requests',JSON.stringify(draftRequests));localStorage.setItem('schematica-review-targets',JSON.stringify(draftTargets));}catch{imageError='Draft storage is unavailable. Keep this page open until your comment is saved.';}}
const draftKey=()=>`${local.selected}:${local.revision}${editing?':edit:'+editing:''}`;
async function api(path,method='GET',value,key=crypto.randomUUID()) {
  const response=await fetch('/api/review/'+path,{method,headers:method==='GET'?{}:{'Content-Type':'application/json','Idempotency-Key':key},body:method==='GET'?undefined:JSON.stringify(value),signal:AbortSignal.timeout(30000)});
  const result=await response.json();
  if(response.status===401){notify('Your session ended. Your draft is kept on this device. Sign in again.');throw Error(result.error);}
  if(!response.ok)throw Object.assign(Error(result.error),{status:response.status});return result;
}
async function action(name,value,key=crypto.randomUUID()) {
  for(let attempt=0;attempt<3;attempt++)try{return await api('actions/'+name,'POST',value,key);}catch(e){if(e.status===409&&e.message.includes('Another device')&&attempt<2)continue;throw e;}
}
function notify(message) {
  $('#r-toast').hidden=false;$('#r-toast').classList.add('error');$('#r-toast').setAttribute('role','alert');$('#r-toast').innerHTML=`<span>${esc(message)}</span><button data-action="dismiss" aria-label="Dismiss message">×</button>`;$('#r-live').textContent=message;
}
async function save(name,value,message='Saved',key) {
  if(busy||preparingImages)return false;busy=true;local.save='Saving…';saveLabel();
  const locked=[...document.querySelectorAll('#dialog button,#dialog input,#dialog textarea')].map(node=>[node,node.disabled]);locked.forEach(([node])=>node.disabled=true);
  try{await action(name,value,key);local.save=message;$('#r-toast').hidden=true;await refreshSaved();return true;}
  catch(e){local.save='Save failed · draft kept';notify(e.message);return false;}
  finally{busy=false;locked.forEach(([node,disabled])=>node.disabled=disabled);render();}
}
async function refreshSaved(){try{await refresh(true);local.refreshNeeded=false;}catch{local.refreshNeeded=true;notify('Saved on the server. Reconnect to refresh the drawing; your review has not advanced.');}}
function saveLabel(){for(const id of ['r-save','phone-save'])if($('#'+id)){$('#'+id).textContent=local.save;$('#'+id).className=local.save.includes('failed')?'status-error':local.save==='Unsaved'?'status-attention':'status-success';}for(const id of ['r-undo','phone-undo'])if($('#'+id)){$('#'+id).hidden=!undo;$('#'+id).disabled=busy;}}
const selected=()=>data?.symbols[local.selected];
const current=()=>revisions.get(local.revision);
const list=()=>Object.values(data?.symbols||{}).filter(s=>s.candidate);
const comments=(id=local.selected,rev=local.revision)=>Object.values(data?.comments||{}).filter(c=>!c.deleted&&c.targets.some(t=>t.symbol===id&&t.revision===rev));
const reviewed=s=>!ReviewTools.needsReview(data,s);
function label(s){if(s.discarded)return 'Discarded';if(s.published===s.latest&&s.confirmed)return 'Published';if(s.selected)return s.selected===s.latest?'Verified':'Earlier revision verified';if(comments(s.id,s.latest).length)return 'Feedback saved';return 'Needs review';}
function filtered(){return list().filter(s=>(local.filter==='discarded'?s.discarded:!s.discarded)&&(local.filter!=='needs'||!reviewed(s))&&(local.filter!=='feedback'||comments(s.id,s.latest).length)&&(local.filter!=='verified'||s.selected&&s.selected!==s.published)&&(local.filter!=='published'||s.confirmed)&&(local.filter!=='new'||local.arrivals.includes(s.id))&&(local.batch==='all'||s.batch===local.batch)&&s.name.toLowerCase().includes(local.search.toLowerCase()));}
async function loadRevision(id){if(!revisions.has(id))revisions.set(id,await api('revisions/'+id));return revisions.get(id);}
function refresh(force=false){if(refreshPending)return force?refreshPending.then(()=>refresh(true)):refreshPending;refreshPending=readState(force).finally(()=>{refreshPending=null;});return refreshPending;}
async function readState(force) {
  try {
    const next=await api('state');
    if(data&&next.version===data.version&&!force)return;
    if(data)for(const s of Object.values(next.symbols))if(s.candidate&&data.symbols[s.id]?.latest!==s.latest&&!local.arrivals.includes(s.id))local.arrivals.push(s.id);
    const first=!data,updatesChanged=data&&JSON.stringify(ReviewTools.updates(data))!==JSON.stringify(ReviewTools.updates(next));data=next;
    if(!local.selected){const cursor=data.cursor,s=data.symbols[cursor?.symbol];local.selected=s?.candidate?s.id:list()[0]?.id;local.revision=s?.candidate?cursor.revision:selected()?.latest;}
    if(local.revision)await loadRevision(local.revision);
    // Polls update the badge/status only. Arrivals never replace the drawing,
    // reset an open editor, change focus or move the user's scroll position.
    if(!first&&!force){renderStatus();if(modal==='updates'&&updatesChanged){const scroll=$('#dialog').scrollTop,opened=[...$('#dialog').querySelectorAll('details')].map(d=>d.open);jobsDialog();$('#dialog').querySelectorAll('details').forEach((d,i)=>d.open=!!opened[i]);$('#dialog').scrollTop=scroll;}return;}
    local.refreshNeeded=false;render();if(first&&(local.drafts[draftKey()]||draftImages[draftKey()]?.length)){local.save='Unsaved';saveLabel();}
  }catch(e){if(!data)$('#r-app').innerHTML=`<div class="toolbar"><p>${esc(e.message)}</p><a href="/review">Sign in / retry</a></div>`;else if(force)throw e;}
}
async function select(id,rev) {
  if(!data.symbols[id]||busy)return;const serial=++selectionSerial,revision=rev||data.symbols[id].latest;
  // Keep a complete current drawing until the requested revision is available.
  // A later navigation supersedes an earlier request without mixing their IDs.
  await loadRevision(revision);if(serial!==selectionSerial)return;
  local.selected=id;local.revision=revision;local.options={};local.tab='drawing';local.queue=false;local.feedback=false;local.queueComplete=false;editing=null;imageError='';
  render();cursorSave=cursorSave.catch(()=>{}).then(()=>serial===selectionSerial?action('cursor',{symbol:id,revision}):null).catch(e=>notify(e.message));
  if(local.drafts[draftKey()]||draftImages[draftKey()]?.length){local.save='Unsaved';saveLabel();}
}
function config(r=current(),overrides={}) {
  if(!r)return null;const options=Object.fromEntries(Object.entries(r.symbol.options||{}).map(([key,spec])=>[key,local.options[key]||spec.default]));
  Object.assign(options,overrides.options||{});return r.symbol.configurations.find(c=>c.size===(overrides.size||local.size)&&c.stroke===(overrides.stroke||local.stroke)&&JSON.stringify(Object.entries(c.options||{}).sort())===JSON.stringify(Object.entries(options).sort()));
}
function art(r=current(),overrides={},small=false,inspection=false) {
  const c=config(r,overrides);if(!c)return '<span>Preview unavailable</span>';
  const bounds=SchematicaPreview.imageBounds(c),[x,y,w,h]=bounds;
  const pins=!small&&local.pins?Object.entries(c.pins_mm).map(([id,point])=>{const [px,py]=SchematicaPreview.pinPosition(point);return `<circle data-pin="${esc(id)}" cx="${px}" cy="${py}" r=".25" class="pin-dot"/>`;}).join(''):'';
  const gridId=`review-grid-${++artSerial}`;
  const grid=small||!inspection?'':`<defs><pattern id="${gridId}" class="mm-grid" patternUnits="userSpaceOnUse" x="-.5" y="-.5" width="1" height="1"><circle cx=".5" cy=".5" r=".055"/></pattern></defs><rect class="grid-surface" x="${x}" y="${y}" width="${w}" height="${h}" fill="url(#${gridId})"/>`;
  return `<svg class="symbol-art ${small?'mini':''}" role="img" aria-label="${esc(r.symbol.name)}, ${esc(c.size)}, ${esc(c.stroke)}" width="${c.width_mm*12}" height="${c.height_mm*12}" viewBox="${bounds.join(' ')}">${grid}<image class="symbol-drawing" href="/review/assets/${c.sha256}" x="${x}" y="${y}" width="${w}" height="${h}"/>${pins}</svg>`;
}
function fitDrawing() {
  const canvas=$('.drawing-canvas'),svg=canvas?.querySelector('svg'),c=config();
  if(!svg||!c||!canvas.clientWidth||!canvas.clientHeight)return;
  const box=SchematicaPreview.fitViewport(c,canvas.clientWidth,canvas.clientHeight);
  svg.setAttribute('viewBox',box.join(' '));
  const surface=svg.querySelector('.grid-surface');
  ['x','y','width','height'].forEach((name,i)=>surface.setAttribute(name,box[i]));
}
function renderStatus(){
  saveLabel();const el=$('#desktop-status');if(el)el.textContent=desktopLabel();
  const u=ReviewTools.updates(data),button=$('#updates-button');
  if(button){button.innerHTML=`Updates <span class="update-badge">${u.ready.length}</span>`;button.setAttribute('aria-label',`Updates, ${u.ready.length} ready to review`);button.classList.toggle('status-attention',!!u.attention.length);}
  const progress=$('#review-progress');if(progress){const done=list().filter(reviewed).length;progress.textContent=`${done} of ${list().length} reviewed`;$('#r-app progress').value=done;}
}
function desktopLabel(){return Date.now()-Date.parse(data.desktop.at||0)<75000&&!['Stopped','Paused'].includes(data.desktop.status)?`Desktop · ${data.desktop.status}`:'Waiting for desktop · start the connector to process';}
function reviewButton(s,r){return s.discarded?'<button class="primary" data-action="restore">Restore</button>':`<button class="primary" data-action="verify-next" ${local.queueComplete?'disabled':''}>${local.queueComplete?'Review complete':s.selected===r.id?'Next needing review':'Verify &amp; next'}</button>`;}
function render() {
  if(!data)return;const scroll=[scrollX,scrollY];canvasObserver.disconnect();
  const s=selected(),r=current(),done=list().filter(reviewed).length;
  $('#r-app').innerHTML=`
    <div class="toolbar"><div><h1>Review</h1><p class="subtitle">Private workspace</p></div>
      <div class="actions"><span id="desktop-status" class="availability">${esc(desktopLabel())}</span>
      <button class="primary" data-action="process">Process Review</button><button class="outline" id="updates-button" data-action="updates">Updates</button></div></div>
    <div class="progress-line"><span id="review-progress">${done} of ${list().length} reviewed</span><progress max="${list().length||1}" value="${done}" aria-label="Review decisions"></progress>
      <span id="r-save" role="status"></span><button id="r-undo" class="quiet" data-action="undo" ${undo?'':'hidden'}>Undo</button></div>
    ${!s?'<main class="empty-review"><h2>Ready for new symbols</h2><p>Finished candidates will appear here as they arrive.</p></main>':`
    <main class="workspace"><aside class="queue ${local.queue?'open':''}" aria-label="Candidate queue">
      <div class="row between queue-title"><h3>Candidates</h3><button class="quiet" data-action="select-mode">${local.selecting?'Done':'Select'}</button></div>
      <div class="queue-filters"><input type="search" id="search" aria-label="Find a candidate" placeholder="Find a symbol" value="${esc(local.search)}">
        <div class="filter-pair"><select id="filter" aria-label="Review status">${[['all','All candidates'],['needs','Needs review'],['feedback','Feedback'],['verified','Verified'],['published','Published'],['new','New arrivals'],['discarded','Discarded']].map(([v,n])=>`<option value="${v}" ${v===local.filter?'selected':''}>${n}</option>`).join('')}</select>
        <select id="batch" aria-label="Batch"><option value="all">All batches</option>${[...new Set(list().map(s=>s.batch))].map(b=>`<option ${local.batch===b?'selected':''}>${esc(b)}</option>`).join('')}</select></div></div>
      <div id="queue-items">${queueHTML()}</div><div class="queue-bottom"><button class="outline" data-action="shared">${local.selection.length?'Comment on selected':'Comment on batch'}</button>
        ${local.selection.length?'<button class="quiet danger" data-action="discard-many">Discard selected</button>':''}<button data-action="discarded" class="quiet">Discarded</button><button data-action="close-queue" class="mobile-only">Back to drawing</button></div></aside>
      <section class="inspector" aria-label="Symbol inspection">
        <div class="mobile-top mobile-only"><button class="outline" data-action="queue">Candidates</button></div>
        <div class="symbol-top"><div class="row between"><span class="small muted">${esc(s.family)}</span><div class="row navigation">
          <button class="outline" data-action="previous" aria-label="Previous symbol">‹</button><span>${list().findIndex(x=>x.id===s.id)+1} / ${list().length}</span><button class="outline" data-action="next" aria-label="Next symbol">›</button></div></div>
          <h2>${esc(r.symbol.name)} <span class="tag">r${r.symbol.revision}</span></h2><p class="status ${s.selected===r.id?'status-success':'status-attention'}">${esc(s.discarded?'Discarded':s.published===r.id&&s.confirmed?'Published':s.selected===r.id?'Verified · awaiting publication':comments().length?'Feedback saved':'Needs review')}</p>
          <div class="decision-bar desktop-review-actions">${reviewButton(s,r)}<button class="outline" data-action="comment">Comment</button><button class="quiet danger" data-action="discard">Discard</button></div></div>
        ${local.queueComplete?'<div class="queue-complete" role="status">✓ This queue is reviewed.</div>':''}
        ${s.selected&&s.selected!==r.id?'<div class="pinned-revision">Your verified revision stays selected.</div>':''}
        <div class="tabs" role="tablist" aria-label="Symbol view">${['drawing','variations','history'].map(t=>`<button role="tab" aria-selected="${local.tab===t}" class="${local.tab===t?'active':''}" data-action="tab" data-value="${t}">${t[0].toUpperCase()+t.slice(1)}</button>`).join('')}</div>
        <div id="panel" role="tabpanel">${panelHTML()}</div>
        <div class="mobile-only secondary-review-actions"><button class="quiet danger" data-action="discard">Discard</button></div>
      </section>
      <aside class="feedback ${local.feedback?'open':''}" aria-label="Feedback"><div id="feedback-content">${feedbackHTML()}</div></aside>
    </main><nav class="phone-action-bar" aria-label="Review actions"><div class="phone-save-line"><span id="phone-save" role="status"></span><button id="phone-undo" class="quiet" data-action="undo" ${undo?'':'hidden'}>Undo</button></div><button class="outline" data-action="previous">Previous</button><button class="outline" data-action="comment">Comment</button>${reviewButton(s,r)}</nav>`}`;
  if(local.tab==='history')loadHistory();
  const canvas=$('.drawing-canvas');if(canvas){fitDrawing();canvasObserver.observe(canvas);}
  if(busy)document.querySelectorAll('#r-app button,#r-app textarea,#r-app input,#r-app select').forEach(n=>n.disabled=true);
  document.body.classList.toggle('feedback-open',local.feedback);document.body.classList.toggle('queue-open',local.queue);renderStatus();window.scrollTo(...scroll);
}
function queueHTML(){return filtered().map(s=>`<div class="queue-item ${s.id===local.selected?'active':''}">${local.selecting?`<input type="checkbox" aria-label="Select ${esc(s.name)}" data-select="${esc(s.id)}" ${local.selection.includes(s.id)?'checked':''}>`:''}<button class="queue-entry" data-action="select" data-value="${esc(s.id)}"><span>${esc(s.name)}</span><small>${esc(label(s))}</small></button></div>`).join('')||'<p class="muted small">No matching candidates.</p>';}
function settingsHTML(){const r=current();return `<div class="settings">${[['size','Size',r.symbol.presets.sizes],['stroke','Stroke',r.symbol.presets.strokes],...Object.entries(r.symbol.options||{}).map(([key,spec])=>[key,spec.name,spec.values.map(v=>v.id)])].map(([key,name,values])=>`<fieldset><legend>${esc(name)}</legend><div class="segmented">${values.map(v=>`<button class="${(local[key]||local.options[key]||r.symbol.options?.[key]?.default)===v?'active':''}" data-setting="${esc(key)}" data-value="${esc(v)}">${esc(r.symbol.options?.[key]?.values.find(x=>x.id===v)?.name||v[0].toUpperCase()+v.slice(1))}</button>`).join('')}</div></fieldset>`).join('')}</div>`;}
function panelHTML() {
  const r=current();
  if(local.tab==='drawing')return `<div class="drawing-canvas">${art(current(),{},false,true)}</div><div class="canvas-controls"><label class="small"><input id="pins-toggle" type="checkbox" ${local.pins?'checked':''}> Connections</label></div>${settingsHTML()}<details class="description-text" id="review-description" ${descriptionOpen?'open':''}><summary>Description</summary><p class="small muted">${esc(r.symbol.description)}</p></details>`;
  if(local.tab==='history')return '<div id="history-list" class="history-list">Loading saved revisions…</div>';
  const defaults={size:'medium',stroke:'medium',options:Object.fromEntries(Object.entries(r.symbol.options||{}).map(([k,v])=>[k,v.default]))};
  const rows=[['Size','size',r.symbol.presets.sizes.map(id=>({id,name:id}))],['Stroke','stroke',r.symbol.presets.strokes.map(id=>({id,name:id}))],...Object.entries(r.symbol.options||{}).map(([k,s])=>[s.name,k,s.values])];
  return `<div class="variation-rows">${rows.map(([name,key,values])=>`<section class="variation-row"><h3>${esc(name)}</h3><div class="variation-examples">${values.map(v=>`<figure>${art(r,{...defaults,...(['size','stroke'].includes(key)?{[key]:v.id}:{options:{...defaults.options,[key]:v.id}})},true)}<figcaption>${esc(v.name[0].toUpperCase()+v.name.slice(1))}</figcaption></figure>`).join('')}</div></section>`).join('')}</div>`;
}
async function loadHistory(){const id=local.selected;await Promise.all(selected().revisions.map(loadRevision));if(local.tab!=='history'||local.selected!==id||!$('#history-list'))return;
  $('#history-list').innerHTML=selected().revisions.slice().reverse().map(rev=>{const r=revisions.get(rev);return `<article class="history-card"><div class="row between"><h3>Revision ${r.symbol.revision}</h3><span class="small muted">${esc(new Date(r.at).toLocaleString())}</span></div>${art(r,{},true)}<p>${esc(r.change?.why||r.readiness?.visual?.summary||'Saved drawing')}</p><div class="row"><button class="outline" data-action="revision" data-value="${rev}">View${rev===local.revision?' · current':''}</button><button class="quiet" data-action="compare" data-value="${rev}">Compare</button></div>${commentsHTML(comments(id,rev),false)}</article>`;}).join('');}
function imageURL(a){return a.body?`data:${a.mime};base64,${a.body}`:`/review/images/${a.hash}`;}
function imageHTML(images,draft=false,context=draftKey()){return `<div class="image-thumbnails">${images.map(a=>`<figure class="comment-image"><button class="image-open" data-action="image" data-value="${a.hash}" data-key="${esc(context)}" ${draft?'data-draft="true"':''} aria-label="Enlarge ${esc(a.name)}"><img src="${imageURL(a)}" alt="${esc(a.name)}"></button>${draft?`<figcaption class="small ${a.status==='Upload failed'?'status-error':''}">${esc(a.status||'Uploaded')}</figcaption><button class="remove-image" data-action="remove-image" data-key="${esc(context)}" data-value="${a.hash}" aria-label="Remove ${esc(a.name)}">×</button>`:''}</figure>`).join('')}</div>`;}
function commentsHTML(items,editable=true){return items.map(c=>`<article class="comment-card"><p>${esc(c.text)}</p>${imageHTML(c.attachments||[])}<small class="muted">${c.targets.length>1?`${c.targets.length} symbols · `:''}${esc(new Date(c.at).toLocaleString())}</small>${editable?`<button class="quiet" data-action="edit-comment" data-value="${c.id}">Edit</button>`:''}${c.edit!==c.id?`<button class="quiet" data-action="comment-history" data-value="${c.id}">Earlier edits</button>`:''}</article>`).join('');}
function feedbackHTML(){return `<div class="row between"><h3>Feedback</h3><button class="mobile-only" data-action="close-feedback" aria-label="Close feedback">Close</button></div>
  <label class="sr-only" for="comment">Comment on this revision</label><textarea id="comment" rows="4" placeholder="What should change?">${esc(local.drafts[draftKey()]||'')}</textarea>
  <div id="image-drafts">${imageHTML(draftImages[draftKey()]||[],true)}</div>
  <div class="image-picker row"><label class="outline picker-button">Add images<input id="image-picker" class="sr-only" type="file" accept="image/png,image/jpeg,image/webp" multiple ${!imagesReady?'disabled':''}></label>
    <label class="outline picker-button mobile-only">Take photo<input id="photo-picker" class="sr-only" type="file" accept="image/jpeg,image/png,image/webp" capture="environment" ${!imagesReady?'disabled':''}></label></div>
  <p class="small muted image-help">Up to 4 PNG, JPEG or WebP images. Photos are resized to 1 MB. Paste or drop images here.</p>
  <p id="image-error" class="status-error small" role="alert">${esc(imageError)}</p>
  ${editing?'':`<label class="small"><input id="this-config" type="checkbox" ${draftTargets[draftKey()]?.length?'checked':''}> This configuration only</label>${draftTargets[draftKey()]?.length&&draftTargets[draftKey()][0]!==config().key?`<p class="small muted">Saved target: ${esc(draftTargets[draftKey()][0])}</p>`:''}`}
  <div class="comment-actions"><button class="primary" data-action="save-comment-next">Save comment &amp; next</button><button class="outline" data-action="save-comment">${editing?'Save edit':'Save comment'}</button></div>
  <div class="comments">${commentsHTML(comments())}</div>`;}
function openDialog(title,html,kind){modal=kind;$('#dialog').innerHTML=`<div class="row between"><h2 id="dialog-title">${esc(title)}</h2><button data-action="close-dialog" aria-label="Close">×</button></div>${html}`;if(!$('#dialog').open)$('#dialog').showModal();}
function shareDialog(include=false){const pool=local.selection.length?list().filter(s=>local.selection.includes(s.id)):list().filter(s=>local.batch==='all'?s.batch===selected().batch:s.batch===local.batch);const targets=pool.filter(s=>!s.discarded&&(include||!s.selected));
  openDialog('Shared comment',`<label class="small"><input id="include-verified" type="checkbox" ${include?'checked':''}> Include verified symbols</label><div class="target-list">${targets.map(s=>`<label><input type="checkbox" data-target="${s.id}" data-revision="${s.latest}" checked> ${esc(s.name)} · r${s.revisions.length}</label>`).join('')||'<p>No unverified targets. Choose another batch or include verified symbols.</p>'}</div><textarea id="shared-text" rows="5" placeholder="What should change?">${esc(local.drafts.shared||'')}</textarea><div id="shared-image-drafts">${imageHTML(draftImages.shared||[],true,'shared')}</div><label class="outline picker-button">Add images<input id="shared-image-picker" type="file" class="sr-only" accept="image/png,image/jpeg,image/webp" multiple></label><p id="shared-image-error" class="small status-error" role="alert">${esc(imageError)}</p><button class="primary" data-action="save-shared">Save shared comment</button>`,'shared');}
function jobTarget(job){return job.corrections[0]||job.publications[0];}
function jobCard(job,attention=false){const t=jobTarget(job),name=data.symbols[t?.symbol]?.name||'Review',legacy=job.workflow!==2&&!job.approved;
  return `<article class="job-card"><div class="row between"><strong>${esc(name)}</strong><span class="small ${attention?(job.status==='Failed'?'status-error':'status-attention'):''}">${esc(legacy?'Previous proposal · not started':job.status==='Waiting for desktop'?'Queued · '+desktopLabel():job.status)}</span></div>
    ${job.status==='Needs your answer'&&job.question?`<p>${esc(job.question.text)}</p><button class="primary" data-action="answer" data-value="${job.id}">Answer</button>`:''}
    ${job.error?`<p class="status-error">${esc(job.error)}</p>`:''}
    ${t?`<button class="outline" data-action="open-job" data-value="${job.id}">Open drawing</button>`:''}
    ${job.status==='Failed'?`<button class="outline" data-action="retry" data-value="${job.id}">Retry</button>`:''}
    ${attention?`<button class="quiet" data-action="reject" data-value="${job.id}">Close</button>`:''}
    <details><summary>Details</summary><p class="small muted">${esc(new Date(job.created).toLocaleString())} · ${esc(job.id)}</p>${job.proposal?`<p>${esc(job.proposal.changes.map(c=>c.intent).join(' '))}</p>`:''}<p class="small">${esc(job.phase)} · ${job.attempts} attempt${job.attempts===1?'':'s'}</p></details></article>`;}
function jobsDialog(){const u=ReviewTools.updates(data);openDialog('Updates',`
  <section><h3>Ready to review <span class="update-badge">${u.ready.length}</span></h3>${u.ready.map(item=>`<article class="job-card"><strong>${esc(data.symbols[item.symbol].name)}</strong><p>${esc(item.summary)}</p><span class="small status-attention">${item.seen?'Seen · still needs review':'New · needs review'}</span><button class="primary" data-action="open-update" data-value="${item.symbol}" data-revision="${item.revision}">Open drawing</button></article>`).join('')||'<p class="small muted">No revised drawings waiting.</p>'}</section>
  <section><h3>Working / queued</h3>${u.working.map(j=>jobCard(j)).join('')||'<p class="small muted">Nothing queued.</p>'}</section>
  <section><h3>Needs your answer / failed</h3>${u.attention.map(j=>jobCard(j,true)).join('')||'<p class="small muted">Nothing needs action.</p>'}</section>
  <details><summary>Completed job history</summary>${Object.values(data.jobs).filter(j=>['Ready to review','Closed'].includes(j.status)).reverse().map(j=>`<article class="history-card"><strong>${esc(data.symbols[jobTarget(j)?.symbol]?.name||'Review')}</strong><p class="small">${esc(j.status)} · ${esc(new Date(j.created).toLocaleString())}</p><details><summary>Details</summary><pre>${esc(JSON.stringify(j,null,2))}</pre></details></article>`).join('')||'<p>No completed jobs yet.</p>'}</details>`,'updates');}
function navigationPool(){return list().filter(s=>!s.discarded&&(local.batch==='all'||s.batch===local.batch)&&s.name.toLowerCase().includes(local.search.toLowerCase()));}
async function advance(){if(local.refreshNeeded)return;const next=ReviewTools.nextCandidate(data,navigationPool(),local.selected);if(next)await select(next);else{local.queueComplete=true;local.feedback=false;render();}$('#comment')?.blur();document.querySelector('.symbol-top')?.scrollIntoView({block:'start'});}
async function persistImages(key){try{if(draftImages[key]?.length)await ReviewTools.drafts.put(key,draftImages[key]);else await ReviewTools.drafts.remove(key);}catch{imageError='Image draft storage is unavailable. Keep this page open until saved.';}if($('#image-error'))$('#image-error').textContent=imageError;}
function renderImageDrafts(){if($('#image-drafts'))$('#image-drafts').innerHTML=imageHTML(draftImages[draftKey()]||[],true);if($('#shared-image-drafts'))$('#shared-image-drafts').innerHTML=imageHTML(draftImages.shared||[],true,'shared');for(const id of ['image-error','shared-image-error'])if($('#'+id))$('#'+id).textContent=preparingImages?'Preparing image…':imageError;document.querySelectorAll('[data-action=save-comment],[data-action=save-comment-next],[data-action=save-shared]').forEach(node=>node.disabled=busy||!!preparingImages);}
async function addImages(files,key=modal==='shared'?'shared':draftKey()){if(busy||!imagesReady)return;imageError='';
  preparingImages++;local.save='Preparing image…';saveLabel();renderImageDrafts();
  try{for(const file of files){try{if((draftImages[key]||[]).length>=4)throw Error('Use up to four images per comment.');const image=await ReviewTools.prepareImage(file);if(!(draftImages[key]||[]).some(a=>a.hash===image.hash)){if((draftImages[key]||[]).length>=4)throw Error('Use up to four images per comment.');(draftImages[key]??=[]).push(image);}await persistImages(key);local.save='Unsaved';saveLabel();}catch(e){imageError=e.message;}renderImageDrafts();}}finally{preparingImages--;renderImageDrafts();}}
async function saveComment(next,shared=false){if(busy||preparingImages||!imagesReady)return;const key=shared?'shared':draftKey(),content=local.drafts[key]||'',edit=!shared&&editing?data.comments[editing]:null;
  const targets=shared?[...document.querySelectorAll('[data-target]:checked')].map(n=>({symbol:n.dataset.target,revision:n.dataset.revision,configurations:[]})):edit?edit.targets:[{symbol:local.selected,revision:local.revision,configurations:draftTargets[key]||[]}];
  const images=draftImages[key]||[];if(!content.trim()&&!images.length){imageError='Add text or an image.';renderImageDrafts();return;}
  busy=true;imageError='';local.save=images.some(a=>!a.uploaded)?'Uploading images…':'Saving…';saveLabel();render();
  const locked=[...document.querySelectorAll('#dialog button,#dialog input,#dialog textarea')].map(node=>[node,node.disabled]);locked.forEach(([node])=>node.disabled=true);
  try{for(const image of images){if(image.uploaded)continue;image.status='Uploading…';renderImageDrafts();try{const saved=await api('images','POST',{hash:image.hash,mime:image.mime,body:image.body});Object.assign(image,saved,{uploaded:true,status:'Uploaded'});await persistImages(key);}catch(e){image.status='Upload failed';await persistImages(key);throw e;}renderImageDrafts();}
    const value={text:content,attachments:images.map(({hash,mime,bytes,name})=>({hash,mime,bytes,name})),targets,...(edit?{comment:edit.id,expected:edit.edit}:{})};
    const payload=JSON.stringify(value);if(draftRequests[key]?.payload!==payload)draftRequests[key]={payload,id:crypto.randomUUID()};remember();
    await action('comment',value,draftRequests[key].id);
    delete local.drafts[key];delete draftImages[key];delete draftRequests[key];delete draftTargets[key];remember();await persistImages(key);editing=null;local.save='Saved';$('#r-toast').hidden=true;await refreshSaved();if(shared){$('#dialog').close();modal=null;}
  }catch(e){local.save='Save failed · draft kept';imageError=e.message;notify(e.message);return;}
  finally{busy=false;locked.forEach(([node,disabled])=>node.disabled=disabled);render();}
  if(next)await advance();
}
document.addEventListener('input',e=>{if(e.target.id==='comment'){local.drafts[draftKey()]=e.target.value;remember();local.save='Unsaved';saveLabel();}if(e.target.id==='shared-text'){local.drafts.shared=e.target.value;remember();}if(e.target.id==='question-answer'){local.drafts['answer:'+e.target.dataset.job]=e.target.value;remember();}if(e.target.id==='search'){local.search=e.target.value;$('#queue-items').innerHTML=queueHTML();}});
document.addEventListener('change',e=>{if(e.target.id==='this-config'){draftTargets[draftKey()]=e.target.checked?[config().key]:[];remember();}if(e.target.id==='pins-toggle'){local.pins=e.target.checked;render();}if(e.target.id==='filter'||e.target.id==='batch'){local[e.target.id]=e.target.value;render();}if(e.target.dataset.select){const id=e.target.dataset.select;local.selection=e.target.checked?[...new Set([...local.selection,id])]:local.selection.filter(x=>x!==id);render();}if(e.target.id==='include-verified')shareDialog(e.target.checked);});
document.addEventListener('click',async e=>{
  const button=e.target.closest('button');if(!button)return;
  if(busy||preparingImages)return;
  if(button.id==='logout'){await fetch('/review/logout',{method:'POST'});location.replace('/review');return;}
  if(button.dataset.setting){const key=button.dataset.setting;if(['size','stroke'].includes(key))local[key]=button.dataset.value;else local.options[key]=button.dataset.value;render();return;}
  const act=button.dataset.action,value=button.dataset.value,s=selected();
  try {
    if(act==='select')return select(value);
    if(act==='revision')return select(local.selected,value);
    if(act==='tab'){local.tab=value;render();return;}
    if(act==='queue'||act==='close-queue'){local.queue=act==='queue';render();return;}
    if(act==='comment'||act==='close-feedback'){local.feedback=act==='comment';render();if(local.feedback)$('#comment').focus();return;}
    if(act==='select-mode'){local.selecting=!local.selecting;if(!local.selecting)local.selection=[];render();return;}
    if(act==='arrivals'||act==='discarded'){local.filter=act==='arrivals'?'new':'discarded';local.queue=true;render();return;}
    if(act==='previous'||act==='next'){const pool=navigationPool(),idx=pool.findIndex(x=>x.id===s.id);if(pool.length)await select(pool[(idx+(act==='next'?1:pool.length-1))%pool.length].id);document.querySelector('.symbol-top')?.scrollIntoView({block:'start'});return;}
    if(act==='verify-next'){const revision=local.revision,previous=s.selected;if(s.selected===revision){await advance();return;}if(await save('verify',{symbol:s.id,revision},'Verified')){undo={action:'unverify',value:{symbol:s.id,expected:revision,previous}};await advance();renderStatus();}return;}
    if(act==='discard'||act==='discard-many'){const ids=act==='discard-many'?[...local.selection]:[s.id],changed=ids.filter(id=>!data.symbols[id].discarded);if(await save('discard',{symbols:ids},'Discarded · recoverable')){undo=changed.length?{action:'restore',value:{symbols:changed}}:null;local.selection=[];render();}return;}
    if(act==='restore'){await save('restore',{symbols:[s.id]},'Symbol restored');return;}
    if(act==='undo'&&undo){const op=undo;if(await save(op.action,op.value,'Undone')){undo=null;local.queueComplete=false;render();}return;}
    if(act==='dismiss'){$('#r-toast').hidden=true;return;}
    if(act==='save-comment'||act==='save-comment-next'){await saveComment(act==='save-comment-next');return;}
    if(act==='edit-comment'){editing=value;const c=data.comments[value],key=draftKey();local.drafts[key]??=c.text;draftImages[key]??=(c.attachments||[]).map(a=>({...a,uploaded:true,status:'Uploaded'}));await persistImages(key);local.feedback=true;remember();render();$('#comment').focus();return;}
    if(act==='remove-image'){const key=button.dataset.key||draftKey();draftImages[key]=(draftImages[key]||[]).filter(a=>a.hash!==value);await persistImages(key);local.save='Unsaved';saveLabel();renderImageDrafts();return;}
    if(act==='image'){const image=button.dataset.draft?(draftImages[button.dataset.key]||[]).find(a=>a.hash===value):Object.values(data.comments).flatMap(c=>c.attachments||[]).find(a=>a.hash===value)||historicImages.get(value);if(image){let dialog=$('#image-dialog');if(!dialog){dialog=document.createElement('dialog');dialog.id='image-dialog';$('#schematica-review-demo').append(dialog);}dialog.innerHTML=`<div class="row between"><h2>Comment image</h2><button data-action="close-image" aria-label="Close image">×</button></div><img class="enlarged-image" src="${imageURL(image)}" alt="${esc(image.name)}">`;dialog.showModal();}return;}
    if(act==='comment-history'){let after=0,events=[];while(true){const page=await api(`comment-history/${value}?after=${after}`);events.push(...page.events);if(page.events.length<100)break;after=page.next;}for(const event of events)for(const image of event.attachments||[])historicImages.set(image.hash,image);openDialog('Comment history',events.map(event=>`<article class="comment-card"><p>${esc(event.text)}</p>${imageHTML(event.attachments||[])}<small class="muted">${esc(new Date(event.at).toLocaleString())}</small></article>`).join(''),'comment-history');return;}
    if(act==='close-image'){$('#image-dialog').close();return;}
    if(act==='shared'){shareDialog();return;}
    if(act==='save-shared'){await saveComment(false,true);return;}
    if(act==='process'){if(await save('process',{},'Queued'))jobsDialog();return;}
    if(act==='updates'||act==='jobs'){await refresh(true);jobsDialog();return;}
    if(act==='open-update'){const revision=button.dataset.revision;$('#dialog').close();modal=null;await select(value,revision);await action('seen',{symbol:value,revision});data.symbols[value].seenRevision=revision;document.querySelector('.symbol-top')?.scrollIntoView({block:'start'});return;}
    if(act==='open-job'){const target=jobTarget(data.jobs[value]);$('#dialog').close();modal=null;await select(target.symbol,target.revision);document.querySelector('.symbol-top')?.scrollIntoView({block:'start'});return;}
    if(act==='answer'){const job=data.jobs[value];openDialog('Your answer',`<p>${esc(job.question.text)}</p><label class="sr-only" for="question-answer">Answer</label><textarea id="question-answer" data-job="${value}" rows="4">${esc(local.drafts['answer:'+value]||'')}</textarea><button class="primary" data-action="save-answer" data-value="${value}" data-question="${job.question.id}">Send answer</button>`,'answer');return;}
    if(act==='save-answer'){if(await save('answer',{job:value,question:button.dataset.question,text:local.drafts['answer:'+value]||''},'Answer saved')){delete local.drafts['answer:'+value];remember();jobsDialog();}return;}
    if(act==='approve'){if(await save('approve',{job:value,proposal:data.jobs[value].proposal.id}))jobsDialog();return;}
    if(act==='reject'||act==='retry'){if(await save(act,{job:value}))jobsDialog();return;}
    if(act==='compare'){const older=await loadRevision(value);openDialog('Compare revisions',`<div class="comparison"><section><h3>Revision ${current().symbol.revision}</h3>${art(current())}</section><section><h3>Revision ${older.symbol.revision}</h3>${art(older)}</section></div><p>${esc(older.change?.why||'Saved drawing')}</p>`,'compare');return;}
    if(act==='close-dialog'){$('#dialog').close();modal=null;}
  }catch(error){notify(error.message);}
});
window.addEventListener('online',()=>refresh(true));
window.addEventListener('beforeunload',e=>{if(preparingImages||busy||local.save==='Unsaved'||local.save.startsWith('Save failed')){e.preventDefault();e.returnValue='';}});
document.addEventListener('change',e=>{if(['image-picker','photo-picker','shared-image-picker'].includes(e.target.id))addImages([...e.target.files]);});
const imageEditor=target=>target.closest('.feedback')||modal==='shared'&&target.closest('#dialog');
document.addEventListener('paste',e=>{if(!imageEditor(e.target))return;const files=[...e.clipboardData.items].filter(x=>x.kind==='file').map(x=>x.getAsFile()).filter(Boolean);if(files.length){e.preventDefault();addImages(files);}});
document.addEventListener('dragover',e=>{if(imageEditor(e.target)&&e.dataTransfer.types.includes('Files'))e.preventDefault();});
document.addEventListener('drop',e=>{if(imageEditor(e.target)&&e.dataTransfer.files.length){e.preventDefault();addImages([...e.dataTransfer.files]);}});
document.addEventListener('toggle',e=>{if(e.target.id==='review-description'){descriptionOpen=e.target.open;try{localStorage.setItem('schematica-review-description',descriptionOpen?'open':'closed');}catch{}}},true);
function keyboardLayout(){document.body.classList.toggle('keyboard-open',!!document.activeElement?.matches('textarea,input[type=text],input[type=search]'));document.documentElement.style.setProperty('--review-viewport-height',`${window.visualViewport?.height||innerHeight}px`);}
document.addEventListener('focusin',keyboardLayout);document.addEventListener('focusout',()=>requestAnimationFrame(keyboardLayout));window.visualViewport?.addEventListener('resize',keyboardLayout);
$('#dialog').addEventListener('close',()=>{modal=null;});
ReviewTools.drafts.all().then(rows=>{for(const row of rows)draftImages[row.key]=row.images.map(a=>({...a,status:a.uploaded?'Uploaded':'Pending upload'}));}).catch(()=>{imageError='Image draft storage is unavailable. Keep this page open until saved.';}).finally(()=>{imagesReady=true;refresh();});
setInterval(()=>{if(!busy)refresh();},5000);
