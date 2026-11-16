/* Shared, testable review navigation and browser-private draft storage. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.ReviewTools=api;})(globalThis,function(){
  'use strict';
  const comments=(state,s)=>Object.values(state.comments||{}).filter(c=>!c.deleted&&c.targets.some(t=>t.symbol===s.id&&t.revision===s.latest));
  const needsReview=(state,s)=>!!s?.candidate&&!s.discarded&&s.selected!==s.latest&&!comments(state,s).length;
  function nextCandidate(state,pool,id){const start=pool.findIndex(s=>s.id===id);for(let n=1;n<=pool.length;n++){const s=pool[(start+n+pool.length)%pool.length];if(s.id!==id&&needsReview(state,s))return s.id;}return null;}
  function updates(state){
    const jobs=Object.values(state.jobs||{}),ready=[],working=[],attention=[];
    for(const s of Object.values(state.symbols||{})){
      const result=jobs.flatMap(j=>j.results||[]).find(r=>r.symbol===s.id&&r.revision===s.latest);
      if((s.updateRevision===s.latest||result)&&needsReview(state,s))ready.push({symbol:s.id,revision:s.latest,summary:s.updateSummary||result?.summary||'Updated drawing',seen:s.seenRevision===s.latest});
    }
    for(const job of jobs){
      if(['Waiting for desktop','Working'].includes(job.status)&&(job.workflow===2||job.approved))working.push(job);
      else if(['Needs your answer','Failed','Stale','Waiting for approval'].includes(job.status)||job.workflow!==2&&job.status==='Waiting for desktop'&&!job.approved)attention.push(job);
    }
    return {ready,working,attention};
  }
  let database;
  async function db(){if(!database)database=new Promise((resolve,reject)=>{const r=indexedDB.open('schematica-review-drafts',1);r.onupgradeneeded=()=>r.result.createObjectStore('images',{keyPath:'key'});r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);});return database;}
  async function stored(mode,operation){const d=await db();return new Promise((resolve,reject)=>{const tx=d.transaction('images',mode),r=operation(tx.objectStore('images'));tx.oncomplete=()=>resolve(r.result);tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error);});}
  const drafts={all:()=>stored('readonly',s=>s.getAll()),put:(key,images)=>stored('readwrite',s=>s.put({key,images})),remove:key=>stored('readwrite',s=>s.delete(key))};
  async function prepareImage(file){
    if(!['image/png','image/jpeg','image/webp'].includes(file.type))throw Error('Choose PNG, JPEG or WebP images.');
    if(file.size>10*1024*1024)throw Error('Choose an image smaller than 10 MB.');
    const source=await createImageBitmap(file);let scale=Math.min(1,1600/Math.max(source.width,source.height)),blob;
    const canvas=document.createElement('canvas');
    try{for(let attempt=0;attempt<5;attempt++){
      canvas.width=Math.max(1,Math.round(source.width*scale));canvas.height=Math.max(1,Math.round(source.height*scale));
      const ctx=canvas.getContext('2d');ctx.fillStyle='white';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(source,0,0,canvas.width,canvas.height);
      blob=await new Promise(resolve=>canvas.toBlob(resolve,file.type==='image/png'&&attempt===0?'image/png':'image/jpeg',.88-attempt*.06));
      if(blob&&blob.size<=1048576)break;scale*=.8;
    }}finally{source.close();}
    if(!blob||blob.size>1048576)throw Error('This image could not fit the 1 MB upload limit. Try a smaller image.');
    const bytes=new Uint8Array(await blob.arrayBuffer()),hash=[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(n=>n.toString(16).padStart(2,'0')).join('');
    let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.slice(i,i+8192));
    return {hash,name:file.name||'Pasted image',mime:blob.type,bytes:bytes.length,body:btoa(binary),status:'Pending upload',uploaded:false};
  }
  return {needsReview,nextCandidate,updates,drafts,prepareImage};
});
