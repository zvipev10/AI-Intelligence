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

let selected;
let sourceData;
const handlers={};
const interactiveMap={
  on(event,layer,handler){ handlers[`${event}:${layer}`]=handler; },
  doubleClickZoom:{isEnabled:()=>true,disable(){},enable(){}},
  getContainer:()=>({classList:{toggle(){}}}), getCanvas:()=>({style:{}}),
  project:p=>({x:p[0],y:p[1]}), isStyleLoaded:()=>true,
  getSource:()=>null, addSource(_id,value){ sourceData=value.data; }, addLayer(){}
};
const interactive=new Draw(interactiveMap,{addEventListener(){},setAttribute(){}},{hidden:true},{onSelect:value=>selected=value});
interactive.start(); interactive.click({lngLat:{lng:0,lat:0},point:{x:0,y:0}}); interactive.click({lngLat:{lng:100,lat:0},point:{x:100,y:0}}); interactive.click({lngLat:{lng:100,lat:100},point:{x:100,y:100}}); interactive.click({lngLat:{lng:0,lat:0},point:{x:0,y:0}});
assert.equal(sourceData.features[0].properties.polygonId, interactive.polygonIds[0]);
handlers["click:draw-polygon-fill"]({features:[{properties:{polygonId:interactive.polygonIds[0]}}],originalEvent:{preventDefault(){},stopPropagation(){}}});
assert.deepEqual(selected.coordinates,[[0,0],[100,0],[100,100],[0,0]]);
console.log("PASS: clicking a completed polygon selects it for the memory workflow");
