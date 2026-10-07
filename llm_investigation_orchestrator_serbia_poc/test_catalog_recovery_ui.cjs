const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
const names = ['openCatalogLayer', 'buildCatalogLayer', 'isCallsLayer', 'canonicalCatalogLayerId', 'resolveCatalogLayerId'];
const context = {
  URL, Date, Set, JSON,
  console: { ...console, error() {} }, // the expected load failure is logged by openCatalogLayer
  CATALOG_LAYER_ALIASES: { 'events:שיחות סלולר': 'events:Cellular Calls' },
  state: { layerCatalog: [{ id: 'events:UAV', label: 'UAV', kind: 'events', capabilities: { table: true, map: true } }], layers: [], openingLayerIds: new Set() },
  window: { location: { href: 'http://localhost/' } },
  urls: [], views: [], fail: false, empty: false, renders: 0,
  buildLocaleApiUrl: path => `http://localhost${path}`,
  activeLocaleText: (he, en) => en,
  roleWorkspaceAllowsCatalogLayer: () => true,
  isCellularCallRecord: item => Boolean(item.call_id),
  renderAllViews() { context.renders += 1; }, renderLayerSelector() {},
  activateView(view) { context.views.push(view); },
  applySavedFiltersToLayer(layer, saved) { layer.savedFrom = saved; },
};
context.addResultLayers = ({ sourceId, layers }) => {
  const added = layers.map(layer => ({ ...layer, id: `${sourceId}::${layer.dataId}` }));
  context.state.layers.push(...added);
  return added;
};
context.fetch = async url => {
  context.urls.push(url);
  const filters = JSON.parse(new URL(url).searchParams.get('filters') || '{}');
  return { ok: !context.fail, json: async () => context.fail ? { error: 'load failed' } : {
    layer: context.state.layerCatalog[0],
    rows: context.empty ? [] : filters.location_ids ? [{ event_id: '1', location_id: filters.location_ids[0] }] : [{ event_id: '1' }, { event_id: '2' }],
  } };
};
vm.createContext(context);
for (const name of names) {
  const start = source.search(new RegExp(`(?:async )?function ${name}\\(`));
  assert.notEqual(start, -1, `missing ${name}`);
  const next = source.slice(start + 1).search(/\n(?:async )?function /);
  vm.runInContext(source.slice(start, next < 0 ? undefined : start + 1 + next), context);
}
(async () => {
  const filters = { location_ids: ['LOC-1', 'LOC-3'] };
  const filtered = await context.openCatalogLayer('events:UAV', { filters, silent: true });
  assert.equal(context.state.layers.length, 1);
  assert.equal(filtered.items.length, 1, 'filtered scope loads only matching rows');
  assert.match(filtered.label, /filtered/);
  assert.deepEqual(JSON.parse(new URL(context.urls[0]).searchParams.get('filters')), filters);

  await context.openCatalogLayer('events:UAV', { silent: true });
  assert.equal(context.state.layers.length, 2, 'full catalog must not reuse filtered layer');
  await context.openCatalogLayer('events:UAV', { filters: { location_ids: ['LOC-3', 'LOC-1'] }, silent: true });
  assert.equal(context.state.layers.length, 2, 'equivalent filters reuse a layer');

  context.state.layers = [];
  const saved = { id: 'MEM-1', catalog_filters: filters };
  const restored = await context.openCatalogLayer('events:UAV', { savedLayer: saved, silent: true, memoryRestore: true });
  assert.equal(restored.items.length, 1, 'saved scope must not restore entire catalog');
  assert.equal(restored.savedFrom, saved, 'saved filters are re-applied');

  context.state.layers = [];
  context.empty = true;
  const empty = await context.openCatalogLayer('events:UAV');
  assert.equal(empty.items.length, 0, 'empty catalog layer remains presentable');
  assert.ok(context.renders > 0, 'opening a layer from the selector renders the views');

  context.state.layers = [];
  context.empty = false;
  context.fail = true;
  assert.equal(await context.openCatalogLayer('events:UAV', { silent: true }), null);
  assert.equal(context.state.layerCatalogError, 'load failed', 'failures are surfaced in the layer selector');
  assert.equal(context.state.layers.length, 0);
  assert.equal(context.state.openingLayerIds.size, 0);

  context.state.layerCatalog = [{ id: 'events:שיחות סלולר' }];
  assert.equal(context.resolveCatalogLayerId('events:Cellular Calls'), 'events:שיחות סלולר', 'role defaults find the localized calls layer');
  assert.equal(context.canonicalCatalogLayerId('events:שיחות סלולר'), 'events:Cellular Calls');
  console.log('PASS: filtered loading, scope identity, saved restore, empty layer, failure outcome, localized calls layer id');
})().catch(error => { console.error(error); process.exitCode = 1; });
