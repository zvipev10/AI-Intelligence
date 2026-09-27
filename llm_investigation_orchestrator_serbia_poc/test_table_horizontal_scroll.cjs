const assert = require('node:assert/strict');
const fs = require('node:fs');

const css = fs.readFileSync(`${__dirname}/styles.css`, 'utf8');

assert.match(css, /\.raw-events-table \{[^}]*overflow-x: scroll;[^}]*scrollbar-gutter: stable;[^}]*scrollbar-width: auto;/);
assert.match(css, /\.raw-events-table::-webkit-scrollbar \{ width: 12px; height: 12px; \}/);
assert.match(css, /\.raw-events-table::-webkit-scrollbar-thumb \{[^}]*min-width: 48px;/);
assert.match(css, /\.view-stack\.table-mode \.raw-events-overlay/);

console.log('PASS: the shared map and Table presentation records table reserves a visible horizontal scrollbar');
