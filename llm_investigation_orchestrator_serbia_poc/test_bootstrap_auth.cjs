const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const source = fs.readFileSync(`${__dirname}/demo_bootstrap.js`, 'utf8');

function element(tag = 'div') {
  const node = {
    tagName: tag.toUpperCase(), children: [], hidden: false, dataset: {}, style: {}, listeners: {},
    classList: { values: new Set(), add(value) { this.values.add(value); }, contains(value) { return this.values.has(value); } },
    setAttribute(key, value) { this[key] = value; },
    addEventListener(type, fn) { this.listeners[type] = fn; },
    appendChild(child) { this.children.push(child); return child; },
    append() {}, focus() {}, select() {},
    querySelector(selector) {
      this.parts = this.parts || {};
      if (!this.parts[selector]) this.parts[selector] = element();
      return this.parts[selector];
    },
  };
  return node;
}

async function boot({ status, responses = {} }) {
  const body = element('body');
  const root = { lang: 'en', dataset: {} };
  const ids = { sessionControls: element(), sessionUserName: element(), signOutButton: element() };
  const calls = [];
  const fetch = async (url, options = {}) => {
    calls.push([String(url), options.method || 'GET']);
    if (url === '/api/status') return { ok: true, status: 200, json: async () => status };
    const answer = responses[url] || { status: 200, body: {} };
    return { ok: answer.status < 400, status: answer.status, json: async () => answer.body, text: async () => '' };
  };
  const window = { fetch, location: { href: 'http://app.test/', reload() { window.reloaded = true; } } };
  const storage = new Map();
  const context = {
    window, URL, Headers, console, location: { origin: 'http://app.test', href: 'http://app.test/' },
    localStorage: { getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value), removeItem: key => storage.delete(key) },
    document: { documentElement: root, body, createElement: element, getElementById: id => ids[id] || null },
  };
  vm.createContext(context);
  await vm.runInContext(source.replace(/^\/\*.*\*\/\n\(async \(\) => \{/, 'globalThis.__boot = (async () => {').replace(/\}\)\(\);\s*$/, '})();'), context);
  await context.__boot;
  await new Promise(resolve => setTimeout(resolve, 0));
  return { body, root, window, calls, ids, context };
}

(async () => {
  // Signed out: the login screen replaces the application and app.js is not loaded.
  const signedOut = await boot({ status: { authenticated: false, scenario_id: 'syria', dataset_version: 'i360' } });
  assert.ok(signedOut.body.classList.contains('auth-required'));
  const screen = signedOut.body.children.find(child => child.id === 'loginScreen');
  assert.ok(screen, 'login screen is shown');
  assert.match(screen.innerHTML, /type="password"/);
  assert.match(screen.innerHTML, /כניסה למערכת/);
  assert.match(screen.innerHTML, /Sign in/);
  assert.ok(!signedOut.body.children.some(child => child.tagName === 'SCRIPT'), 'app.js is not loaded while signed out');
  assert.equal(signedOut.root.dataset.appReady, 'true');
  assert.equal(typeof signedOut.window.DEMO_STORAGE.getItem, 'function', 'namespaced storage is still available');

  // Wrong password shows an error; a correct one reloads the page.
  const wrong = await boot({ status: { authenticated: false }, responses: { '/api/login': { status: 401, body: { error: 'invalid_credentials' } } } });
  const wrongScreen = wrong.body.children.find(child => child.id === 'loginScreen');
  wrongScreen.querySelector('#loginUsername').value = 'analyst';
  wrongScreen.querySelector('#loginPassword').value = 'nope';
  await wrongScreen.querySelector('#loginForm').listeners.submit({ preventDefault() {} });
  assert.equal(wrongScreen.querySelector('#loginError').hidden, false, 'wrong credentials show the error message');
  assert.ok(!wrong.window.reloaded);
  const right = await boot({ status: { authenticated: false }, responses: { '/api/login': { status: 200, body: { user: { user_name: 'analyst' } } } } });
  const rightScreen = right.body.children.find(child => child.id === 'loginScreen');
  rightScreen.querySelector('#loginUsername').value = 'analyst';
  rightScreen.querySelector('#loginPassword').value = 'analyst';
  await rightScreen.querySelector('#loginForm').listeners.submit({ preventDefault() {} });
  assert.ok(right.window.reloaded, 'successful sign-in reloads the page');

  // Signed in: app.js loads, the user name is shown, sign-out posts /api/logout.
  const signedIn = await boot({ status: { authenticated: true, scenario_id: 'syria', dataset_version: 'i360' }, responses: { '/api/me': { status: 200, body: { user_name: 'analyst' } } } });
  const script = signedIn.body.children.find(child => child.tagName === 'SCRIPT');
  assert.match(script.src, /^\.\/app\.js\?v=/);
  assert.equal(signedIn.ids.sessionControls.hidden, false);
  assert.equal(signedIn.ids.sessionUserName.textContent, 'analyst');
  await signedIn.ids.signOutButton.listeners.click();
  assert.ok(signedIn.calls.some(([url, method]) => url === '/api/logout' && method === 'POST'));
  assert.ok(signedIn.window.reloaded);
  assert.ok(!signedIn.calls.some(([url]) => /agent-queue|investigate/.test(url)));

  // An expired session (401 from any same-origin /api/* call) brings the login screen back.
  const expired = await boot({ status: { authenticated: true }, responses: { '/api/layers': { status: 401, body: { error: 'signed_out' } } } });
  assert.ok(!expired.body.children.some(child => child.id === 'loginScreen'));
  await expired.window.fetch('/api/layers');
  const expiredScreen = expired.body.children.find(child => child.id === 'loginScreen');
  assert.ok(expiredScreen, 'login screen returns after a 401');
  assert.match(expiredScreen.innerHTML, /class="login-expired" role="status" >/);
  assert.doesNotMatch(source, /X-Demo-Generation|agent-queue|maintenance/);
  console.log('PASS: sign-in screen, wrong-password error, reload on success, app load when signed in, sign-out, expiry handling');
})().catch(error => { console.error(error); process.exitCode = 1; });
