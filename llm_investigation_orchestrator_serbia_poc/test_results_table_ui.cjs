const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
function element(extra = {}) {
  const classes = new Set();
  return { innerHTML: '', hidden: false, style: { setProperty() {} },
    classList: { toggle(k,v) { v ? classes.add(k) : classes.delete(k); }, contains: k => classes.has(k) },
    setAttribute() {}, ...extra };
}
const stack = element();
const nodes = Object.fromEntries(['rawEventsOverlay','rawEventsTabs','evidenceHead','evidenceRows','layerFilterPanel','rawEventsMinimize'].map(id => [id, element()]));
nodes.rawEventsOverlay.closest = () => stack;
const tabs = ['map','timeline','table'].map(view => element({dataset:{view}}));
const panes = ['map','timeline','table'].map(view => element({id:`${view}View`}));
const row = {event_id:'REC-SYR-IPDR-137', source_type:'IPDR', timestamp_utc:'2026-09-20T08:00:00Z', imei:'000000000001370', ip_address:'192.0.2.10', entity_name:'', location_name:''};
const layer = {id:'ipdr', kind:'events', label:'IPDR', items:[row], visible:true, capabilities:{table:true,map:false,timeline:true}};
const context = { console, Set, Map, Date, LOCATIONS:{}, IPDR_SOURCE_FIELDS:['start_time','end_time','ip_source','ip_target','ip_public','ip_private','ip_out','source_record_id','source_port','target_port','public_port','protocol','bytes_sent','bytes_received','source_system','imei','mac','SUBNETMASK'],
 state:{layers:[layer],activeLayerId:'ipdr',rawOverlayMinimized:true,rawOverlayHeight:28,focusedViewerRecordId:null},
 document:{getElementById:id=>nodes[id],querySelector:()=>stack,querySelectorAll:q=>q==='.view-tab'?tabs:panes},
 viewLabels:()=>({map:'Map',timeline:'Timeline',table:'Table'}), viewRecommendation:element(),
 renderQueryInspector(){}, ensureLayerFilterState(){}, activeTableLayer:()=>layer,
 roleWorkspaceLayers:()=>context.state.layers,
 itemsForLayerPresentation:l=>l.items, layerHasAppliedFilters:()=>false,currentLocaleTag:()=> 'en-US',
 layerColorStyle:()=>'',escapeHtml:v=>String(v??''),validAppliedFilters:()=>[],activeLocaleText:(he,en)=>en,
 renderLayerFilterPanel(){},isCellularCallRecord:()=>false,isMapItemSelected:()=>false,
 mapActionButton:()=>'',collectionImeiButton:value=>String(value || ''),recordLinkIndicator:()=>'',enhanceResultsTable(){},layerId:(kind,label)=>`${kind}:${label}`
};
vm.createContext(context);
for (const name of ['activateView','renderEvidence','resolveFinalResultView','isCallsLayer','eventMapCoordinates','buildEventLayers','isIpdrRecord','isAdintRecord','isCellularGeolocationRecord','isCellularCallRecord','isViewerRecordSelected','viewerFieldLabel','ipdrTableFieldLabel','viewerFields','filterFieldsForLayer','filterFieldPathsForValue']) {
 const start = source.indexOf(`function ${name}(`);
 const next = source.slice(start+1).search(/\n(?:async )?function /);
 vm.runInContext(source.slice(start,start+1+next),context);
}
context.activateView('table');
assert(stack.classList.contains('table-mode'));
assert(!nodes.rawEventsOverlay.classList.contains('minimized'));
assert(context.state.rawOverlayMinimized, 'overlay preference must survive table mode');
assert.match(nodes.evidenceRows.innerHTML,/data-viewer-kind="record" data-viewer-id="REC-SYR-IPDR-137"/);
assert(tabs[2].classList.contains('active'));
assert.match(nodes.evidenceHead.innerHTML, /IP address/);
assert.match(nodes.evidenceHead.innerHTML, /IMEI/);
assert.doesNotMatch(nodes.evidenceHead.innerHTML, /Actor|Location|result-map-action/);
assert.match(nodes.evidenceRows.innerHTML, /192\.0\.2\.10/);
assert.match(nodes.evidenceRows.innerHTML, /000000000001370/);
row.source_record_id='3495155497992130';context.renderEvidence();
assert.match(nodes.evidenceHead.innerHTML,/Canonical record ID/);
assert.match(nodes.evidenceHead.innerHTML,/Source record ID/);
assert(nodes.evidenceHead.innerHTML.indexOf('Canonical record ID') < nodes.evidenceHead.innerHTML.indexOf('Source record ID'));
assert.match(nodes.evidenceRows.innerHTML,/REC-SYR-IPDR-137/);
assert.match(nodes.evidenceRows.innerHTML,/3495155497992130/);
assert.doesNotMatch(nodes.evidenceRows.innerHTML,/ipdr-canonical-id-column/);
context.state.focusedViewerRecordId='REC-SYR-IPDR-137';context.renderEvidence();
assert.match(nodes.evidenceRows.innerHTML,/viewer-selected-row/);
context.state.focusedViewerRecordId=null;
const fields = context.viewerFields({...row, entity_name:'placeholder', location_name:'Unknown'},'record');
assert(!fields.some(([key])=>['entity_name','location_name'].includes(key)));
assert(fields.some(([key,value])=>key==='imei' && value==='000000000001370'));
assert(!context.filterFieldsForLayer(layer).includes('location_name'));
assert(context.filterFieldsForLayer(layer).includes('ip_address'));
row.source_type='ADINT'; context.renderEvidence();
assert.match(nodes.evidenceHead.innerHTML,/Device ID/);
assert.match(nodes.evidenceHead.innerHTML,/Latitude/);
row.source_type='IPDR'; context.renderEvidence();
const sharedBody = nodes.evidenceRows;
context.activateView('timeline');
assert(!stack.classList.contains('table-mode'));
assert(nodes.rawEventsOverlay.classList.contains('minimized'));
context.activateView('evidence');
assert(stack.classList.contains('table-mode'),'legacy saved recommendation maps to Table');
assert.equal(nodes.evidenceRows,sharedBody,'same table component across modes');
assert.equal(context.resolveFinalResultView({},[layer]),'table');
assert.equal(context.resolveFinalResultView({recommended_view:'table'},[layer]),'table');
assert.equal(context.resolveFinalResultView({recommended_view:'timeline'},[layer]),'timeline');
assert.equal(context.resolveFinalResultView({recommended_view:'map'},[layer]),'table');
assert.equal(context.buildEventLayers([row])[0].capabilities.map,false);
row.source_type='Cellular Geolocations';row.sim='00001234';row.imei='000000000000001';row.target_msisdn='9630943700780';row.target_imsi='417011234567890';row.operator_msisdn='963940952424';row.operator_imsi='417015344104770';row.location_id='LOC-1';context.renderEvidence();
assert.match(nodes.evidenceHead.innerHTML,/SIM/);assert.match(nodes.evidenceHead.innerHTML,/IMEI/);
assert.match(nodes.evidenceHead.innerHTML,/Target MSISDN/);assert.match(nodes.evidenceHead.innerHTML,/Target IMSI/);
assert.match(nodes.evidenceHead.innerHTML,/Operator MSISDN/);assert.match(nodes.evidenceHead.innerHTML,/Operator IMSI/);
assert.doesNotMatch(nodes.evidenceHead.innerHTML,/Actor/);assert.match(nodes.evidenceRows.innerHTML,/00001234/);assert.match(nodes.evidenceRows.innerHTML,/9630943700780/);assert.match(nodes.evidenceRows.innerHTML,/417011234567890/);
assert(context.viewerFields(row,'record').some(([k,v])=>k==='sim' && v==='00001234'));
assert(context.viewerFields(row,'record').some(([k,v])=>k==='target_msisdn' && v==='9630943700780'));
row.source_type='Cellular Calls';row.call_id='CALL-1';row.side_a_sim='89000000000000000001';row.side_b_sim='89000000000000000002';row.side_a_imei='000000000000001';row.side_b_imei='000000000000002';context.renderEvidence();
assert.match(nodes.evidenceHead.innerHTML,/Side A IMEI/);assert.match(nodes.evidenceHead.innerHTML,/Side B IMEI/);
assert.match(nodes.evidenceRows.innerHTML,/000000000000001/);assert.match(nodes.evidenceRows.innerHTML,/000000000000002/);
context.state.layers=[];context.renderEvidence();
assert(nodes.rawEventsOverlay.hidden,'empty table exposes its placeholder');
console.log('PASS: shared table, geometry-free record links, recommendation, legacy restore, empty state and minimization');

const callsLayer={kind:'events',items:[{call_id:'CALL-1'}],capabilities:{map:true,timeline:true,table:true}};
assert.equal(context.resolveFinalResultView({},[callsLayer]),'timeline');
assert.equal(context.resolveFinalResultView({recommended_view:'map'},[callsLayer]),'map');
assert.equal(context.resolveFinalResultView({recommended_view:'table'},[callsLayer]),'table');
assert.equal(context.resolveFinalResultView({},[callsLayer,{kind:'events',items:[{}],capabilities:{map:true}}]),'map');
console.log('PASS: calls default to Timeline; explicit views and mixed sources preserved');

context.state.layers=[layer];context.renderEvidence();assert.match(nodes.evidenceHead.innerHTML,/Side A SIM/);assert.match(nodes.evidenceRows.innerHTML,/89000000000000000001/);
