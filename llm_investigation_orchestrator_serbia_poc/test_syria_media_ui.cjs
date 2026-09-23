const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
const context = {URL, window: {location: {href: 'http://localhost/'}}, activeLocaleText: (he,en) => en,
  escapeHtml: text => String(text).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;')};
vm.createContext(context);
for (const name of ['safeMediaUrl','viewerMedia','isUavVideoRecord','isCellularCallRecord','viewerMediaHtml']) {
  const start = source.search(new RegExp(`function ${name}\\(`));
  const next = source.slice(start + 1).search(/\n(?:async )?function /);
  vm.runInContext(source.slice(start, next < 0 ? undefined : start + 1 + next), context);
}
const video = context.viewerMediaHtml({video_url:'/clip.mp4',synthetic_media:'true'});
assert.match(video, /<video controls/); assert.match(video, /SYNTHETIC DEMO/);
const html = context.viewerMediaHtml({synthetic_media:'true',image_series: JSON.stringify([
  {image_url:'/one.png',timestamp_utc:'2026-09-22T08:00:00Z'},
  {image_url:'/two.png',timestamp_utc:'2026-09-22T08:05:00Z'},
  {image_url:'javascript:alert(1)',timestamp_utc:'bad'}])});
assert.equal((html.match(/<img /g)||[]).length,2);
assert.match(html,/08:00:00Z/);assert.match(html,/08:05:00Z/);assert.doesNotMatch(html,/javascript:/);
assert.equal(context.viewerMediaHtml({image_series:'broken'}),'');
const pairedHtml = context.viewerMediaHtml({image_series:[{image_url:'/second.png',timestamp_utc:'2026-09-20T08:15:00Z',pair_id:'VISIT-1',paired_image_url:'/first.png',paired_timestamp_utc:'2026-09-20T08:00:00Z'}]});
assert.equal((pairedHtml.match(/<img /g)||[]).length,1);
assert.doesNotMatch(pairedHtml,/first\.png/);
assert.match(pairedHtml,/second\.png/);
assert.match(pairedHtml,/VISIT-1/);
console.log('PASS: CCTV player, timestamped image sequence, synthetic labels and URL validation');
