const LOCATIONS = {
  "LOC-001": { name: "אזור גשר איבר", type: "מוקד ליבה", lat: 42.883, lon: 20.848 },
  "LOC-002": { name: "מבנה העירייה", type: "מוקד ליבה", lat: 42.887, lon: 20.848 },
  "LOC-003": { name: "אזור מבנה העירייה", type: "מוקד ליבה", lat: 42.908, lon: 20.822 },
  "LOC-004": { name: "הכביש לצפון מיטרוביצה", type: "ציר", lat: 42.912, lon: 20.822 },
  "LOC-005": { name: "מרכז העיירה", type: "מוקד ליבה", lat: 43.111, lon: 20.785 },
  "LOC-006": { name: "הציר לכיוון סרביה", type: "ציר", lat: 43.115, lon: 20.785 },
  "LOC-007": { name: "אזור כפרי מערבי", type: "מוקד ליבה", lat: 42.902, lon: 20.677 },
  "LOC-008": { name: "הדרך לאגם גזיבודה", type: "ציר", lat: 42.906, lon: 20.677 },
  "LOC-009": { name: "תחנת משטרה אזורית", type: "מוקד ביטחוני", lat: 42.887, lon: 20.854 },
  "LOC-010": { name: "צומת כניסה לעיירה", type: "ציר", lat: 42.908, lon: 20.828 },
  "LOC-011": { name: "כביש כפרי צפוני", type: "כפר/ציר", lat: 43.107, lon: 20.791 },
  "LOC-012": { name: "אזור מיוער סמוך לכפר", type: "כפר/שטח", lat: 42.922, lon: 20.677 },
  "LOC-013": { name: "משרד הפנים", type: "מוסד מדיני", lat: 42.675, lon: 21.154 },
  "LOC-014": { name: "מטה ממשלת קוסובו", type: "מוסד מדיני", lat: 42.651, lon: 21.16 },
  "LOC-015": { name: "אזור כללי סמוך לגבול", type: "צד סרבי", lat: 43.279, lon: 20.609 },
  "LOC-016": { name: "מרכז עירוני", type: "צד סרבי", lat: 43.136, lon: 20.509 },
  "LOC-017": { name: "משרד ממשלתי", type: "מדיני", lat: 44.812, lon: 20.455 },
  "LOC-018": { name: "בית חולים אזורי", type: "אזרחי/חירום", lat: 42.895, lon: 20.86 },
  "LOC-019": { name: "תחנת דלק מרכזית", type: "אזרחי", lat: 42.916, lon: 20.834 },
  "LOC-020": { name: "בית ספר סרבי מקומי", type: "אזרחי", lat: 43.115, lon: 20.797 },
  "LOC-021": { name: "כפר סמוך 1", type: "כפר/יישוב", lat: 42.879, lon: 20.866 },
  "LOC-022": { name: "תחנת דלק 2", type: "אזרחי", lat: 42.9, lon: 20.84 },
  "LOC-023": { name: "נקודת בידוק כללית 3", type: "מוקד ביטחוני", lat: 42.887, lon: 20.866 },
  "LOC-024": { name: "כפר סמוך 4", type: "כפר/יישוב", lat: 42.914, lon: 20.689 },
  "LOC-025": { name: "תחנת דלק 5", type: "אזרחי", lat: 42.912, lon: 20.84 },
  "LOC-026": { name: "נקודת בידוק כללית 6", type: "מוקד ביטחוני", lat: 42.899, lon: 20.866 },
  "LOC-027": { name: "תחנת דלק 7", type: "אזרחי", lat: 42.926, lon: 20.689 },
  "LOC-028": { name: "כפר סמוך 8", type: "כפר/יישוב", lat: 43.091, lon: 20.809 },
  "LOC-029": { name: "אזור תעשייה קטן 9", type: "אזרחי", lat: 42.9, lon: 20.846 },
  "LOC-030": { name: "תחנת דלק 10", type: "אזרחי", lat: 42.904, lon: 20.846 },
  "LOC-031": { name: "ציר גישה 11", type: "ציר", lat: 43.103, lon: 20.809 },
  "LOC-032": { name: "בית ספר 12", type: "אזרחי", lat: 42.895, lon: 20.872 },
  "LOC-033": { name: "כפר סמוך 13", type: "כפר/יישוב", lat: 43.111, lon: 20.809 },
  "LOC-034": { name: "אזור תעשייה קטן 14", type: "אזרחי", lat: 42.903, lon: 20.872 },
  "LOC-035": { name: "כיכר מרכזית 15", type: "אזרחי/ציבורי", lat: 43.091, lon: 20.815 },
  "LOC-036": { name: "כיכר מרכזית 16", type: "אזרחי/ציבורי", lat: 43.095, lon: 20.815 },
  "LOC-037": { name: "כפר סמוך 17", type: "כפר/יישוב", lat: 42.887, lon: 20.878 },
  "LOC-038": { name: "ציר גישה 18", type: "ציר", lat: 43.103, lon: 20.815 },
  "LOC-039": { name: "אזור תעשייה קטן 19", type: "אזרחי", lat: 42.895, lon: 20.878 },
  "LOC-040": { name: "צומת מקומי 20", type: "ציר", lat: 43.111, lon: 20.815 },
  "LOC-041": { name: "מרכז בריאות 21", type: "אזרחי/חירום", lat: 42.92, lon: 20.852 },
  "LOC-042": { name: "כיכר מרכזית 22", type: "אזרחי/ציבורי", lat: 42.879, lon: 20.884 },
  "LOC-043": { name: "צומת מקומי 23", type: "ציר", lat: 42.9, lon: 20.858 },
  "LOC-044": { name: "נקודת בידוק כללית 24", type: "מוקד ביטחוני", lat: 43.099, lon: 20.821 },
  "LOC-045": { name: "כפר סמוך 25", type: "כפר/יישוב", lat: 43.103, lon: 20.821 },
  "LOC-046": { name: "בית ספר 26", type: "אזרחי", lat: 42.895, lon: 20.884 },
  "LOC-047": { name: "תחנת דלק 27", type: "אזרחי", lat: 42.899, lon: 20.884 },
  "LOC-048": { name: "תחנת דלק 28", type: "אזרחי", lat: 43.115, lon: 20.821 },
  "LOC-049": { name: "אזור מיוער 29", type: "שטח", lat: 42.902, lon: 20.671 },
  "LOC-050": { name: "תחנת דלק 30", type: "אזרחי", lat: 42.9, lon: 20.822 },
  "LOC-051": { name: "כיכר מרכזית 31", type: "אזרחי/ציבורי", lat: 43.099, lon: 20.785 },
  "LOC-052": { name: "בית ספר 32", type: "אזרחי", lat: 42.914, lon: 20.671 },
  "LOC-053": { name: "נקודת בידוק כללית 33", type: "מוקד ביטחוני", lat: 42.912, lon: 20.822 },
  "LOC-054": { name: "ציר גישה 34", type: "ציר", lat: 42.899, lon: 20.848 },
  "LOC-055": { name: "אזור תעשייה קטן 35", type: "אזרחי", lat: 42.92, lon: 20.822 },
  "LOC-056": { name: "אזור תעשייה קטן 36", type: "אזרחי", lat: 42.902, lon: 20.677 },
  "LOC-057": { name: "נקודת בידוק כללית 37", type: "מוקד ביטחוני", lat: 42.906, lon: 20.677 },
  "LOC-058": { name: "ציר גישה 38", type: "ציר", lat: 42.887, lon: 20.854 },
  "LOC-059": { name: "בית ספר 39", type: "אזרחי", lat: 43.103, lon: 20.791 },
  "LOC-060": { name: "צומת מקומי 40", type: "ציר", lat: 42.918, lon: 20.677 },
  "LOC-061": { name: "נקודת בידוק כללית 41", type: "מוקד ביטחוני", lat: 43.111, lon: 20.791 },
  "LOC-062": { name: "מרכז בריאות 42", type: "אזרחי/חירום", lat: 42.903, lon: 20.854 },
  "LOC-063": { name: "צומת מקומי 43", type: "ציר", lat: 42.896, lon: 20.834 },
  "LOC-064": { name: "נקודת בידוק כללית 44", type: "מוקד ביטחוני", lat: 42.9, lon: 20.834 },
  "LOC-065": { name: "כיכר מרכזית 45", type: "אזרחי/ציבורי", lat: 42.887, lon: 20.86 },
  "LOC-066": { name: "ציר גישה 46", type: "ציר", lat: 42.891, lon: 20.86 },
  "LOC-067": { name: "תחנת דלק 47", type: "אזרחי", lat: 43.107, lon: 20.797 },
  "LOC-068": { name: "ציר גישה 48", type: "ציר", lat: 42.899, lon: 20.86 },
  "LOC-069": { name: "נקודת בידוק כללית 49", type: "מוקד ביטחוני", lat: 42.903, lon: 20.86 },
  "LOC-070": { name: "אזור מיוער 50", type: "שטח", lat: 42.896, lon: 20.84 },
  "LOC-071": { name: "מרכז בריאות 51", type: "אזרחי/חירום", lat: 42.9, lon: 20.84 },
  "LOC-072": { name: "תחנת דלק 52", type: "אזרחי", lat: 42.91, lon: 20.689 },
  "LOC-073": { name: "מרכז בריאות 53", type: "אזרחי/חירום", lat: 42.908, lon: 20.84 },
  "LOC-074": { name: "אזור מיוער 54", type: "שטח", lat: 43.107, lon: 20.803 },
  "LOC-075": { name: "ציר גישה 55", type: "ציר", lat: 42.922, lon: 20.689 },
  "LOC-076": { name: "בית ספר 56", type: "אזרחי", lat: 42.903, lon: 20.866 },
  "LOC-077": { name: "כיכר מרכזית 57", type: "אזרחי/ציבורי", lat: 42.896, lon: 20.846 },
  "LOC-078": { name: "כפר סמוך 58", type: "כפר/יישוב", lat: 42.883, lon: 20.872 },
  "LOC-079": { name: "בית ספר 59", type: "אזרחי", lat: 42.887, lon: 20.872 },
  "LOC-080": { name: "מרכז בריאות 60", type: "אזרחי/חירום", lat: 42.908, lon: 20.846 },
  "LOC-081": { name: "נקודת בידוק כללית 61", type: "מוקד ביטחוני", lat: 42.912, lon: 20.846 },
  "LOC-082": { name: "תחנת דלק 62", type: "אזרחי", lat: 42.922, lon: 20.695 },
  "LOC-083": { name: "תחנת דלק 63", type: "אזרחי", lat: 42.926, lon: 20.695 },
  "LOC-084": { name: "בית ספר 64", type: "אזרחי", lat: 42.902, lon: 20.701 },
  "LOC-085": { name: "כפר סמוך 65", type: "כפר/יישוב", lat: 42.906, lon: 20.701 },
  "LOC-086": { name: "כפר סמוך 66", type: "כפר/יישוב", lat: 42.887, lon: 20.878 },
  "LOC-087": { name: "ציר גישה 67", type: "ציר", lat: 43.103, lon: 20.815 },
  "LOC-088": { name: "נקודת בידוק כללית 68", type: "מוקד ביטחוני", lat: 42.912, lon: 20.852 },
  "LOC-089": { name: "צומת מקומי 69", type: "ציר", lat: 42.922, lon: 20.701 },
  "LOC-090": { name: "ציר גישה 70", type: "ציר", lat: 42.92, lon: 20.852 },
  "LOC-091": { name: "כפר סמוך 71", type: "כפר/יישוב", lat: 42.879, lon: 20.884 },
  "LOC-092": { name: "ציר גישה 72", type: "ציר", lat: 42.883, lon: 20.884 },
  "LOC-093": { name: "צומת מקומי 73", type: "ציר", lat: 42.904, lon: 20.858 },
  "LOC-094": { name: "תחנת דלק 74", type: "אזרחי", lat: 42.914, lon: 20.707 },
  "LOC-095": { name: "צומת מקומי 75", type: "ציר", lat: 42.895, lon: 20.884 },
  "LOC-096": { name: "מרכז בריאות 76", type: "אזרחי/חירום", lat: 42.922, lon: 20.707 },
  "LOC-097": { name: "מרכז בריאות 77", type: "אזרחי/חירום", lat: 42.926, lon: 20.707 },
  "LOC-098": { name: "צומת מקומי 78", type: "ציר", lat: 42.902, lon: 20.671 },
  "LOC-099": { name: "כפר סמוך 79", type: "כפר/יישוב", lat: 42.9, lon: 20.822 },
  "LOC-100": { name: "בית ספר 80", type: "אזרחי", lat: 42.887, lon: 20.848 },
  "LOC-101": { name: "נקודת בידוק כללית 81", type: "מוקד ביטחוני", lat: 42.914, lon: 20.671 },
  "LOC-102": { name: "כפר סמוך 82", type: "כפר/יישוב", lat: 42.912, lon: 20.822 },
  "LOC-103": { name: "צומת מקומי 83", type: "ציר", lat: 42.899, lon: 20.848 },
  "LOC-104": { name: "תחנת דלק 84", type: "אזרחי", lat: 42.903, lon: 20.848 },
  "LOC-105": { name: "כיכר מרכזית 85", type: "אזרחי/ציבורי", lat: 42.896, lon: 20.828 },
  "LOC-106": { name: "אזור תעשייה קטן 86", type: "אזרחי", lat: 42.883, lon: 20.854 },
  "LOC-107": { name: "מרכז בריאות 87", type: "אזרחי/חירום", lat: 43.099, lon: 20.791 },
  "LOC-108": { name: "תחנת דלק 88", type: "אזרחי", lat: 43.103, lon: 20.791 },
  "LOC-109": { name: "מרכז בריאות 89", type: "אזרחי/חירום", lat: 42.912, lon: 20.828 },
  "LOC-110": { name: "כפר סמוך 90", type: "כפר/יישוב", lat: 42.899, lon: 20.854 },
  "LOC-111": { name: "ציר גישה 91", type: "ציר", lat: 42.903, lon: 20.854 },
  "LOC-112": { name: "צומת מקומי 92", type: "ציר", lat: 43.091, lon: 20.797 },
  "LOC-113": { name: "תחנת דלק 93", type: "אזרחי", lat: 42.883, lon: 20.86 },
  "LOC-114": { name: "אזור מיוער 94", type: "שטח", lat: 42.904, lon: 20.834 },
  "LOC-115": { name: "כיכר מרכזית 95", type: "אזרחי/ציבורי", lat: 43.103, lon: 20.797 },
  "LOC-116": { name: "נקודת בידוק כללית 96", type: "מוקד ביטחוני", lat: 42.895, lon: 20.86 },
  "LOC-117": { name: "צומת מקומי 97", type: "ציר", lat: 42.899, lon: 20.86 },
  "LOC-118": { name: "נקודת בידוק כללית 98", type: "מוקד ביטחוני", lat: 42.903, lon: 20.86 },
  "LOC-119": { name: "כיכר מרכזית 99", type: "אזרחי/ציבורי", lat: 43.091, lon: 20.803 },
  "LOC-120": { name: "תחנת דלק 100", type: "אזרחי", lat: 43.095, lon: 20.803 },
  "LOC-121": { name: "נקודת בידוק כללית 101", type: "מוקד ביטחוני", lat: 43.099, lon: 20.803 },
  "LOC-122": { name: "ציר גישה 102", type: "ציר", lat: 42.891, lon: 20.866 },
  "LOC-123": { name: "כפר סמוך 103", type: "כפר/יישוב", lat: 43.107, lon: 20.803 },
  "LOC-124": { name: "מרכז בריאות 104", type: "אזרחי/חירום", lat: 42.916, lon: 20.84 },
  "LOC-125": { name: "נקודת בידוק כללית 105", type: "מוקד ביטחוני", lat: 42.926, lon: 20.689 },
  "LOC-126": { name: "ציר גישה 106", type: "ציר", lat: 42.879, lon: 20.872 },
  "LOC-127": { name: "נקודת בידוק כללית 107", type: "מוקד ביטחוני", lat: 42.9, lon: 20.846 },
  "LOC-128": { name: "כיכר מרכזית 108", type: "אזרחי/ציבורי", lat: 43.099, lon: 20.809 },
  "LOC-129": { name: "צומת מקומי 109", type: "ציר", lat: 42.914, lon: 20.695 },
  "LOC-130": { name: "כפר סמוך 110", type: "כפר/יישוב", lat: 43.107, lon: 20.809 },
  "LOC-131": { name: "תחנת דלק 111", type: "אזרחי", lat: 42.916, lon: 20.846 },
  "LOC-132": { name: "נקודת בידוק כללית 112", type: "מוקד ביטחוני", lat: 43.115, lon: 20.809 },
  "LOC-133": { name: "כיכר מרכזית 113", type: "אזרחי/ציבורי", lat: 42.902, lon: 20.701 },
  "LOC-134": { name: "צומת מקומי 114", type: "ציר", lat: 42.9, lon: 20.852 },
  "LOC-135": { name: "אזור תעשייה קטן 115", type: "אזרחי", lat: 42.904, lon: 20.852 },
  "LOC-136": { name: "אזור תעשייה קטן 116", type: "אזרחי", lat: 43.103, lon: 20.815 },
  "LOC-137": { name: "מרכז בריאות 117", type: "אזרחי/חירום", lat: 42.912, lon: 20.852 },
  "LOC-138": { name: "אזור תעשייה קטן 118", type: "אזרחי", lat: 42.899, lon: 20.878 },
  "LOC-139": { name: "תחנת דלק 119", type: "אזרחי", lat: 42.926, lon: 20.701 },
  "LOC-140": { name: "בית ספר 120", type: "אזרחי", lat: 42.902, lon: 20.707 },
  "LOC-141": { name: "תחנת דלק 121", type: "אזרחי", lat: 42.9, lon: 20.858 },
  "LOC-142": { name: "אזור תעשייה קטן 122", type: "אזרחי", lat: 42.904, lon: 20.858 },
  "LOC-143": { name: "מרכז בריאות 123", type: "אזרחי/חירום", lat: 42.891, lon: 20.884 },
  "LOC-144": { name: "נקודת בידוק כללית 124", type: "מוקד ביטחוני", lat: 42.918, lon: 20.707 },
  "LOC-145": { name: "ציר גישה 125", type: "ציר", lat: 42.899, lon: 20.884 },
  "LOC-146": { name: "צומת מקומי 126", type: "ציר", lat: 43.115, lon: 20.821 },
  "LOC-147": { name: "כפר סמוך 127", type: "כפר/יישוב", lat: 43.091, lon: 20.785 },
  "LOC-148": { name: "בית ספר 128", type: "אזרחי", lat: 42.906, lon: 20.671 },
  "LOC-149": { name: "אזור תעשייה קטן 129", type: "אזרחי", lat: 43.099, lon: 20.785 },
  "LOC-150": { name: "אזור תעשייה קטן 130", type: "אזרחי", lat: 42.891, lon: 20.848 },
  "LOC-151": { name: "משרד ההגנה האלבני", type: "מדיני", lat: 41.331, lon: 19.8 },
  "LOC-152": { name: "משרד ממשלתי", type: "מדיני", lat: 42.908, lon: 20.782 },
  "LOC-153": { name: "מטה נאט״ו", type: "מדיני", lat: 50.862, lon: 4.334 },
  "LOC-154": { name: "מרכז עירוני", type: "רעש/רקע", lat: 42.648, lon: 20.276 },
  "LOC-155": { name: "מרכז עירוני", type: "רעש/רקע", lat: 42.892, lon: 20.788 }
};

const PRIMARY_IDS = new Set([]);
const EVENT_ID_PATTERN = /\b(?:REC-\d{6}|LOC-\d{3})\b/g;

function createInvestigationId() {
  const random = crypto?.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  return `investigation-${random}`;
}

const state = {
  events: [],
  current: [],
  stage: 0,
  aggregateLocations: [],
  aggregateTimeline: [],
  aggregateGroups: [],
  locationMetadata: [],
  entityMetadata: [],
  map: null,
  mapReady: false,
  markers: [],
  history: [],
  investigationId: createInvestigationId(),
  recordedQuestions: [],
  savedQuestions: [],
  busy: false,
  activeAssistantMessage: null,
  activeActivityList: null,
  activeActivityEmpty: null,
  lastResult: null,
  lastPrompt: null,
  queryContext: null,
  layers: [],
  activeLayerId: null,
  rawOverlayMinimized: false,
  rawOverlayHeight: 28,
  queryEdited: false,
  originalQuery: null
};

const conversation = document.getElementById("conversation");
const suggestions = document.getElementById("suggestions");
const promptForm = document.getElementById("promptForm");
const promptInput = document.getElementById("promptInput");
const resultTitle = document.getElementById("resultTitle");
const resultSubtitle = document.getElementById("resultSubtitle");
const resultCount = document.getElementById("resultCount");
const sendButton = document.getElementById("sendButton");
const saveQuestionButton = document.getElementById("saveQuestionButton");
const recordedButton = document.getElementById("recordedButton");
const recordedModal = document.getElementById("recordedModal");
const recordedClose = document.getElementById("recordedClose");
const recordedList = document.getElementById("recordedList");
const agentStatus = document.getElementById("agentStatus");
const viewRecommendation = document.getElementById("viewRecommendation");
const workspace = document.querySelector(".workspace");
const queryLayerName = document.getElementById("queryLayerName");
const queryToolName = document.getElementById("queryToolName");
const queryModal = document.getElementById("queryModal");
const queryModalTitle = document.getElementById("queryModalTitle");
const queryModalBody = document.getElementById("queryModalBody");
const queryModalClose = document.getElementById("queryModalClose");

const VIEW_LABELS = {
  map: "מפה",
  timeline: "ציר זמן",
  evidence: "אירועים גולמיים"
};

const LAYER_QUERY_LABELS = {
  map: "שכבת אירועים גולמיים",
  timeline: "שכבת אירועים גולמיים",
  evidence: "שכבת אירועים גולמיים"
};

const LAYER_COLORS = [
  "#8ab4f8",
  "#81c995",
  "#f28b82",
  "#fdd663",
  "#c58af9",
  "#78d9ec",
  "#ff9f80",
  "#b3d46f",
  "#f78fb3",
  "#a7b7ff",
  "#c9ab76",
  "#7fd1ae"
];

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
      const hasKnownLocation = Boolean(LOCATIONS[locationId]);
      const hasCoordinates = item.latitude !== undefined && item.latitude !== null && item.longitude !== undefined && item.longitude !== null;
      if (!hasKnownLocation && !hasCoordinates) return;
      const existing = byLocation.get(locationId);
      const count = Number(item.count || 0);
      if (!existing || count > existing.count) {
        byLocation.set(locationId, {
          location_id: locationId,
          location_name: item.location_name || item.municipality || (LOCATIONS[locationId] && LOCATIONS[locationId].name) || locationId,
          latitude: hasCoordinates ? Number(item.latitude) : undefined,
          longitude: hasCoordinates ? Number(item.longitude) : undefined,
          count
        });
      }
    });
  });
  let locations = [...byLocation.values()].sort((a, b) => b.count - a.count);
  const idsInAnswer = new Set((result.answer || "").match(/\bLOC-\d{3}\b/g) || []);
  if (idsInAnswer.size) {
    locations = locations.filter(item => idsInAnswer.has(item.location_id) || !String(item.location_id || "").match(/^LOC-\d{3}$/));
  }
  return locations;
}

function parseAggregateGroupsFromText(text) {
  const match = String(text || "").match(/קבוצות:\s*(.+?)(?:\.|$)/);
  if (!match) return [];
  return match[1].split(",").map(part => {
    const item = part.trim();
    const separator = item.lastIndexOf("=");
    if (separator === -1) return null;
    const label = item.slice(0, separator).trim();
    const count = Number(item.slice(separator + 1).trim());
    if (!label || !Number.isFinite(count)) return null;
    return { label, count };
  }).filter(Boolean);
}

function collectAggregateTimeline(result) {
  const items = [];
  (result.investigation_steps || []).forEach(step => {
    if (step.tool !== "aggregate_events") return;
    const groupBy = step.technical?.arguments?.group_by;
    if (!["date", "hour"].includes(groupBy)) return;
    const groups = step.aggregate_groups || parseAggregateGroupsFromText(step.result);
    groups.forEach(group => {
      const label = group.label || group.key;
      const count = Number(group.count || 0);
      if (!label || !Number.isFinite(count)) return;
      let sortKey = label;
      let timeLabel = label;
      if (groupBy === "date") {
        sortKey = `${label}T00:00:00Z`;
        timeLabel = label;
      } else if (groupBy === "hour") {
        const hour = String(label).match(/\d{1,2}/)?.[0] || "0";
        sortKey = Number(hour);
        timeLabel = `${String(hour).padStart(2, "0")}:00`;
      }
      items.push({
        group_by: groupBy,
        label,
        timeLabel,
        count,
        sortKey,
        summary: `${count.toLocaleString("he-IL")} אירועים בקבוצת ${label}`
      });
    });
  });
  const priority = items.some(item => item.group_by === "date") ? "date" : "hour";
  return items
    .filter(item => item.group_by === priority)
    .sort((a, b) => a.sortKey > b.sortKey ? 1 : a.sortKey < b.sortKey ? -1 : 0);
}

function collectGenericAggregateGroups(result) {
  const items = [];
  (result.investigation_steps || []).forEach(step => {
    const groupBy = step.technical?.arguments?.group_by || step.aggregate_groups?.[0]?.group_by;
    if (!step.aggregate_groups?.length || ["date", "hour", "location", "municipality"].includes(groupBy)) return;
    step.aggregate_groups.forEach(group => {
      items.push({
        group_by: group.group_by || groupBy,
        key: group.key,
        label: group.label || group.key,
        count: Number(group.count || 0),
        first_event_id: group.first_event_id,
        first_event_time: group.first_event_time,
        last_event_id: group.last_event_id,
        last_event_time: group.last_event_time
      });
    });
  });
  return items.sort((a, b) => b.count - a.count);
}

function collectLocationMetadata(result) {
  const byId = new Map();
  (result.investigation_steps || []).forEach(step => {
    (step.location_layers || []).forEach(item => {
      const locationId = item.location_id;
      if (!locationId) return;
      const existing = byId.get(locationId);
      const count = Number(item.event_count ?? item.count ?? 0);
      if (!existing || count > Number(existing.event_count ?? existing.count ?? 0)) {
        byId.set(locationId, { ...item, event_count: count });
      }
    });
  });
  return [...byId.values()].sort((a, b) => Number(b.event_count || 0) - Number(a.event_count || 0));
}

function collectEntityMetadata(result) {
  const byId = new Map();
  (result.investigation_steps || []).forEach(step => {
    (step.entity_layers || []).forEach(item => {
      const entityId = item.entity_id;
      if (!entityId) return;
      const existing = byId.get(entityId);
      const count = Number(item.event_count ?? item.count ?? 0);
      if (!existing || count > Number(existing.event_count ?? existing.count ?? 0)) {
        byId.set(entityId, { ...item, event_count: count });
      }
    });
  });
  return [...byId.values()].sort((a, b) => Number(b.event_count || 0) - Number(a.event_count || 0));
}

function layerId(kind, label) {
  return `${kind}:${String(label || "unknown").replace(/\s+/g, "-")}`;
}

function buildEventLayers(events) {
  const grouped = new Map();
  [...events].sort((a, b) => a.date - b.date).forEach(event => {
    const label = event.source_type || "מקור לא ידוע";
    if (!grouped.has(label)) grouped.set(label, []);
    grouped.get(label).push(event);
  });
  return [...grouped.entries()]
    .sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0], "he"))
    .map(([label, items]) => ({
      dataId: layerId("events", label),
      label,
      kind: "events",
      visible: true,
      items,
      capabilities: { table: true, map: true, timeline: true }
    }));
}

function buildLocationLayer(locations) {
  if (!locations.length) return null;
  const layerKey = locations
    .map(item => item.location_id || item.location_name || item.label || item.key)
    .filter(Boolean)
    .slice(0, 8)
    .join("-");
  return {
    dataId: layerId("locations", layerKey || "summary"),
    label: "ריכוזי מיקומים",
    kind: "locations",
    visible: true,
    items: locations,
    capabilities: { table: true, map: true, timeline: false }
  };
}

function buildTimeAggregationLayer(items) {
  if (!items.length) return null;
  return {
    dataId: "aggregations:time",
    label: items[0]?.group_by === "hour" ? "סיכום לפי שעה" : "סיכום לפי תאריך",
    kind: "time_aggregation",
    visible: true,
    items,
    capabilities: { table: true, map: false, timeline: true }
  };
}

function buildGroupAggregationLayer(items) {
  if (!items.length) return null;
  const groupBy = items[0]?.group_by || "group";
  return {
    dataId: layerId("aggregations", groupBy),
    label: `סיכום לפי ${groupBy}`,
    kind: "group_aggregation",
    visible: true,
    items,
    capabilities: { table: true, map: false, timeline: false }
  };
}

function buildLocationMetadataLayer(items) {
  if (!items.length) return null;
  return {
    dataId: layerId("location-metadata", items.map(item => item.location_id).slice(0, 8).join("-")),
    label: "שכבת מיקומים",
    kind: "location_metadata",
    visible: true,
    items,
    capabilities: { table: true, map: true, timeline: false }
  };
}

function buildEntityMetadataLayer(items) {
  if (!items.length) return null;
  return {
    dataId: layerId("entity-metadata", items.map(item => item.entity_id).slice(0, 8).join("-")),
    label: "שכבת ישויות",
    kind: "entity_metadata",
    visible: true,
    items,
    capabilities: { table: true, map: true, timeline: false }
  };
}

function buildResultLayers({ events = [], locations = [], timeline = [], groups = [], locationMetadata = [], entityMetadata = [] } = {}) {
  return [
    ...buildEventLayers(events),
    buildLocationLayer(locations),
    buildTimeAggregationLayer(timeline),
    buildGroupAggregationLayer(groups),
    buildLocationMetadataLayer(locationMetadata),
    buildEntityMetadataLayer(entityMetadata)
  ].filter(Boolean);
}

function sanitizeLayerKey(value) {
  return String(value || "unknown").replace(/[^\p{L}\p{N}_:-]+/gu, "-");
}

function usedLayerColors() {
  return new Set(state.layers.map(layer => layer.color).filter(Boolean));
}

function nextLayerColor() {
  const used = usedLayerColors();
  return LAYER_COLORS.find(color => !used.has(color)) || LAYER_COLORS[state.layers.length % LAYER_COLORS.length];
}

function ensureActiveLayer() {
  const activeStillExists = state.layers.some(layer => layer.id === state.activeLayerId);
  if (!activeStillExists) {
    state.activeLayerId = state.layers.find(layer => layer.capabilities.table && layer.visible)?.id
      || state.layers.find(layer => layer.capabilities.table)?.id
      || null;
  }
  if (!state.layers.some(layer => layer.id === state.activeLayerId && layer.visible && layer.capabilities.table)) {
    state.activeLayerId = state.layers.find(layer => layer.capabilities.table && layer.visible)?.id
      || state.layers.find(layer => layer.capabilities.table)?.id
      || null;
  }
}

function addResultLayers({ sourceId, sourceLabel, preferredView = "map", layers = [] }) {
  const cleanSourceId = sanitizeLayerKey(sourceId);
  const existingSourceLayers = state.layers.filter(layer => layer.sourceId === cleanSourceId);
  const added = [];

  if (existingSourceLayers.length) {
    existingSourceLayers.forEach(layer => { layer.visible = true; });
  }

  layers.forEach(layer => {
    const dataId = layer.dataId || layer.id || layerId(layer.kind, layer.label);
    const id = `${cleanSourceId}::${sanitizeLayerKey(dataId)}`;
    const existing = state.layers.find(item => item.id === id);
    if (existing) {
      existing.visible = true;
      added.push(existing);
      return;
    }
    const next = {
      ...layer,
      id,
      dataId,
      sourceId: cleanSourceId,
      sourceLabel,
      preferredView,
      color: nextLayerColor(),
      visible: true
    };
    state.layers.push(next);
    added.push(next);
  });

  const preferredLayer = added.find(layer => layer.capabilities.table)
    || existingSourceLayers.find(layer => layer.capabilities.table)
    || state.layers.find(layer => layer.capabilities.table);
  if (preferredLayer) state.activeLayerId = preferredLayer.id;
  ensureActiveLayer();
  return added;
}

function resultSourceBase(result = {}) {
  return sanitizeLayerKey(result.run_id || result.recorded_id || result.source_run_id || state.investigationId || "current");
}

function finalSourceId(result = {}) {
  return `msg:${resultSourceBase(result)}:final`;
}

function stepSourceId(resultOrBase = {}, stepNumber = 0) {
  const base = typeof resultOrBase === "string" ? sanitizeLayerKey(resultOrBase) : resultSourceBase(resultOrBase);
  return `msg:${base}:step:${stepNumber || "unknown"}`;
}

function layerColorStyle(layer) {
  return `--layer-color:${escapeHtml(layer?.color || "#8ab4f8")}`;
}

function visibleLayers(capability = null) {
  return state.layers.filter(layer => layer.visible && (!capability || layer.capabilities[capability]));
}

function activeTableLayer() {
  return state.layers.find(layer => layer.id === state.activeLayerId && layer.capabilities.table)
    || state.layers.find(layer => layer.capabilities.table)
    || null;
}

function visibleEventItems() {
  return visibleLayers("timeline")
    .filter(layer => layer.kind === "events")
    .flatMap(layer => layer.items);
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
    center: [20.82, 42.92],
    zoom: 8.4,
    minZoom: 6.0,
    maxZoom: 15,
    maxBounds: [[19.0, 41.0], [22.2, 44.0]],
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
  return article;
}

function startAssistantResearchMessage(message = "Hermes מנתח את הבקשה ומפעיל כלי חקירה...") {
  const article = document.createElement("article");
  article.className = "message assistant-message";
  article.innerHTML = `
    <div class="message-label">סוכן חקירה</div>
    <section class="research-process research-process-live">
      <h3>תהליך המחקר</h3>
      <div class="activity-empty">${escapeHtml(message)}</div>
      <ol class="activity-list"></ol>
    </section>`;
  conversation.appendChild(article);
  state.activeAssistantMessage = article;
  state.activeActivityEmpty = article.querySelector(".activity-empty");
  state.activeActivityList = article.querySelector(".activity-list");
  return article;
}

function ensureAssistantResearchMessage(message) {
  if (!state.activeAssistantMessage || !state.activeActivityList || !state.activeActivityEmpty) {
    startAssistantResearchMessage(message);
  }
}

function setActiveResearchMessage(message) {
  ensureAssistantResearchMessage(message);
  state.activeActivityList.innerHTML = "";
  state.activeActivityEmpty.hidden = false;
  state.activeActivityEmpty.textContent = message;
}

function finalizeAssistantMessage(answer, options = {}) {
  ensureAssistantResearchMessage();
  const article = state.activeAssistantMessage;
  const existingList = state.activeActivityList;
  const stepsCount = existingList ? existingList.children.length : 0;
  const research = article.querySelector(".research-process");
  const details = document.createElement("details");
  details.className = "research-steps-toggle";
  details.innerHTML = `<summary>תהליך המחקר${stepsCount ? ` · ${stepsCount} צעדים` : ""}</summary>`;
  if (existingList && stepsCount) {
    details.appendChild(existingList);
  } else {
    const empty = document.createElement("div");
    empty.className = "activity-empty";
    empty.textContent = "לא התקבל פירוט צעדי מחקר.";
    details.appendChild(empty);
  }
  if (research) research.replaceWith(details);
  const answerBody = document.createElement("div");
  answerBody.className = "answer-body";
  answerBody.innerHTML = options.html ? answer : answerHtml(answer);
  article.appendChild(answerBody);
  if (options.result) {
    const actions = document.createElement("div");
    actions.className = "final-answer-actions";
    actions.innerHTML = `<button type="button" class="final-answer-show-btn">הצג תוצאות</button>`;
    actions.querySelector(".final-answer-show-btn").addEventListener("click", () => {
      showFinalAnswerResult(options.result, options.prompt || "");
    });
    const evidenceToggle = answerBody.querySelector(".evidence-ids-toggle");
    if (evidenceToggle) {
      answerBody.insertBefore(actions, evidenceToggle);
    } else {
      answerBody.appendChild(actions);
    }
  }
  state.activeAssistantMessage = null;
  state.activeActivityList = null;
  state.activeActivityEmpty = null;
  updateSaveQuestionButton();
}

function showFinalAnswerResult(result, prompt) {
  if (!result) return;
  applyHermesResult(result, prompt, { keepRenderedSteps: true, restoreOnly: true });
}

const TOOL_LABELS = {
  classify_question_intent: "סיווג כוונת השאלה",
  resolve_location: "הבנת המקום",
  resolve_event_reference: "זיהוי אירוע העוגן",
  search_events: "חיפוש ממוקד במאגר",
  get_objects: "שליפת אובייקטים",
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

function compactArguments(argumentsPayload) {
  const payload = argumentsPayload || {};
  return Object.fromEntries(Object.entries(payload).filter(([key]) => key !== "step_bridge"));
}

function layerFromStep(step, fallback = "evidence") {
  const groupBy = step?.technical?.arguments?.group_by;
  if (step?.map_locations?.length || step?.location_layers?.length || step?.entity_layers?.length || ["location", "municipality"].includes(groupBy)) return "map";
  const aggregateGroupBy = step?.aggregate_groups?.[0]?.group_by || groupBy;
  if ((step?.aggregate_groups?.length && ["date", "hour"].includes(aggregateGroupBy)) || ["date", "hour"].includes(groupBy)) return "timeline";
  if (step?.event_ids?.length) return "evidence";
  return fallback;
}

function pickLayerStep(layer, result) {
  const steps = result?.investigation_steps || [];
  const ordered = [...steps].reverse();
  if (layer === "map") {
    return ordered.find(step => layerFromStep(step) === "map") || null;
  }
  if (layer === "timeline") {
    return ordered.find(step => layerFromStep(step) === "timeline") || null;
  }
  return ordered.find(step => step.event_ids?.length || step.technical?.arguments) || null;
}

function buildFinalQueryContext(result, prompt) {
  const inferred = inferRecommendedView(prompt, result?.answer || "");
  return {
    mode: "final",
    prompt: prompt || result?.question || "",
    result,
    preferredLayer: result?.recommended_view || inferred.view
  };
}

function buildStepQueryContext(step, label) {
  return {
    mode: "step",
    label,
    step,
    preferredLayer: layerFromStep(step)
  };
}

function activeLayer() {
  const layer = document.querySelector(".view-tab.active")?.dataset.view || "map";
  return layer === "evidence" ? "map" : layer;
}

function queryReadoutForLayer(layer) {
  if (!state.queryContext) {
    return {
      tool: "אין שאילתה פעילה",
      text: "",
      available: false
    };
  }

  if (state.queryContext.mode === "step") {
    const step = state.queryContext.step || {};
    const payload = {
      layer,
      tool: step.tool || state.queryContext.label,
      arguments: compactArguments(step.technical?.arguments)
    };
    return { tool: step.tool || state.queryContext.label, text: JSON.stringify(payload, null, 2), available: true };
  }

  const result = state.queryContext.result || {};
  const step = pickLayerStep(layer, result);
  const payload = {
    layer,
    source: step ? "agent_tool" : "final_answer",
    analyst_question: state.queryContext.prompt,
    tool: step?.tool || "final_answer",
    arguments: compactArguments(step?.technical?.arguments),
    recommended_view: result.recommended_view || state.queryContext.preferredLayer,
    view_reason: result.view_reason || ""
  };
  return { tool: step?.tool || "final_answer", text: JSON.stringify(payload, null, 2), available: true };
}

function renderQueryInspector() {
  const button = document.getElementById("queryToolName");
  if (!button) return;
  const layer = activeLayer();
  if (queryLayerName) queryLayerName.textContent = LAYER_QUERY_LABELS[layer] || "שכבת אירועים גולמיים";
  const readout = queryReadoutForLayer(layer);
  button.textContent = readout.tool;
  button.disabled = !readout.available;
  button.dataset.queryDetails = readout.text || "";
}

function openQueryModal(trigger = null) {
  const button = trigger || document.getElementById("queryToolName");
  if (!queryModal || !button || button.disabled) return;

  let queryObj = {};
  try { queryObj = JSON.parse(button.dataset.queryDetails || "{}"); } catch (e) {}

  state.originalQuery = JSON.stringify(queryObj.arguments || {}, null, 2);
  state.queryEdited = false;

  document.getElementById("queryFormTool").textContent = queryObj.tool || button.textContent || "";
  const layerSelect = document.getElementById("queryFormLayer");
  if (layerSelect) layerSelect.value = queryObj.layer || "map";
  const argsArea = document.getElementById("queryFormArguments");
  if (argsArea) argsArea.value = JSON.stringify(queryObj.arguments || {}, null, 2);
  const runBtn = document.getElementById("queryFormRunButton");
  if (runBtn) runBtn.disabled = true;

  queryModal.hidden = false;
  attachQueryFormListeners();
}

function attachQueryFormListeners() {
  const form = document.getElementById("queryForm");
  if (!form || form.dataset.listenersAttached) return;
  form.querySelectorAll("select, textarea").forEach(input => {
    input.addEventListener("input", detectQueryEdits);
    input.addEventListener("change", detectQueryEdits);
  });
  form.dataset.listenersAttached = "1";
}

function detectQueryEdits() {
  const argsArea = document.getElementById("queryFormArguments");
  const currentArgs = argsArea ? argsArea.value : "";
  state.queryEdited = currentArgs !== state.originalQuery;
  const runBtn = document.getElementById("queryFormRunButton");
  if (runBtn) runBtn.disabled = !state.queryEdited;
}

function handleQueryFormSubmit() {
  const tool = document.getElementById("queryFormTool")?.textContent || "";
  const layer = document.getElementById("queryFormLayer")?.value || "map";
  let args = {};
  try { args = JSON.parse(document.getElementById("queryFormArguments")?.value || "{}"); } catch (e) {}
  console.log("Query form submitted (Phase 2 will implement execution):", { tool, layer, arguments: args });
}

function closeQueryModal() {
  if (queryModal) queryModal.hidden = true;
}

function stepQueryDetails(step, label) {
  return {
    source: "investigation_step",
    description: label,
    tool: step.tool || label,
    layer: layerFromStep(step),
    arguments: compactArguments(step.technical?.arguments),
    event_ids: (step.event_ids || []).slice(0, 100),
    map_locations: (step.map_locations || []).slice(0, 50),
    aggregate_groups: (step.aggregate_groups || []).slice(0, 50),
    location_layers: (step.location_layers || []).slice(0, 50),
    entity_layers: (step.entity_layers || []).slice(0, 50),
    result: step.result || "",
    observed_clue: step.observed_clue || "",
    decision: step.decision || step.rationale || ""
  };
}

function showStepResult(step) {
  const eventIds = step.event_ids || [];
  const mapLocations = step.map_locations || [];
  const aggregateGroups = step.aggregate_groups || [];
  const locationMetadata = step.location_layers || [];
  const entityMetadata = step.entity_layers || [];
  const label = humanToolLabel(String(step.tool || "").replace(/^\d+\.\s*/, ""));
  state.queryContext = buildStepQueryContext(step, label);

  // Build a synthetic result object compatible with applyHermesResult's visualization path
  const evidence = new Set(eventIds);
  state.current = state.events.filter(event => evidence.has(event.event_id));

  if (mapLocations.length) {
    state.aggregateLocations = mapLocations.filter(item => {
      const hasKnown = Boolean(LOCATIONS[item.location_id]);
      const hasCoords = item.latitude != null && item.longitude != null;
      return hasKnown || hasCoords;
    });
  } else {
    state.aggregateLocations = [];
  }

  if (aggregateGroups.length) {
    const stepGroupBy = step.technical?.arguments?.group_by;
    const timelineGroups = aggregateGroups.filter(group => ["date", "hour"].includes(group.group_by || stepGroupBy));
    const genericGroups = aggregateGroups.filter(group => !["date", "hour", "location", "municipality"].includes(group.group_by || stepGroupBy));
    state.aggregateTimeline = timelineGroups.map(group => ({
      group_by: group.group_by || stepGroupBy || "date",
      label: group.label || group.key,
      timeLabel: group.label || group.key,
      count: Number(group.count || 0),
      sortKey: group.key || group.label,
      summary: `${Number(group.count || 0).toLocaleString("he-IL")} אירועים`
    }));
    state.aggregateGroups = genericGroups;
  } else {
    state.aggregateTimeline = [];
    state.aggregateGroups = [];
  }
  state.locationMetadata = locationMetadata;
  state.entityMetadata = entityMetadata;

  const hasData = state.current.length || state.aggregateLocations.length || state.aggregateTimeline.length || state.aggregateGroups.length || state.locationMetadata.length || state.entityMetadata.length;
  const candidateLayers = buildResultLayers({
    events: state.current,
    locations: state.aggregateLocations,
    timeline: state.aggregateTimeline,
    groups: state.aggregateGroups,
    locationMetadata: state.locationMetadata,
    entityMetadata: state.entityMetadata
  });
  const addedLayers = addResultLayers({
    sourceId: resolvedStepSourceId(step),
    sourceLabel: step.__sourceLabel || `צעד ${step.__stepNumber || ""}: ${label}`.trim(),
    preferredView: layerFromStep(step),
    layers: candidateLayers
  });
  const preferredStepLayer =
    addedLayers.find(layer => state.aggregateLocations.length && layer.kind === "locations")
    || addedLayers.find(layer => state.locationMetadata.length && layer.kind === "location_metadata")
    || addedLayers.find(layer => state.entityMetadata.length && layer.kind === "entity_metadata")
    || addedLayers.find(layer => state.aggregateTimeline.length && layer.kind === "time_aggregation")
    || addedLayers.find(layer => state.aggregateGroups.length && layer.kind === "group_aggregation")
    || addedLayers.find(layer => state.current.length && layer.kind === "events")
    || addedLayers.find(layer => layer.capabilities.table);
  if (preferredStepLayer) state.activeLayerId = preferredStepLayer.id;
  showResult(
    `צעד: ${label}`,
    hasData
      ? `נוספו או הוצגו ${addedLayers.length.toLocaleString("he-IL")} שכבות מהצעד הזה.`
      : "הצעד הזה לא החזיר נתונים שניתן להציג בתצוגה."
  );

  if (state.aggregateTimeline.length) {
    activateView("timeline", { automatic: true, reason: "צעד עם נתוני זמן" });
  } else if (state.aggregateLocations.length || state.locationMetadata.length || state.entityMetadata.length || state.current.some(e => e.location_id)) {
    activateView("map", { automatic: true, reason: "צעד עם נתוני מיקום" });
  } else {
    activateView("map", { automatic: true, reason: "צעד עם רשומות" });
  }

  updateStepVisibilityButtons();
}

function updateSourceVisibilityBtn(btn) {
  const sourceId = btn.dataset.sourceId;
  const sourceLayers = state.layers.filter(layer => layer.sourceId === sourceId);
  const anyVisible = sourceLayers.some(layer => layer.visible);
  btn.classList.toggle("layers-hidden", !anyVisible);
  const icon = btn.querySelector(".visibility-eye-icon");
  if (icon) icon.classList.toggle("off", !anyVisible);
  const label = btn.querySelector(".step-visibility-label");
  const actionLabel = label
    ? (anyVisible ? "הסתר תוצאות" : "הצג תוצאות")
    : (anyVisible ? "הסתר שכבות" : "הצג שכבות");
  btn.title = actionLabel;
  btn.setAttribute("aria-label", actionLabel);
  btn.setAttribute("aria-pressed", anyVisible ? "true" : "false");
  if (label) label.textContent = actionLabel;
}

function updateStepVisibilityButtons() {
  document.querySelectorAll(".step-visibility-btn").forEach(updateSourceVisibilityBtn);
}

function resolvedStepSourceId(step) {
  // After investigation completes, state.lastResult has the authoritative run_id.
  // Prefer re-deriving from lastResult to avoid stale investigationId-based sourceIds.
  if (state.lastResult && step.__stepNumber) {
    return sanitizeLayerKey(stepSourceId(state.lastResult, step.__stepNumber));
  }
  return sanitizeLayerKey(step.__sourceId || stepSourceId(state.lastResult || state.investigationId, step.__stepNumber));
}

function toggleStepVisibility(step, btn) {
  const sourceId = resolvedStepSourceId(step);
  const sourceLayers = state.layers.filter(layer => layer.sourceId === sourceId);
  const anyVisible = sourceLayers.some(layer => layer.visible);
  if (!sourceLayers.length || !anyVisible) {
    showStepResult(step);
    return;
  }
  sourceLayers.forEach(layer => { layer.visible = false; });
  updateSourceVisibilityBtn(btn);
  renderAllViews();
}

function addActivity(tool, detail, result, options = {}) {
  ensureAssistantResearchMessage();
  state.activeActivityEmpty.hidden = true;
  const item = document.createElement("li");
  item.className = "activity-item";
  const stepNumber = options.stepNumber || state.activeActivityList.children.length + 1;
  const cleanTool = String(tool || "").replace(/^\d+\.\s*/, "");
  const bridgeSummary = options.bridgeSummary || options.rationale || "הסוכן ממשיך לצעד זה כדי לצמצם את השאלה לפי ההקשר שנאסף עד עכשיו.";
  const baseStepData = options.stepData || {
    tool: cleanTool,
    action: detail,
    result,
    technical: options.technical || { tool: cleanTool, arguments: {} }
  };
  const stepData = {
    ...baseStepData,
    __sourceId: options.sourceId || baseStepData.__sourceId || stepSourceId(state.lastResult || state.investigationId, stepNumber),
    __sourceLabel: options.sourceLabel || baseStepData.__sourceLabel || `צעד ${stepNumber}: ${humanToolLabel(cleanTool)}`,
    __stepNumber: stepNumber
  };
  const hasStepData = Boolean(stepData);
  const sourceId = sanitizeLayerKey(stepData.__sourceId);
  const label = humanToolLabel(cleanTool);
  const queryDetails = stepQueryDetails(stepData, label);
  item.innerHTML = `
    <div class="activity-card-header">
      <span class="activity-step-number">${stepNumber}</span>
      <div class="activity-card-title">
        <strong>${escapeHtml(label)}</strong>
        <span class="activity-tool">${escapeHtml(cleanTool)}</span>
      </div>
      <div class="activity-card-actions">
        <span class="activity-status ${options.isError ? "error" : "success"}">${options.isError ? "נכשל" : "הושלם"}</span>
      </div>
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
    ${hasStepData ? `
      <div class="activity-step-actions">
        <button type="button" class="step-visibility-btn layers-hidden" data-source-id="${escapeHtml(sourceId)}" title="הצג תוצאות" aria-label="הצג תוצאות" aria-pressed="false">
          <span class="step-visibility-label">הצג תוצאות</span>
        </button>
        <button type="button" class="step-query-btn" title="הצג שאילתה">הצג שאילתה</button>
      </div>` : ""}`;
  if (hasStepData) {
    const visibilityBtn = item.querySelector(".step-visibility-btn");
    visibilityBtn.addEventListener("click", event => {
      event.stopPropagation();
      toggleStepVisibility(stepData, visibilityBtn);
    });
    const queryBtn = item.querySelector(".step-query-btn");
    queryBtn.dataset.queryDetails = JSON.stringify(queryDetails, null, 2);
    queryBtn.addEventListener("click", () => openQueryModal(queryBtn));
    updateSourceVisibilityBtn(visibilityBtn);
  }
  state.activeActivityList.appendChild(item);
}

function setSuggestions(items) {
  suggestions.innerHTML = items.map(item => `<button type="button" data-prompt="${item}">${item}</button>`).join("");
}

function eventText(event) {
  return `${event.event_summary} ${event.entity_name || event.entity_id || ""} ${event.location_name}`;
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

function renderActivitySteps(steps, sourceBase = null) {
  ensureAssistantResearchMessage();
  state.activeActivityList.innerHTML = "";
  (steps || []).forEach((step, index) => {
    const explanation = step.model_explanation || {};
    const number = index + 1;
    addActivity(step.tool, step.action, step.result, {
      stepNumber: number,
      bridgeSummary: explanation.bridge_summary || step.bridge_summary,
      rationale: explanation.decision || step.rationale || step.decision,
      technical: step.technical,
      isError: step.technical?.is_error,
      stepData: step,
      sourceId: stepSourceId(sourceBase || state.lastResult || state.investigationId, number),
      sourceLabel: `צעד ${number}: ${humanToolLabel(step.tool)}`
    });
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function canSaveCurrentResult() {
  return Boolean(
    state.lastPrompt
    && state.lastResult
    && state.lastResult.answer
    && !state.lastResult.demo_replay
    && !state.lastResult.recorded_id
    && !state.lastResult.saved_question_id
  );
}

function updateSaveQuestionButton() {
  if (!saveQuestionButton) return;
  saveQuestionButton.disabled = state.busy || !canSaveCurrentResult();
  saveQuestionButton.textContent = "שמור";
  saveQuestionButton.title = "שמור את תוצאת החקירה";
}

function formatSavedTime(value) {
  if (!value) return "זמן שמירה לא ידוע";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString("he-IL", {
    dateStyle: "short",
    timeStyle: "short",
  });
}

async function saveCurrentQuestion() {
  if (!canSaveCurrentResult() || state.busy) return;
  saveQuestionButton.disabled = true;
  saveQuestionButton.textContent = "שומר...";
  try {
    const title = state.lastPrompt.trim().slice(0, 60);
    const response = await fetch("/api/saved-question", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify({
        title,
        question: state.lastPrompt,
        result: state.lastResult,
      }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "שמירת השאלה נכשלה");
    state.lastResult = { ...state.lastResult, saved_question_id: payload.id };
    saveQuestionButton.textContent = "נשמר";
  } catch (error) {
    saveQuestionButton.textContent = "נכשל";
    saveQuestionButton.title = error.message;
  } finally {
    setTimeout(updateSaveQuestionButton, 1400);
  }
}

async function deleteSavedQuestion(savedId) {
  if (!savedId || state.busy) return;
  try {
    const response = await fetch(`/api/saved-question?id=${encodeURIComponent(savedId)}`, { method: "DELETE" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "מחיקת השאלה נכשלה");
    state.savedQuestions = state.savedQuestions.filter(item => item.id !== savedId);
    loadRecordedQuestions();
  } catch (error) {
    recordedList.innerHTML = `<div class="activity-empty">מחיקת השאלה השמורה נכשלה: ${escapeHtml(error.message)}</div>`;
  }
}

function applyHermesResult(result, prompt, options = {}) {
  result.answer = cleanAssistantAnswer(result.answer);
  // Save last result so the step-view return button can restore it
  if (!options.restoreOnly) {
    // Reconcile sourceIds: live-poll layers were keyed with investigationId;
    // final result has run_id. Rekey so buttons match after renderActivitySteps.
    if (result.run_id && state.investigationId && result.run_id !== state.investigationId) {
      const oldBase = sanitizeLayerKey(state.investigationId);
      const newBase = sanitizeLayerKey(result.run_id);
      state.layers.forEach(layer => {
        if (layer.sourceId && layer.sourceId.includes(oldBase)) {
          layer.sourceId = layer.sourceId.replace(oldBase, newBase);
          if (layer.id && layer.id.includes(oldBase)) {
            layer.id = layer.id.replace(oldBase, newBase);
          }
        }
      });
    }
    state.lastResult = result;
    state.lastPrompt = prompt;
    state.rawOverlayMinimized = false;
    state.rawOverlayHeight = 28;
    updateSaveQuestionButton();
  }

  if (options.restoreOnly) {
    state.queryContext = buildFinalQueryContext(result, prompt);
    const idsFromAnswer = (result.answer || "").match(EVENT_ID_PATTERN) || [];
    const evidence = new Set([...(result.event_ids || []), ...idsFromAnswer]);
    state.current = state.events.filter(event => evidence.has(event.event_id));
    state.aggregateLocations = collectAggregateLocations(result);
    state.aggregateTimeline = collectAggregateTimeline(result);
    state.aggregateGroups = collectGenericAggregateGroups(result);
    state.locationMetadata = collectLocationMetadata(result);
    state.entityMetadata = collectEntityMetadata(result);
    const addedLayers = addResultLayers({
      sourceId: finalSourceId(result),
      sourceLabel: "תשובת הסוכן",
      preferredView: result.recommended_view || inferRecommendedView(prompt, result.answer).view,
      layers: buildResultLayers({
      events: state.current,
      locations: state.aggregateLocations,
      timeline: state.aggregateTimeline,
      groups: state.aggregateGroups,
      locationMetadata: state.locationMetadata,
      entityMetadata: state.entityMetadata
      })
    });
    // Just restore visualization state, don't touch the chat DOM
    showResult(
      "ממצאי חקירת הסוכן",
      addedLayers.length
        ? `נוספו או הוצגו ${addedLayers.length.toLocaleString("he-IL")} שכבות מתוך תשובת הסוכן.`
        : "הסוכן השיב, אך לא נמצאו בתשובה נתונים שניתן לקשר לתצוגה."
    );
    const inferred = inferRecommendedView(prompt, result.answer);
    activateView(result.recommended_view || inferred.view, { automatic: true, reason: result.view_reason || inferred.reason });
    renderQueryInspector();
    return;
  }
  if (!options.keepRenderedSteps) renderActivitySteps(result.investigation_steps || [], result);
  if (!options.keepRenderedSteps && !(result.investigation_steps || []).length) {
    const started = (result.events || []).filter(event => event.event === "tool.started");
    started.forEach((event, index) => {
      const tool = (event.tool || "MCP").replace(/^mcp_(?:serbia_events_poc|intelligence_events_poc)_/, "");
      const input = event.preview ? `קלט שנשלח לכלי: ${event.preview}` : "Hermes לא החזיר את פרטי הקלט עבור פעולה זו.";
      addActivity(tool, input, "הכלי הסתיים ללא שגיאה; פירוט התוצאה לא נכלל ביומן Hermes.", {
        stepNumber: index + 1,
        observedClue: "Hermes דיווח שהסוכן בחר להפעיל כלי, אך לא החזיר רמז מפורט לשלב הזה.",
        rationale: "הסוכן בחר בכלי הזה כדי להמשיך לצמצם את אי-הוודאות בחקירה.",
        expectedValue: "לקבל ראיות נוספות או לאמת מועמד שכבר עלה.",
        technical: { tool, preview: event.preview || null },
        sourceId: stepSourceId(result, index + 1),
        sourceLabel: `צעד ${index + 1}: ${humanToolLabel(tool)}`
      });
    });
  }
  if (!options.keepRenderedSteps && !(result.investigation_steps || []).length && !(result.events || []).some(event => event.event === "tool.started")) {
    addActivity("Hermes", `שאלת החקירה שנשלחה: ${prompt}`, `התקבלה תשובה בריצה ${result.run_id}, ללא יומן כלי מפורט.`);
  }

  finalizeAssistantMessage(result.answer, { result, prompt });
  updateStepVisibilityButtons();
  renderQueryInspector();
  setSuggestions(["אילו הסברים תמימים יכולים להתאים לאותן ראיות?", "מה חסר כדי להעלות את רמת הביטחון?", "הצג את רצף האירועים לפי סדר הזמן"]);
}

async function runSavedQuestion(savedId) {
  if (state.busy) return;
  closeRecordedModal();
  state.busy = true;
  sendButton.disabled = true;
  recordedButton.disabled = true;
  updateSaveQuestionButton();
  sendButton.textContent = "מציג...";
  try {
    const response = await fetch(`/api/saved-question?id=${encodeURIComponent(savedId)}`, { cache: "no-store" });
    const saved = await response.json();
    if (!response.ok) throw new Error(saved.error || "טעינת השאלה השמורה נכשלה");
    const result = {
      ...(saved.result || {}),
      saved_question_id: saved.id,
      source_run_id: saved.source_run_id || saved.result?.run_id,
    };
    const prompt = (saved.question || "").trim();
    appendMessage("user", `<p>${escapeHtml(prompt)}</p>`);
    state.history.push({ role: "user", content: prompt }, { role: "assistant", content: result.answer || "" });
    applyHermesResult(result, prompt);
  } catch (error) {
    startAssistantResearchMessage("טעינת שאלה שמורה נכשלה.");
    finalizeAssistantMessage(`<p>לא הצלחתי להציג את השאלה השמורה.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`, { html: true });
  } finally {
    state.busy = false;
    sendButton.disabled = false;
    recordedButton.disabled = false;
    sendButton.textContent = "שלח";
    updateSaveQuestionButton();
  }
}

function openRecordedModal() {
  recordedModal.hidden = false;
  loadRecordedQuestions();
}

function closeRecordedModal() {
  recordedModal.hidden = true;
}

async function loadRecordedQuestions() {
  recordedList.innerHTML = `<div class="activity-empty">טוען שאלות שמורות...</div>`;
  try {
    const response = await fetch("/api/saved-questions", { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Saved questions unavailable");
    state.savedQuestions = payload.saved_questions || [];
    if (!state.savedQuestions.length) {
      recordedList.innerHTML = `<div class="activity-empty">לא נמצאו שאלות שמורות.</div>`;
      return;
    }
    recordedList.innerHTML = state.savedQuestions.map(item => `
      <article class="recorded-question saved-question-card">
        <div class="saved-question-main">
          <strong>${escapeHtml(item.title || item.question || "שאלה שמורה")}</strong>
          <p>${escapeHtml(item.question || "")}</p>
          <span>${escapeHtml(formatSavedTime(item.saved_at_utc))} · ${escapeHtml(VIEW_LABELS[item.recommended_view] || item.recommended_view || "תצוגה")} · ${Number(item.step_count || 0)} צעדים</span>
        </div>
        <div class="saved-question-actions">
          <button type="button" data-saved-id="${escapeHtml(item.id)}">פתח</button>
          <button type="button" class="danger-button" data-saved-delete="${escapeHtml(item.id)}">מחק</button>
        </div>
      </article>
    `).join("");
  } catch (error) {
    recordedList.innerHTML = `<div class="activity-empty">טעינת השאלות השמורות נכשלה: ${escapeHtml(error.message)}</div>`;
  }
}

async function runPrompt(prompt) {
  const clean = prompt.trim();
  if (!clean || state.busy) return;
  const clientStarted = performance.now();
  let firstLiveStepAt = null;
  appendMessage("user", `<p>${escapeHtml(clean)}</p>`);
  startAssistantResearchMessage();
  state.busy = true;
  sendButton.disabled = true;
  updateSaveQuestionButton();
  sendButton.textContent = "חוקר...";
  suggestions.innerHTML = "";
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
        investigation_id: state.investigationId
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
    addActivity("connection_error", "לא ניתן היה להשלים ריצת Hermes.", error.message);
    finalizeAssistantMessage(`<p>לא הצלחתי להשלים את ריצת הסוכן האמיתית.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`, { html: true });
    agentStatus.textContent = "Hermes אינו זמין";
    agentStatus.className = "agent-error";
  } finally {
    if (progressTimer) clearInterval(progressTimer);
    state.busy = false;
    sendButton.disabled = false;
    sendButton.textContent = "שלח";
    updateSaveQuestionButton();
  }
}

function showResult(title, subtitle) {
  if (resultTitle) resultTitle.textContent = title;
  if (resultSubtitle) resultSubtitle.textContent = subtitle;
  if (resultCount) {
    const visibleEvents = visibleEventItems().length;
    const visibleLocationLayers = visibleLayers("map").filter(layer => layer.kind === "locations").reduce((sum, layer) => sum + layer.items.length, 0);
    const visibleTimeGroups = visibleLayers("timeline").filter(layer => layer.kind === "time_aggregation").reduce((sum, layer) => sum + layer.items.length, 0);
    resultCount.textContent = visibleEvents
      ? `${visibleEvents} אירועים`
      : (visibleTimeGroups ? `${visibleTimeGroups} נקודות זמן` : `${visibleLocationLayers} מיקומים`);
  }
  renderAllViews();
}

function renderAllViews() {
  renderMap();
  renderTimeline();
  renderEvidence();
  updateStepVisibilityButtons();
}

function activateView(view, options = {}) {
  const requestedView = view === "evidence" ? "map" : view;
  const safeView = VIEW_LABELS[requestedView] ? requestedView : "map";
  document.querySelectorAll(".view-tab").forEach(button => button.classList.toggle("active", button.dataset.view === safeView));
  document.querySelectorAll(".view-pane").forEach(pane => pane.classList.toggle("active", pane.id === `${safeView}View`));
  if (safeView === "map" && state.map) {
    setTimeout(() => {
      state.map.resize();
      renderMap();
    }, 0);
  }
  if (options.automatic) {
    viewRecommendation.hidden = false;
    viewRecommendation.textContent = `הסוכן בחר להציג: ${VIEW_LABELS[safeView]} · ${options.reason}`;
  } else {
    viewRecommendation.hidden = true;
    viewRecommendation.textContent = "";
  }
  renderQueryInspector();
}

function setPanelWidths(chatWidth, resultWidth) {
  workspace.style.setProperty("--chat-width", `${Math.round(chatWidth)}px`);
  workspace.style.setProperty("--result-width", `${Math.round(resultWidth)}px`);
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
      const start = {
        chat: chat.getBoundingClientRect(),
        result: result.getBoundingClientRect()
      };
      const min = { chat: 240, result: 420 };

      const onMove = moveEvent => {
        const boundary = moveEvent.clientX;
        let chatWidth = start.chat.width;
        let resultWidth = start.result.width;
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
        setPanelWidths(chatWidth, resultWidth);
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
  const byLocation = new Map();
  const addLocationCount = (locationId, count, label, aggregateLocation = null, color = null) => {
    if (!locationId) return;
    const existing = byLocation.get(locationId) || { location_id: locationId, count: 0, labels: new Set(), colors: new Set(), aggregateLocation };
    existing.count += Number(count || 0);
    existing.labels.add(label);
    if (color) existing.colors.add(color);
    if (aggregateLocation) existing.aggregateLocation = aggregateLocation;
    byLocation.set(locationId, existing);
  };
  visibleLayers("map").forEach(layer => {
    if (layer.kind === "events") {
      const counts = {};
      layer.items.forEach(event => { counts[event.location_id] = (counts[event.location_id] || 0) + 1; });
      Object.entries(counts).forEach(([locationId, count]) => addLocationCount(locationId, count, layer.label, null, layer.color));
    } else if (layer.kind === "locations") {
      layer.items.forEach(item => addLocationCount(item.location_id, item.count || 1, layer.label, item, layer.color));
    } else if (layer.kind === "location_metadata") {
      layer.items.forEach(item => addLocationCount(item.location_id, item.event_count || item.count || 1, item.location_name || layer.label, item, layer.color));
    } else if (layer.kind === "entity_metadata") {
      layer.items.forEach(entity => {
        (entity.top_locations || []).forEach(location => {
          addLocationCount(
            location.location_id,
            location.count || 1,
            entity.canonical_name || entity.entity_id || layer.label,
            {
              location_id: location.location_id,
              location_name: location.location_name,
              latitude: location.latitude,
              longitude: location.longitude,
              count: location.count
            },
            layer.color
          );
        });
      });
    }
  });
  const bounds = new maplibregl.LngLatBounds();
  byLocation.forEach(item => {
    const locationId = item.location_id;
    const aggregateLocation = item.aggregateLocation;
    const location = LOCATIONS[locationId] || (
      aggregateLocation && aggregateLocation.latitude !== undefined && aggregateLocation.longitude !== undefined
        ? { name: aggregateLocation.location_name, lon: aggregateLocation.longitude, lat: aggregateLocation.latitude }
        : null
    );
    if (!location) return;
    const element = document.createElement("div");
    element.className = `map-marker`;
    element.style.setProperty("--layer-color", [...item.colors][0] || "#8ab4f8");
    element.setAttribute("role", "button");
    element.setAttribute("aria-label", `${location.name}: ${item.count.toLocaleString("he-IL")} פריטים`);
    element.innerHTML = `<span class="map-marker-dot"></span>${item.count > 1 ? `<span class="map-marker-count">${item.count.toLocaleString("he-IL")}</span>` : ""}`;
    const popupHtml = `
      <div class="map-popup" dir="rtl">
        <strong>${escapeHtml(location.name)}</strong>
        <span>${item.count.toLocaleString("he-IL")} פריטים</span>
        <em>${escapeHtml([...item.labels].join(" · "))}</em>
      </div>`;
    const popup = new maplibregl.Popup({ offset: 18, closeButton: true, closeOnClick: true }).setHTML(popupHtml);
    const marker = new maplibregl.Marker({ element, anchor: "center" }).setLngLat([location.lon, location.lat]).setPopup(popup).addTo(state.map);
    state.markers.push(marker);
    bounds.extend([location.lon, location.lat]);
  });
  if (!bounds.isEmpty()) state.map.fitBounds(bounds, { padding: 110, maxZoom: 10.2, duration: 450 });
}

function renderTimeline() {
  const timeline = document.getElementById("timeline");
  const eventTimelineItems = visibleLayers("timeline")
    .filter(layer => layer.kind === "events")
    .flatMap(layer => layer.items.map(event => ({ type: "event", layer, event, sort: event.date })));
  const aggregateTimelineItems = visibleLayers("timeline")
    .filter(layer => layer.kind === "time_aggregation")
    .flatMap(layer => layer.items.map(item => ({ type: "aggregation", layer, item, sort: item.sortKey })));
  if (!eventTimelineItems.length && !aggregateTimelineItems.length) { timeline.className = "timeline empty-state"; timeline.textContent = "לא נבחרו שכבות עם ציר זמן להצגה."; return; }
  timeline.className = "timeline";
  const aggregationHtml = aggregateTimelineItems.map(({ layer, item }) => `
    <article class="timeline-item" style="${layerColorStyle(layer)}">
      <span class="timeline-dot"></span>
      <div class="timeline-time">${escapeHtml(item.timeLabel)}</div>
      <div class="timeline-title">${escapeHtml(layer.label)} · ${item.count.toLocaleString("he-IL")} אירועים</div>
      <div class="timeline-summary">${escapeHtml(item.summary)}</div>
    </article>`).join("");
  const eventHtml = eventTimelineItems.sort((a, b) => a.sort - b.sort).map(({ layer, event }) => `
    <article class="timeline-item" style="${layerColorStyle(layer)}">
      <span class="timeline-dot"></span>
      <div class="timeline-time">${escapeHtml(event.timestamp_utc.replace("T", " ").replace("Z", ""))}</div>
      <div class="timeline-title">${escapeHtml(layer.label)} · ${escapeHtml(event.location_name)}</div>
      <div class="timeline-summary">${escapeHtml(event.event_summary)}</div>
    </article>`).join("");
  timeline.innerHTML = aggregationHtml + eventHtml;
}

function renderEvidence() {
  const overlay = document.getElementById("rawEventsOverlay");
  const tabs = document.getElementById("rawEventsTabs");
  const head = document.getElementById("evidenceHead");
  const body = document.getElementById("evidenceRows");
  if (!overlay || !tabs || !head || !body) return;

  const tableLayers = state.layers.filter(layer => layer.capabilities.table);
  if (!tableLayers.length) {
    overlay.hidden = true;
    tabs.innerHTML = "";
    head.innerHTML = "";
    body.innerHTML = "";
    return;
  }

  if (!tableLayers.some(layer => layer.id === state.activeLayerId)) state.activeLayerId = tableLayers[0].id;
  const activeLayer = activeTableLayer();

  overlay.hidden = false;
  overlay.classList.toggle("minimized", state.rawOverlayMinimized);
  overlay.style.setProperty("--raw-overlay-height", `${state.rawOverlayHeight}%`);
  const minimizeButton = document.getElementById("rawEventsMinimize");
  if (minimizeButton) {
    minimizeButton.textContent = state.rawOverlayMinimized ? "□" : "−";
    minimizeButton.title = state.rawOverlayMinimized ? "הגדל" : "מזער";
    minimizeButton.setAttribute("aria-label", state.rawOverlayMinimized ? "הגדל טבלת תוצאות" : "מזער טבלת תוצאות");
  }
  tabs.innerHTML = tableLayers.map(layer => `
    <button type="button" class="raw-source-tab ${layer.id === activeLayer?.id ? "active" : ""} ${layer.visible ? "" : "hidden-source"}" style="${layerColorStyle(layer)}" data-layer-id="${escapeHtml(layer.id)}" role="tab" aria-selected="${layer.id === activeLayer?.id}" title="${escapeHtml(layer.sourceLabel || layer.label)}">
      <span class="raw-source-color"></span>
      <span class="raw-source-name">${escapeHtml(layer.label)}</span>
      <strong>${layer.items.length.toLocaleString("he-IL")}</strong>
        <span class="raw-source-eye" data-layer-visibility="${escapeHtml(layer.id)}" title="${layer.visible ? "הסתר שכבה" : "הצג שכבה"}" aria-label="${layer.visible ? "הסתר שכבה" : "הצג שכבה"}" aria-pressed="${layer.visible ? "true" : "false"}">
          <span class="visibility-eye-icon ${layer.visible ? "" : "off"}" aria-hidden="true"></span>
        </span>
      <span class="raw-source-close" data-layer-close="${escapeHtml(layer.id)}" title="סגור שכבה" aria-label="סגור שכבה">×</span>
    </button>`).join("");

  if (!activeLayer) return;
  if (activeLayer.kind === "location_metadata") {
    head.innerHTML = "<tr><th>מיקום</th><th>אירועים</th><th>רשות</th><th>סוג</th><th>דיוק</th><th>מזהה</th></tr>";
    body.innerHTML = activeLayer.visible && activeLayer.items.length ? activeLayer.items.map(item => `
      <tr>
        <td>${escapeHtml(item.location_name || item.name || item.location_id || "-")}</td>
        <td>${Number(item.event_count || item.count || 0).toLocaleString("he-IL")}</td>
        <td>${escapeHtml(item.municipality || "-")}</td>
        <td>${escapeHtml(item.type || "-")}</td>
        <td>${escapeHtml(item.precision || "-")}</td>
        <td dir="ltr">${escapeHtml(item.location_id || "-")}</td>
      </tr>`).join("") : '<tr><td colspan="6" class="empty-cell">השכבה מוסתרת או ריקה.</td></tr>';
    return;
  }
  if (activeLayer.kind === "entity_metadata") {
    head.innerHTML = "<tr><th>ישות</th><th>אירועים</th><th>סוג</th><th>ערכי actor</th><th>מוקדים מובילים</th><th>מזהה</th></tr>";
    body.innerHTML = activeLayer.visible && activeLayer.items.length ? activeLayer.items.map(item => {
      const aliases = (item.aliases || []).slice(0, 4).join(", ");
      const topLocations = (item.top_locations || []).slice(0, 4).map(location => `${location.location_name || location.location_id} (${Number(location.count || 0).toLocaleString("he-IL")})`).join(", ");
      return `
      <tr>
        <td>${escapeHtml(item.canonical_name || item.entity_id || "-")}</td>
        <td>${Number(item.event_count || item.count || 0).toLocaleString("he-IL")}</td>
        <td>${escapeHtml(item.entity_type || "-")}</td>
        <td>${escapeHtml(aliases || "-")}</td>
        <td>${escapeHtml(topLocations || "-")}</td>
        <td dir="ltr">${escapeHtml(item.entity_id || "-")}</td>
      </tr>`;
    }).join("") : '<tr><td colspan="6" class="empty-cell">השכבה מוסתרת או ריקה.</td></tr>';
    return;
  }
  if (activeLayer.kind === "locations") {
    head.innerHTML = "<tr><th>מיקום</th><th>כמות</th><th>מזהה</th><th>סוג שכבה</th></tr>";
    body.innerHTML = activeLayer.visible && activeLayer.items.length ? activeLayer.items.map(item => `
      <tr>
        <td>${escapeHtml(item.location_name || item.label || item.key || item.location_id || "-")}</td>
        <td>${Number(item.count || 0).toLocaleString("he-IL")}</td>
        <td dir="ltr">${escapeHtml(item.location_id || item.key || "-")}</td>
        <td>${escapeHtml(activeLayer.label)}</td>
      </tr>`).join("") : '<tr><td colspan="4" class="empty-cell">השכבה מוסתרת או ריקה.</td></tr>';
    return;
  }
  if (activeLayer.kind === "time_aggregation") {
    head.innerHTML = "<tr><th>זמן</th><th>כמות</th><th>סוג קיבוץ</th><th>תקציר</th></tr>";
    body.innerHTML = activeLayer.visible && activeLayer.items.length ? activeLayer.items.map(item => `
      <tr>
        <td>${escapeHtml(item.timeLabel || item.label || "-")}</td>
        <td>${Number(item.count || 0).toLocaleString("he-IL")}</td>
        <td>${escapeHtml(item.group_by === "hour" ? "שעה" : "תאריך")}</td>
        <td>${escapeHtml(item.summary || "-")}</td>
      </tr>`).join("") : '<tr><td colspan="4" class="empty-cell">השכבה מוסתרת או ריקה.</td></tr>';
    return;
  }
  if (activeLayer.kind === "group_aggregation") {
    head.innerHTML = "<tr><th>קבוצה</th><th>כמות</th><th>סוג קיבוץ</th><th>אירוע ראשון</th><th>אירוע אחרון</th></tr>";
    body.innerHTML = activeLayer.visible && activeLayer.items.length ? activeLayer.items.map(item => `
      <tr>
        <td>${escapeHtml(item.label || item.key || "-")}</td>
        <td>${Number(item.count || 0).toLocaleString("he-IL")}</td>
        <td>${escapeHtml(item.group_by || "-")}</td>
        <td dir="ltr">${escapeHtml(item.first_event_id || item.first_event_time || "-")}</td>
        <td dir="ltr">${escapeHtml(item.last_event_id || item.last_event_time || "-")}</td>
      </tr>`).join("") : '<tr><td colspan="5" class="empty-cell">השכבה מוסתרת או ריקה.</td></tr>';
    return;
  }
  head.innerHTML = "<tr><th>זמן</th><th>אמינות</th><th>ודאות</th><th>גורם</th><th>מיקום</th><th>תקציר</th></tr>";
  body.innerHTML = activeLayer.visible && activeLayer.items.length ? activeLayer.items.map(event => `
    <tr>
      <td dir="ltr">${escapeHtml(event.timestamp_utc)}</td>
      <td>${escapeHtml(event.source_reliability_label || event.source_reliability || "-")}</td>
      <td>${escapeHtml(event.certainty_level || "-")}</td>
      <td>${escapeHtml(event.entity_name || event.entity_id || "-")}</td>
      <td>${escapeHtml(event.location_name || "-")}</td>
      <td>${escapeHtml(event.event_summary || "-")}</td>
    </tr>`).join("") : '<tr><td colspan="6" class="empty-cell">השכבה מוסתרת או ריקה.</td></tr>';
}

function resetInvestigation() {
  state.current = [];
  state.stage = 0;
  state.aggregateLocations = [];
  state.aggregateTimeline = [];
  state.aggregateGroups = [];
  state.locationMetadata = [];
  state.entityMetadata = [];
  state.layers = [];
  state.activeLayerId = null;
  state.rawOverlayMinimized = false;
  state.rawOverlayHeight = 28;
  state.history = [];
  state.investigationId = createInvestigationId();
  state.activeAssistantMessage = null;
  state.activeActivityList = null;
  state.activeActivityEmpty = null;
  state.lastResult = null;
  state.lastPrompt = null;
  state.queryContext = null;
  conversation.innerHTML = '<article class="message assistant-message"><div class="message-label">סוכן חקירה</div><p>אפשר להתחיל בשאלה פתוחה. אשתמש בכלי החיפוש, הזמן והמפה כדי לבנות תשובה שניתן לבדוק מול האירועים הגולמיים.</p></article>';
  if (resultTitle) resultTitle.textContent = "טרם בוצעה חקירה";
  if (resultSubtitle) resultSubtitle.textContent = "תוצאות, המחשות וראיות יופיעו כאן לאחר השאלה הראשונה.";
  if (resultCount) resultCount.textContent = "0 אירועים";
  activateView("map");
  setSuggestions(["אילו דיווחים על חסימות הופיעו ראשונים?", "האם הטענה על חציית גבול מגובה במקור אמין?", "איפה יש ריכוזי דיווחים מרכזיים?"]);
  renderAllViews();
  renderQueryInspector();
  updateSaveQuestionButton();
  if (state.map) setTimeout(() => state.map.resize(), 0);
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[char]);
}

document.addEventListener("click", event => {
  const suggestion = event.target.closest("[data-prompt]");
  if (suggestion) runPrompt(suggestion.dataset.prompt);
  if (event.target.closest("#queryToolName")) openQueryModal();
  if (event.target.closest("#queryModalClose")) closeQueryModal();
  if (event.target === queryModal) closeQueryModal();
  if (event.target.id === "queryFormRunButton") handleQueryFormSubmit();
  const savedDelete = event.target.closest("[data-saved-delete]");
  if (savedDelete) {
    event.stopPropagation();
    deleteSavedQuestion(savedDelete.dataset.savedDelete);
    return;
  }
  const savedQuestion = event.target.closest("[data-saved-id]");
  if (savedQuestion) runSavedQuestion(savedQuestion.dataset.savedId);
  const viewButton = event.target.closest("[data-view]");
  if (viewButton) activateView(viewButton.dataset.view);
  const sourceVisibilityBtn = event.target.closest(".source-visibility-btn");
  if (sourceVisibilityBtn) {
    event.stopPropagation();
    const sourceId = sourceVisibilityBtn.dataset.sourceId;
    const sourceLayers = state.layers.filter(layer => layer.sourceId === sourceId);
    const anyVisible = sourceLayers.some(layer => layer.visible);
    sourceLayers.forEach(layer => { layer.visible = !anyVisible; });
    updateSourceVisibilityBtn(sourceVisibilityBtn);
    renderAllViews();
    return;
  }
  const visibilityToggle = event.target.closest("[data-layer-visibility]");
  if (visibilityToggle) {
    event.stopPropagation();
    const layer = state.layers.find(item => item.id === visibilityToggle.dataset.layerVisibility);
    if (layer) layer.visible = !layer.visible;
    renderAllViews();
    return;
  }
  const closeLayer = event.target.closest("[data-layer-close]");
  if (closeLayer) {
    event.stopPropagation();
    const layerIdToClose = closeLayer.dataset.layerClose;
    state.layers = state.layers.filter(item => item.id !== layerIdToClose);
    if (state.activeLayerId === layerIdToClose) {
      state.activeLayerId = state.layers.find(layer => layer.capabilities.table && layer.visible)?.id
        || state.layers.find(layer => layer.capabilities.table)?.id
        || null;
    }
    renderAllViews();
    return;
  }
  const rawLayerTab = event.target.closest("[data-layer-id]");
  if (rawLayerTab) {
    state.activeLayerId = rawLayerTab.dataset.layerId;
    renderEvidence();
  }
  if (event.target.closest("#rawEventsMinimize")) {
    state.rawOverlayMinimized = !state.rawOverlayMinimized;
    renderEvidence();
  }
  if (event.target.closest("#rawEventsClose")) {
    state.layers = [];
    state.activeLayerId = null;
    state.current = [];
    state.aggregateLocations = [];
    state.aggregateTimeline = [];
    state.locationMetadata = [];
    state.entityMetadata = [];
    state.queryContext = null;
    renderAllViews();
    renderQueryInspector();
  }
  if (event.target === recordedModal) closeRecordedModal();
});

document.addEventListener("pointerdown", event => {
  const handle = event.target.closest("#rawEventsResizeHandle");
  if (!handle) return;
  const overlay = document.getElementById("rawEventsOverlay");
  const stack = document.querySelector(".view-stack");
  if (!overlay || !stack || overlay.hidden || state.rawOverlayMinimized) return;

  event.preventDefault();
  handle.setPointerCapture(event.pointerId);
  const stackRect = stack.getBoundingClientRect();
  const startY = event.clientY;
  const startHeight = overlay.getBoundingClientRect().height;

  const onMove = moveEvent => {
    const delta = startY - moveEvent.clientY;
    const nextPx = Math.min(Math.max(startHeight + delta, stackRect.height * 0.16), stackRect.height * 0.55);
    state.rawOverlayHeight = Math.round((nextPx / stackRect.height) * 100);
    overlay.style.setProperty("--raw-overlay-height", `${state.rawOverlayHeight}%`);
  };
  const onUp = () => {
    document.removeEventListener("pointermove", onMove);
    document.removeEventListener("pointerup", onUp);
    document.removeEventListener("pointercancel", onUp);
  };
  document.addEventListener("pointermove", onMove);
  document.addEventListener("pointerup", onUp);
  document.addEventListener("pointercancel", onUp);
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
saveQuestionButton.addEventListener("click", saveCurrentQuestion);
recordedButton.addEventListener("click", openRecordedModal);
recordedClose.addEventListener("click", closeRecordedModal);
initPanelResizers();

async function boot() {
  initMap();
  try {
    const response = await fetch("./data/serbia_kosovo_events_projection.csv");
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
