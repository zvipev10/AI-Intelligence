const assert = require('node:assert/strict');
const fs = require('node:fs');

const app = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
const html = fs.readFileSync(`${__dirname}/index.html`, 'utf8');

assert.match(app, /state\.activeRoleWorkspace === "sigint"/);
assert.match(app, /\["cellular_geolocations", "cellular_calls"\]/);
assert.match(app, /state\.activeRoleWorkspace === "visint"/);
assert.match(app, /\["satellite", "cctv"\]/);
assert.match(app, /data-collection-imei/);
assert.match(app, /openPolygonActionDialog\(polygon\)/);
assert.match(app, /fetch\("\/api\/collection-request"/);
assert.match(html, /id="collectionRequestModal"/);
assert.match(html, /id="polygonActionModal"/);

console.log('PASS: role-aware collection requests are available from polygons and IMEI values');
