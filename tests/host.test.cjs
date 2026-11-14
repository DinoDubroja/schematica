const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../app/viewer/host.js'), 'utf8');

function harness({rejectContext = false} = {}) {
  const handlers = {}, messages = [];
  const data = {catalog: {symbols: []}, session: {filters: {}}, result: {session_id:'s', sequence:1}};
  const parent = {postMessage(message) {
    messages.push(message);
    if (!message.id) return;
    let result = {};
    if (message.method === 'ui/initialize') result = {protocolVersion:'2026-01-26', hostContext:{theme:'light'}, hostCapabilities:{serverTools:{}}};
    if (message.method === 'tools/call') result = message.params.name === 'viewer_data' ? {_meta:data} :
      message.params.name === 'get_artwork' ? {_meta:{svg:'<svg/>'}} : {structuredContent:{id:'resistor-eu',revision:1,configuration:{size:'small',stroke:'thick'}}};
    queueMicrotask(() => handlers.message({source:parent,origin:'https://host.example',data:{jsonrpc:'2.0',id:message.id,
      ...(rejectContext && message.method === 'ui/update-model-context' ? {error:{message:'Denied'}} : {result})}}));
    if (message.method === 'ui/initialize') queueMicrotask(() => queueMicrotask(() => handlers.message({source:parent,origin:'https://host.example',data:{jsonrpc:'2.0',method:'ui/notifications/tool-result',params:{structuredContent:{session_id:'s',sequence:1}}}})));
  }};
  const window = {SCHEMATICA_EMBEDDED:true,parent,addEventListener:(name,fn)=>handlers[name]=fn};
  const document = {documentElement:{dataset:{}},body:{scrollHeight:500}};
  vm.runInNewContext(source,{window,document,setTimeout,clearTimeout,queueMicrotask,ResizeObserver:class{observe(){}},URL,Blob});
  return {Host:window.SchematicaHost,messages,handlers,parent,data,document};
}

test('MCP Apps initializes, receives metadata, fetches artwork and sends an exact choice', async()=>{
  const h=harness();
  const loaded=await h.Host.load();
  assert.equal(loaded,h.data);
  assert.equal(h.messages[0].method,'ui/initialize');
  assert.equal(h.messages[1].method,'ui/notifications/initialized');
  assert.equal(h.document.documentElement.dataset.theme,'light');
  assert.equal(await h.Host.artwork({asset:'base/svg/r.svg'}),'<svg/>');
  const result=await h.Host.select({id:'resistor-eu',revision:1},{size:'small',stroke:'thick'});
  assert.equal(result.contextDelivered,true);
  const context=h.messages.find(m=>m.method==='ui/update-model-context');
  assert.equal(context.params.structuredContent.schematica_selection.revision,1);
});

test('host context refusal leaves a retrievable selection and reports fallback',async()=>{
  const h=harness({rejectContext:true});await h.Host.load();
  const result=await h.Host.select({id:'resistor-eu',revision:1},{size:'small',stroke:'thick'});
  assert.equal(result.contextDelivered,false);assert.equal(result.selection.id,'resistor-eu');
});

test('messages from another window do not change the viewer session',async()=>{
  const h=harness();await h.Host.load();let called=false;h.Host.subscribe(()=>called=true);
  h.handlers.message({source:{},origin:'https://host.example',data:{jsonrpc:'2.0',method:'ui/notifications/tool-result',params:{structuredContent:{session_id:'forged'}}}});
  assert.equal(called,false);
});
