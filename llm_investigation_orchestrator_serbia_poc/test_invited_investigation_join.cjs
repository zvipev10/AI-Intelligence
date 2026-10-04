const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const source = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
const selected = [];
const views = [];
const context = {
  state: { busy: false },
  activeLocaleText: (he, en) => en,
  ensureInvestigationRecord: name => ({ id: 'joined-convoy', name }),
  selectInvestigation: investigation => selected.push(investigation),
  setPageView: view => views.push(view),
};
vm.createContext(context);
const start = source.indexOf('function joinInvitedInvestigation(');
const end = source.indexOf('function renderWelcomePage()', start);
assert.notEqual(start, -1, 'missing invitation join handler');
vm.runInContext(source.slice(start, end), context);
context.joinInvitedInvestigation({ titleHe: 'שיירה צבאית חשודה', titleEn: 'Suspicious military convoy' });
assert.deepEqual(selected, [{ id: 'joined-convoy', name: 'Suspicious military convoy' }]);
assert.deepEqual(views, ['workspace']);
console.log('PASS: joining an invited investigation selects it and opens the workspace');
