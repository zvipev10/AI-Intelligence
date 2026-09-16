const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
const names = ['openCatalogLayer', 'buildCatalogLayer', 'executeCatalogLayerActions', 'presentFinalAgentResult', 'reloadOpenCatalogLayers'];
const context = {
  URL, console, Date, Set,
  state: { layerCatalog: [{ id: 'events:UAV', label: 'UAV', kind: 'events', capabilities: { table: true, map: true } }], layers: [], openingLayerIds: new Set() },
  window: { location: { href: 'http://localhost/' } },
  urls: [], notices: [], fail: false,
  buildLocaleApiUrl: path => path,
  activeLocaleText: (he, en) => en,
  renderAllViews() {}, renderLayerSelector() {}, renderQueryLayersModal() {}, renderQueryInspector() {}, ensureActiveLayer() {}, activateView() {},
  buildTypedResultLayers: () => [], buildFinalQueryContext: () => ({}), finalSourceId: () => 'final', resolveFinalResultView: () => 'map',
  localizedRestoreOnlySummary: () => 'summary', applySavedFiltersToLayer() {},
};
context.showResult = (...args) => context.notices.push(args);
context.addResultLayers = ({ layers }) => { context.state.layers.push(...layers); return layers; };
context.fetch = async url => {
  context.urls.push(url);
  const filters = JSON.parse(new URL(url).searchParams.get('filters') || '{}');
  return { ok: !context.fail, json: async () => context.fail ? { error: 'load failed' } : {
    layer: context.state.layerCatalog[0], rows: filters.location_ids ? [{ event_id: '1', location_id: filters.location_ids[0] }] : [{event_id: '1'}, {event_id: '2'}],
  } };
};
vm.createContext(context);
for (const name of names) {
  const start = source.search(new RegExp(`(?:async )?function ${name}\\(`));
  const next = source.slice(start + 1).search(/\n(?:async )?function /);
  vm.runInContext(source.slice(start, next < 0 ? undefined : start + 1 + next), context);
}
(async () => {
  const action = { action: 'open', catalog_layer_id: 'events:UAV', filters: { location_ids: ['LOC-1', 'LOC-3'] } };
  const result = { catalog_layer_actions: [action] };
  await context.presentFinalAgentResult(result, 'show filtered layer', { showSummary: true });
  assert.equal(context.state.layers.length, 1);
  assert.equal(context.state.layers[0].items.length, 1);
  assert.equal(context.notices.at(-1)[0], 'Layer opened');
  assert.match(context.urls[0], /filters=/);
  assert.deepEqual(JSON.parse(new URL(context.urls[0]).searchParams.get('filters')), action.filters);
  await context.openCatalogLayer('events:UAV', { silent: true });
  assert.equal(context.state.layers.length, 2, 'full catalog must not reuse filtered layer');
  await context.openCatalogLayer('events:UAV', { filters: { location_ids: ['LOC-3', 'LOC-1'] }, silent: true });
  assert.equal(context.state.layers.length, 2, 'equivalent filters reuse a layer');
  await context.reloadOpenCatalogLayers();
  assert.equal(context.state.layers.length, 2, 'refresh preserves both scopes');
  assert.equal(context.state.layers[0].catalogFilters.location_ids.length, 2);
  context.state.layers = [];
  await context.openCatalogLayer('events:UAV', { savedLayer: { catalog_filters: action.filters }, silent: true });
  assert.equal(context.state.layers[0].items.length, 1, 'saved scope must not restore entire catalog');
  context.state.layers = [];
  context.fail = true;
  await context.presentFinalAgentResult({ catalog_layer_actions: [action] }, 'show', { showSummary: true });
  assert.equal(context.notices.at(-1)[0], 'Layer opening failed', 'summary must not overwrite failure');
  assert.equal(context.state.layers.length, 0);
  console.log('PASS: filtered loading, scope identity, refresh, saved restore, success and failure outcomes');
})().catch(error => { console.error(error); process.exitCode = 1; });
