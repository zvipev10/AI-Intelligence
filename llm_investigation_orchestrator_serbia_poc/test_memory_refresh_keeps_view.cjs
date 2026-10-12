const fs=require("fs"),vm=require("vm");
const assert=require("assert");
const src=fs.readFileSync(require("path").join(__dirname,"app.js"),"utf8");
function fn(name){const i=src.indexOf((src.includes("async function "+name+"(")?"async function ":"function ")+name+"(");let d=0,j=src.indexOf(") {",i)+2;for(let k=j;k<src.length;k++){if(src[k]=="{")d++;else if(src[k]=="}"){d--;if(!d)return src.slice(i,k+1);}}}
const names=["loadInvestigationItemLayers","refreshInvestigationItemLayers","addResultLayers","ensureActiveLayer","buildCatalogLayer","sanitizeLayerKey","usedLayerColors","nextLayerColor","roleWorkspaceLayers","roleWorkspaceAllowsLayer","ensureLayerFilterState"];
let groups=[];
const ctx={state:{layers:[],investigationId:"inv",investigationMemoryLoadToken:1,activeLayerId:null},LAYER_COLORS:["#1","#2","#3"],
 fetch:async()=>({ok:true,json:async()=>({layers:groups})}),buildLocaleApiUrl:x=>x,activeLocaleText:(h,e)=>e,renderAllViews(){},renderLayerSelector(){},
 roleWorkspaceAllowsCatalogLayer:()=>true,layerId:(k,l)=>k+":"+l,console};
vm.createContext(ctx);
for(const n of names){const f=fn(n); if(!f){console.log("missing",n);continue;} vm.runInContext(f.replace(/^(async )?function (\w+)/,(m,a,b)=>`${b}=${a||""}function ${b}`),ctx);}
// Opening an investigation goes through loadInvestigationItemLayers; a save or removal only refreshes.
assert.match(fn("loadInvestigationMemory"), /if \(options\.restoreLayers\) \{[\s\S]*loadInvestigationItemLayers\(token\);[\s\S]*\} else \{[\s\S]*refreshInvestigationItemLayers\(token\);/);
(async()=>{
 const s=ctx.state, vis=()=>Object.fromEntries(s.layers.map(l=>[l.label||l.id,l.visible]));
 s.layers.push({id:"cat::ADINT",kind:"events",label:"ADINT",visible:true,capabilities:{table:true,map:true},sourceId:"cat",catalogLayerId:"events:ADINT"});
 s.activeLayerId="cat::ADINT";
 groups=[{label:"Satellite",rows:[{event_id:"r1",latitude:"1"}]}];
 await ctx.loadInvestigationItemLayers(1);  // opening the investigation opens its memory tab
 assert.equal(true, vis()["Satellite · memory"]);
 s.activeLayerId="cat::ADINT";
 const before=JSON.stringify(vis());
 groups=[{label:"Satellite",rows:[{event_id:"r1",latitude:"1"},{event_id:"r2",latitude:"1"}]},{label:"ADINT",rows:[{event_id:"a1",latitude:"1"}]}];
 await ctx.refreshInvestigationItemLayers(1);  // a save: the open tab gets its row, no new tab
 assert.equal("cat::ADINT", s.activeLayerId);
 assert.equal(before, JSON.stringify(vis()));
 assert.equal(2, s.layers.find(l=>l.label==="Satellite · memory").items.length);
 groups=[{label:"ADINT",rows:[{event_id:"a1",latitude:"1"}]}];
 await ctx.refreshInvestigationItemLayers(1);  // a removal empties the Satellite tab: it closes
 assert.deepEqual({"ADINT":true}, vis());
 assert.equal("cat::ADINT", s.activeLayerId);
 console.log("PASS: saving to memory updates the open memory tabs without opening, showing or hiding any");
})().catch(e=>{console.error(e);process.exit(1);});
