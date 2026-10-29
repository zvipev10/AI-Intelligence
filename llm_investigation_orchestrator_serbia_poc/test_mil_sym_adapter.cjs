const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");
const lib = require("./vendor/mil-sym-ts/C5Ren.umd.js");
require("./mil_sym_adapter.js");
const adapter = globalThis.MilitarySymbols;
const names = {unit:"Unspecified", brigade:"Unspecified", infantry:"Infantry", "mechanized-infantry":"Armored/Mechanized/Tracked", engineer:"Engineer", headquarters:"Unspecified", aviation:"Unspecified", "armored-vehicle":"Armored", "logistics-truck":"Vehicle (Generic)", "vehicle-convoy":"Vehicle", helicopter:"Rotary Wing"};
for (const [key, name] of Object.entries(names)) {
  for (const [affiliation, digit] of Object.entries({unknown:"1",friendly:"3",neutral:"4",hostile:"6"})) {
    const id = adapter.sidc(key, affiliation);
    assert.match(id, /^15[0-9]{18}$/);
    assert.equal(id[3], digit);
    const info = lib.MSLookup.getInstance().getMSLInfo(id);
    assert.equal(info.getName(), name);
    assert.equal(info.getMinPointCount(), 1);
    assert.equal(info.getBasicSymbolID(), adapter.registry[key].basic);
  }
}
assert.equal(adapter.sidc("brigade").slice(8,10), "18");
assert.equal(adapter.sidc("headquarters")[7], "2");
assert.equal(adapter.sidc("unmapped"), null);
assert.equal(adapter.render("infantry", "friendly"), null); // library absent: plain fallback
// Exercise the application's real descriptors using both actual dataset fixtures and view metadata.
const source = fs.readFileSync(path.join(__dirname,"app.js"),"utf8");
const chunk = source.slice(source.indexOf("const MIL_STD_VERSION"), source.indexOf("function createInvestigationId"));
const sandbox = {console, activeLocaleText: (he,en)=>en, itemsForLayerPresentation: layer=>layer.items};
vm.createContext(sandbox);vm.runInContext(chunk,sandbox);
for (const family of ["airborne_isr_video_exploitation", "cctv_video", "satellite_imagery"]) {
 const event = {collection_family:family,object_class:"military vehicle convoy",location_id:"site",record_id:"REC-1",entity_id:"ENT-KFOR-RCE"};
 const d=sandbox.milStdObservationDescriptor(event);
 assert.equal(d.symbolKey,"vehicle-convoy");assert.equal(d.affiliation,"unknown");assert.equal(d.id,"REC-1");
 assert.equal(d.sourceBadge, {airborne_isr_video_exploitation:"UAV",cctv_video:"CCTV",satellite_imagery:"Satellite"}[family]);
 assert.equal(sandbox.milStdObservationDescriptor({...event,location_id:""}),null);
}
for (const family of ["adint","ipdr","supplied_cellular_record","scenario_cellular_call_collection","future_sensor","",undefined]) {
 const d=sandbox.milStdObservationDescriptor({collection_family:family,object_class:"Vehicle convoy",location_id:"site",record_id:"REC-2"});
 assert.equal(d.symbolKey,"vehicle-convoy");assert.equal(d.affiliation,"unknown");assert.equal(d.sourceBadge,"");
 assert.equal(sandbox.milStdObservationDescriptor({collection_family:family,location_id:"site"}),null);
 assert.equal(sandbox.milStdObservationDescriptor({collection_family:family,object_class:"Unclassified",location_id:"site"}),null);
}
const makeEvidence=(object_class)=>sandbox.milStdEvidenceDescriptor({evidence_id:object_class,location_ids:["site"],subject_entity_ids:[],object_class,source_record_ids:[],confidence:"high"});
const grouped=sandbox.coalesceEvidenceDescriptors([makeEvidence("Vehicle convoy"),makeEvidence("Armored vehicle")]);
assert.equal(grouped.length,2,"different symbols at one location must not be merged");
const org=sandbox.milStdOrganizationDescriptors({items:[{entity_id:"ENT-SAF-2BRIGADE",top_locations:[{location_id:"site",presence_claim:true}]}]});
assert.equal(org[0].symbolKey,"brigade");assert.equal(org[0].affiliation,"friendly");
console.log("PASS: 44 catalog mappings, affiliation/echelon/HQ, source-independent classification, provenance, fallback, distinct evidence grouping");

if (process.argv.includes("--render")) {
  const {createCanvas} = require("./.demo-build/render-check/node_modules/canvas");
  globalThis.document = {createElement(tag) {assert.equal(tag,"canvas");return createCanvas(64,64);}};
  globalThis.C5Ren = lib;
  for (const key of Object.keys(names)) for (const affiliation of ["unknown","friendly","neutral","hostile"]) {
    const rendered=adapter.render(key,affiliation);
    assert.ok(rendered,`${key}/${affiliation} must render`);
    assert.equal(rendered.sidc,adapter.sidc(key,affiliation));
    const svg=decodeURIComponent(rendered.uri.split(",").slice(1).join(","));
    assert.match(svg, /<svg[ >]/);assert.match(svg, /<\/svg>/);
    assert.equal(adapter.render(key,affiliation),rendered,"same symbol reuses cached rendering");
  }
  console.log("PASS: 44 actual SVG renders using native canvas; cache reuse");
}
