/* Resolve the session before app.js reads local state or starts background requests. */
(async () => {
  const nativeFetch = window.fetch.bind(window);
  const root = document.documentElement;
  const notice = document.createElement("div");
  notice.setAttribute("role", "status");
  notice.className = "bootstrap-notice";
  notice.hidden = true;
  document.body.appendChild(notice);

  function setNotice(message = "") {
    notice.textContent = message;
    notice.hidden = !message;
  }

  function isEnglish() {
    return root.lang === "en";
  }

  function text(he, en) {
    return isEnglish() ? en : he;
  }

  let loginShown = false;

  function showLoginScreen({ expired = false } = {}) {
    if (loginShown) return;
    loginShown = true;
    root.dataset.appReady = "true";
    document.body.classList.add("auth-required");
    const screen = document.createElement("div");
    screen.id = "loginScreen";
    screen.className = "login-screen";
    screen.innerHTML = `
      <form class="login-panel" id="loginForm" novalidate aria-labelledby="loginTitle">
        <h1 id="loginTitle"><span lang="he" dir="rtl">כניסה למערכת</span><span lang="en" dir="ltr">Sign in</span></h1>
        <p class="login-subtitle"><span lang="he" dir="rtl">סביבת מודיעין</span> · <span lang="en" dir="ltr">Intelligence Workspace</span></p>
        <p class="login-expired" role="status" ${expired ? "" : "hidden"}><span lang="he" dir="rtl">פג תוקף ההתחברות. יש להתחבר מחדש.</span> <span lang="en" dir="ltr">Your session has expired. Sign in again.</span></p>
        <label for="loginUsername"><span lang="he" dir="rtl">שם משתמש</span> / <span lang="en" dir="ltr">Username</span></label>
        <input id="loginUsername" name="username" type="text" autocomplete="username" autocapitalize="none" spellcheck="false" required dir="ltr">
        <label for="loginPassword"><span lang="he" dir="rtl">סיסמה</span> / <span lang="en" dir="ltr">Password</span></label>
        <input id="loginPassword" name="password" type="password" autocomplete="current-password" required dir="ltr">
        <p id="loginError" class="login-error" role="alert" hidden></p>
        <button id="loginSubmit" type="submit"><span lang="he" dir="rtl">כניסה</span> / <span lang="en" dir="ltr">Sign in</span></button>
      </form>`;
    document.body.appendChild(screen);
    const form = screen.querySelector("#loginForm");
    const username = screen.querySelector("#loginUsername");
    const password = screen.querySelector("#loginPassword");
    const error = screen.querySelector("#loginError");
    const submit = screen.querySelector("#loginSubmit");
    const showError = (he, en) => {
      error.innerHTML = "";
      const heSpan = document.createElement("span");
      heSpan.lang = "he";
      heSpan.dir = "rtl";
      heSpan.textContent = he;
      const enSpan = document.createElement("span");
      enSpan.lang = "en";
      enSpan.dir = "ltr";
      enSpan.textContent = en;
      error.append(heSpan, " ", enSpan);
      error.hidden = false;
    };
    form.addEventListener("submit", async event => {
      event.preventDefault();
      error.hidden = true;
      if (!username.value.trim() || !password.value) {
        showError("יש להזין שם משתמש וסיסמה.", "Enter a username and password.");
        (username.value.trim() ? password : username).focus();
        return;
      }
      submit.disabled = true;
      try {
        const response = await nativeFetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json; charset=utf-8" },
          body: JSON.stringify({ username: username.value.trim(), password: password.value })
        });
        await response.text().catch(() => "");
        if (response.ok) {
          window.location.reload();
          return;
        }
        if (response.status === 401) showError("שם משתמש או סיסמה שגויים.", "Wrong username or password.");
        else showError("ההתחברות נכשלה. נסו שוב.", "Sign-in failed. Try again.");
        password.select();
        password.focus();
      } catch {
        showError("השרת אינו זמין. נסו שוב.", "The server is unavailable. Try again.");
      } finally {
        submit.disabled = false;
      }
    });
    username.focus();
  }

  async function initSessionControls() {
    const controls = document.getElementById("sessionControls");
    const userLabel = document.getElementById("sessionUserName");
    const signOut = document.getElementById("signOutButton");
    if (!controls || !signOut) return;
    controls.hidden = false;
    signOut.addEventListener("click", async () => {
      signOut.disabled = true;
      try {
        const response = await nativeFetch("/api/logout", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
        await response.text().catch(() => "");
      } catch {
        // Reloading shows the sign-in screen when the cookie is gone; otherwise the user can retry.
      }
      window.location.reload();
    });
    try {
      const response = await window.fetch("/api/me", { cache: "no-store" });
      if (!response.ok) return;
      const user = await response.json();
      if (userLabel) userLabel.textContent = String(user.user_name || user.id || "");
    } catch {
      // The name is informational only.
    }
  }

  try {
    const response = await nativeFetch("/api/status", { cache: "no-store" });
    if (!response.ok) throw new Error("Application unavailable");
    const runtime = await response.json();
    window.DEMO_RUNTIME = runtime;
    const namespace = runtime.scenario_id ? `${runtime.scenario_id}:${runtime.dataset_version}:` : "";
    window.DEMO_STORAGE = {
      getItem(key) {
        const value = localStorage.getItem(namespace + key);
        // One-time copy of existing Kosovo browser state, never imported into Syria.
        if (value === null && runtime.scenario_id === "kosovo") {
          const old = localStorage.getItem(key);
          if (old !== null) { localStorage.setItem(namespace + key, old); return old; }
        }
        return value;
      },
      setItem: (key, value) => localStorage.setItem(namespace + key, value),
      removeItem: key => localStorage.removeItem(namespace + key)
    };
    if (!runtime.authenticated) {
      showLoginScreen();
      return;
    }
    window.fetch = async (input, options) => {
      const result = await nativeFetch(input, options);
      if (result.status === 401) {
        let url = null;
        try { url = new URL(typeof input === "string" || input instanceof URL ? input : input.url, location.href); } catch { url = null; }
        if (url && url.origin === location.origin && url.pathname.startsWith("/api/") && url.pathname !== "/api/login") {
          showLoginScreen({ expired: true });
        }
      }
      return result;
    };
    const script = document.createElement("script");
    script.src = "./app.js?v=282";
    script.onerror = () => {
      root.dataset.appReady = "true";
      setNotice(text("לא ניתן לטעון את היישום. יש לרענן.", "Application could not load. Reload to retry."));
    };
    document.body.appendChild(script);
    void initSessionControls();
  } catch (error) {
    root.dataset.appReady = "true";
    setNotice(text("היישום אינו זמין. יש לרענן.", "Application unavailable. Reload to retry."));
  }
})();
