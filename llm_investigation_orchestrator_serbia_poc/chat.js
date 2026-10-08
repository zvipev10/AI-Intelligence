/* chat.js: the chat panel.

   The server runs each message as one turn (POST /api/chat/ask, an SSE stream): its assistant asks the
   i360 chat (events relayed as "i360") and drives the app through actions ("action"), with its own
   steps ("step") and a closing note ("note"). This file renders that stream in the original chat
   panel's look (message bubbles, the live "Research process" list that folds into "N steps", the
   answer, Show results / Save to memory) and carries the actions out with app.js's own functions:
   addResultLayers, openCatalogLayer, openObjectViewer, openMemoryEntry, saveLayerToInvestigationMemory.

   The server keeps nothing between turns: the history, the i360 conversation id and the previous
   answer's citations live here and travel with every message. */
(function () {
  "use strict";

  const CHAT = {
    on: false, busy: false, controller: null, turnCounter: 0,
    history: [], citations: [], i360ConversationId: "", investigationId: null,
    scope: "investigation", openedLayerKey: "chat:opened-records",
  };
  const MAX_SOURCES = 8;
  const $ = id => document.getElementById(id);

  // -- small helpers ------------------------------------------------------------------------
  function esc(value) {
    return String(value ?? "").replace(/[&<>"']/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
  }

  function inline(text, citations) {
    return esc(text)
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/\[(\d{1,3})\]/g, (match, n) => {
        const cite = citations[Number(n) - 1];
        return cite ? `<button type="button" class="cite-ref" data-cite-id="${esc(cite.id)}" title="${esc(cite.text || cite.id)}">${n}</button>` : match;
      });
  }

  /* Markdown as i360 writes it: paragraphs, bullet and numbered lists, headings, bold, code, [n] citations. */
  function markdown(text, citations = []) {
    const blocks = String(text || "").replace(/\r/g, "").split(/\n{2,}/);
    return blocks.map(block => {
      const lines = block.split("\n").filter(line => line.trim());
      if (!lines.length) return "";
      if (lines.every(line => /^\s*[-*•]\s+/.test(line))) {
        return `<ul>${lines.map(line => `<li>${inline(line.replace(/^\s*[-*•]\s+/, ""), citations)}</li>`).join("")}</ul>`;
      }
      if (lines.every(line => /^\s*\d+[.)]\s+/.test(line))) {
        return `<ol>${lines.map(line => `<li>${inline(line.replace(/^\s*\d+[.)]\s+/, ""), citations)}</li>`).join("")}</ol>`;
      }
      return lines.map(line => /^#{1,4}\s+/.test(line)
        ? `<p><strong>${inline(line.replace(/^#{1,4}\s+/, ""), citations)}</strong></p>`
        : `<p>${inline(line, citations)}</p>`).join("");
    }).join("");
  }

  function nearBottom() {
    const box = $("conversation");
    return box.scrollHeight - box.scrollTop - box.clientHeight <= 96;
  }

  function follow(shouldFollow) {
    if (!shouldFollow) return;
    const box = $("conversation");
    box.scrollTop = box.scrollHeight;
    requestAnimationFrame(() => { box.scrollTop = box.scrollHeight; });
  }

  function thinkingHtml(text = "Thinking") {
    return `<span class="thinking-indicator" role="status"><span>${esc(text)}</span><span class="thinking-dots" aria-hidden="true"><i></i><i></i><i></i></span></span>`;
  }

  // -- messages -----------------------------------------------------------------------------
  function appendMessage(role, html) {
    const shouldFollow = role === "user" || nearBottom();
    const article = document.createElement("article");
    article.className = `message ${role === "user" ? "user-message" : "assistant-message"}`;
    article.innerHTML = `<div class="message-label">${role === "user" ? "Analyst" : "Assistant"}</div>${html}`;
    $("conversation").appendChild(article);
    follow(shouldFollow);
    return article;
  }

  function startTurn() {
    const article = appendMessage("assistant", `
      <section class="research-process research-process-live">
        <h3>Research process</h3>
        <ol class="activity-list"></ol>
        <div class="activity-empty">${thinkingHtml()}</div>
      </section>
      <div class="answer-body" hidden></div>`);
    return {
      id: ++CHAT.turnCounter, article,
      list: article.querySelector(".activity-list"),
      empty: article.querySelector(".activity-empty"),
      body: article.querySelector(".answer-body"),
      streamed: "", answer: null, citations: [], note: "", errors: [], shownLayerIds: [], steps: 0,
    };
  }

  function addStep(turn, title, detail = "", isError = false, tool = "") {
    const shouldFollow = nearBottom();
    turn.steps += 1;
    const item = document.createElement("li");
    item.className = "activity-item";
    item.innerHTML = `
      <details class="activity-disclosure">
        <summary class="activity-card-summary">
          <span class="activity-step-number">${turn.steps}</span>
          <strong class="activity-step-title">${esc(title)}</strong>
          <span class="material-symbols-rounded activity-expand-icon" aria-hidden="true">expand_more</span>
        </summary>
        <div class="activity-expanded">
          <div class="activity-card-meta">
            <span class="activity-tool">${esc(tool)}</span>
            <span class="activity-status ${isError ? "error" : "success"}">${isError ? "Failed" : "Completed"}</span>
          </div>
          ${detail ? `<div class="activity-flow"><section class="activity-section"><p class="activity-detail">${esc(detail)}</p></section></div>` : ""}
        </div>
      </details>`;
    turn.list.appendChild(item);
    follow(shouldFollow);
  }

  function setWaiting(turn, text) {
    if (turn.empty) turn.empty.innerHTML = thinkingHtml(text || "Thinking");
  }

  function renderStreaming(turn) {
    const shouldFollow = nearBottom();
    turn.body.hidden = false;
    turn.body.innerHTML = `<div class="answer-streaming-wrap">${markdown(turn.streamed)}</div>`;
    turn.body.lastElementChild?.lastElementChild?.classList.add("answer-streaming");
    follow(shouldFollow);
  }

  function renderAnswer(turn, answer) {
    const shouldFollow = nearBottom();
    const citations = (answer.citations || []).map(c => typeof c === "string" ? { id: c } : c).filter(c => c && c.id);
    turn.answer = answer;
    turn.citations = citations;
    turn.body.hidden = false;
    turn.body.innerHTML = markdown(answer.content || "", citations);
    if (citations.length) {
      const sources = document.createElement("div");
      sources.className = "chat-sources";
      citations.slice(0, MAX_SOURCES).forEach((cite, index) => {
        const button = document.createElement("button");
        button.type = "button";
        button.dataset.citeId = cite.id;
        button.title = cite.text || cite.id;
        button.textContent = `${index + 1}. ${[cite.type, (cite.time || "").replace("T", " ").slice(0, 16)].filter(Boolean).join(" · ") || cite.id}`;
        sources.appendChild(button);
      });
      const total = Number(answer.total || citations.length);
      if (total > MAX_SOURCES) {
        const more = document.createElement("span");
        more.className = "chat-sources-more";
        more.textContent = `${total - MAX_SOURCES} more`;
        sources.appendChild(more);
      }
      turn.body.appendChild(sources);
    }
    if (answer.action && ["tag", "note"].includes(answer.action.kind)) turn.body.appendChild(i360ActionCard(answer.action));
    const followUps = (answer.follow || []).filter(f => typeof f === "string").slice(0, 4);
    if (followUps.length) {
      const box = document.createElement("div");
      box.className = "chat-follow";
      followUps.forEach(text => {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = text;
        button.addEventListener("click", () => send(text));
        box.appendChild(button);
      });
      turn.body.appendChild(box);
    }
    follow(shouldFollow);
  }

  function finishTurn(turn) {
    const research = turn.article.querySelector(".research-process");
    const details = document.createElement("details");
    details.className = "research-steps-toggle";
    details.innerHTML = `<summary>Research process${turn.steps ? ` · ${turn.steps} step${turn.steps === 1 ? "" : "s"}` : ""}</summary>`;
    if (turn.steps) details.appendChild(turn.list);
    else details.insertAdjacentHTML("beforeend", `<div class="activity-empty">No steps were needed.</div>`);
    research?.replaceWith(details);
    turn.body.hidden = false;
    if (!turn.answer && turn.streamed) turn.body.innerHTML = markdown(turn.streamed);
    if (turn.note) turn.body.insertAdjacentHTML("beforeend", `<div class="chat-note">${markdown(turn.note)}</div>`);
    turn.errors.forEach(text => turn.body.insertAdjacentHTML("beforeend", `<div class="chat-error">${esc(text)}</div>`));
    if (!turn.answer && !turn.note && !turn.errors.length && !turn.streamed) {
      turn.body.insertAdjacentHTML("beforeend", `<p class="chat-note">No answer.</p>`);
    }
    if (turn.shownLayerIds.length) turn.body.appendChild(answerActions(turn));
  }

  /* Under an answer that added layers: Show results (toggle them) and Save to memory, as in the original chat. */
  function answerActions(turn) {
    const actions = document.createElement("div");
    actions.className = "final-answer-actions";
    const show = document.createElement("button");
    show.type = "button";
    show.className = "final-answer-show-btn";
    show.textContent = "Hide results";
    show.addEventListener("click", () => {
      const layers = state.layers.filter(layer => turn.shownLayerIds.includes(layer.id));
      const visible = !layers.some(layer => layer.visible);
      layers.forEach(layer => { layer.visible = visible; });
      show.textContent = visible ? "Hide results" : "Show results";
      renderAllViews();
    });
    actions.appendChild(show);
    if (state.investigationId) {
      const save = document.createElement("button");
      save.type = "button";
      save.className = "final-answer-memory-btn";
      save.textContent = "Save to memory";
      save.addEventListener("click", () => {
        const layer = state.layers.find(item => turn.shownLayerIds.includes(item.id));
        if (layer) saveLayerToInvestigationMemory(layer, save);
      });
      actions.appendChild(save);
    }
    return actions;
  }

  // -- confirm cards ------------------------------------------------------------------------
  function confirmCard(question, onConfirm) {
    const card = document.createElement("div");
    card.className = "chat-confirm";
    card.innerHTML = `<div>${question}</div><div class="chat-confirm-actions"><button type="button" class="chat-confirm-ok">Confirm</button><button type="button">Cancel</button></div><div class="chat-confirm-result" hidden></div>`;
    const [ok, cancel] = card.querySelectorAll("button");
    const result = card.querySelector(".chat-confirm-result");
    const done = text => { card.querySelector(".chat-confirm-actions").remove(); result.hidden = false; result.textContent = text; };
    ok.addEventListener("click", async () => {
      ok.disabled = cancel.disabled = true;
      try { done(await onConfirm(ok) || "Done."); } catch (error) { done(error.message || "That did not work."); }
    });
    cancel.addEventListener("click", () => done("Cancelled. Nothing was written."));
    return card;
  }

  /* A tag or note the i360 answer proposed: only the click writes, through the chat service. */
  function i360ActionCard(action) {
    const count = (action.ids || []).length;
    const question = action.kind === "tag"
      ? `Tag <b>${count}</b> record${count === 1 ? "" : "s"} with <code>${esc(action.type)}: ${esc(action.value)}</code>?`
      : `Add this note to <b>${count}</b> record${count === 1 ? "" : "s"}? <code>${esc(String(action.value || "").slice(0, 200))}</code>`;
    return confirmCard(question, async () => {
      const response = await fetch("/api/chat/action", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action, conversation_id: CHAT.i360ConversationId }),
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(payload.message || "The write was refused.");
      return payload.line || "Written.";
    });
  }

  // -- actions from the assistant -----------------------------------------------------------
  function itemLayers(groups, label, sourceId, view) {
    const layers = [];
    groups.forEach(group => {
      const rows = Array.isArray(group.rows) ? group.rows : [];
      if (!rows.length) return;
      const name = groups.length > 1 ? `Chat: ${label} · ${group.label}` : `Chat: ${label}`;
      const meta = {
        id: `${sourceId}:${group.label}`, label: name, kind: "events", source_type: group.label,
        capabilities: { table: true, timeline: true, map: rows.some(row => row.latitude || row.location_id) },
      };
      layers.push(buildCatalogLayer(meta, rows));
    });
    return addResultLayers({ sourceId, sourceLabel: `Chat: ${label}`, preferredView: view || "table", layers });
  }

  async function ensureCatalog() {
    if (!state.layerCatalog?.length) await loadLayerCatalog();
  }

  function openRow(row, groupLabel) {
    const recordId = row.record_id || row.event_id || row.i360_item_id;
    const already = state.layers.some(layer => (layer.items || []).some(item => (item.record_id || item.event_id) === recordId));
    if (!already) {
      const existing = state.layers.find(layer => layer.sourceId === CHAT.openedLayerKey);
      if (existing) {
        existing.items.push({ ...row, date: new Date(row.timestamp_utc) });
      } else {
        itemLayers([{ label: groupLabel || "records", rows: [row] }], "opened records", CHAT.openedLayerKey, "table");
      }
      renderAllViews();
      renderLayerSelector();
    }
    if (!openObjectViewer("record", recordId)) throw new Error("The record viewer could not open this record.");
  }

  async function openCited(id) {
    const response = await fetch("/api/chat/items", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ids: [id], locale: "en" }),
    });
    const payload = await response.json().catch(() => ({}));
    const group = (payload.groups || [])[0];
    const row = group?.rows?.[0];
    if (!response.ok || !row) throw new Error(payload.message || "This record could not be read.");
    openRow(row, group.label);
  }

  async function runAction(turn, action) {
    try {
      if (action.kind === "show_items") {
        const added = itemLayers(action.groups || [], action.label || "results", `chat:${turn.id}`, action.view);
        turn.shownLayerIds.push(...added.map(layer => layer.id));
        if (added[0]) state.activeLayerId = added[0].id;
        renderAllViews();
        renderLayerSelector();
        activateView(action.view || "table");
      } else if (action.kind === "open_layer") {
        await ensureCatalog();
        const layer = await openCatalogLayer(action.layer_id, { filters: action.filters || {} });
        if (!layer) throw new Error("The layer could not be opened.");
        if (action.view) activateView(action.view);
      } else if (action.kind === "open_item") {
        openRow(action.row, action.group);
      } else if (action.kind === "show_memory") {
        for (const id of action.ids || []) await openMemoryEntry("layers", id);
      } else if (action.kind === "confirm_save") {
        turn.body.hidden = false;
        turn.body.appendChild(confirmCard(`Save the layer <b>${esc(action.layer)}</b> to this investigation's memory?`, async button => {
          const wanted = String(action.layer || "").toLowerCase();
          const layer = state.layers.find(item => String(item.label).toLowerCase() === wanted)
            || state.layers.find(item => String(item.label).toLowerCase().includes(wanted));
          if (!layer) throw new Error("That layer is not on screen.");
          await saveLayerToInvestigationMemory(layer, button);
          return "Opened the save dialog.";
        }));
      }
    } catch (error) {
      turn.errors.push(error.message || "An action failed.");
    }
  }

  // -- the stream ---------------------------------------------------------------------------
  function parseBlock(block) {
    const event = (block.match(/^event: *(\w+)/m) || [])[1];
    if (!event) return null;
    const data = block.split("\n").filter(line => line.startsWith("data:")).map(line => line.slice(5).replace(/^ /, "")).join("\n");
    try { return { event, data: data ? JSON.parse(data) : null }; } catch { return { event, data: null }; }
  }

  async function handle(turn, event, data) {
    if (event === "step") {
      addStep(turn, data?.text || "Step", "", Boolean(data?.error), data?.tool || "");
      if (data?.tool === "ask_i360") setWaiting(turn, "i360 is searching");
    } else if (event === "i360") {
      const inner = data?.event, payload = data?.data || {};
      if (inner === "status") {
        setWaiting(turn, payload.text || "i360 is searching");
        (payload.steps || []).slice(turn.i360Steps || 0).forEach(step => addStep(turn, `i360: ${step.summary || step.text || step.tool || "step"}`, step.args ? JSON.stringify(step.args) : "", false, step.tool || "i360"));
        turn.i360Steps = Math.max(turn.i360Steps || 0, (payload.steps || []).length);
      } else if (inner === "token") {
        turn.streamed += payload.text || "";
        renderStreaming(turn);
      } else if (inner === "answer") {
        renderAnswer(turn, payload);
      } else if (inner === "error") {
        turn.errors.push(`i360: ${payload.message || "error"}`);
      }
    } else if (event === "action") {
      await runAction(turn, data || {});
    } else if (event === "note") {
      turn.note = data?.text || "";
    } else if (event === "error") {
      turn.errors.push(data?.message || "The chat failed.");
    } else if (event === "done") {
      CHAT.i360ConversationId = data?.i360_conversation_id || CHAT.i360ConversationId;
      if (Array.isArray(data?.citations)) CHAT.citations = data.citations;
    }
  }

  function setBusy(busy) {
    CHAT.busy = busy;
    $("sendButton").disabled = busy;
    $("chatStop").hidden = !busy;
  }

  function resetConversation(message) {
    CHAT.controller?.abort();
    CHAT.history = [];
    CHAT.citations = [];
    CHAT.i360ConversationId = "";
    CHAT.investigationId = state.investigationId || null;
    $("conversation").innerHTML = "";
    if (message) appendMessage("assistant", `<p class="chat-welcome">${esc(message)}</p>`);
    renderScope();
  }

  async function send(text) {
    const message = String(text || "").trim();
    if (!message || CHAT.busy) return;
    if ((state.investigationId || null) !== CHAT.investigationId) resetConversation();
    appendMessage("user", `<p>${esc(message)}</p>`);
    const turn = startTurn();
    setBusy(true);
    CHAT.controller = new AbortController();
    const body = {
      message,
      history: CHAT.history.slice(-12),
      investigation_id: state.investigationId || "",
      investigation_name: state.investigationName || "",
      scope: state.investigationId ? CHAT.scope : "all",
      i360_conversation_id: CHAT.i360ConversationId,
      previous_citations: CHAT.citations,
      open_layers: state.layers.filter(layer => layer.visible).map(layer => layer.label).slice(0, 40),
      tz: (() => { try { return Intl.DateTimeFormat().resolvedOptions().timeZone; } catch { return ""; } })(),
      locale: "en",
    };
    try {
      const response = await fetch("/api/chat/ask", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body), signal: CHAT.controller.signal,
      });
      if (!response.ok || !response.body) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(payload.message || `The chat answered ${response.status}.`);
      }
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      for (;;) {
        const chunk = await reader.read();
        if (chunk.done) break;
        buffer += decoder.decode(chunk.value, { stream: true }).replace(/\r\n/g, "\n");
        let index;
        while ((index = buffer.indexOf("\n\n")) >= 0) {
          const block = buffer.slice(0, index);
          buffer = buffer.slice(index + 2);
          const parsed = parseBlock(block);
          if (parsed) await handle(turn, parsed.event, parsed.data);
        }
      }
    } catch (error) {
      turn.errors.push(error.name === "AbortError" ? "Stopped." : (error.message || "The chat could not be reached."));
    } finally {
      finishTurn(turn);
      setBusy(false);
      CHAT.controller = null;
      const summary = [turn.answer?.content ? `i360 answered: ${String(turn.answer.content).slice(0, 600)}` : "", turn.note]
        .filter(Boolean).join("\n");
      CHAT.history.push({ role: "user", content: message }, { role: "assistant", content: summary || "(no answer)" });
      $("promptInput").focus();
    }
  }

  // -- panel --------------------------------------------------------------------------------
  function renderScope() {
    const hasInvestigation = Boolean(state.investigationId);
    const scope = hasInvestigation ? CHAT.scope : "all";
    $("chatScopeInvestigation").disabled = !hasInvestigation;
    $("chatScopeInvestigation").setAttribute("aria-pressed", String(scope === "investigation"));
    $("chatScopeAll").setAttribute("aria-pressed", String(scope === "all"));
  }

  function bindResizer() {
    const resizer = document.querySelector(".panel-resizer");
    const workspace = document.querySelector(".workspace");
    resizer.addEventListener("pointerdown", event => {
      if (event.target.closest("button") || workspace.classList.contains("chat-panel-collapsed")) return;
      resizer.classList.add("dragging");
      resizer.setPointerCapture(event.pointerId);
      const left = workspace.getBoundingClientRect().left;
      const move = moveEvent => {
        const width = Math.max(280, Math.min(moveEvent.clientX - left - 12, workspace.clientWidth * 0.6));
        workspace.style.setProperty("--chat-width", `${Math.round(width)}px`);
        if (state.map) state.map.resize();
      };
      const up = () => {
        resizer.classList.remove("dragging");
        resizer.removeEventListener("pointermove", move);
        resizer.removeEventListener("pointerup", up);
      };
      resizer.addEventListener("pointermove", move);
      resizer.addEventListener("pointerup", up);
    });
  }

  function bind() {
    const workspace = document.querySelector(".workspace");
    workspace.classList.add("has-chat");
    $("conversationPanel").hidden = false;
    document.querySelector(".panel-resizer").hidden = false;
    $("promptForm").addEventListener("submit", event => {
      event.preventDefault();
      const input = $("promptInput");
      const text = input.value;
      input.value = "";
      send(text);
    });
    $("promptInput").addEventListener("keydown", event => {
      if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
        event.preventDefault();
        $("promptForm").requestSubmit();
      }
    });
    $("chatStop").addEventListener("click", () => CHAT.controller?.abort());
    $("chatNew").addEventListener("click", () => resetConversation("New conversation."));
    $("chatScopeInvestigation").addEventListener("click", () => { CHAT.scope = "investigation"; renderScope(); });
    $("chatScopeAll").addEventListener("click", () => { CHAT.scope = "all"; renderScope(); });
    $("chatPanelToggle").addEventListener("click", () => {
      const collapsed = workspace.classList.toggle("chat-panel-collapsed");
      $("chatPanelToggle").setAttribute("aria-expanded", String(!collapsed));
      $("chatPanelToggle").title = collapsed ? "Open the chat" : "Collapse the chat";
      setTimeout(() => state.map?.resize(), 220);
    });
    $("conversation").addEventListener("click", event => {
      const button = event.target.closest("[data-cite-id]");
      if (!button) return;
      openCited(button.dataset.citeId).catch(error => { button.title = error.message; });
    });
    bindResizer();
    CHAT.investigationId = state.investigationId || null;
    renderScope();
    setInterval(renderScope, 1500);  // the investigation can change from the header at any time
    setTimeout(() => state.map?.resize(), 0);
  }

  async function init() {
    try {
      const response = await fetch("/api/status", { cache: "no-store" });
      const status = await response.json();
      if (!status?.features?.ai) return;  // no chat service on this deployment: the panel stays hidden
    } catch {
      return;
    }
    CHAT.on = true;
    bind();
  }

  /* app.js is loaded by demo_bootstrap.js after the session is known; wait for its functions. */
  let tries = 0;
  const ready = setInterval(() => {
    tries += 1;
    if (typeof addResultLayers === "function" && typeof state === "object" && document.querySelector(".workspace")) {
      clearInterval(ready);
      init();
    } else if (tries > 600) {
      clearInterval(ready);
    }
  }, 100);

  window.AIIChat = { send, state: CHAT };
})();
