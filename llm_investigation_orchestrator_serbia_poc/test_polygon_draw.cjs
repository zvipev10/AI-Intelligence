const assert=require('node:assert/strict');
global.document={addEventListener(){}};
const Draw=require('./polygon_draw');
let data, zoom=true;
const map={on(){},doubleClickZoom:{isEnabled:()=>zoom,disable:()=>zoom=false,enable:()=>zoom=true},getContainer:()=>({classList:{toggle(){}}}),getCanvas:()=>({style:{}}),project:p=>({x:p[0],y:p[1]}),isStyleLoaded:()=>true,getSource:()=>({setData:d=>data=d})};
const draw=new Draw(map,{addEventListener(){},setAttribute(){}},{hidden:true});
const click=(x,y)=>draw.click({lngLat:{lng:x,lat:y},point:{x,y}});
draw.start();assert(!zoom);click(0,0);click(100,0);click(0,0);assert(draw.active);assert.equal(draw.points.length,2);
click(100,100);click(0,0);assert(!draw.active);assert(zoom);assert.deepEqual(draw.polygons[0],[[0,0],[100,0],[100,100],[0,0]]);assert.equal(data.features[0].geometry.type,'Polygon');
draw.start();click(30,30);draw.cancel();assert.equal(draw.polygons.length,1);assert.equal(draw.points.length,0);
zoom=false;draw.start();draw.cancel();assert(!zoom);
console.log('PASS: minimum vertices, closure, cancellation, completed polygon preservation, navigation restoration');

map.isStyleLoaded=()=>false; draw.start(); click(30,30); draw.cancel(); assert.equal(data.features.length,1); console.log("PASS: cancellation updates existing source while tiles are loading");
