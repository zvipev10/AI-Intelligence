const LOCATIONS = {
  "L-201": { name: "נמל חיפה", type: "נמל", lat: 32.820, lon: 35.000 },
  "L-202": { name: "מתחם מחסנים קישון", type: "אזור תעשייה", lat: 32.790, lon: 35.040 },
  "L-203": { name: "מעבר נהר הירדן", type: "מעבר גבול", lat: 32.503, lon: 35.570 },
  "L-204": { name: "צומת גולני", type: "צומת דרכים", lat: 32.782, lon: 35.409 },
  "L-205": { name: "שוק נצרת", type: "מרכז עירוני", lat: 32.699, lon: 35.303 },
  "L-206": { name: "כביש גישה צדדי ליד בית שאן", type: "דרך צדדית", lat: 32.505, lon: 35.500 },
  "L-207": { name: "אזור התעשייה בית שאן", type: "אזור תעשייה", lat: 32.500, lon: 35.500 },
  "L-208": { name: "משרד סיוע מרחב בחיפה", type: "משרד", lat: 32.815, lon: 34.995 },
  "L-209": { name: "מסוף דלק צמח", type: "מסוף דלק", lat: 32.703, lon: 35.586 }
};

const PRIMARY_IDS = new Set([
  "PORT-0090", "CUST-0101", "FIN-0098", "TEL-0112", "MOVE-0134", "OBS-0002",
  "CAM-0153", "SIG-0002", "ACOU-0137", "BORD-0001", "DRONE-0001", "FIN-0144", "TEL-0152"
]);
const EVENT_ID_PATTERN = /\b(?:PORT|CUST|FIN|TEL|MOVE|OBS|CAM|SIG|ACOU|BORD|DRONE|MAINT|SOC)-\d{4}\b/g;

function createInvestigationId() {
  const random = crypto?.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  return `investigation-${random}`;
}

const state = {
  events: [],
  current: [],
  stage: 0,
  region: null,
  window: null,
  actors: [],
  aggregateLocations: [],
  map: null,
  mapReady: false,
  markers: [],
  history: [],
  investigationId: createInvestigationId(),
  investigationState: null,
  busy: false
};

function buildInvestigationState(result, prompt) {
  const prev = state.investigationState || {
    turn: 0,
    confirmed_event_ids: [],
    confirmed_actors: [],
    entities_resolved: {},
    open_leads: [],
    current_hypothesis: null,
    confidence: null,
    gaps: []
  };

  // Accumulate confirmed event IDs across turns (union, preserve order)
  const existingIds = new Set(prev.confirmed_event_ids);
  const newIds = (result.event_ids || []).concat(
    ((result.answer || "").match(EVENT_ID_PATTERN) || [])
  );
  newIds.forEach(id => existingIds.add(id));
  const confirmed_event_ids = [...existingIds];

  // Accumulate actors
  const existingActors = new Set(prev.confirmed_actors);
  state.actors.forEach(actor => existingActors.add(actor));
  const confirmed_actors = [...existingActors];

  // Accumulate entity resolutions from audit steps
  const entities_resolved = { ...prev.entities_resolved };
  (result.investigation_steps || []).forEach(step => {
    if (step.tool === "resolve_entity" && step.result) {
      // Extract "canonical ← aliases" patterns reported in audit summary
      const match = step.result.match(/ישות\s+(\S+).*?כינויים:\s*(.+)/);
      if (match) entities_resolved[match[1]] = match[2].split(",").map(s => s.trim());
    }
  });

  // Extract hypothesis — look for the first sentence after "השערה" or "ההשערה"
  let current_hypothesis = prev.current_hypothesis;
  const hypoMatch = (result.answer || "").match(/(?:ההשערה|השערה)[^\n:：]*[:\n]\s*([^\n.]{20,200})/i);
  if (hypoMatch) current_hypothesis = hypoMatch[1].trim();

  // Extract confidence level
  let confidence = prev.confidence;
  const confMatch = (result.answer || "").match(/(?:רמת ביטחון|ביטחון)[^\n:：]*[:\n]?\s*(גבוהה|בינונית|נמוכה)/i);
  if (confMatch) confidence = confMatch[1];

  // Extract gaps from challenge_hypothesis audit steps
  const gaps = [...prev.gaps];
  (result.investigation_steps || []).forEach(step => {
    if (step.tool === "challenge_hypothesis" && step.result) {
      const gapMatch = step.result.match(/פערים:\s*(.+)/);
      if (gapMatch) {
        gapMatch[1].split(";").map(s => s.trim()).filter(Boolean).forEach(gap => {
          if (!gaps.includes(gap)) gaps.push(gap);
        });
      }
    }
  });

  // Open leads: carry forward previous, trim if list grows too long
  const open_leads = prev.open_leads.slice(-5);

  return {
    turn: prev.turn + 1,
    confirmed_event_ids,
    confirmed_actors,
    entities_resolved,
    open_leads,
    current_hypothesis,
    confidence,
    gaps
  };
}

const conversation = document.getElementById("conversation");
const suggestions = document.getElementById("suggestions");
const promptForm = document.getElementById("promptForm");
const promptInput = document.getElementById("promptInput");
const resultTitle = document.getElementById("resultTitle");
const resultSubtitle = document.getElementById("resultSubtitle");
const resultCount = document.getElementById("resultCount");
const activityList = document.getElementById("activityList");
const activityEmpty = document.getElementById("activityEmpty");
const sendButton = document.getElementById("sendButton");
const agentStatus = document.getElementById("agentStatus");
const viewRecommendation = document.getElementById("viewRecommendation");
const workspace = document.querySelector(".workspace");

const VIEW_LABELS = {
  map: "מפה",
  timeline: "ציר זמן",
  evidence: "אירועים גולמיים"
};

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];
    if (char === '"' && quoted && next === '"') { cell += '"'; i += 1; }
    else if (char === '"') quoted = !quoted;
    else if (char === ',' && !quoted) { row.push(cell); cell = ""; }
    else if ((char === '\n' || char === '\r') && !quoted) {
      if (char === '\r' && next === '\n') i += 1;
      row.push(cell);
      if (row.some(value => value !== "")) rows.push(row);
      row = [];
      cell = "";
    } else cell += char;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  const headers = rows.shift().map(header => header.replace(/^\uFEFF/, ""));
  return rows.map(values => Object.fromEntries(headers.map((header, index) => [header, values[index] || ""])));
}

function enrich(event) {
  const location = LOCATIONS[event.location_id] || { name: event.location_id, type: "" };
  return { ...event, location_name: location.name, location_type: location.type, date: new Date(event.timestamp_utc) };
}

function collectAggregateLocations(result) {
  const byLocation = new Map();
  (result.investigation_steps || []).forEach(step => {
    (step.map_locations || []).forEach(item => {
      const locationId = item.location_id;
      if (!LOCATIONS[locationId]) return;
      const existing = byLocation.get(locationId);
      const count = Number(item.count || 0);
      if (!existing || count > existing.count) {
        byLocation.set(locationId, {
          location_id: locationId,
          location_name: item.location_name || LOCATIONS[locationId].name,
          count
        });
      }
    });
  });
  let locations = [...byLocation.values()].sort((a, b) => b.count - a.count);
  const idsInAnswer = new Set((result.answer || "").match(/\bL-\d{3}\b/g) || []);
  if (idsInAnswer.size) locations = locations.filter(item => idsInAnswer.has(item.location_id));
  return locations;
}

function initMap() {
  state.map = new maplibregl.Map({
    container: "map",
    style: {
      version: 8,
      sources: {
        osm: {
          type: "raster",
          tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
          tileSize: 256,
          attribution: "© OpenStreetMap contributors"
        }
      },
      layers: [{ id: "osm", type: "raster", source: "osm" }]
    },
    center: [35.28, 32.68],
    zoom: 8.2,
    minZoom: 7.1,
    maxZoom: 15,
    maxBounds: [[34.72, 32.30], [35.86, 33.08]],
    attributionControl: true
  });
  state.map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-left");
  state.map.on("load", () => { state.mapReady = true; renderMap(); });
}

function appendMessage(role, html) {
  const article = document.createElement("article");
  article.className = `message ${role === "user" ? "user-message" : "assistant-message"}`;
  article.innerHTML = `<div class="message-label">${role === "user" ? "אנליסט" : "סוכן חקירה"}</div>${html}`;
  conversation.appendChild(article);
  conversation.scrollTop = conversation.scrollHeight;
}

const TOOL_LABELS = {
  classify_question_intent: "סיווג כוונת השאלה",
  resolve_location: "הבנת המקום",
  resolve_event_reference: "זיהוי אירוע העוגן",
  search_events: "חיפוש ממוקד במאגר",
  get_events: "אימות הרשומות",
  find_actor_history: "בדיקת היסטוריית גורם",
  aggregate_events: "זיהוי ריכוזים",
  explain_linkage: "בדיקת גשר ראייתי",
  build_event_sequence: "בניית רצף האירועים",
  resolve_entity: "פתרון שמות וכינויים",
  trace_identifier: "מעקב אחר מזהה חוזר",
  trace_semantic_clues: "מעקב אחר רמזים סמנטיים",
  plan_next_investigation_step: "בקרת תהליך החקירה",
  find_related_events: "הרחבת מעגל הראיות",
  challenge_hypothesis: "בדיקת ההשערה מול חלופות"
};

function humanToolLabel(tool) {
  const clean = String(tool || "").replace(/^\d+\.\s*/, "");
  return TOOL_LABELS[clean] || "פעולת חקירה";
}

function formatTechnical(technical, fallbackTool) {
  const payload = technical || { tool: fallbackTool, arguments: {} };
  return JSON.stringify(payload, null, 2);
}

function addActivity(tool, detail, result, options = {}) {
  activityEmpty.hidden = true;
  const item = document.createElement("li");
  item.className = "activity-item";
  const stepNumber = options.stepNumber || activityList.children.length + 1;
  const cleanTool = String(tool || "").replace(/^\d+\.\s*/, "");
  const bridgeSummary = options.bridgeSummary || options.rationale || "הסוכן ממשיך לצעד זה כדי לצמצם את השאלה לפי ההקשר שנאסף עד עכשיו.";
  const technical = formatTechnical(options.technical, cleanTool);
  item.innerHTML = `
    <div class="activity-card-header">
      <span class="activity-step-number">${stepNumber}</span>
      <div class="activity-card-title">
        <strong>${escapeHtml(humanToolLabel(cleanTool))}</strong>
        <span class="activity-tool">${escapeHtml(cleanTool)}</span>
      </div>
      <span class="activity-status ${options.isError ? "error" : "success"}">${options.isError ? "נכשל" : "הושלם"}</span>
    </div>
    <div class="activity-flow">
      <section class="activity-section rationale-section">
        <div class="activity-section-label">ניתוח הסוכן והחלטת המשך</div>
        <p class="activity-rationale">${escapeHtml(bridgeSummary)}</p>
      </section>
      <section class="activity-section">
        <div class="activity-section-label">מה נבדק</div>
        <p class="activity-detail">${escapeHtml(detail)}</p>
      </section>
      <section class="activity-section result-section">
        <div class="activity-section-label">מה התקבל</div>
        <p class="activity-result">${escapeHtml(result)}</p>
      </section>
    </div>
    <details class="activity-technical">
      <summary>פרטים טכניים</summary>
      <pre>${escapeHtml(technical)}</pre>
    </details>`;
  activityList.appendChild(item);
}

function setSuggestions(items) {
  suggestions.innerHTML = items.map(item => `<button type="button" data-prompt="${item}">${item}</button>`).join("");
}

function eventText(event) {
  return `${event.event_summary} ${event.entity_or_actor} ${event.location_name}`;
}

function firstInvestigation() {
  const anchor = state.events.find(event => event.event_id === "BORD-0001");
  const start = new Date("2026-05-17T18:00:00Z");
  const end = anchor ? anchor.date : new Date("2026-05-18T01:05:00Z");
  const relevantLocations = new Set(["L-202", "L-204", "L-206", "L-207", "L-203"]);
  const result = state.events.filter(event => PRIMARY_IDS.has(event.event_id) && relevantLocations.has(event.location_id) && event.date >= start && event.date <= end);
  state.current = result;
  state.stage = 1;
  state.region = "בית שאן והצירים המובילים אליו";
  state.window = "17 במאי 18:00 עד אירוע הגבול ב־18 במאי 01:05";
  state.actors = [...new Set(result.map(event => event.entity_or_actor).filter(actor => actor && actor !== "לא ידוע"))];
  addActivity("resolve_reference", "פירוש 'אירוע הגבול' כאירוע BORD-0001 ופירוש 'אזור בית שאן' כמיקומים הסמוכים והצירים המובילים אליו.", "עוגן זמן אחד ו־5 מיקומים");
  addActivity("filter_events", "סינון אירועים לפני העוגן, החל מהערב הקודם ובמיקומים הרלוונטיים.", `${result.length} אירועים נבחרו`);
  addActivity("cross_reference", "חיבור תנועה, תצפית, אות וחיישני גבול לפי זמן, מקום וגורמים חוזרים.", "רצף פעילות אחד נמצא");
  showResult("פעילות לילית מתכנסת לכיוון בית שאן", "נמצא רצף רב־מקורי המתחיל בקישון, עובר בצומת גולני ומגיע לאזור בית שאן לפני אירוע הגבול.");
  appendMessage("assistant", `<p>כן. זוהה רצף חריג של <strong>${result.length} אירועים</strong> לפני אירוע הגבול.</p><div class="answer-callout">הרצף כולל יציאת משאיות מכוסות מקישון, מעבר מזרחה בצומת גולני, מסר המתייחס לדרך צדדית, רעש כלי רכב כבדים ולבסוף מקבץ כלי רכב סמוך למעבר נהר הירדן.</div><p>החיבור מעניין משום שהוא נשען על כמה סוגי מקורות ולא על התאמה מילולית אחת.</p>`);
  setSuggestions(["מי מהגורמים האלה הופיע קודם באזור חיפה?", "הצג רק פעילות לילית", "האם היו תנועות כספיות הקשורות אליהם?"]);
}

function priorHaifa() {
  const actors = new Set(state.actors);
  const cutoff = new Date("2026-05-17T18:00:00Z");
  const result = state.events.filter(event => event.date < cutoff && ["L-201", "L-208", "L-202"].includes(event.location_id) && (actors.has(event.entity_or_actor) || PRIMARY_IDS.has(event.event_id)));
  state.current = result.filter(event => PRIMARY_IDS.has(event.event_id));
  state.stage = 2;
  state.region = "חיפה וקישון";
  state.window = "לפני 17 במאי 18:00";
  addActivity("resolve_context", "המונח 'הגורמים האלה' נפתר מול הגורמים שנמצאו בשאלה הקודמת.", `${actors.size} גורמים בהקשר`);
  addActivity("search_history", "חיפוש הופעות קודמות של אותם גורמים בנמל חיפה, משרד הסיוע ומתחם קישון.", `${state.current.length} ראיות ישירות`);
  showResult("הופעות קודמות באזור חיפה", "נמצאו חוליות מוקדמות בנמל, במשרד סיוע ובמתחם קישון לפני התנועה מזרחה.");
  appendMessage("assistant", `<p>נמצאו הופעות מוקדמות באזור חיפה הקשורות לאותו רצף:</p><div class="answer-callout"><strong>אופק לוגיסטיקה</strong> מופיעה ברישום המכולה בנמל; <strong>א. לוי</strong> מופיע בתשלום הקשור למשלוח; ו־<strong>לוי ימי</strong> יוצר קשר עם מנהל מחסן 11.</div><p>כלומר, מוקד הפעילות אינו מתחיל בבית שאן אלא נבנה קודם באזור חיפה וקישון.</p>`);
  setSuggestions(["הצג רק פעילות לילית", "האם היו תנועות כספיות הקשורות אליהם?", "חזור לכל הרצף עד אירוע הגבול"]);
}

function nightOnly() {
  const base = state.current.length ? state.current : state.events.filter(event => PRIMARY_IDS.has(event.event_id));
  const result = base.filter(event => { const hour = event.date.getUTCHours(); return hour >= 20 || hour < 6; });
  state.current = result;
  state.stage = 3;
  state.window = "20:00–06:00 בתוך קבוצת התוצאות הקודמת";
  addActivity("refine_time", "החלת מסנן פעילות לילית על קבוצת התוצאות הפעילה, ללא הרצת החקירה מחדש.", `${result.length} אירועים נותרו`);
  showResult("פעילות לילית בלבד", "התצוגה צומצמה לאירועים בין 20:00 ל־06:00 מתוך ההקשר הפעיל.");
  appendMessage("assistant", `<p>צמצמתי את קבוצת התוצאות הפעילה לשעות 20:00–06:00.</p><div class="answer-callout">נותרו <strong>${result.length} אירועים</strong>. המפה, ציר הזמן וטבלת הראיות עודכנו יחד, תוך שמירת הגורמים והמיקומים מהחקירה הקודמת.</div>`);
  setSuggestions(["האם היו תנועות כספיות הקשורות אליהם?", "חזור לכל הרצף עד אירוע הגבול"]);
}

function financialMoves() {
  const relatedActors = new Set([...state.actors, "א. לוי", "נועה ברק", "אופק לוגיסטיקה", "חוליית שעון חול"]);
  const result = state.events.filter(event => event.source_type === "התראה פיננסית" && (relatedActors.has(event.entity_or_actor) || PRIMARY_IDS.has(event.event_id)) && event.date >= new Date("2026-05-17T00:00:00Z") && event.date <= new Date("2026-05-18T12:00:00Z"));
  state.current = result.filter(event => PRIMARY_IDS.has(event.event_id));
  state.stage = 4;
  state.window = "17 במאי עד 18 במאי 12:00";
  addActivity("query_financial", "חיפוש התראות פיננסיות עבור הגורמים שנשמרו בהקשר ובחלון הזמן הסמוך לרצף.", `${state.current.length} תנועות רלוונטיות`);
  addActivity("link_evidence", "קישור התנועות הפיננסיות למיקומים ולאירועי התנועה באמצעות גורם, זמן והקשר משלוח.", "שני קשרים תומכים נמצאו");
  showResult("תנועות כספיות הקשורות לרצף", "נמצאו תשלום מוקדם לחשבון הטיפול של אופק וניסיון העברה מאוחר באזור בית שאן.");
  appendMessage("assistant", `<p>כן. נמצאו שתי תנועות כספיות המחזקות את הרצף:</p><div class="answer-callout">תשלום של <strong>48,000 ש״ח</strong> לחשבון טיפול של אופק לפני יציאת המשאיות, וניסיון העברה שנדחה לחשבון ספק באזור בית שאן לאחר ההגעה מזרחה.</div><p>הן אינן מוכיחות לבדן פעילות עוינת, אבל העיתוי והמיקומים מחזקים את הקשר בין שלבי ההתרחשות.</p>`);
  setSuggestions(["חזור לכל הרצף עד אירוע הגבול", "הצג רק פעילות לילית"]);
}

function restoreSequence() {
  firstInvestigation();
}

function fallback(prompt) {
  addActivity("interpret_request", "הבקשה נותחה אך אינה מכוסה עדיין בחוזה הכלים של תרחיש ה־POC.", "נדרשת הבהרה");
  appendMessage("assistant", `<p>התרחיש הנוכחי יודע להדגים חקירה סביב בית שאן, הופעות קודמות בחיפה, סינון לילי ותנועות כספיות.</p><p>אפשר לבחור אחת משאלות ההמשך המוצעות כדי לבדוק שמירת הקשר ותזמור כלים.</p>`);
}

function runScriptedPrompt(prompt) {
  const clean = prompt.trim();
  if (!clean) return;
  appendMessage("user", `<p>${escapeHtml(clean)}</p>`);
  if (clean.includes("מי מהגורמים") || clean.includes("אזור חיפה")) priorHaifa();
  else if (clean.includes("לילית") || clean.includes("שעות הלילה")) nightOnly();
  else if (clean.includes("כספ") || clean.includes("פיננס")) financialMoves();
  else if (clean.includes("חזור") || clean.includes("כל הרצף")) restoreSequence();
  else if (clean.includes("בית שאן") || clean.includes("אירוע הגבול")) firstInvestigation();
  else fallback(clean);
  updateContext();
}

function answerHtml(text) {
  const normalized = String(text || "")
    .replace(/(^|\n)(\s*מזהי\s+(?:ראיות|אירועים)\s*:)/m, "\n\n$2")
    .trim();
  const escaped = escapeHtml(normalized);
  if (!escaped) return "<p></p>";
  return escaped.split(/\n{2,}/).map(block => {
    const trimmed = block.trim();
    const evidenceMatch = trimmed.match(/^מזהי\s+(?:ראיות|אירועים)\s*:\s*(.+)$/s);
    if (evidenceMatch) {
      return `<details class="evidence-ids-toggle"><summary>מזהי אירועים</summary><p>${evidenceMatch[1].replace(/\n/g, "<br>")}</p></details>`;
    }
    const formatted = trimmed
      .replace(/^###?\s+(.+)$/gm, "<strong>$1</strong>")
      .replace(/^[-*]\s+(.+)$/gm, "• $1")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br>");
    return `<p>${formatted}</p>`;
  }).join("");
}

function cleanAssistantAnswer(text) {
  return String(text || "")
    .replace(/^\s*שלב חקירה\s*:.*(?:\r?\n|$)/gm, "")
    .trim();
}

function inferRecommendedView(prompt, answer) {
  const text = `${prompt || ""}\n${answer || ""}`;
  const scores = { map: 0, timeline: 0, evidence: 0 };
  const scoreTerms = (view, terms, weight = 1) => terms.forEach(term => {
    if (text.includes(term)) scores[view] += weight;
  });

  scoreTerms("map", ["מפה", "מסלול", "ציר תנועה", "מיקום", "אזור", "מרחק", "מערבית", "מזרח", "כביש", "מעבר"], 2);
  scoreTerms("timeline", ["רצף", "סדר הזמן", "ציר זמן", "לפני", "אחרי", "עיתוי", "בשעה", "דקות", "התחיל", "הסתיים"], 2);
  scoreTerms("evidence", ["אירועים גולמיים", "רשומות", "מקורות", "ראיות", "ציטוט", "אימות", "בדוק", "מזהי ראיות"], 2);

  if (/\b\d{2}:\d{2}\b/.test(text)) scores.timeline += 2;
  if ((answer || "").match(EVENT_ID_PATTERN)?.length >= 6) scores.evidence += 1;
  const view = Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0];
  const reasons = {
    map: "המיקומים ומסלול התנועה במוקד התשובה",
    timeline: "רצף האירועים והעיתוי במוקד התשובה",
    evidence: "בדיקת הראיות והרשומות במוקד התשובה"
  };
  return { view, reason: reasons[view] };
}

function renderActivitySteps(steps) {
  activityList.innerHTML = "";
  (steps || []).forEach((step, index) => {
    const explanation = step.model_explanation || {};
    addActivity(step.tool, step.action, step.result, {
      stepNumber: index + 1,
      bridgeSummary: explanation.bridge_summary || step.bridge_summary,
      rationale: explanation.decision || step.rationale || step.decision,
      technical: step.technical,
      isError: step.technical?.is_error
    });
  });
}

function applyHermesResult(result, prompt) {
  result.answer = cleanAssistantAnswer(result.answer);
  const idsFromAnswer = (result.answer || "").match(EVENT_ID_PATTERN) || [];
  const evidence = new Set([...(result.event_ids || []), ...idsFromAnswer]);
  state.current = state.events.filter(event => evidence.has(event.event_id));
  state.aggregateLocations = collectAggregateLocations(result);
  state.actors = [...new Set(state.current.map(event => event.entity_or_actor).filter(actor => actor && actor !== "לא ידוע"))];
  const locations = state.current.length
    ? [...new Set(state.current.map(event => event.location_name))]
    : state.aggregateLocations.map(item => item.location_name);
  state.region = locations.length ? locations.join(" · ") : "לא זוהה מתוך התשובה";
  if (state.current.length) {
    const ordered = [...state.current].sort((a, b) => a.date - b.date);
    state.window = `${ordered[0].timestamp_utc} עד ${ordered[ordered.length - 1].timestamp_utc}`;
  } else state.window = "לא זוהה מתוך התשובה";

  renderActivitySteps(result.investigation_steps || []);
  if (!(result.investigation_steps || []).length) {
    const started = (result.events || []).filter(event => event.event === "tool.started");
    started.forEach((event, index) => {
      const tool = (event.tool || "MCP").replace("mcp_intelligence_events_poc_", "");
      const input = event.preview ? `קלט שנשלח לכלי: ${event.preview}` : "Hermes לא החזיר את פרטי הקלט עבור פעולה זו.";
      addActivity(tool, input, "הכלי הסתיים ללא שגיאה; פירוט התוצאה לא נכלל ביומן Hermes.", {
        stepNumber: index + 1,
        observedClue: "Hermes דיווח שהסוכן בחר להפעיל כלי, אך לא החזיר רמז מפורט לשלב הזה.",
        rationale: "הסוכן בחר בכלי הזה כדי להמשיך לצמצם את אי-הוודאות בחקירה.",
        expectedValue: "לקבל ראיות נוספות או לאמת מועמד שכבר עלה.",
        technical: { tool, preview: event.preview || null }
      });
    });
  }
  if (!(result.investigation_steps || []).length && !(result.events || []).some(event => event.event === "tool.started")) {
    addActivity("Hermes", `שאלת החקירה שנשלחה: ${prompt}`, `התקבלה תשובה בריצה ${result.run_id}, ללא יומן כלי מפורט.`);
  }

  appendMessage("assistant", answerHtml(result.answer));
  showResult(
    "ממצאי חקירת הסוכן",
    state.current.length
      ? "הראיות שהסוכן ציטט מוצגות במפה, בציר הזמן ובטבלה."
      : (state.aggregateLocations.length ? "התוצאה האגרגטיבית מוצגת לפי מיקומים על המפה ובטבלה." : "הסוכן השיב, אך לא נמצאו בתשובה מזהי אירועים שניתן לקשר לתצוגה.")
  );
  const inferred = inferRecommendedView(prompt, result.answer);
  activateView(result.recommended_view || inferred.view, {
    automatic: true,
    reason: result.view_reason || inferred.reason
  });
  setSuggestions(["אילו הסברים תמימים יכולים להתאים לאותן ראיות?", "מה חסר כדי להעלות את רמת הביטחון?", "הצג את רצף האירועים לפי סדר הזמן"]);
  state.investigationState = buildInvestigationState(result, prompt);
  updateContext();
}

async function runPrompt(prompt) {
  const clean = prompt.trim();
  if (!clean || state.busy) return;
  const clientStarted = performance.now();
  let firstLiveStepAt = null;
  appendMessage("user", `<p>${escapeHtml(clean)}</p>`);
  state.busy = true;
  sendButton.disabled = true;
  sendButton.textContent = "חוקר...";
  suggestions.innerHTML = "";
  activityList.innerHTML = "";
  activityEmpty.hidden = false;
  activityEmpty.textContent = "Hermes מנתח את הבקשה ומפעיל כלי חקירה...";
  let liveStepCount = 0;
  let progressTimer = null;
  const pollLiveSteps = async () => {
    try {
      const response = await fetch("/api/live-steps", { cache: "no-store" });
      if (!response.ok) return;
      const live = await response.json();
      const steps = live.investigation_steps || [];
      if (steps.length && steps.length !== liveStepCount) {
        if (!firstLiveStepAt) firstLiveStepAt = performance.now();
        liveStepCount = steps.length;
        renderActivitySteps(steps);
        activityEmpty.hidden = true;
      }
    } catch (error) {
      // Live progress is best-effort; the final investigation response still drives completion.
    }
  };
  try {
    const investigationRequest = fetch("/api/investigate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt: clean,
        history: state.history,
        investigation_id: state.investigationId,
        investigation_state: state.investigationState
      })
    });
    progressTimer = setInterval(pollLiveSteps, 1800);
    setTimeout(pollLiveSteps, 900);
    const response = await investigationRequest;
    const responseReceivedAt = performance.now();
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Hermes request failed");
    result.answer = cleanAssistantAnswer(result.answer);
    state.history.push({ role: "user", content: clean }, { role: "assistant", content: result.answer });
    const renderStarted = performance.now();
    applyHermesResult(result, clean);
    const renderEnded = performance.now();
    const clientPerformance = {
      total_ms: Number((renderEnded - clientStarted).toFixed(3)),
      request_response_ms: Number((responseReceivedAt - clientStarted).toFixed(3)),
      render_ms: Number((renderEnded - renderStarted).toFixed(3)),
      time_to_first_live_step_ms: firstLiveStepAt ? Number((firstLiveStepAt - clientStarted).toFixed(3)) : null,
    };
    if (result.run_id) {
      fetch("/api/performance-client", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ run_id: result.run_id, client: clientPerformance })
      }).catch(() => {});
    }
  } catch (error) {
    activityEmpty.hidden = true;
    addActivity("connection_error", "לא ניתן היה להשלים ריצת Hermes.", error.message);
    appendMessage("assistant", `<p>לא הצלחתי להשלים את ריצת הסוכן האמיתית.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`);
    agentStatus.textContent = "Hermes אינו זמין";
    agentStatus.className = "agent-error";
  } finally {
    if (progressTimer) clearInterval(progressTimer);
    state.busy = false;
    sendButton.disabled = false;
    sendButton.textContent = "שלח";
  }
}

function showResult(title, subtitle) {
  resultTitle.textContent = title;
  resultSubtitle.textContent = subtitle;
  resultCount.textContent = state.current.length
    ? `${state.current.length} אירועים`
    : `${state.aggregateLocations.length} מיקומים`;
  renderAllViews();
}

function renderAllViews() {
  renderMap();
  renderTimeline();
  renderEvidence();
}

function activateView(view, options = {}) {
  const safeView = VIEW_LABELS[view] ? view : "evidence";
  document.querySelectorAll(".view-tab").forEach(button => button.classList.toggle("active", button.dataset.view === safeView));
  document.querySelectorAll(".view-pane").forEach(pane => pane.classList.toggle("active", pane.id === `${safeView}View`));
  if (safeView === "map" && state.map) setTimeout(() => state.map.resize(), 0);
  if (options.automatic) {
    viewRecommendation.hidden = false;
    viewRecommendation.textContent = `הסוכן בחר להציג: ${VIEW_LABELS[safeView]} · ${options.reason}`;
  } else {
    viewRecommendation.hidden = true;
    viewRecommendation.textContent = "";
  }
}

function setPanelWidths(chatWidth, resultWidth, activityWidth) {
  workspace.style.setProperty("--chat-width", `${Math.round(chatWidth)}px`);
  workspace.style.setProperty("--result-width", `${Math.round(resultWidth)}px`);
  workspace.style.setProperty("--activity-width", `${Math.round(activityWidth)}px`);
  if (state.map) setTimeout(() => state.map.resize(), 0);
}

function initPanelResizers() {
  document.querySelectorAll(".panel-resizer").forEach(handle => {
    handle.addEventListener("pointerdown", event => {
      event.preventDefault();
      handle.setPointerCapture(event.pointerId);
      handle.classList.add("dragging");
      const chat = document.querySelector(".conversation-panel");
      const result = document.querySelector(".result-panel");
      const activity = document.querySelector(".activity-panel");
      const start = {
        chat: chat.getBoundingClientRect(),
        result: result.getBoundingClientRect(),
        activity: activity.getBoundingClientRect(),
      };
      const min = { chat: 220, result: 340, activity: 220 };

      const onMove = moveEvent => {
        let chatWidth = start.chat.width;
        let resultWidth = start.result.width;
        let activityWidth = start.activity.width;
        const boundary = moveEvent.clientX;
        if (handle.dataset.resizer === "left") {
          const chatOnRight = start.chat.left > start.result.left;
          const unionLeft = Math.min(start.chat.left, start.result.left);
          const unionRight = Math.max(start.chat.right, start.result.right);
          if (chatOnRight) {
            resultWidth = Math.max(min.result, boundary - unionLeft);
            chatWidth = Math.max(min.chat, unionRight - boundary);
          } else {
            chatWidth = Math.max(min.chat, boundary - unionLeft);
            resultWidth = Math.max(min.result, unionRight - boundary);
          }
        } else {
          const activityOnRight = start.activity.left > start.result.left;
          const unionLeft = Math.min(start.activity.left, start.result.left);
          const unionRight = Math.max(start.activity.right, start.result.right);
          if (activityOnRight) {
            resultWidth = Math.max(min.result, boundary - unionLeft);
            activityWidth = Math.max(min.activity, unionRight - boundary);
          } else {
            activityWidth = Math.max(min.activity, boundary - unionLeft);
            resultWidth = Math.max(min.result, unionRight - boundary);
          }
        }
        setPanelWidths(chatWidth, resultWidth, activityWidth);
      };

      const onUp = upEvent => {
        handle.releasePointerCapture(upEvent.pointerId);
        handle.classList.remove("dragging");
        window.removeEventListener("pointermove", onMove);
        window.removeEventListener("pointerup", onUp);
      };

      window.addEventListener("pointermove", onMove);
      window.addEventListener("pointerup", onUp);
    });
  });
}

function clearMarkers() {
  state.markers.forEach(marker => marker.remove());
  state.markers = [];
}

function renderMap() {
  if (!state.mapReady) return;
  clearMarkers();
  const counts = {};
  state.current.forEach(event => { counts[event.location_id] = (counts[event.location_id] || 0) + 1; });
  if (!state.current.length) {
    state.aggregateLocations.forEach(item => { counts[item.location_id] = item.count; });
  }
  const bounds = new maplibregl.LngLatBounds();
  Object.entries(counts).forEach(([locationId, count]) => {
    const location = LOCATIONS[locationId];
    if (!location) return;
    const element = document.createElement("div");
    element.className = `map-marker${["L-206", "L-207", "L-203"].includes(locationId) ? " focus" : ""}`;
    element.innerHTML = `<strong>${count} אירועים</strong><span>${location.name}</span>`;
    state.markers.push(new maplibregl.Marker({ element, anchor: "center", offset: [0, -30] }).setLngLat([location.lon, location.lat]).addTo(state.map));
    bounds.extend([location.lon, location.lat]);
  });
  if (!bounds.isEmpty()) state.map.fitBounds(bounds, { padding: 110, maxZoom: 10.2, duration: 450 });
}

function renderTimeline() {
  const timeline = document.getElementById("timeline");
  if (!state.current.length) { timeline.className = "timeline empty-state"; timeline.textContent = "לא נבחרו אירועים להצגה."; return; }
  timeline.className = "timeline";
  timeline.innerHTML = [...state.current].sort((a, b) => a.date - b.date).map(event => `
    <article class="timeline-item">
      <span class="timeline-dot"></span>
      <div class="timeline-time">${event.timestamp_utc.replace("T", " ").replace("Z", "")}</div>
      <div class="timeline-title">${event.location_name} · ${event.source_type}</div>
      <div class="timeline-summary">${event.event_summary}</div>
    </article>`).join("");
}

function renderEvidence() {
  const body = document.getElementById("evidenceRows");
  if (!state.current.length && state.aggregateLocations.length) {
    body.innerHTML = state.aggregateLocations.map(item => `
      <tr><td dir="ltr">אגרגציה</td><td>קיבוץ לפי מיקום</td><td>${item.count} אירועים</td><td>${item.location_name}</td><td>${item.location_id}</td></tr>`).join("");
    return;
  }
  if (!state.current.length) { body.innerHTML = '<tr><td colspan="5" class="empty-cell">לא נבחרו אירועים להצגה.</td></tr>'; return; }
  body.innerHTML = [...state.current].sort((a, b) => a.date - b.date).map(event => `
    <tr><td dir="ltr">${event.timestamp_utc}</td><td>${event.source_type}</td><td>${event.entity_or_actor}</td><td>${event.location_name}</td><td>${event.event_summary}</td></tr>`).join("");
}

function updateContext() {
  const context = document.getElementById("contextState");
  context.innerHTML = `
    <div><dt>אזור</dt><dd>${state.region || "לא הוגדר"}</dd></div>
    <div><dt>חלון זמן</dt><dd>${state.window || "לא הוגדר"}</dd></div>
    <div><dt>גורמים במיקוד</dt><dd>${state.actors.length ? state.actors.join(" · ") : "לא הוגדרו"}</dd></div>
    <div><dt>מזהה חקירה</dt><dd dir="ltr">${state.investigationId}</dd></div>`;
}

function resetInvestigation() {
  state.current = [];
  state.stage = 0;
  state.region = null;
  state.window = null;
  state.actors = [];
  state.aggregateLocations = [];
  state.history = [];
  state.investigationId = createInvestigationId();
  state.investigationState = null;
  conversation.innerHTML = '<article class="message assistant-message"><div class="message-label">סוכן חקירה</div><p>אפשר להתחיל בשאלה פתוחה. אשתמש בכלי החיפוש, הזמן והמפה כדי לבנות תשובה שניתן לבדוק מול האירועים הגולמיים.</p></article>';
  activityList.innerHTML = "";
  activityEmpty.hidden = false;
  resultTitle.textContent = "טרם בוצעה חקירה";
  resultSubtitle.textContent = "תוצאות, המחשות וראיות יופיעו כאן לאחר השאלה הראשונה.";
  resultCount.textContent = "0 אירועים";
  activateView("map");
  setSuggestions(["האם הייתה פעילות חריגה באזור בית שאן לפני אירוע הגבול?"]);
  updateContext();
  renderAllViews();
  if (state.map) setTimeout(() => state.map.resize(), 0);
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[char]);
}

document.addEventListener("click", event => {
  const suggestion = event.target.closest("[data-prompt]");
  if (suggestion) runPrompt(suggestion.dataset.prompt);
  const viewButton = event.target.closest("[data-view]");
  if (viewButton) activateView(viewButton.dataset.view);
});

promptForm.addEventListener("submit", event => {
  event.preventDefault();
  const prompt = promptInput.value;
  promptInput.value = "";
  runPrompt(prompt);
});

promptInput.addEventListener("keydown", event => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    promptForm.requestSubmit();
  }
});

document.getElementById("resetButton").addEventListener("click", resetInvestigation);
initPanelResizers();

async function boot() {
  initMap();
  try {
    const response = await fetch("./data/events_he_expanded_5000.csv");
    if (!response.ok) throw new Error("dataset unavailable");
    state.events = parseCsv(await response.text()).map(enrich);
    document.getElementById("datasetStatus").textContent = `${state.events.length.toLocaleString("he-IL")} אירועים זמינים במאגר`;
    document.querySelector(".status-dot").classList.add("ready");
  } catch (error) {
    document.getElementById("datasetStatus").textContent = "טעינת הנתונים נכשלה";
  }
  try {
    const status = await fetch("/api/status").then(response => response.json());
    if (!status.configured) throw new Error("not configured");
    agentStatus.textContent = "Hermes + MCP מחוברים";
    agentStatus.className = "agent-live";
  } catch (error) {
    agentStatus.textContent = "מצב הדגמה מקומי";
    agentStatus.className = "agent-error";
  }
}

boot();
