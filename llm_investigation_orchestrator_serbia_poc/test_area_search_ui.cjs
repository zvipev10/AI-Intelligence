const assert = require('node:assert/strict');
const fs = require('node:fs');

const app = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
const html = fs.readFileSync(`${__dirname}/index.html`, 'utf8');

assert.match(html, /id="polygonAreaSearch"[^>]*role="menuitem"/);
assert.match(html, /data-i18n-text-en="Search data in area"/);
// No date dialog: the search runs at once, in the profile's window (its own records only), read from /api/status.
assert.doesNotMatch(html, /id="areaSearchModal"/);
assert.match(html, /id="areaSearchStatus"[^>]*role="status"/);
assert.match(app, /state\.areaSearchDefaults = runtimeStatus\.area_search \|\| \{\}/);
assert.match(app, /if \(polygon\) void runAreaSearch\(polygon\);/);
const search = app.slice(app.indexOf('async function runAreaSearch'), app.indexOf('function openCollectionRequestDialog'));
assert.match(search, /start_time: defaults\.start_time, end_time: defaults\.end_time/);
assert.match(search, /fetch\("\/api\/area-search"/);
assert.match(search, /polygon: polygon\.coordinates/);
// The found records open as the layers' own records: the layer, filtered to them and the time range.
assert.match(search, /openCatalogLayer\(resolveCatalogLayerId\(layer\.layer_id\), \{ filters: \{ event_ids: layer\.event_ids/);
assert.match(app, /getElementById\("polygonAreaSearch"\)\?\.addEventListener\("click"/);
assert.match(app, /const menuHeight = 122;/);

console.log('PASS: Search data in area opens from the polygon menu in the default window, without a date dialog, and opens the found records in their layers');
