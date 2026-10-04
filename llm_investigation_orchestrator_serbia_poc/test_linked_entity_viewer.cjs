const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const source = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
const context = {
  Map, Set,
  state: { events: [], entityDirectory: [{ entity_id: 'ENT-PERSON-1', entity_type: 'person', canonical_name: 'Linked person' }], entityMetadata: [], layers: [] },
  escapeHtml: value => String(value ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('"', '&quot;'),
  activeLocaleText: (he, en) => en,
};
vm.createContext(context);

function loadFunction(name) {
  const start = source.indexOf(`function ${name}(`);
  assert.notEqual(start, -1, `missing ${name}`);
  const next = source.slice(start + 1).search(/\n(?:async )?function /);
  vm.runInContext(source.slice(start, start + 1 + next), context);
}

loadFunction('viewerObjects');
loadFunction('isPersonEntity');
const viewerValueStart = source.indexOf('function viewerValue(');
const viewerValueEnd = source.indexOf('const ENTITY_REFERENCE_FIELDS', viewerValueStart);
vm.runInContext(source.slice(viewerValueStart, viewerValueEnd), context);
const referencesStart = source.indexOf('const ENTITY_REFERENCE_FIELDS');
const referencesEnd = source.indexOf('function organizationEvidenceHtml', referencesStart);
assert.notEqual(referencesStart, -1, 'entity references must have a renderer');
vm.runInContext(source.slice(referencesStart, referencesEnd), context);
loadFunction('recordLinkedEntitiesHtml');
loadFunction('recordLinkedRawRecordsHtml');
loadFunction('recordLinkIndicator');

assert.equal(context.viewerObjects().get('person:ENT-PERSON-1').canonical_name, 'Linked person');
assert.match(context.entityViewerLinkHtml('ENT-PERSON-1', 'Linked person'), /data-viewer-kind="person" data-viewer-id="ENT-PERSON-1"/);
assert.match(context.viewerFieldValueHtml('associated_entity_ids', ['ENT-PERSON-1']), /data-viewer-kind="person"/);
assert.match(context.recordLinkedEntitiesHtml({ observed_entity_links: [{ entity_id: 'ENT-PERSON-1', entity_type: 'person', entity_name: 'Linked person', rule_id: 'entity_imei_to_ipdr_imei_v1', record_field: 'imei', entity_field: 'imei', matched_value: '123' }] }), /data-viewer-kind="person" data-viewer-id="ENT-PERSON-1"/);
const rawRecordLink = context.recordLinkedRawRecordsHtml({ observed_record_links: [{ record_id: 'REC-IPDR-1', rule_id: 'adint_ip_to_ipdr_public_ip_v1', record_field: 'ip', linked_record_field: 'ip_public', matched_value: '203.0.113.91' }] });
assert.match(rawRecordLink, /data-linked-record-open="true"/);
assert.match(rawRecordLink, /data-viewer-kind="record" data-viewer-id="REC-IPDR-1"/);
assert.match(source, /async function openLinkedRawRecord\(id, trigger\)[\s\S]*?activateView\("table"\)[\s\S]*?openObjectViewer\("record", id, trigger\)/);
assert.match(source, /function revealViewerRecordInTable\(recordId\)[\s\S]*?scrollIntoView\(\{ block: "center", inline: "nearest" \}\)/);
assert.match(source, /state\.focusedViewerRecordId = kind === "record" \? String\(id\) : null;[\s\S]*?revealViewerRecordInTable\(id\)/);
assert.match(context.recordLinkIndicator({ observed_record_links: [{}] }), /record-link-tooltip/);
assert.doesNotMatch(context.recordLinkIndicator({ observed_record_links: [{}] }), /title=/);
assert.doesNotMatch(context.entityViewerLinkHtml('ENT-MISSING', 'Missing'), /data-viewer-kind=/);
assert.match(source, /const item = viewerObjects\(\)\.get\(`\$\{kind\}:\$\{id\}`\)/);
console.log('PASS: linked entity references resolve to openable item viewers');
