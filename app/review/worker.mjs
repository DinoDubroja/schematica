import {Problem,need,hash,canonical,transition} from './domain.mjs';

const PRIVATE={'Cache-Control':'private, no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'same-origin'};
const CSP="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'";
const json=(body,status=200,headers={})=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json',...PRIVATE,...headers}});
const stamp=()=>new Date().toISOString();
const random=()=>crypto.randomUUID();
const equal=(a,b)=>{if(typeof a!=='string'||typeof b!=='string'||a.length!==b.length)return false;let v=0;for(let i=0;i<a.length;i++)v|=a.charCodeAt(i)^b.charCodeAt(i);return v===0;};
async function body(request,max=1800000) {
  need(Number(request.headers.get('content-length')||0)<=max,'Request too large',413);
  const reader=request.body?.getReader(); need(reader,'Missing body'); const pieces=[];let n=0;
  while(true){const {done,value}=await reader.read();if(done)break;n+=value.length;if(n>max){await reader.cancel();throw new Problem('Request too large',413);}pieces.push(value);}
  const bytes=new Uint8Array(n);let offset=0;for(const piece of pieces){bytes.set(piece,offset);offset+=piece.length;}
  try{return JSON.parse(new TextDecoder().decode(bytes));}catch{throw new Problem('Invalid JSON');}
}
async function password(value,encoded) {
  if(!encoded || typeof value!=='string' || value.length>256)return false;
  const [salt,expected]=encoded.split(':');
  const key=await crypto.subtle.importKey('raw',new TextEncoder().encode(value),'PBKDF2',false,['deriveBits']);
  const bits=await crypto.subtle.deriveBits({name:'PBKDF2',salt:new TextEncoder().encode(salt),iterations:100000,hash:'SHA-256'},key,256);
  return equal([...new Uint8Array(bits)].map(n=>n.toString(16).padStart(2,'0')).join(''),expected);
}
async function auth(request,env) {
  const token=request.headers.get('authorization');
  if(token?.startsWith('Bearer ') && equal(await hash(token.slice(7)),env.DESKTOP_TOKEN_HASH))return 'desktop';
  const cookie=request.headers.get('cookie')?.match(/(?:^|;\s*)review_session=([^;]+)/)?.[1];
  if(cookie && await env.DB.prepare('SELECT hash FROM sessions WHERE hash=? AND expires>?').bind(await hash(cookie),Date.now()).first())return 'user';
  return null;
}
function sameOrigin(request) {
  need(request.headers.get('origin')===new URL(request.url).origin,'Open Review on its own website',403);
}
async function readState(env) {
  const row=await env.DB.prepare('SELECT * FROM state WHERE id=1').first();need(row,'Review storage is not initialized',503);
  return {...row,value:JSON.parse(row.body)};
}
async function getRevision(env,id) {
  const row=await env.DB.prepare('SELECT body FROM revisions WHERE id=?').bind(id).first();need(row,'Unknown revision',404);
  const revision=JSON.parse(row.body);await completeGeometry(env,revision.symbol.configurations);return revision;
}
async function completeGeometry(env,configs) {
  const missing=configs.filter(c=>!c.visual_center_from_origin_mm),hashes=[...new Set(missing.map(c=>c.sha256))],art=new Map();
  for(let i=0;i<hashes.length;i+=90){const chunk=hashes.slice(i,i+90);for(const a of(await env.DB.prepare(`SELECT hash,body FROM assets WHERE hash IN (${chunk.map(()=>'?').join(',')})`).bind(...chunk).all()).results)art.set(a.hash,a.body);}
  for(const c of missing){const match=art.get(c.sha256)?.match(/viewBox="([^"]+)"/);need(match,'Missing drawing bounds',503);const [x,y,w,h]=match[1].split(/\s+/).map(Number);c.visual_center_from_origin_mm=[(x+w/2-c.origin_svg[0])*25.4/72,(y+h/2-c.origin_svg[1])*25.4/72];}
}
export function validateSVG(svg) {
  need(typeof svg==='string' && svg.length<500000 && /<svg[\s>]/.test(svg),'Invalid SVG');
  need(!/<!DOCTYPE|<!ENTITY|<\?xml-stylesheet|<(?:script|foreignObject|iframe|image|animate\w*|set|style|a|audio|video)\b|\bon[a-z]+\s*=|javascript:|data:|@import/i.test(svg),'Unsafe SVG');
  const tags=new Set(['svg','g','defs','symbol','path','use','metadata','title','desc','rect','line','circle','ellipse','polyline','polygon','text','tspan','clipPath','mask','linearGradient','radialGradient','stop']);
  for(const match of svg.matchAll(/<\/?([A-Za-z][\w:.-]*)\b/g))need(tags.has(match[1]),'Unsupported SVG element');
  need(!/\bstyle\s*=/i.test(svg),'Inline SVG styles are not supported; use presentation attributes');
  for(const match of svg.matchAll(/(?:href\s*=\s*["']([^"']+)|url\(\s*["']?([^\s)"']+))/gi))need((match[1]||match[2]).startsWith('#'),'External SVG references are not allowed');
}
async function validateRevision(env,r) {
  need(r && /^[a-f0-9-]{36}$/.test(r.id) && /^[a-z][a-z0-9-]{0,79}$/.test(r.symbol?.id),'Invalid revision identity');
  need(typeof r.source==='object' && r.source.definition?.id===r.symbol.id && typeof r.source.recipe==='string','Drawing source required');
  for(const field of ['name','description'])need(typeof r.symbol[field]==='string' && r.symbol[field].trim(),'Missing symbol metadata');
  need(Array.isArray(r.symbol.keywords) && r.symbol.keywords.length,'Keywords required');
  need(Array.isArray(r.symbol.pins) && r.symbol.pins.length && new Set(r.symbol.pins.map(p=>p.id)).size===r.symbol.pins.length,'Invalid pins');
  need(Array.isArray(r.symbol.parts) && r.symbol.parts.length && new Set(r.symbol.parts.map(p=>p.id)).size===r.symbol.parts.length,'Invalid parts');
  need(r.symbol.pins.every(p=>r.symbol.parts.some(part=>part.id===p.lead_part)),'A connection needs its named lead part');
  need(canonical([...r.symbol.presets?.sizes||[]].sort())===canonical(['large','medium','small']) && canonical([...r.symbol.presets?.strokes||[]].sort())===canonical(['medium','thick','thin']),'Support all three sizes and independent strokes');
  for(const field of ['id','revision','name','description','keywords','parts','pins','presets','options'])need(canonical(r.source.definition[field]??null)===canonical(r.symbol[field]??null),'Source definition differs from symbol metadata: '+field);
  const expected=[];
  for(const size of r.symbol.presets?.sizes||[])for(const stroke of r.symbol.presets?.strokes||[]){
    let combos=[{}];for(const [name,spec] of Object.entries(r.symbol.options||{})) {
      need(spec.name && spec.values?.length>=2 && spec.values.some(v=>v.id===spec.default),'Invalid option');
      combos=combos.flatMap(o=>spec.values.map(v=>({...o,[name]:v.id})));
    } for(const options of combos)expected.push(canonical({size,stroke,options}));
  }
  need(expected.length>=9 && expected.length<=288 && expected.length===r.symbol.configurations?.length,'Every supported configuration is required');
  const seen=new Set(), hashes=new Set();
  for(const c of r.symbol.configurations) {
    const choice=canonical({size:c.size,stroke:c.stroke,options:c.options||{}});
    need(expected.includes(choice) && !seen.has(choice),'Missing or duplicate configuration'); seen.add(choice);
    need(/^[a-z0-9-]+$/.test(c.key) && /^[a-f0-9]{64}$/.test(c.sha256) && /^[a-f0-9]{64}$/.test(c.fragment),'Invalid artwork manifest');
    need(Number.isFinite(c.width_mm) && c.width_mm>0 && c.width_mm<1000 && Number.isFinite(c.height_mm) && c.height_mm>0 && c.height_mm<1000,'Invalid drawing bounds');
    need(c.pins_mm && r.symbol.pins.every(p=>Array.isArray(c.pins_mm[p.id]) && c.pins_mm[p.id].length===2 && c.pins_mm[p.id].every(x=>Number.isFinite(x)&&Math.abs(x-Math.round(x))<1e-6)),'Connections must be on the 1 mm grid');
    hashes.add(c.sha256);hashes.add(c.fragment);
  }
  const list=[...hashes],artwork=new Map();
  for(let i=0;i<list.length;i+=90) {
    const chunk=list.slice(i,i+90), rows=await env.DB.prepare(`SELECT hash,body FROM assets WHERE hash IN (${chunk.map(()=>'?').join(',')})`).bind(...chunk).all();
    need(rows.results.length===chunk.length,'Upload every asset before the revision');
    for(const row of rows.results)artwork.set(row.hash,row.body);
  }
  for(const c of r.symbol.configurations) {
    need(c.symbol_id===r.symbol.id && c.key.startsWith(r.symbol.id+'-'),'Configuration identity mismatch');
    const raw=artwork.get(c.sha256),match=raw.match(/<metadata(?:\s[^>]*)?>([\s\S]*?)<\/metadata>/);
    need(match,'Artwork metadata is required');
    let meta;try{meta=JSON.parse(match[1].replace(/&quot;/g,'"').replace(/&apos;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&'));}catch{throw new Problem('Invalid artwork metadata');}
    need(meta.symbol_id===r.symbol.id && meta.revision===r.symbol.revision && meta.settings.size===c.size && meta.settings.stroke===c.stroke,'Artwork does not match its configuration');
    need(canonical(meta.pins_mm)===canonical(c.pins_mm) && canonical(meta.settings.options||{})===canonical(c.options||{}),'Artwork connections or options differ from metadata');
    const partIds=r.symbol.parts.map(p=>p.id).sort();need(canonical([...meta.parts].sort())===canonical(partIds),'Artwork parts differ from definition');
  }
  need(r.readiness?.configurations===expected.length && r.readiness?.reference && r.readiness?.renderer && r.readiness?.visual?.summary && r.readiness?.visual?.by,'Rendering and visual comparison evidence required');
  need(r.fingerprint===await hash({source:r.source,configurations:r.symbol.configurations.map(c=>({key:c.key,sha256:c.sha256,fragment:c.fragment}))}),'Fingerprint does not match source and artwork');
  need(JSON.stringify(r).length<1500000,'Revision is too large');
}
async function mutate(request,env,actor,action) {
  const input=await body(request), id=request.headers.get('idempotency-key');
  need(id && /^[\w:.-]{8,160}$/.test(id),'Provide an Idempotency-Key');
  const requestHash=await hash({actor,action,input});
  const prior=await env.DB.prepare('SELECT * FROM requests WHERE id=?').bind(id).first();
  if(prior){need(prior.hash===requestHash,'Idempotency key reused for a different request',409);return json(JSON.parse(prior.response));}
  const row=await readState(env), at=stamp(), token=random();
  if(action==='upload') {
    await validateRevision(env,input.revision);
    if(input.revision.migration) need(env.MIGRATION_ENABLED==='true','Initial migration is closed',403);
    if(input.revision.parent) {
      const parent=await getRevision(env,input.revision.parent);need(parent.symbol.id===input.revision.symbol.id,'Parent belongs to another symbol');
      need(input.revision.symbol.revision===parent.symbol.revision+1,'Increment the drawing revision for a new saved revision');
    }
  }
  if(action==='comment')for(const target of input.targets||[]) {
    const rev=await getRevision(env,target.revision);
    need((target.configurations||[]).every(key=>rev.symbol.configurations.some(c=>c.key===key)),'Unknown target configuration');
  }
  if(action==='published') {
    const rev=await getRevision(env,input.revision);
    need(canonical([...input.proof.assets].sort())===canonical([...new Set(rev.symbol.configurations.map(c=>c.sha256))].sort()),'Incomplete public retrieval proof');
  }
  const changed=await transition(row.value,action,input,{actor,now:at,id:token});
  if(action==='claim' && changed.result.job===null && !changed.result.stale)return json({job:null,version:row.version});
  const response={...changed.result,version:row.version+1};
  const guard='EXISTS(SELECT 1 FROM state WHERE id=1 AND token=?)';
  const statements=[env.DB.prepare('UPDATE state SET version=version+1,token=?,body=? WHERE id=1 AND version=?').bind(token,JSON.stringify(changed.state),row.version)];
  if(action==='upload') {
    const r=input.revision;
    statements.push(env.DB.prepare(`INSERT INTO revisions(id,symbol,parent,fingerprint,at,body,public,migration) SELECT ?,?,?,?,?,?,?,? WHERE ${guard}`).bind(r.id,r.symbol.id,r.parent||null,r.fingerprint,at,JSON.stringify({...r,at}),JSON.stringify(r.symbol),r.migration?1:0,token));
  }
  if(action==='publication') {
    const catalog=(await publishedCatalog(request,env,changed.state)).catalog;
    statements.push(env.DB.prepare(`INSERT INTO publication(id,body) SELECT 1,? WHERE ${guard} ON CONFLICT(id) DO UPDATE SET body=excluded.body`).bind(JSON.stringify(catalog),token));
  }
  statements.push(env.DB.prepare(`INSERT INTO events(id,at,actor,action,body) SELECT ?,?,?,?,? WHERE ${guard}`).bind(token,at,actor,action,JSON.stringify(changed.evidence),token));
  statements.push(env.DB.prepare(`INSERT INTO requests(id,hash,response) SELECT ?,?,? WHERE ${guard}`).bind(id,requestHash,JSON.stringify(response),token));
  const results=await env.DB.batch(statements);need(results[0].meta.changes===1,'Another device saved first. Retry the same request.',409);
  return json(response);
}
async function publishedCatalog(request,env,state=null) {
  if(!state) {
    const saved=await env.DB.prepare('SELECT body FROM publication WHERE id=1').first();
    if(saved){const catalog=JSON.parse(saved.body);return {catalog,revisions:catalog.symbols.map(s=>({id:s.review_revision,symbol:s,migration:s.review_migrated}))};}
  }
  const base=await (await env.ASSETS.fetch(new Request(new URL('/library/catalog.json',request.url)))).json();
  const row=state?{value:state}:await readState(env), lookup=new Map(base.symbols.map(s=>[s.id,s]));
  const ids=Object.values(row.value.symbols).filter(s=>s.published).map(s=>s.published), revisions=[];
  for(let i=0;i<ids.length;i+=90){const chunk=ids.slice(i,i+90);revisions.push(...(await env.DB.prepare(`SELECT id,public,migration FROM revisions WHERE id IN (${chunk.map(()=>'?').join(',')})`).bind(...chunk).all()).results.map(x=>({id:x.id,symbol:JSON.parse(x.public),migration:!!x.migration})));}
  for(const r of revisions) {
    const s=structuredClone(r.symbol);s.review_revision=r.id;s.review_migrated=!!r.migration;
    if(!r.migration) {
      for(const c of s.configurations)c.svg=`published/${r.id}/${c.key}.svg`;
      s.verification={status:'verified',fingerprint:s.verification?.fingerprint};
    }
    lookup.set(s.id,s);
  }
  base.symbols=[...lookup.values()];
  await completeGeometry(env,base.symbols.flatMap(s=>s.configurations));
  if(revisions.some(r=>!r.migration)) {
    const specs={};for(const s of base.symbols)for(const [name,spec] of Object.entries(s.options||{})) {
      if(!specs[name])specs[name]={default:spec.default,values:[]};
      for(const v of spec.values)if(!specs[name].values.includes(v.id))specs[name].values.push(v.id);
    }
    base.export_defaults=Object.fromEntries(Object.entries(specs).map(([k,s])=>[k,s.default]));
    let profiles=[{}];for(const name of Object.keys(specs).sort())profiles=profiles.flatMap(p=>specs[name].values.map(v=>({...p,[name]:v})));
    need(profiles.length<=1024,'Too many complete-library export profiles',503);
    base.exports={};base.export_settings={};
    for(const size of Object.keys(base.presets.sizes))for(const stroke of Object.keys(base.presets.strokes))for(const options of profiles) {
      const suffix=Object.entries(options).filter(([k,v])=>v!==specs[k].default).map(([k,v])=>`-${k}-${v}`).join(''),key=`${size}-${stroke}${suffix}`;
      base.exports[key]=`exports/schematica-${key}.svg`;base.export_settings[key]={size,stroke,options};
    }
  }
  // Complete-library profiles retain their existing URLs. The worker builds them from published revisions.
  return {catalog:base,revisions};
}
const xml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
async function libraryExport(request,env,key) {
  if(!await env.DB.prepare('SELECT id FROM publication WHERE id=1').first())return env.ASSETS.fetch(request);
  const {catalog,revisions}=await publishedCatalog(request,env), settings=catalog.export_settings[key];need(settings,'Unknown export',404);
  if(revisions.every(r=>r.migration))return env.ASSETS.fetch(request);
  need(revisions.length===catalog.symbols.length,'Complete published source migration is required',503);
  const items=revisions.map(r=>{
    const options=Object.fromEntries(Object.entries(r.symbol.options||{}).map(([name,spec])=>[name,spec.values.some(v=>v.id===settings.options[name])?settings.options[name]:spec.default]));
    const c=r.symbol.configurations.find(c=>c.size===settings.size&&c.stroke===settings.stroke&&canonical(c.options||{})===canonical(options));need(c,'Unsupported export profile');return {...c,name:r.symbol.name};
  });
  await completeGeometry(env,items);
  const columns=Math.min(3,items.length),widths=Array.from({length:columns},(_,i)=>Math.max(...items.filter((_,n)=>n%columns===i).map(c=>c.width_mm)));
  const heights=Array.from({length:Math.ceil(items.length/columns)},(_,r)=>Math.max(...items.slice(r*columns,(r+1)*columns).map(c=>c.height_mm)));
  const defs=[],uses=[],byHash=new Map();
  const hashes=[...new Set(items.map(c=>c.fragment))];for(let i=0;i<hashes.length;i+=90){const chunk=hashes.slice(i,i+90);for(const a of(await env.DB.prepare(`SELECT hash,body FROM assets WHERE hash IN (${chunk.map(()=>'?').join(',')})`).bind(...chunk).all()).results)byHash.set(a.hash,a.body);}
  for(let i=0;i<items.length;i++) {
    const c=items[i],row=Math.floor(i/columns),col=i%columns,fragment=byHash.get(c.fragment);need(fragment,'Missing published export asset',503);
    // Fragments already have stable per-symbol/configuration ID namespaces and millimetre origins.
    const id=`library-${c.key}`,inner=fragment.replace(/^[\s\S]*?<svg[^>]*>/,'').replace(/<\/svg>\s*$/,'');
    const metadata=Object.fromEntries(['symbol_id','revision','size','stroke','pins_mm','options'].filter(k=>k in c).map(k=>[k,c[k]]));
    defs.push(`<symbol id="${xml(id)}" overflow="visible"><title>${xml(c.name)}</title><desc>Unlink the placed instance to edit its named parts.</desc><metadata>${xml(JSON.stringify(metadata))}</metadata>${inner}</symbol>`);
    const [dx,dy]=c.visual_center_from_origin_mm;
    uses.push(`<use href="#${xml(id)}" xlink:href="#${xml(id)}" transform="translate(${4+widths.slice(0,col).reduce((a,b)=>a+b,0)+6*col+widths[col]/2-dx},${4+heights.slice(0,row).reduce((a,b)=>a+b,0)+6*row+heights[row]/2-dy})"/>`);
  }
  const w=8+widths.reduce((a,b)=>a+b,0)+6*(columns-1),h=8+heights.reduce((a,b)=>a+b,0)+6*(heights.length-1);
  return new Response(`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="${w}mm" height="${h}mm" viewBox="0 0 ${w} ${h}"><title>Schematica symbol library</title><defs>${defs.join('')}</defs>${uses.join('')}</svg>`,{headers:{'Content-Type':'image/svg+xml','Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'}});
}
async function main(request,env) {
  const url=new URL(request.url), path=url.pathname;
  if(path==='/library/catalog.json') {
    const saved=await env.DB.prepare('SELECT body FROM publication WHERE id=1').first();
    if(!saved)return env.ASSETS.fetch(request);
    return new Response(saved.body,{headers:{'Content-Type':'application/json','Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'}});
  }
  if(path.startsWith('/library/published/')) {
    const [, , ,id,file]=path.split('/'),r=await getRevision(env,id),row=await readState(env);
    need(row.value.symbols[r.symbol.id]?.published===id,'Not published',404);
    const config=r.symbol.configurations.find(c=>c.key+'.svg'===file);need(config,'Unknown artwork',404);
    const asset=await env.DB.prepare('SELECT body FROM assets WHERE hash=?').bind(config.sha256).first();need(asset,'Missing artwork',503);
    return new Response(asset.body,{headers:{'Content-Type':'image/svg+xml','Cache-Control':'no-cache','Content-Security-Policy':"sandbox; default-src 'none'; style-src 'unsafe-inline'",'X-Content-Type-Options':'nosniff'}});
  }
  if(path.startsWith('/exports/schematica-')&&path.endsWith('.svg'))return libraryExport(request,env,path.slice('/exports/schematica-'.length,-4));
  if(path!=='/review' && !path.startsWith('/review/') && path!=='/api/review' && !path.startsWith('/api/review/'))return env.ASSETS.fetch(request);
  if(path==='/review/login' && request.method==='POST') {
    sameOrigin(request);const data=await body(request,2048),ip=await hash(request.headers.get('CF-Connecting-IP')||'local'),now=Date.now();
    const attempt=await env.DB.prepare('SELECT * FROM attempts WHERE key=?').bind(ip).first();
    need(!attempt||attempt.until<now||attempt.count<10,'Too many attempts. Try again in 15 minutes.',429);
    await env.DB.prepare('INSERT INTO attempts VALUES(?,1,?) ON CONFLICT(key) DO UPDATE SET count=CASE WHEN until<? THEN 1 ELSE count+1 END, until=CASE WHEN until<? THEN excluded.until ELSE until END').bind(ip,now+900000,now,now).run();
    need(await password(data.password,env.REVIEW_PASSWORD_HASH),'Password not recognized',401);
    const token=random()+random();await env.DB.prepare('INSERT INTO sessions VALUES(?,?)').bind(await hash(token),now+30*86400000).run();
    await env.DB.prepare('DELETE FROM attempts WHERE key=?').bind(ip).run();
    return json({ok:true},200,{'Set-Cookie':`review_session=${token}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=2592000`});
  }
  const actor=await auth(request,env);
  if(!actor) {
    if((path==='/review'||path==='/review/')&&request.method==='GET')return new Response(LOGIN,{headers:{'Content-Type':'text/html',...PRIVATE,'Content-Security-Policy':CSP.replace("script-src 'self'","script-src 'nonce-login'").replace("style-src 'self'","style-src 'nonce-login'")}});
    throw new Problem('Sign in to Review',401);
  }
  if(request.method!=='GET' && actor==='user')sameOrigin(request);
  if(path==='/review/logout' && request.method==='POST') {
    const cookie=request.headers.get('cookie')?.match(/review_session=([^;]+)/)?.[1];if(cookie)await env.DB.prepare('DELETE FROM sessions WHERE hash=?').bind(await hash(cookie)).run();
    return json({ok:true},200,{'Set-Cookie':'review_session=; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=0'});
  }
  if(path==='/api/review/state'&&request.method==='GET') {
    const row=await readState(env);const value=structuredClone(row.value);for(const j of Object.values(value.jobs))delete j.lease;
    return json({version:row.version,...value});
  }
  if(path==='/api/review/assets'&&request.method==='POST') {
    need(actor==='desktop','Desktop authentication required',403);const data=await body(request,1000000);validateSVG(data.body);
    need(data.hash===await hash(data.body),'Artwork checksum mismatch');
    await env.DB.prepare('INSERT OR IGNORE INTO assets(hash,mime,body) VALUES(?,?,?)').bind(data.hash,'image/svg+xml',data.body).run();return json({hash:data.hash});
  }
  if(path.startsWith('/api/review/actions/')&&request.method==='POST')return mutate(request,env,actor,path.slice('/api/review/actions/'.length));
  if(path.startsWith('/api/review/revisions/')&&request.method==='GET')return json(await getRevision(env,path.slice('/api/review/revisions/'.length)));
  if(path.startsWith('/review/assets/')&&request.method==='GET') {
    const h=path.slice('/review/assets/'.length);need(/^[a-f0-9]{64}$/.test(h),'Invalid artwork hash');
    const asset=await env.DB.prepare('SELECT body,mime FROM assets WHERE hash=?').bind(h).first();need(asset,'Unknown asset',404);
    return new Response(asset.body,{headers:{'Content-Type':asset.mime,...PRIVATE,'Content-Security-Policy':"sandbox; default-src 'none'; style-src 'unsafe-inline'"}});
  }
  if(path==='/api/review/evidence'&&request.method==='GET') {
    const after=Number(url.searchParams.get('after')||0);need(Number.isInteger(after)&&after>=0,'Invalid cursor');
    const events=(await env.DB.prepare('SELECT * FROM events WHERE sequence>? ORDER BY sequence LIMIT 100').bind(after).all()).results.map(e=>({...e,body:JSON.parse(e.body)}));
    return json({events,next:events.at(-1)?.sequence||after});
  }
  if(path==='/api/review/backup'&&request.method==='GET') {
    need(actor==='desktop','Desktop authentication required',403);
    const table=url.searchParams.get('table')||'state',after=url.searchParams.get('after')||'';
    need(['state','events','revisions','assets','requests','publication'].includes(table),'Unknown backup collection');
    const key={state:'id',events:'sequence',revisions:'id',assets:'hash',requests:'id',publication:'id'}[table],numeric=['state','events','publication'].includes(table);
    const rows=(await env.DB.prepare(`SELECT * FROM ${table} WHERE ${key}>? ORDER BY ${key} LIMIT 10`).bind(numeric?Number(after||0):after).all()).results;
    return json({rows,next:rows.at(-1)?.[key]??null});
  }
  if(path==='/review'||path==='/review/'||['/review/review.css','/review/review-app.js'].includes(path)) {
    const target=path.endsWith('.css')||path.endsWith('.js')?path:'/review/index.html';
    const response=await env.ASSETS.fetch(new Request(new URL(target,request.url)));return new Response(response.body,{status:response.status,headers:{...Object.fromEntries(response.headers),...PRIVATE,'Content-Security-Policy':CSP}});
  }
  throw new Problem('Not found',404);
}
export default {async fetch(request,env) {try{return await main(request,env);}catch(error){return json({error:error instanceof Problem?error.message:'Review could not complete this request. Your draft is retained.'},error.status||500);}}};

const LOGIN=`<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Schematica Review</title><style nonce="login">body{margin:0;background:#111914;color:#e4ece0;font:16px Segoe UI,sans-serif;min-height:100vh;display:grid;place-items:center}main{padding:28px;width:min(340px,80vw);background:#1a251e;border:1px solid #344639;border-radius:14px}h1{font-size:25px}input,button{box-sizing:border-box;width:100%;padding:13px;margin-top:12px;font:inherit;border-radius:7px;border:1px solid #344639}input{background:#111914;color:inherit}button{background:#b6d69f;color:#152710;cursor:pointer}a{color:#b6d69f}#message{font-size:14px;color:#ebc886}</style><main><a href="/">Schematica</a><h1>Review</h1><form><label for="password">Password</label><input id="password" type="password" autocomplete="current-password" required><button>Open Review</button><p id="message" role="status"></p></form></main><script nonce="login">document.querySelector('form').onsubmit=async e=>{e.preventDefault();const b=document.querySelector('button'),m=document.querySelector('#message');b.disabled=true;m.textContent='Signing in…';try{const r=await fetch('/review/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:document.querySelector('input').value})});const d=await r.json();if(!r.ok)throw Error(d.error);location.replace('/review');}catch(e){m.textContent=e.message;b.disabled=false;}};</script></html>`;
