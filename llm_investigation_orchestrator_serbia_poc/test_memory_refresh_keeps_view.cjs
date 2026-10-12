const fs=require("fs"),vm=require("vm");
const assert=require("assert");
const src=fs.readFileSync(require("path").join(__dirname,"app.js"),"utf8");
function fn(name){const i=src.indexOf((src.includes("async function "+name+"(")?"async function ":"function ")+name+"(");let d=0,j=src.indexOf(") {",i)+2;for(let k=j;k<src.length;k++){if(src[k]=="{")d++;else if(src[k]=="}"){d--;if(!d)return src.slice(i,k+1);}}}
const names=["loadInvestigationItemLayers","addResultLayers","ensureActiveLayer","buildCatalogLayer","sanitizeLayerKey","usedLayerColors","nextLayerColor","roleWorkspaceLayers","roleWorkspaceAllowsLayer","ensureLayerFilterState"];
let groups=[];
const ctx={state:{layers:[],investigationId:"inv",investigationMemoryLoadToken:1,activeLayerId:null},LAYER_COLORS:["#1","#2","#3"],
 fetch:async()=>({ok:true,json:async()=>({layers:groups})}),buildLocaleApiUrl:x=>x,activeLocaleText:(h,e)=>e,renderAllViews(){},renderLayerSelector(){},
 roleWorkspaceAllowsCatalogLayer:()=>true,layerId:(k,l)=>k+":"+l,console};
vm.createContext(ctx);
for(const n of names){const f=fn(n); if(!f){console.log("missing",n);continue;} vm.runInContext(f.replace(/^(async )?function (\w+)/,(m,a,b)=>`${b}=${a||""}function ${b}`),ctx);}
(async()=>{
 const s=ctx.state, vis=()=>Object.fromEntries(s.layers.map(l=>[l.label||l.id,l.visible]));
 s.layers.push({id:"cat::ADINT",kind:"events",label:"ADINT",visible:true,capabilities:{table:true,map:true},sourceId:"cat",catalogLayerId:"events:ADINT"});
 s.activeLayerId="cat::ADINT";
 groups=[{label:"Satellite",rows:[{event_id:"r1",latitude:"1"}]}];
 await ctx.loadInvestigationItemLayers(1);  // opening the investigation opens its memory tab
 assert.equal(true, vis()["Satellite · memory"]);
 s.activeLayerId="cat::ADINT";
 groups=[{label:"Satellite",rows:[{event_id:"r1",latitude:"1"}]},{label:"ADINT",rows:[{event_id:"a1",latitude:"1"}]}];
 await ctx.loadInvestigationItemLayers(1);  // a save: nothing new is shown, the active layer stays
 assert.equal("cat::ADINT", s.activeLayerId);
 assert.deepEqual({"ADINT":true,"Satellite · memory":true,"ADINT · memory":false}, vis());
 groups=[]; await ctx.loadInvestigationItemLayers(1);
 groups=[{label:"Satellite",rows:[{event_id:"r1",latitude:"1"}]}]; await ctx.loadInvestigationItemLayers(1);  // delete, save again
 assert.equal(false, vis()["Satellite · memory"]);
 assert.equal("cat::ADINT", s.activeLayerId);
 console.log("PASS: saving to memory refreshes the memory tabs without opening or showing them");
})().catch(e=>{console.error(e);process.exit(1);});
