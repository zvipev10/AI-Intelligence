const assert = require('node:assert/strict');
const fs = require('node:fs');

const app = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
const html = fs.readFileSync(`${__dirname}/index.html`, 'utf8');
const polygonDraw = fs.readFileSync(`${__dirname}/polygon_draw.js`, 'utf8');

assert.match(app, /state\.activeRoleWorkspace === "sigint"/);
assert.match(app, /\["cellular_geolocations", "cellular_calls"\]/);
assert.match(app, /state\.activeRoleWorkspace === "visint"/);
assert.match(app, /\["satellite", "cctv"\]/);
assert.match(app, /data-collection-imei/);
assert.match(app, /openPolygonActionMenu\(polygon\)/);
const polygonMenuFunction = app.slice(app.indexOf('function openPolygonActionMenu'), app.indexOf('function openCollectionRequestDialog'));
assert.doesNotMatch(polygonMenuFunction, /draftSessionActive/);
assert.match(polygonMenuFunction, /state\.pageView !== "workspace"/);
assert.match(polygonDraw, /getCanvas\(\)\.addEventListener\("contextmenu"/);
assert.match(polygonDraw, /queryRenderedFeatures\(point,\{layers:\["draw-polygon-fill"\]\}\)/);
assert.doesNotMatch(polygonDraw, /map\.on\("click","draw-polygon-fill"/);
assert.match(app, /fetch\("\/api\/collection-request"/);
assert.match(html, /id="collectionRequestModal"/);
assert.match(html, /id="polygonActionMenu"/);
assert.match(html, /id="cctvTaskModal"/);
assert.match(html, /NEW COLLECTION TASK · CCTV/);
assert.match(html, /id="cellularCallsTaskModal"/);
assert.match(html, /NEW COLLECTION TASK · CELLULAR CALLS/);
assert.match(app, /target\.type === "polygon" && type === "cctv"/);
assert.match(app, /target\.type === "imei" && type === "cellular_calls"/);
assert.match(app, /completeDemoCollectionTask\(cctvTaskModal, "cctv"\)/);
assert.match(app, /completeDemoCollectionTask\(cellularCallsTaskModal, "cellular_calls"\)/);

console.log('PASS: source-specific collection requests are available from polygons and IMEI values');
