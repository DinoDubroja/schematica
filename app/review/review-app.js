'use strict';
const $=s=>document.querySelector(s), esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const local={selected:null,revision:null,tab:'drawing',size:'medium',stroke:'medium',options:{},filter:'all',batch:'all',search:'',selection:[],selecting:false,queue:false,feedback:false,arrivals:[],drafts:{},save:'Saved',pins:true};
try{local.drafts=JSON.parse(localStorage.getItem('schematica-review-drafts')||'{}');}catch{}
let data=null,revisions=new Map(),undo=null, busy=false,modal=null,editing=null,polling=false;
function remember(){try{localStorage.setItem('schematica-review-drafts',JSON.stringify(local.drafts));}catch{}}
const draftKey=()=>`${local.selected}:${local.revision}`;
async function api(path,method='GET',value,key=crypto.randomUUID()) {
  const response=await fetch('/api/review/'+path,{method,headers:method==='GET'?{}:{'Content-Type':'application/json','Idempotency-Key':key},body:method==='GET'?undefined:JSON.stringify(value)});
  const result=await response.json();
  if(response.status===401){notify('Your session ended. Your draft is kept on this device. Sign in again.');throw Error(result.error);}
  if(!response.ok)throw Object.assign(Error(result.error),{status:response.status});return result;
}
async function action(name,value) {
  const key=crypto.randomUUID();
  for(let attempt=0;attempt<3;attempt++)try{return await api('actions/'+name,'POST',value,key);}catch(e){if(e.status===409&&e.message.includes('Another device')&&attempt<2)continue;throw e;}
}
function notify(message,canUndo=false) {
  $('#r-toast').hidden=false;$('#r-toast').innerHTML=`<span>${esc(message)}</span>${canUndo?'<button data-action="undo">Undo</button>':''}<button data-action="dismiss" aria-label="Dismiss message">×</button>`;$('#r-live').textContent=message;
}
async function save(name,value,message) {
  if(busy)return false;busy=true;local.save='Saving…';saveLabel();
  try{await action(name,value);local.save='Saved';await refresh(true);if(message)notify(message);return true;}
  catch(e){local.save='Save failed · draft kept';notify(e.message);return false;}
  finally{busy=false;saveLabel();}
}
function saveLabel(){if($('#r-save'))$('#r-save').textContent=local.save;}
const selected=()=>data?.symbols[local.selected];
const current=()=>revisions.get(local.revision);
const list=()=>Object.values(data?.symbols||{}).filter(s=>s.candidate);
const comments=(id=local.selected,rev=local.revision)=>Object.values(data?.comments||{}).filter(c=>!c.deleted&&c.targets.some(t=>t.symbol===id&&t.revision===rev));
const reviewed=s=>s.discarded||(s.selected&&(!s.arrivedAt||s.decisionAt>=s.arrivedAt))||comments(s.id,s.latest).length;
function label(s){if(s.discarded)return 'Discarded';if(s.published===s.latest&&s.confirmed)return 'Published';if(s.selected)return s.selected===s.latest?'Verified':'Earlier revision verified';if(comments(s.id,s.latest).length)return 'Feedback saved';return 'Needs review';}
function filtered(){return list().filter(s=>(local.filter==='discarded'?s.discarded:!s.discarded)&&(local.filter!=='needs'||!reviewed(s))&&(local.filter!=='feedback'||comments(s.id,s.latest).length)&&(local.filter!=='verified'||s.selected&&s.selected!==s.published)&&(local.filter!=='published'||s.confirmed)&&(local.filter!=='new'||local.arrivals.includes(s.id))&&(local.batch==='all'||s.batch===local.batch)&&s.name.toLowerCase().includes(local.search.toLowerCase()));}
async function loadRevision(id){if(!revisions.has(id))revisions.set(id,await api('revisions/'+id));return revisions.get(id);}
async function refresh(force=false) {
  if(polling)return;polling=true;
  try {
    const next=await api('state');
    if(data&&next.version===data.version&&!force)return;
    if(data)for(const s of Object.values(next.symbols))if(s.candidate&&data.symbols[s.id]?.latest!==s.latest&&!local.arrivals.includes(s.id))local.arrivals.push(s.id);
    const first=!data;data=next;
    if(!local.selected){const cursor=data.cursor,s=data.symbols[cursor?.symbol];local.selected=s?.candidate?s.id:list()[0]?.id;local.revision=s?.candidate?cursor.revision:selected()?.latest;}
    if(local.revision)await loadRevision(local.revision);
    if(document.activeElement?.matches('textarea,input[type=search]')&&!force){renderStatus();return;}
    render();if(first&&local.drafts[draftKey()])notify('Your unfinished comment was restored.');
  }catch(e){if(!data)$('#r-app').innerHTML=`<div class="toolbar"><p>${esc(e.message)}</p><a href="/review">Sign in / retry</a></div>`;else if(force)throw e;}
  finally{polling=false;}
}
async function select(id,rev) {
  if(!data.symbols[id])return;local.selected=id;local.revision=rev||data.symbols[id].latest;local.options={};local.tab='drawing';local.queue=false;editing=null;
  await loadRevision(local.revision);render();action('cursor',{symbol:id,revision:local.revision}).catch(e=>notify(e.message));
}
function config(r=current(),overrides={}) {
  if(!r)return null;const options=Object.fromEntries(Object.entries(r.symbol.options||{}).map(([key,spec])=>[key,local.options[key]||spec.default]));
  Object.assign(options,overrides.options||{});return r.symbol.configurations.find(c=>c.size===(overrides.size||local.size)&&c.stroke===(overrides.stroke||local.stroke)&&JSON.stringify(Object.entries(c.options||{}).sort())===JSON.stringify(Object.entries(options).sort()));
}
function art(r=current(),overrides={},small=false) {
  const c=config(r,overrides);if(!c)return '<span>Preview unavailable</span>';
  const [dx,dy]=c.visual_center_from_origin_mm,ox=c.width_mm/2-dx,oy=c.height_mm/2-dy;
  const pins=!small&&local.pins?Object.values(c.pins_mm).map(([x,y])=>`<circle cx="${ox+x}" cy="${oy-y}" r=".25" class="pin-dot"/>`).join(''):'';
  return `<svg class="symbol-art ${small?'mini':''}" role="img" aria-label="${esc(r.symbol.name)}, ${esc(c.size)}, ${esc(c.stroke)}" width="${c.width_mm*12}" height="${c.height_mm*12}" viewBox="0 0 ${c.width_mm} ${c.height_mm}"><image class="symbol-drawing" href="/review/assets/${c.sha256}" width="${c.width_mm}" height="${c.height_mm}"/>${pins}</svg>`;
}
function renderStatus(){saveLabel();const el=$('#desktop-status');if(el)el.textContent=desktopLabel();const arrival=$('#arrivals');if(arrival){arrival.hidden=!local.arrivals.length;arrival.querySelector('span').textContent=`${local.arrivals.length} new arrival${local.arrivals.length===1?'':'s'} · your place is kept`;}}
function desktopLabel(){return Date.now()-Date.parse(data.desktop.at||0)<75000&&data.desktop.status!=='Stopped'?`Desktop · ${data.desktop.status}`:'Desktop offline';}
function render() {
  const s=selected(),r=current(),done=list().filter(reviewed).length;
  $('#r-app').innerHTML=`<div class="toolbar"><div><h1>Review</h1><p class="subtitle">Private workspace</p></div><div class="actions"><span id="desktop-status" class="availability">${esc(desktopLabel())}</span><button class="primary" data-action="process">Process Review</button><button class="outline" data-action="jobs">Progress</button></div></div><div class="progress-line"><span>${done} of ${list().length} reviewed</span><progress max="${list().length||1}" value="${done}" aria-label="Review decisions"></progress><span id="r-save" role="status">${esc(local.save)}</span></div><div id="arrivals" class="arrival" ${local.arrivals.length?'':'hidden'}><span>${local.arrivals.length} new arrival${local.arrivals.length===1?'':'s'} · your place is kept</span><button data-action="arrivals">View</button></div>
  ${!s?'<main class="empty-review"><h2>Ready for new symbols</h2><p>Finished candidates will appear here as they arrive.</p><button class="outline" data-action="jobs">Desktop status</button></main>':`<main class="workspace"><aside class="queue ${local.queue?'open':''}" aria-label="Candidate queue"><div class="row between queue-title"><h3>Candidates</h3><button data-action="select-mode">${local.selecting?'Done':'Select'}</button></div><div class="queue-filters"><input type="search" id="search" aria-label="Find a candidate" placeholder="Find a symbol" value="${esc(local.search)}"><div class="filter-pair"><select id="filter" aria-label="Review status">${[['all','All candidates'],['needs','Needs review'],['feedback','Feedback'],['verified','Verified'],['published','Published'],['new','New arrivals'],['discarded','Discarded']].map(([v,n])=>`<option value="${v}" ${v===local.filter?'selected':''}>${n}</option>`).join('')}</select><select id="batch" aria-label="Batch"><option value="all">All batches</option>${[...new Set(list().map(s=>s.batch))].map(b=>`<option ${local.batch===b?'selected':''}>${esc(b)}</option>`).join('')}</select></div></div><div id="queue-items">${queueHTML()}</div><div class="queue-bottom"><button class="outline" data-action="shared">${local.selection.length?'Comment on selected':'Comment on batch'}</button>${local.selection.length?'<button class="quiet danger" data-action="discard-many">Discard selected</button>':''}<button data-action="discarded" class="quiet">Discarded</button><button data-action="close-queue" class="mobile-only">Back to drawing</button></div></aside>
  <section class="inspector" aria-label="Symbol inspection"><div class="mobile-top mobile-only"><button class="outline" data-action="queue">Candidates</button></div><div class="symbol-top"><div class="row between"><span class="small muted">${esc(s.family)}</span><div class="row navigation"><button data-action="previous" aria-label="Previous symbol">‹</button><span>${list().findIndex(x=>x.id===s.id)+1} / ${list().length}</span><button data-action="next" aria-label="Next symbol">›</button></div></div><h2>${esc(r.symbol.name)} <span class="tag">r${r.symbol.revision}</span></h2><p class="status">${esc(s.discarded?'Discarded':s.published===r.id&&s.confirmed?'Published':s.selected===r.id?'Verified · awaiting publication':'Needs review')}</p></div>${s.selected&&s.selected!==r.id?'<div class="pinned-revision">Your verified revision stays selected.</div>':''}<div class="tabs" role="tablist" aria-label="Symbol view">${['drawing','variations','history'].map(t=>`<button role="tab" aria-selected="${local.tab===t}" class="${local.tab===t?'active':''}" data-action="tab" data-value="${t}">${t[0].toUpperCase()+t.slice(1)}</button>`).join('')}</div><div id="panel" role="tabpanel">${panelHTML()}</div><div class="decision-bar">${s.discarded?'<button class="primary" data-action="restore">Restore symbol</button>':`<button class="primary" data-action="verify" ${s.selected===r.id?'disabled':''}>${s.selected===r.id?'Verified':'Verify'}</button><button class="outline" data-action="comment">Comment</button><button class="quiet" data-action="discard">Discard</button>`}</div><p class="decision-caption">All supported configurations · publish with Process Review</p></section><aside class="feedback ${local.feedback?'open':''}" aria-label="Feedback"><div id="feedback-content">${feedbackHTML()}</div></aside></main>`}`;
  if(local.tab==='history')loadHistory();
}
function queueHTML(){return filtered().map(s=>`<div class="queue-item ${s.id===local.selected?'active':''}">${local.selecting?`<input type="checkbox" aria-label="Select ${esc(s.name)}" data-select="${esc(s.id)}" ${local.selection.includes(s.id)?'checked':''}>`:''}<button class="queue-entry" data-action="select" data-value="${esc(s.id)}"><span>${esc(s.name)}</span><small>${esc(label(s))}</small></button></div>`).join('')||'<p class="muted small">No matching candidates.</p>';}
function settingsHTML(){const r=current();return `<div class="settings">${[['size','Size',r.symbol.presets.sizes],['stroke','Stroke',r.symbol.presets.strokes],...Object.entries(r.symbol.options||{}).map(([key,spec])=>[key,spec.name,spec.values.map(v=>v.id)])].map(([key,name,values])=>`<fieldset><legend>${esc(name)}</legend><div class="segmented">${values.map(v=>`<button class="${(local[key]||local.options[key]||r.symbol.options?.[key]?.default)===v?'active':''}" data-setting="${esc(key)}" data-value="${esc(v)}">${esc(r.symbol.options?.[key]?.values.find(x=>x.id===v)?.name||v[0].toUpperCase()+v.slice(1))}</button>`).join('')}</div></fieldset>`).join('')}</div>`;}
function panelHTML() {
  const r=current();
  if(local.tab==='drawing')return `<div class="drawing-canvas">${art()}</div><div class="canvas-controls"><label class="small"><input id="pins-toggle" type="checkbox" ${local.pins?'checked':''}> Connections</label></div>${settingsHTML()}<p class="small muted description-text">${esc(r.symbol.description)}</p>`;
  if(local.tab==='history')return '<div id="history-list" class="history-list">Loading saved revisions…</div>';
  const defaults={size:'medium',stroke:'medium',options:Object.fromEntries(Object.entries(r.symbol.options||{}).map(([k,v])=>[k,v.default]))};
  const rows=[['Size','size',r.symbol.presets.sizes.map(id=>({id,name:id}))],['Stroke','stroke',r.symbol.presets.strokes.map(id=>({id,name:id}))],...Object.entries(r.symbol.options||{}).map(([k,s])=>[s.name,k,s.values])];
  return `<div class="variation-rows">${rows.map(([name,key,values])=>`<section class="variation-row"><h3>${esc(name)}</h3><div class="variation-examples">${values.map(v=>`<figure>${art(r,{...defaults,...(['size','stroke'].includes(key)?{[key]:v.id}:{options:{...defaults.options,[key]:v.id}})},true)}<figcaption>${esc(v.name[0].toUpperCase()+v.name.slice(1))}</figcaption></figure>`).join('')}</div></section>`).join('')}</div>`;
}
async function loadHistory(){const id=local.selected;await Promise.all(selected().revisions.map(loadRevision));if(local.tab!=='history'||local.selected!==id||!$('#history-list'))return;
  $('#history-list').innerHTML=selected().revisions.slice().reverse().map(rev=>{const r=revisions.get(rev);return `<article class="history-card"><div class="row between"><h3>Revision ${r.symbol.revision}</h3><span class="small muted">${esc(new Date(r.at).toLocaleString())}</span></div>${art(r,{},true)}<p>${esc(r.change?.why||r.readiness?.visual?.summary||'Saved drawing')}</p><div class="row"><button class="outline" data-action="revision" data-value="${rev}">View${rev===local.revision?' · current':''}</button><button class="quiet" data-action="compare" data-value="${rev}">Compare</button></div></article>`;}).join('');}
function feedbackHTML(){return `<div class="row between"><h3>Feedback</h3><button class="mobile-only" data-action="close-feedback">Close</button></div><div class="comments">${comments().map(c=>`<article class="comment-card"><p>${esc(c.text)}</p><small class="muted">${c.targets.length>1?`${c.targets.length} symbols · `:''}${esc(new Date(c.at).toLocaleString())}</small><button class="quiet" data-action="edit-comment" data-value="${c.id}">Edit</button></article>`).join('')}</div><label class="sr-only" for="comment">Comment on this revision</label><textarea id="comment" rows="5" placeholder="What should change?">${esc(local.drafts[draftKey()]||'')}</textarea><label class="small"><input id="this-config" type="checkbox"> This configuration only</label><button class="primary" data-action="save-comment">${editing?'Save edit':'Save comment'}</button><p class="small muted">Saved with this drawing revision.</p>`;}
function openDialog(title,html,kind){modal=kind;$('#dialog').innerHTML=`<div class="row between"><h2 id="dialog-title">${esc(title)}</h2><button data-action="close-dialog" aria-label="Close">×</button></div>${html}`;if(!$('#dialog').open)$('#dialog').showModal();}
function shareDialog(include=false){const pool=local.selection.length?list().filter(s=>local.selection.includes(s.id)):list().filter(s=>local.batch==='all'?s.batch===selected().batch:s.batch===local.batch);const targets=pool.filter(s=>!s.discarded&&(include||!s.selected));
  openDialog('Shared comment',`<label class="small"><input id="include-verified" type="checkbox" ${include?'checked':''}> Include verified symbols</label><div class="target-list">${targets.map(s=>`<label><input type="checkbox" data-target="${s.id}" data-revision="${s.latest}" checked> ${esc(s.name)} · r${s.revisions.length}</label>`).join('')||'<p>No unverified targets. Choose another batch or include verified symbols.</p>'}</div><textarea id="shared-text" rows="5" placeholder="What should change?">${esc(local.drafts.shared||'')}</textarea><button class="primary" data-action="save-shared">Save shared comment</button>`,'shared');}
function jobsDialog(){openDialog('Review progress',`<p class="muted">${esc(desktopLabel())}</p>${data.desktop.detail?`<p>${esc(data.desktop.detail)}</p>`:''}${Object.values(data.jobs).reverse().map(j=>`<article class="job-card"><h3>${esc(j.status)}</h3><p class="small muted">${esc(new Date(j.created).toLocaleString())}</p>${j.error?`<p class="danger">${esc(j.error)}</p>`:''}${j.proposal?.changes.map(c=>`<div class="proposal"><strong>${esc(data.symbols[c.symbol]?.name||c.symbol)}</strong><p>${esc(c.intent)}</p><small>Source: ${esc(c.revision)}</small></div>`).join('')||''}${j.status==='Waiting for approval'?`<button class="primary" data-action="approve" data-value="${j.id}">Approve changes</button><button data-action="reject" data-value="${j.id}">Close proposal</button>`:''}${j.status==='Failed'?`<button class="outline" data-action="retry" data-value="${j.id}">Retry</button>`:''}${j.status==='Stale'?'<p>Source or feedback changed. Process Review again.</p>':''}${['Failed','Stale'].includes(j.status)?`<button class="quiet" data-action="reject" data-value="${j.id}">Close job</button>`:''}</article>`).join('')||'<p>Nothing queued yet.</p>'}`,'jobs');}
document.addEventListener('input',e=>{if(e.target.id==='comment'){local.drafts[draftKey()]=e.target.value;remember();local.save='Unsaved';saveLabel();}if(e.target.id==='shared-text'){local.drafts.shared=e.target.value;remember();}if(e.target.id==='search'){local.search=e.target.value;$('#queue-items').innerHTML=queueHTML();}});
document.addEventListener('change',e=>{if(e.target.id==='pins-toggle'){local.pins=e.target.checked;render();}if(e.target.id==='filter'||e.target.id==='batch'){local[e.target.id]=e.target.value;render();}if(e.target.dataset.select){const id=e.target.dataset.select;local.selection=e.target.checked?[...new Set([...local.selection,id])]:local.selection.filter(x=>x!==id);render();}if(e.target.id==='include-verified')shareDialog(e.target.checked);});
document.addEventListener('click',async e=>{
  const button=e.target.closest('button');if(!button)return;
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
    if(act==='previous'||act==='next'){const pool=filtered(),idx=pool.findIndex(x=>x.id===s.id);if(pool.length)await select(pool[(idx+(act==='next'?1:pool.length-1))%pool.length].id);return;}
    if(act==='verify'){const revision=local.revision,previous=s.selected;if(await save('verify',{symbol:s.id,revision})){undo={action:'unverify',value:{symbol:s.id,expected:revision,previous}};notify('Revision verified. Publish with Process Review.',true);}return;}
    if(act==='discard'||act==='discard-many'){const ids=act==='discard-many'?[...local.selection]:[s.id],changed=ids.filter(id=>!data.symbols[id].discarded);if(await save('discard',{symbols:ids})){undo=changed.length?{action:'restore',value:{symbols:changed}}:null;local.selection=[];render();notify(`${ids.length===1?'Symbol':'Symbols'} discarded. Published versions are kept.`,!!undo);}return;}
    if(act==='restore'){await save('restore',{symbols:[s.id]},'Symbol restored');return;}
    if(act==='undo'&&undo){const op=undo;if(await save(op.action,op.value,'Undone'))undo=null;return;}
    if(act==='dismiss'){$('#r-toast').hidden=true;return;}
    if(act==='save-comment'){
      const key=draftKey(),content=local.drafts[key]||'',edit=editing?data.comments[editing]:null;
      const targets=edit?edit.targets:[{symbol:s.id,revision:local.revision,configurations:$('#this-config').checked?[config().key]:[]}];
      if(await save('comment',{text:content,targets,...(edit?{comment:edit.id,expected:edit.edit}:{})})){delete local.drafts[key];remember();editing=null;render();notify('Comment saved');}return;
    }
    if(act==='edit-comment'){editing=value;local.drafts[draftKey()]=data.comments[value].text;local.feedback=true;remember();render();$('#comment').focus();return;}
    if(act==='shared'){shareDialog();return;}
    if(act==='save-shared'){const targets=[...document.querySelectorAll('[data-target]:checked')].map(n=>({symbol:n.dataset.target,revision:n.dataset.revision,configurations:[]}));if(await save('comment',{text:local.drafts.shared||'',targets},'Shared comment saved')){delete local.drafts.shared;remember();$('#dialog').close();}return;}
    if(act==='process'){if(await save('process',{}))jobsDialog();return;}
    if(act==='jobs'){await refresh(true);jobsDialog();return;}
    if(act==='approve'){if(await save('approve',{job:value,proposal:data.jobs[value].proposal.id}))jobsDialog();return;}
    if(act==='reject'||act==='retry'){if(await save(act,{job:value}))jobsDialog();return;}
    if(act==='compare'){const older=await loadRevision(value);openDialog('Compare revisions',`<div class="comparison"><section><h3>Revision ${current().symbol.revision}</h3>${art(current())}</section><section><h3>Revision ${older.symbol.revision}</h3>${art(older)}</section></div><p>${esc(older.change?.why||'Saved drawing')}</p>`,'compare');return;}
    if(act==='close-dialog'){$('#dialog').close();modal=null;}
  }catch(error){notify(error.message);}
});
window.addEventListener('online',()=>refresh(true));
window.addEventListener('beforeunload',e=>{if(local.save==='Unsaved'||local.save.startsWith('Save failed')){e.preventDefault();e.returnValue='';}});
refresh();setInterval(()=>{if(!busy)refresh().then(()=>{if(modal==='jobs'&&$('#dialog').open)jobsDialog();});},5000);
