// Pure Review decisions. The HTTP layer commits the result with an optimistic lock.
export class Problem extends Error { constructor(message, status=400) { super(message); this.status=status; } }
export const need = (test, message, status=400) => { if (!test) throw new Problem(message,status); };
export const clone = value => structuredClone(value);
export const canonical = value => JSON.stringify(value, function(key,val) {
  return val && typeof val==='object' && !Array.isArray(val) ? Object.fromEntries(Object.keys(val).sort().map(k=>[k,val[k]])) : val;
});
export async function hash(value) {
  const bytes = new TextEncoder().encode(typeof value==='string'?value:canonical(value));
  return [...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(n=>n.toString(16).padStart(2,'0')).join('');
}
export const initial = () => ({symbols:{},comments:{},jobs:{},cursor:null,desktop:{}});
export function feedback(state,id,revision) {
  return Object.values(state.comments).filter(c=>!c.deleted && c.targets.some(t=>t.symbol===id && t.revision===revision));
}
export async function signature(state,id,revision) {
  return hash({revision, latest:state.symbols[id]?.latest, discarded:state.symbols[id]?.discarded,
    feedback:feedback(state,id,revision).map(c=>({id:c.id,edit:c.edit,text:c.text,targets:c.targets,...(c.attachments?.length?{attachments:c.attachments}:{})})).sort((a,b)=>a.id.localeCompare(b.id))});
}
export async function stale(state,job) {
  for (const item of job.corrections) if(!job.results?.some(r=>r.symbol===item.symbol) && await signature(state,item.symbol,item.revision)!==item.signature) return true;
  return false;
}
function symbol(state,id) { need(state.symbols[id],'Unknown symbol',404); return state.symbols[id]; }
function revision(state,id,rev) { need(symbol(state,id).revisions.includes(rev),'Revision does not belong to this symbol'); }
function text(value,max=12000) { need(typeof value==='string' && value.trim().length>0 && value.length<=max,'Provide bounded, nonempty text'); return value.trim(); }
function attachments(values=[]) {
  need(Array.isArray(values)&&values.length<=4,'Use up to four images per comment');
  const seen=new Set();
  return values.map(a=>{
    need(a&&/^[a-f0-9]{64}$/.test(a.hash)&&!seen.has(a.hash),'Invalid or duplicate image');seen.add(a.hash);
    need(['image/png','image/jpeg','image/webp'].includes(a.mime)&&Number.isInteger(a.bytes)&&a.bytes>0&&a.bytes<=1048576,'Images must be PNG, JPEG or WebP, up to 1 MB');
    return {hash:a.hash,mime:a.mime,bytes:a.bytes,name:String(a.name||'Image').replace(/[\x00-\x1f]/g,'').slice(0,120)};
  });
}
function commentContent(input) {
  const images=attachments(input.attachments),content=String(input.text||'').trim();
  need(content.length<=12000&&(content.length||images.length),'Add text or an image');
  return {content,images};
}
function targets(state,values) {
  need(Array.isArray(values) && values.length>0 && values.length<=200,'Choose explicit targets');
  const unique = new Set();
  return values.map(t=>{ revision(state,t.symbol,t.revision); const key=t.symbol+':'+t.revision;
    need(!unique.has(key),'Duplicate target'); unique.add(key);
    need(Array.isArray(t.configurations||[]) && (t.configurations||[]).every(x=>typeof x==='string'),'Invalid configurations');
    return {symbol:t.symbol,revision:t.revision,configurations:t.configurations||[]}; });
}
function lease(job,input,now) {
  need(job && job.lease===input.lease && Date.parse(job.until)>Date.parse(now),'Job lease expired; claim it again',409);
}
export async function transition(original,action,input,ctx) {
  const state=clone(original), now=ctx.now, uid=ctx.id;
  let result={}, evidence={input:clone(input)}; delete evidence.input.lease;
  const agentActions=['heartbeat','claim','renew','proposal','published','fail','complete','publication','question'];
  need(ctx.actor==='desktop' || !agentActions.includes(action),'Desktop authentication required',403);
  need(ctx.actor==='user' || agentActions.includes(action) || action==='upload','Browser authentication required',403);
  switch(action) {
    case 'cursor': revision(state,input.symbol,input.revision); state.cursor={symbol:input.symbol,revision:input.revision}; break;
    case 'seen': {
      revision(state,input.symbol,input.revision);symbol(state,input.symbol).seenRevision=input.revision;break;
    }
    case 'verify': {
      const s=symbol(state,input.symbol); revision(state,input.symbol,input.revision); need(!s.discarded,'Restore this candidate first');
      evidence.previous=s.selected; s.selected=input.revision; s.decision='verified'; s.decisionAt=now; break;
    }
    case 'unverify': {
      const s=symbol(state,input.symbol); need(s.selected===input.expected,'Selection changed on another device',409);
      if(input.previous)revision(state,input.symbol,input.previous);
      evidence.previous=s.selected; s.selected=input.previous||null; s.decision=s.selected?'verified':null;s.decisionAt=now; break;
    }
    case 'discard': case 'restore': {
      need(Array.isArray(input.symbols) && input.symbols.length>0 && input.symbols.length<=200,'Choose symbols');
      evidence.previous={};
      for(const id of new Set(input.symbols)) { const s=symbol(state,id); evidence.previous[id]=!!s.discarded;
        s.discarded=action==='discard'; s.decisionAt=now; }
      break;
    }
    case 'comment': {
      const ts=targets(state,input.targets),{content,images}=commentContent(input),existing=input.comment?state.comments[input.comment]:null;
      need(!input.comment || existing,'Unknown comment',404);
      if(existing) need(input.expected===existing.edit,'Comment changed on another device; your draft is retained',409);
      const id=existing?.id||uid;
      evidence.original=existing?clone(existing):null;
      state.comments[id]={id,text:content,attachments:images,targets:ts,originalTargets:existing?.originalTargets||ts,
        originalText:existing?.originalText??content,originalAttachments:existing?.originalAttachments||existing?.attachments||images,
        created:existing?.created||now,at:now,edit:uid,author:'user'};
      result={id}; break;
    }
    case 'process': {
      const publications=[],corrections=[];
      for(const [id,s] of Object.entries(state.symbols)) {
        if(s.discarded || !s.candidate) continue;
        if(s.selected && (s.published!==s.selected || !s.confirmed)) publications.push({symbol:id,revision:s.selected});
        else if(feedback(state,id,s.latest).length) corrections.push({symbol:id,revision:s.latest,signature:await signature(state,id,s.latest),comments:clone(feedback(state,id,s.latest))});
      }
      need(publications.length+corrections.length,'Nothing to process yet');
      const ids=[],existing=[];
      for(const [index,target] of [...publications,...corrections].entries()) {
        const correction=!!target.signature;
        if(correction)for(const job of Object.values(state.jobs))if(job.workflow===2&&['Waiting for desktop','Working','Needs your answer','Failed'].includes(job.status)&&job.corrections.some(t=>t.symbol===target.symbol&&t.signature!==target.signature)&&!job.results.length)job.status='Stale';
        const active=Object.values(state.jobs).find(j=>j.workflow===2&&['Waiting for desktop','Working','Needs your answer','Failed'].includes(j.status)&&
          (correction?j.corrections.some(t=>t.symbol===target.symbol&&t.signature===target.signature):j.publications.some(t=>t.symbol===target.symbol&&t.revision===target.revision)));
        if(active){existing.push(active.id);continue;}
        const id=index===0?uid:`${uid}-${index}`;
        state.jobs[id]={id,workflow:2,created:now,status:'Waiting for desktop',phase:'correct',
          authorized:{at:now,actor:'user',action:'process'},publications:correction?[]:[target],corrections:correction?[target]:[],results:[],attempts:0};
        ids.push(id);
      }
      result={id:ids[0]||existing[0],ids,existing};break;
    }
    case 'approve': {
      const job=state.jobs[input.job]; need(job && job.status==='Waiting for approval','Proposal is not awaiting approval',409);
      need(!(await stale(state,job)),'Proposal is stale. Prepare a new review.',409);
      need(input.proposal===job.proposal.id,'Proposal changed',409);
      job.approved={at:now,proposal:job.proposal.id,actor:'user'}; job.phase='correct'; job.status='Waiting for desktop';
      break;
    }
    case 'reject': {
      const job=state.jobs[input.job]; need(job && (['Waiting for approval','Needs your answer','Failed','Stale'].includes(job.status)||job.workflow!==2&&job.status==='Waiting for desktop'&&!job.approved),'Cannot close an active job');
      job.status='Closed'; job.decision={at:now,actor:'user',action:'rejected'}; break;
    }
    case 'retry': {
      const job=state.jobs[input.job]; need(job && job.status==='Failed','Only failed jobs can be retried');
      need(!(await stale(state,job)),'Feedback or source changed. Prepare a new review.',409);
      job.status='Waiting for desktop'; job.error=null; break;
    }
    case 'heartbeat': state.desktop={at:now,status:text(input.status,500),detail:String(input.detail||'').slice(0,1000),protocol:input.protocol||1}; break;
    case 'claim': {
      let job;
      for(const candidate of Object.values(state.jobs)) {
        if(!(candidate.status==='Waiting for desktop'||candidate.status==='Working'&&Date.parse(candidate.until)<Date.parse(now)))continue;
        // New jobs require an image-aware/direct-processing connector. Never
        // silently turn a legacy unapproved proposal into an authorized job.
        if(candidate.workflow===2?input.protocol!==2:!candidate.approved)continue;
        if(await stale(state,candidate)){candidate.status='Stale';result.stale=candidate.id;continue;}
        job=candidate;break;
      }
      if(job) {
        job.status='Working'; job.lease=uid; job.until=new Date(Date.parse(now)+180000).toISOString(); job.attempts++;
        result={job:clone(job)};
      } else result={...result,job:null};
      break;
    }
    case 'renew': {
      const job=state.jobs[input.job]; lease(job,input,now); job.until=new Date(Date.parse(now)+180000).toISOString(); break;
    }
    case 'proposal': {
      const job=state.jobs[input.job]; lease(job,input,now); need(job.phase==='prepare','Unexpected proposal');
      if(await stale(state,job)) {job.status='Stale'; break;}
      need(Array.isArray(input.changes) && input.changes.length===job.corrections.length,'Proposal must describe exactly the requested targets');
      const ids=new Set();
      for(const change of input.changes) {
        const target=job.corrections.find(t=>t.symbol===change.symbol && t.revision===change.revision);
        need(target && !ids.has(change.symbol),'Unexpected proposal target'); ids.add(change.symbol); text(change.intent,6000);
      }
      job.proposal={id:uid,at:now,author:'agent',changes:clone(input.changes)};
      job.status=job.corrections.length?'Waiting for approval':'Ready to review'; break;
    }
    case 'question': {
      const job=state.jobs[input.job];lease(job,input,now);
      need(job.workflow===2&&job.corrections.length===1,'Unexpected clarification');
      need(!(await stale(state,job)),'Feedback or source changed',409);
      job.question={id:uid,text:text(input.question,2000),at:now};job.status='Needs your answer';break;
    }
    case 'answer': {
      const job=state.jobs[input.job];need(job?.status==='Needs your answer'&&job.question.id===input.question,'Question changed',409);
      need(!(await stale(state,job)),'Feedback or source changed. Process Review again.',409);
      const target=job.corrections[0],content=text(input.text),ts=[{symbol:target.symbol,revision:target.revision,configurations:[]}];
      state.comments[uid]={id:uid,text:content,attachments:[],targets:ts,originalTargets:ts,originalText:content,originalAttachments:[],created:now,at:now,edit:uid,author:'user',question:job.question.id};
      job.answers=[...(job.answers||[]),{question:clone(job.question),comment:uid,at:now}];
      target.comments=clone(feedback(state,target.symbol,target.revision));target.signature=await signature(state,target.symbol,target.revision);
      job.question=null;job.status='Waiting for desktop';break;
    }
    case 'publication': {
      const job=state.jobs[input.job]; lease(job,input,now);
      need(job.publications.some(t=>t.symbol===input.symbol && t.revision===input.revision),'Revision is outside this job');
      const s=symbol(state,input.symbol); need(!s.discarded && s.selected===input.revision,'Selected revision changed',409);
      evidence.previous=s.published; s.published=input.revision; s.confirmed=false; break;
    }
    case 'published': {
      const job=state.jobs[input.job]; lease(job,input,now); const s=symbol(state,input.symbol);
      need(s.published===input.revision && job.publications.some(t=>t.symbol===input.symbol && t.revision===input.revision),'Publication changed',409);
      need(input.proof?.catalog===input.revision && Array.isArray(input.proof.assets),'Missing retrieval proof');
      s.confirmed=true; s.publishedAt=now; s.proof=input.proof; break;
    }
    case 'fail': {
      const job=state.jobs[input.job]; lease(job,input,now); job.status='Failed'; job.error=text(input.error,2000); break;
    }
    case 'complete': {
      const job=state.jobs[input.job]; lease(job,input,now);
      need(job.phase==='correct' && job.corrections.every(t=>job.results.some(r=>r.symbol===t.symbol)),'Correction uploads are incomplete');
      job.status='Ready to review'; break;
    }
    case 'upload': {
      const r=input.revision; need(r?.id && r.symbol?.id,'Missing revision'); const id=r.symbol.id;
      let s=state.symbols[id]; need(!s || !s.revisions.includes(r.id),'Revision exists',409);
      need(!s || r.parent===s.latest,'Parent is not the latest saved revision',409);
      if(input.job) {
        const job=state.jobs[input.job]; lease(job,input,now);
        need(job.phase==='correct' && (job.workflow===2?job.authorized:job.approved),'Correction is not authorized');
        const target=job.corrections.find(t=>t.symbol===id && t.revision===r.parent);
        need(target && !job.results.some(x=>x.symbol===id),'Unexpected correction target');
        need(await signature(state,id,r.parent)===target.signature,'Correction is stale',409);
        job.results.push({symbol:id,revision:r.id,parent:r.parent,proposal:job.proposal?.id||null,summary:String(r.change?.why||'Updated drawing').slice(0,2000),at:now});
      }
      if(!s) state.symbols[id]=s={id,name:r.symbol.name,family:r.symbol.family||r.symbol.types?.[0]||'Symbols',batch:r.batch||'Individual',revisions:[],selected:null,published:null};
      s.revisions.push(r.id); s.latest=r.id; s.name=r.symbol.name; s.arrivedAt=now; s.candidate=!r.migration || s.candidate;
      if(!r.migration){s.updateRevision=r.id;s.updateSummary=String(r.change?.why||'New candidate ready to review').slice(0,2000);}
      if(r.migration) {need(s.revisions.length===1,'Migration cannot overwrite existing history');s.selected=r.id;s.published=r.id;s.confirmed=true;s.migrated=true;}
      // Never clear an earlier verified or published selection on arrival.
      result={id:r.id}; evidence={revision:r.id,symbol:id,parent:r.parent,fingerprint:r.fingerprint,migration:!!r.migration,job:input.job||null};
      break;
    }
    default: throw new Problem('Unknown action',404);
  }
  return {state,result,evidence};
}
