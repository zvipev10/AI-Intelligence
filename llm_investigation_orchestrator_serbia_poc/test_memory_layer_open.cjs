const assert = require('node:assert/strict');
const fs = require('node:fs');

const app = fs.readFileSync(`${__dirname}/app.js`, 'utf8');

assert.match(app, /!options\.roleDefault && !options\.memoryRestore && !roleWorkspaceAllowsCatalogLayer\(layerId\)/);
assert.match(app, /openCatalogLayer\(item\.catalog_layer_id, \{ silent: true, savedLayer: item, memoryRestore: true \}\)/);
assert.match(app, /openCatalogLayer\(catalogLayerId, \{\s*silent: true,\s*savedLayer,\s*memoryRestore: true\s*\}\)/);

console.log('PASS: saved Memory layers bypass role filtering only while restoring their saved presentation');
