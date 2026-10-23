const assert = require('node:assert/strict');
const fs = require('node:fs');

const app = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
const html = fs.readFileSync(`${__dirname}/index.html`, 'utf8');

assert.match(html, /id="polygonAreaSearch"[^>]*role="menuitem"/);
assert.match(html, /data-i18n-text-en="Search data in area"/);
assert.match(html, /id="areaSearchModal"/);
assert.match(html, /id="areaSearchFrom" type="date"/);
assert.match(html, /id="areaSearchTo" type="date"/);
// The dates start at the profile's window (its own records only), read from /api/status.
assert.match(app, /state\.areaSearchDefaults = runtimeStatus\.area_search \|\| \{\}/);
const search = app.slice(app.indexOf('async function submitAreaSearch'), app.indexOf('function openCollectionRequestDialog'));
assert.match(search, /fetch\("\/api\/area-search"/);
assert.match(search, /polygon: target\.coordinates/);
// The found records open as the layers' own records: the layer, filtered to them and the time range.
assert.match(search, /openCatalogLayer\(resolveCatalogLayerId\(layer\.layer_id\), \{ filters: \{ event_ids: layer\.event_ids/);
assert.match(app, /getElementById\("polygonAreaSearch"\)\?\.addEventListener\("click"/);
assert.match(app, /const menuHeight = 122;/);

console.log('PASS: Search data in area opens from the polygon menu with the default window and opens the found records in their layers');
