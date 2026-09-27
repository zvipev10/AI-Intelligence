const assert = require('node:assert/strict');
const fs = require('node:fs');

const app = fs.readFileSync(`${__dirname}/app.js`, 'utf8');

assert.match(app, /!options\.roleDefault && !options\.memoryRestore && !roleWorkspaceAllowsCatalogLayer\(layerId\)/);
assert.match(app, /openCatalogLayer\(item\.catalog_layer_id, \{ silent: true, savedLayer: item, memoryRestore: true \}\)/);
assert.match(app, /openCatalogLayer\(catalogLayerId, \{\s*silent: true,\s*savedLayer,\s*memoryRestore: true\s*\}\)/);
assert.match(app, /return Boolean\(layer\?\.memoryPresentationOpen\) \|\| roleWorkspaceAllowsCatalogLayer\(layer\?\.catalogLayerId\);/);
assert.match(app, /layer\.memoryPresentationOpen = true;\s*applySavedFiltersToLayer\(layer, item\);/);
assert.match(app, /state\.layers\.forEach\(layer => \{ layer\.memoryPresentationOpen = false; \}\);/);

console.log('PASS: saved Memory layers remain visible while opening their presentation, then return to role scoping on role change');
