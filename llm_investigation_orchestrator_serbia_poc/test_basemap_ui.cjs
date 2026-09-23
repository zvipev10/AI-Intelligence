const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(`${__dirname}/app.js`,'utf8');
const buttons=['street','satellite'].map(mode=>({dataset:{basemap:mode},disabled:true,attrs:{},setAttribute(k,v){this.attrs[k]=v;},addEventListener(k,fn){this[k]=fn;}}));
const status={hidden:true};const events={};let options;const sources={},layouts=[],paints=[];
const base=[{id:'land',type:'fill',layout:{visibility:'visible'}},{id:'hidden',type:'line',layout:{visibility:'none'}},{id:'road_pri_fill',type:'line','source-layer':'transportation',paint:{'line-color':'#ddd','line-opacity':1}},{id:'boundary_state',type:'line','source-layer':'boundary',paint:{'line-color':'#aaa','line-opacity':.5}},{id:'place_city',type:'symbol',layout:{'text-field':{stops:[[8,'{name_en}'],[13,'{name}']]}},paint:{'text-color':'#333','text-halo-color':'#fff','text-halo-width':1}},{id:'house',type:'symbol',layout:{'text-field':'{housenumber}'}}];
const layers=structuredClone(base),marker={id:'record-marker'};
const context={state:{markers:[marker]},console,demoRuntime:{demo_profile:{map:{center:[38.5,35],zoom:10,minZoom:6,maxBounds:[[36,32],[42,38]]}}},activeLocaleText:(he,en)=>en,document:{querySelectorAll:()=>buttons,getElementById:()=>status},renderMap(){},maplibregl:{NavigationControl:class{},Map:class{
 constructor(o){options=o;}addControl(){}on(n,fn){events[n]=fn;}getStyle(){return {layers};}getLayer(id){return layers.find(l=>l.id===id);}addSource(id,s){sources[id]=s;}
 addLayer(layer,before){layers.splice(layers.findIndex(l=>l.id===before),0,layer);}moveLayer(id,before){const from=layers.findIndex(l=>l.id===id);const [layer]=layers.splice(from,1);layers.splice(layers.findIndex(l=>l.id===before),0,layer);}
 setLayoutProperty(...args){layouts.push(args);}setPaintProperty(...args){paints.push(args);}
}}};
vm.createContext(context);
for(const name of ['satelliteReferenceLayer','setMapBasemap','initMap']){
 const start=source.indexOf(`function ${name}(`);const end=name==='initMap'?source.indexOf('\nconst CONVERSATION_BOTTOM',start):source.indexOf('\nfunction ',start+1);
 vm.runInContext(source.slice(start,end),context);
}
context.initMap();events['style.load']();
assert.equal(options.center[0],38.5);assert.match(sources['satellite-imagery'].tiles[0],/tile\/\{z\}\/\{y\}\/\{x\}/);assert.match(sources['satellite-imagery'].attribution,/Esri/);
assert(layers.findIndex(l=>l.id==='satellite-imagery')<layers.findIndex(l=>l.id==='place_city'));
assert(layouts.some(([id,k,v])=>id==='place_city'&&JSON.stringify(v).includes('name_en')));
assert(buttons.every(b=>!b.disabled));
layers.push({id:'investigation-route',type:'line'});layouts.length=0;
buttons[1].click();assert.equal(context.state.basemapMode,'satellite');assert.equal(buttons[1].attrs['aria-pressed'],'true');
assert(layouts.some(([id,k,v])=>id==='land'&&v==='none'));assert(layouts.some(([id,k,v])=>id==='satellite-imagery'&&v==='visible'));
assert(layouts.some(([id,k,v])=>id==='road_pri_fill'&&k==='visibility'&&v==='visible'));assert(layouts.some(([id,k,v])=>id==='boundary_state'&&k==='visibility'&&v==='visible'));
assert(paints.some(([id,k,v])=>id==='road_pri_fill'&&k==='line-color'&&String(v).includes('255,215,112')));assert(paints.some(([id,k,v])=>id==='boundary_state'&&k==='line-color'&&String(v).includes('255,255,255')));
assert(layers.findIndex(l=>l.id==='satellite-imagery')<layers.findIndex(l=>l.id==='road_pri_fill'));assert(layers.findIndex(l=>l.id==='boundary_state')<layers.findIndex(l=>l.id==='place_city'));
assert(!layouts.some(([id])=>id==='investigation-route'));assert.equal(context.state.markers[0],marker);
buttons[0].click();assert.equal(context.state.basemapMode,'street');assert(layouts.some(([id,k,v])=>id==='hidden'&&v==='none'));assert(paints.some(([id,k,v])=>id==='place_city'&&k==='text-color'&&v==='#333'));assert(paints.some(([id,k,v])=>id==='road_pri_fill'&&k==='line-color'&&v==='#ddd'));assert(paints.some(([id,k,v])=>id==='boundary_state'&&k==='line-opacity'&&v===.5));
buttons[1].click();events.error({sourceId:'other'});assert.equal(context.state.basemapMode,'satellite');events.error({sourceId:'satellite-imagery'});assert.equal(context.state.basemapMode,'street');assert(!status.hidden);assert.match(status.textContent,/unavailable/);
events.load();assert(context.state.mapReady);
console.log('PASS: Street/Satellite toggle, vector roads/borders, English labels, credits, overlay/marker preservation, contrast restoration, imagery failure fallback');
