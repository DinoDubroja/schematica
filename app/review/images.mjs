import {need} from './domain.mjs';

export const IMAGE_LIMIT=1048576;
// Raster-only, bounded images. SVG and arbitrary documents are never accepted.
export async function validateImage(input) {
  need(typeof input.body==='string'&&input.body.length<=Math.ceil(IMAGE_LIMIT/3)*4,'Image exceeds 1 MB',413);
  need(input.body.length%4===0&&/^[A-Za-z0-9+/]*={0,2}$/.test(input.body),'Invalid image encoding');
  const bytes=Uint8Array.from(atob(input.body),c=>c.charCodeAt(0)),view=new DataView(bytes.buffer);
  need(bytes.length>24&&bytes.length<=IMAGE_LIMIT,'Image exceeds 1 MB or is empty',413);
  const ascii=(at,n)=>String.fromCharCode(...bytes.slice(at,at+n));
  let mime,width,height;
  if(ascii(1,3)==='PNG'&&bytes[0]===137&&ascii(12,4)==='IHDR') {
    need(bytes.slice(4,8).join(',')==='13,10,26,10','Invalid PNG');mime='image/png';width=view.getUint32(16);height=view.getUint32(20);
  } else if(bytes[0]===255&&bytes[1]===216&&bytes[2]===255) {
    mime='image/jpeg';let offset=2;
    while(offset+4<bytes.length) {
      need(bytes[offset]===255,'Invalid JPEG');while(bytes[offset]===255)offset++;
      const marker=bytes[offset++];if(marker===217||marker===218)break;
      if(marker===1||marker>=208&&marker<=215)continue;
      need(offset+2<=bytes.length,'Invalid JPEG');
      const length=view.getUint16(offset);need(length>=2&&offset+length<=bytes.length,'Invalid JPEG');
      if([192,193,194,195,197,198,199,201,202,203,205,206,207].includes(marker)){need(length>=7,'Invalid JPEG');height=view.getUint16(offset+3);width=view.getUint16(offset+5);break;}
      offset+=length;
    }
  } else if(ascii(0,4)==='RIFF'&&ascii(8,4)==='WEBP') {
    mime='image/webp';need(view.getUint32(4,true)+8===bytes.length,'Invalid WebP');
    const kind=ascii(12,4);
    if(kind==='VP8X'&&bytes.length>=30){width=1+bytes[24]+bytes[25]*256+bytes[26]*65536;height=1+bytes[27]+bytes[28]*256+bytes[29]*65536;}
    if(kind==='VP8 '&&bytes.length>=30&&bytes[23]===157&&bytes[24]===1&&bytes[25]===42){width=view.getUint16(26,true)&16383;height=view.getUint16(28,true)&16383;}
    if(kind==='VP8L'&&bytes.length>=25&&bytes[20]===47){const bits=view.getUint32(21,true);width=(bits&16383)+1;height=((bits>>>14)&16383)+1;}
  }
  need(mime&&mime===input.mime,'Choose a PNG, JPEG or WebP image');
  need(width>0&&height>0&&width<=4096&&height<=4096&&width*height<=16000000,'Image dimensions are unsupported');
  const hash=[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(n=>n.toString(16).padStart(2,'0')).join('');
  need(hash===input.hash,'Image checksum mismatch');
  return {hash,mime,bytes:bytes.length,width,height,body:input.body};
}
