const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
const row = {event_id:'REC-IPDR-1',source_type:'IPDR',source_record_id:'000123',package_id:'PKG-1',evidence_type:'ipdr_record',imei:'',start_time:'2026-09-01T01:00:00Z',end_time:'2026-09-01T00:00:00Z',validation:{state:'invalid'},source_reference:{data_row:1}};
const pkg = {package_id:'PKG-1',record_count:300,catalog_layer_id:'ipdr-package:PKG-1'};
const context = {Set,Map,Date, console, activeLocaleText:(he,en)=>en,escapeHtml:v=>String(v??'').replaceAll('<','&lt;'),
  state:{events:[],entityMetadata:[],layerCatalog:[{ipdr_package:pkg}],layers:[{kind:'evidence',items:[{...row,evidence_id:row.event_id}]}]},
  isAdintRecord:()=>false, activeRoleWorkspaceProfile:()=>({allowedCatalogLayerIds:new Set(['events:IPDR'])})};
vm.createContext(context);
vm.runInContext(source.match(/const IPDR_SOURCE_FIELDS = .*;/)[0],context);
for (const name of ['isIpdrRecord','viewerObjects','viewerFields','isCellularGeolocationRecord','ipdrPackageLinkHtml','ipdrTimelineEntry','roleWorkspaceAllowsCatalogLayer','buildCatalogLayer']) {
 const start=source.indexOf(`function ${name}(`), next=source.slice(start+1).search(/\n(?:async )?function /);
 vm.runInContext(source.slice(start,start+1+next),context);
}
const objects=context.viewerObjects();
assert(objects.has('ipdr_package:PKG-1'));
assert(objects.has('record:REC-IPDR-1'));
const fields=context.viewerFields(row,'record');
assert(fields.some(([key,value])=>key==='imei'&&value==='—'));
assert(fields.some(([key])=>key==='source_reference'));
assert(!fields.some(([key])=>['entity_name','location_name'].includes(key)));
assert(context.viewerFields(pkg,'ipdr_package').some(([key,value])=>key==='provider'&&value==='Unknown'));
assert.match(context.ipdrTimelineEntry(row),/Invalid interval/);
assert.match(context.ipdrTimelineEntry(row),/data-viewer-id="REC-IPDR-1"/);
assert.match(context.ipdrTimelineEntry(row),/2026-09-01T00:00:00Z/);
assert.match(context.ipdrPackageLinkHtml(row,'record'),/data-viewer-kind="ipdr_package"/);
assert.match(context.ipdrPackageLinkHtml(pkg,'ipdr_package'),/Synthetic demonstration data/);
assert(context.roleWorkspaceAllowsCatalogLayer('ipdr-package:PKG-1'));
assert(!context.roleWorkspaceAllowsCatalogLayer('events:CCTV'));
assert.equal(context.buildCatalogLayer({id:'ipdr-package:PKG-1',kind:'events',ipdr_package:pkg},[row]).ipdrPackage,pkg);
console.log('PASS: IPDR package links, canonical record access, native blanks, interval warnings, role scope and unknown metadata');
