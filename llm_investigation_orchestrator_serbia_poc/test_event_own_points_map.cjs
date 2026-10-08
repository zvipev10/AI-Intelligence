const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(`${__dirname}/app.js`,'utf8');
const markers=[];
class Marker{constructor(o){this.el=o.element;}setLngLat(p){this.p=p;return this;}setPopup(){return this;}addTo(){markers.push(this);return this;}}
class Bounds{constructor(){this.n=0;}extend(){this.n++;}isEmpty(){return !this.n;}}
const el=()=>({style:{setProperty(){}},dataset:{},setAttribute(){},addEventListener(){},appendChild(){},classList:{add(){}}});
const layer={id:'events:Location updates',kind:'events',label:'Location updates',color:'#f00'};
const rows=[
 {event_id:'LU-1',latitude:'32.08',longitude:'34.78'},
 {event_id:'LU-2',latitude:'32.08',longitude:'34.78'},
 {event_id:'LU-3',latitude:'32.06',longitude:'34.80'},
 {event_id:'LU-4',latitude:'',longitude:''},
];
const context={state:{mapReady:true,markers:[],map:{fitBounds(){}}},LOCATIONS:{},MIL_STD_ORGANIZATIONS:{},console,
 maplibregl:{Marker,Popup:class{setHTML(){return this;}},LngLatBounds:Bounds},document:{createElement:el},
 activeLocaleText:(he,en)=>en,currentLocale:()=>'en',currentLocaleTag:()=>'en-US',escapeHtml:s=>String(s),
 clearMarkers(){},visibleLayers:()=>[layer],itemsForLayerPresentation:()=>rows,isCellularCallRecord:()=>false,
 milStdOrganizationDescriptors:()=>[],renderMilStdDescriptors(){},renderInvestigationOverlays(){},renderPolygonOverlays(){},coalesceEvidenceDescriptors:d=>d,confidenceLabel:String,milStdMarkerElement:el,milStdPopupHtml:()=>"",targetQuantityLabel:String};
vm.createContext(context);
for(const name of ['eventOwnPoint','renderMap']){
 const start=source.indexOf(`function ${name}(`);const end=source.indexOf('\nfunction ',start+1);
 vm.runInContext(source.slice(start,end),context);
}
context.renderMap();
assert.equal(markers.length,2);
const points=markers.map(m=>m.p.join(',')).sort();
assert.deepEqual(points,['34.78,32.08','34.8,32.06']);
assert.equal(context.eventOwnPoint({latitude:'',longitude:''}),null);
assert.equal(context.eventOwnPoint({latitude:'95',longitude:'1'}),null);
console.log('PASS: events without a location object draw at their own coordinates, grouped by point');
