const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const Preview=require('../app/viewer/preview-coordinates.js');
const root=path.join(__dirname,'..');
// Deliberately asymmetric crop: the origin is neither the image nor visual centre.
const asymmetric={width_mm:80*25.4/72,height_mm:40*25.4/72,origin_svg:[30,50],
  visual_center_from_origin_mm:[20*25.4/72,-10*25.4/72],pins_mm:{a:[-4,0],b:[8,2]},
  size:'medium',stroke:'medium',options:{},sha256:'a'.repeat(64)};
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-7,`${a} != ${b}`);

test('asymmetrically cropped artwork maps actual lead endpoints to physical terminals',()=>{
  const svg=fs.readFileSync(path.join(__dirname,'fixtures/asymmetric-preview.svg'),'utf8');
  const [x,y,w,h]=Preview.imageBounds(asymmetric);
  const endpoints=[...svg.matchAll(/data-part="lead-([ab])"><path d="M([\d.]+) ([\d.]+)/g)].map(m=>[m[1],+m[2],+m[3]]);
  assert.equal(endpoints.length,2);
  for(const [id,rawX,rawY] of endpoints){
    const imagePoint=[x+(rawX-10)*w/80,y+(rawY-20)*h/40];
    const libraryPoint=[(rawX-30)*Preview.MM_PER_SVG_UNIT,(rawY-50)*Preview.MM_PER_SVG_UNIT];
    const pin=Preview.pinPosition(asymmetric.pins_mm[id]);
    imagePoint.forEach((n,i)=>close(n,pin[i]));libraryPoint.forEach((n,i)=>close(n,pin[i]));
  }
  assert.equal(Preview.artworkTransform(asymmetric),'scale(0.35277777777777775) translate(-30,-50)');
});

test('resizing and zoom keep isotropic scale, millimetre spacing and origin together',()=>{
  for(const [width,height] of [[820,320],[318,210],[540,320]])for(const zoom of [.8,1,1.25,2]){
    const [x,y,w,h]=Preview.fitViewport(asymmetric,width/zoom,height/zoom);
    close(w/h,width/height);const scaleX=width/w,scaleY=height/h;close(scaleX,scaleY);
    for(const point of Object.values(asymmetric.pins_mm)){
      const [px,py]=Preview.pinPosition(point);
      close((px-x)*scaleX,(-x)*scaleX+px*scaleX);
      close((py-y)*scaleY,(-y)*scaleY+py*scaleY);
    }
    const [bx,by,bw,bh]=Preview.imageBounds(asymmetric);
    assert.ok(bx>x&&by>y&&bx+bw<x+w&&by+bh<y+h,'Drawing must fit with padding');
  }
});

function reviewArt(pins=true,small=false){
  const source=fs.readFileSync(path.join(root,'app/review/review-app.js'),'utf8').split('function renderStatus')[0];
  const context={SchematicaPreview:Preview,ResizeObserver:class{},localStorage:{getItem(){return null}},document:{},crypto:{}};
  vm.createContext(context);vm.runInContext(source,context);
  context.revision={symbol:{name:'Asymmetric fixture',options:{},configurations:[asymmetric]}};
  return vm.runInContext(`local.pins=${pins};art(revision,{},${small},true)`,context);
}
test('actual Review markup gives grid and terminal markers the same SVG origin',()=>{
  const html=reviewArt();
  assert.match(html,/patternUnits="userSpaceOnUse" x="-.5" y="-.5" width="1" height="1"/);
  assert.match(html,/<circle cx=".5" cy=".5"/);
  assert.match(html,/data-pin="a" cx="-4" cy="0"/);
  assert.match(html,/data-pin="b" cx="8" cy="-2"/);
  assert.match(html,/class="symbol-drawing"[^>]+x="-7.055/);
  assert.doesNotMatch(reviewArt(false),/data-pin=/);
  assert.doesNotMatch(reviewArt(true,true),/mm-grid|data-pin=/);
  const css=fs.readFileSync(path.join(root,'app/review/review.css'),'utf8');
  const canvas=css.match(/\.drawing-canvas\{([^}]+)\}/)[1];
  assert.doesNotMatch(canvas,/background-image|background-size/);
});
test('Library and Review load and use the same coordinate module',()=>{
  for(const file of ['app/viewer/index.html','app/review/index.html'])assert.match(fs.readFileSync(path.join(root,file),'utf8'),/preview-coordinates\.js/);
  const library=fs.readFileSync(path.join(root,'app/viewer/app.js'),'utf8');
  assert.match(library,/SchematicaPreview\.artworkTransform\(config\)/);
  assert.match(library,/SchematicaPreview\.pinPosition\(point\)/);
  assert.match(library,/SchematicaPreview\.gridLines/);
  assert.deepEqual(Preview.gridLines([-.5,-.5,2,2]),['M0,-0.5v2','M1,-0.5v2','M-0.5,0h2','M-0.5,1h2']);
});
