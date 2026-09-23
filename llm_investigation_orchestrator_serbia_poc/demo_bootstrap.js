/* Resolve identity before app.js reads local state or starts background requests. */
(async () => {
  const nativeFetch = window.fetch.bind(window);
  const notice = document.createElement("div");
  notice.setAttribute("role", "status");
  notice.style.cssText = "position:fixed;bottom:0;left:0;right:0;z-index:99999;padding:8px;text-align:center;background:#132b41;color:white";
  function setNotice(message = "") {
    notice.textContent = message;
    notice.style.display = message ? "block" : "none";
  }
  setNotice();
  document.body.appendChild(notice);
  const pending = new Set();
  try {
    const response = await nativeFetch("/api/status", { cache: "no-store" });
    if (!response.ok) throw new Error("Application unavailable");
    const runtime = await response.json();
    if (runtime.maintenance) throw new Error("Scenario switching. Reload shortly.");
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
    window.fetch = async (input, options = {}) => {
      const url = new URL(typeof input === "string" ? input : input.url, location.href);
      if (url.origin === location.origin && url.pathname.startsWith("/api/")) {
        const headers = new Headers(options.headers || (input instanceof Request ? input.headers : undefined));
        if (runtime.activation_generation) headers.set("X-Demo-Generation", runtime.activation_generation);
        if (url.pathname === "/api/investigate") {
          const id = Array.from(crypto.getRandomValues(new Uint8Array(16)), byte => byte.toString(16).padStart(2, "0")).join("");
          headers.set("X-Demo-Request-ID", id);
          pending.add(id);
        }
        options = { ...options, headers };
      }
      const result = await nativeFetch(input, options);
      if (result.status === 409 && result.headers.get("X-Demo-Generation") !== runtime.activation_generation) {
        setNotice("Scenario changed. Reload to continue. / התרחיש השתנה. יש לרענן.");
        throw new Error("Scenario changed. Reload to continue.");
      }
      return result;
    };
    setNotice();
    const script = document.createElement("script");
    script.src = "./app.js?v=207";
    script.onerror = () => { setNotice("Application could not load. Reload to retry."); };
    document.body.appendChild(script);
    setInterval(async () => {
      try {
        const status = await nativeFetch("/api/status", { cache: "no-store" }).then(r => r.json());
        if (status.maintenance || status.activation_generation !== runtime.activation_generation) {
          setNotice("Scenario switching or changed. Reload to continue. / יש לרענן.");
        } else if (status.agent_queue?.queued) {
          setNotice(`${status.agent_queue.queued} agent requests queued`);
          const id = status.agent_queue.queued_ids?.find(value => pending.has(value));
          if (id) {
            const cancel = document.createElement("button");
            cancel.textContent = "Cancel my queued request";
            cancel.onclick = async () => {
              await window.fetch("/api/agent-queue/cancel", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ id }) });
              pending.delete(id);
            };
            notice.append(" ", cancel);
          }
        } else setNotice();
      } catch { setNotice("Application restarting. Reload shortly."); }
    }, 5000);
  } catch (error) {
    setNotice(error.message + " / יש לרענן.");
  }
})();
