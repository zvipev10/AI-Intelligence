const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const source = fs.readFileSync(`${__dirname}/app.js`, 'utf8');
const selected = [];
const views = [];
const created = [];
const context = {
  state: {},
  activeLocaleText: (he, en) => en,
  ensureInvestigationRecord: async name => { created.push(name); return { id: 'joined-convoy', name }; },
  selectInvestigation: investigation => selected.push(investigation),
  setPageView: view => views.push(view),
  openWelcomeActionMessage: () => { throw new Error('unexpected failure message'); },
};
vm.createContext(context);
const start = source.indexOf('async function joinInvitedInvestigation(');
const end = source.indexOf('function renderWelcomePage()', start);
assert.notEqual(start, -1, 'missing invitation join handler');
vm.runInContext(source.slice(start, end), context);
(async () => {
  await context.joinInvitedInvestigation({ titleHe: 'שיירה צבאית חשודה', titleEn: 'Suspicious military convoy' });
  assert.deepEqual(created, ['Suspicious military convoy'], 'joining creates (or reuses) the investigation on the server');
  assert.deepEqual(selected, [{ id: 'joined-convoy', name: 'Suspicious military convoy' }]);
  assert.deepEqual(views, ['workspace']);
  console.log('PASS: joining an invited investigation selects it and opens the workspace');
})().catch(error => { console.error(error); process.exitCode = 1; });
