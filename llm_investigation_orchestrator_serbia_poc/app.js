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
const EVENT_ID_PATTERN = /\b(?:REC-(?:V2-)?\d{6}|LOC-(?:V2-)?\d{3})\b/g;

function createInvestigationId() {
  const random = crypto?.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  return `investigation-${random}`;
}

function liveStepsUrl(currentPrompt) {
  return /(^|[^\p{L}\p{N}_])@(משה|Moshe)(?![\p{L}\p{N}_])/iu.test(String(currentPrompt || ""))
    ? "/api/live-steps?agent=moshe"
    : "/api/live-steps?agent=general";
}

const LOCALE_STORAGE_KEY = "serbia-poc-locale-v1";
const DEFAULT_LOCALE = "he";
const INVESTIGATIONS_STORAGE_KEY = "serbia-poc-investigations-v2";
const LEGACY_INVESTIGATIONS_STORAGE_KEYS = ["serbia-poc-investigations-v1"];
const DEFAULT_INVESTIGATION_NAME = "חקירה חדשה";
const TEAM_MENTION_AGENT_INSTRUCTION = [
  "הנחיית ממשק קבועה:",
  "סימוני @ לפני שמות חברי מכלול, כגון @משה או @טליה, הם פנייה פנימית של המשתמש לצוות העבודה.",
  "אל תתייחס לשמות חברי המכלול כאל ישויות מודיעיניות, אנשים לחקירה, מקורות, מיקומים או מילות מפתח, אלא אם המשתמש מבקש במפורש לנתח את חברי המכלול עצמם."
].join("\n");

const MICHLOL_MEMBERS = {
  he: [
    { id: "moshe-targets-officer", displayName: "משה", roleLabel: "קצין מטרות", memberType: "user", avatar: "./assets/michlol/moshe.png", initial: "מ" },
    { id: "talia-tama-officer", displayName: "טליה", roleLabel: "קצינת תמא", memberType: "user", avatar: "./assets/michlol/talia.png", initial: "ט" },
    { id: "naama-field-officer", displayName: "נעמה", roleLabel: "קצינת שטח", memberType: "user", avatar: "./assets/michlol/naama.png", initial: "נ" },
    { id: "gadi-collection-officer", displayName: "גדי", roleLabel: "קצין איסוף", memberType: "user", avatar: "./assets/michlol/gadi.png", initial: "ג" },
    { id: "yahli-processing-officer", displayName: "יהלי", roleLabel: "קצין עיבוד", memberType: "user", avatar: "./assets/michlol/yahli.png", initial: "י" }
  ],
  en: [
    { id: "moshe-targets-officer", displayName: "Moshe", roleLabel: "Targets Officer", memberType: "user", avatar: "./assets/michlol/moshe.png", initial: "M" },
    { id: "talia-tama-officer", displayName: "Talia", roleLabel: "Terrain Officer", memberType: "user", avatar: "./assets/michlol/talia.png", initial: "T" },
    { id: "naama-field-officer", displayName: "Naama", roleLabel: "Field Officer", memberType: "user", avatar: "./assets/michlol/naama.png", initial: "N" },
    { id: "gadi-collection-officer", displayName: "Gadi", roleLabel: "Collection Officer", memberType: "user", avatar: "./assets/michlol/gadi.png", initial: "G" },
    { id: "yahli-processing-officer", displayName: "Yahli", roleLabel: "Processing Officer", memberType: "user", avatar: "./assets/michlol/yahli.png", initial: "Y" }
  ]
};

const MICHLOL_MEMBER_WELCOME = {
  he: "אני מחובר עכשיו לשיחה הזו. שלח לי את המשימה או השאלה הבאה, ובשלב הבא נחבר כאן סוכן ייעודי לחבר המכלול.",
  en: "I’m connected to this conversation now. Send me the next task or question, and in the next step we’ll connect a dedicated agent for this team member here."
};
const MOSHE_MEMBER_ID = "moshe-targets-officer";
const WORKSTREAM_SEEN_STORAGE_KEY = "serbia-poc-workstream-seen-v2";
const MOSHE_MESSAGE_LABEL = {
  he: "משה - קצין מטרות",
  en: "Moshe - Targets Officer"
};
const MOSHE_WELCOME = {
  he: "אני משה, קצין המטרות. אפשר לשאול אותי על אינדיקציות ומטרות, או לפתוח מעקב חדש.",
  en: "I’m Moshe, the targets officer. You can ask me about indications and targets, or open a new workstream."
};
const DEFAULT_SUGGESTIONS = {
  he: [
    "האם הטענה על חציית גבול מגובה במקור אמין?",
    "איפה יש ריכוזי דיווחים מרכזיים בצפון קוסובו?"
  ],
  en: [
    "Is the border-crossing claim supported by a reliable source?",
    "Where are the main reporting hotspots in North Kosovo?"
  ]
};
const FOLLOWUP_SUGGESTIONS = {
  he: [
    "אילו הסברים אזרחיים חלופיים יכולים להתאים לאותן ראיות?",
    "מה חסר כדי להעלות את רמת הביטחון?",
    "הצג את רצף האירועים לפי זמן"
  ],
  en: [
    "What benign explanations could fit the same evidence?",
    "What is missing to raise the confidence level?",
    "Show the event sequence in time order"
  ]
};

function requestedLocaleFromUrl() {
  try {
    const params = new URLSearchParams(window.location.search);
    const lang = params.get("lang");
    return lang == null ? null : normalizeLocale(lang);
  } catch (error) {
    return null;
  }
}

function normalizeLocale(value) {
  const locale = String(value || "").trim().toLowerCase();
  return locale === "en" ? "en" : "he";
}

const INITIAL_LOCALE = normalizeLocale((() => {
  const requested = requestedLocaleFromUrl();
  if (requested) return requested;
  try {
    return localStorage.getItem(LOCALE_STORAGE_KEY);
  } catch (error) {
    return DEFAULT_LOCALE;
  }
})());

function currentLocale() {
  return state.locale === "en" ? "en" : "he";
}

function currentLocaleTag() {
  return currentLocale() === "en" ? "en-US" : "he-IL";
}

function currentMembers() {
  return MICHLOL_MEMBERS[currentLocale()];
}

function activeLocaleText(he, en) {
  return currentLocale() === "en" ? en : he;
}

function buildLocaleApiUrl(path) {
  const url = new URL(path, window.location.origin);
  url.searchParams.set("lang", currentLocale());
  return url.toString();
}

function applyLocaleAttributeSet(attributeName, applyValue) {
  document.querySelectorAll(`[${attributeName}-he][${attributeName}-en]`).forEach(element => {
    const value = currentLocale() === "en"
      ? element.getAttribute(`${attributeName}-en`)
      : element.getAttribute(`${attributeName}-he`);
    if (value != null) applyValue(element, value);
  });
}

function applyLocaleAttributes() {
  applyLocaleAttributeSet("data-i18n-text", (element, value) => {
    element.textContent = value;
  });
  applyLocaleAttributeSet("data-i18n-aria", (element, value) => {
    element.setAttribute("aria-label", value);
  });
  applyLocaleAttributeSet("data-i18n-title", (element, value) => {
    element.title = value;
  });
  applyLocaleAttributeSet("data-i18n-placeholder", (element, value) => {
    element.setAttribute("placeholder", value);
  });
}

function defaultInvestigationName(locale = currentLocale()) {
  return normalizeLocale(locale) === "en" ? "New investigation" : "חקירה חדשה";
}

const state = {
  locale: INITIAL_LOCALE,
  pageView: "welcome",
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
  focusedEventPopup: null,
  focusedMapSelection: null,
  history: [],
  investigationId: createInvestigationId(),
  investigationName: defaultInvestigationName(INITIAL_LOCALE),
  draftSessionActive: false,
  pendingDraftMemoryAction: null,
  investigations: [],
  investigationMemory: null,
  investigationMemoryLoading: false,
  investigationMemoryError: "",
  investigationMemoryLoadToken: 0,
  investigationSelectorOpen: false,
  investigationSearchQuery: "",
  recordedQuestions: [],
  savedQuestions: [],
  busy: false,
  activeAssistantMessage: null,
  activeActivityList: null,
  activeActivityEmpty: null,
  lastResult: null,
  lastPrompt: null,
  queryContext: null,
  layerCatalog: [],
  layerCatalogLoading: false,
  layerCatalogError: "",
  layerSearchQuery: "",
  layerSearchOpen: false,
  promptOptionsOpen: false,
  promptSelectedLayerIds: new Set(),
  workstreamComposerMode: false,
  workstreams: [],
  workstreamsLoading: false,
  workstreamLoadToken: 0,
  workstreamSeen: {},
  workstreamRailCollapsed: false,
  investigationPlayback: null,
  playbackPollToken: 0,
  memoryUpdatePollToken: 0,
  renderedMemoryUpdateKeys: new Set(),
  pendingMosheWorkstreamProposal: null,
  activeConversationMemberId: null,
  openingLayerIds: new Set(),
  layers: [],
  activeLayerId: null,
  rawOverlayMinimized: false,
  rawOverlayHeight: 28,
  resultTableControls: new Map(),
  chatPanelCollapsed: false,
  queryEdited: false,
  originalQuery: null,
  activeTeamMentions: []
};

const conversation = document.getElementById("conversation");
const suggestions = document.getElementById("suggestions");
const promptForm = document.getElementById("promptForm");
const promptInput = document.getElementById("promptInput");
const welcomePromptForm = document.getElementById("welcomePromptForm");
const welcomePromptInput = document.getElementById("welcomePromptInput");
const welcomePromptOptionsButton = document.getElementById("welcomePromptOptionsButton");
const resultTitle = document.getElementById("resultTitle");
const resultSubtitle = document.getElementById("resultSubtitle");
const resultCount = document.getElementById("resultCount");
const sendButton = document.getElementById("sendButton");
const investigationInput = document.getElementById("investigationInput");
const investigationAddButton = document.getElementById("investigationAddButton");
const investigationList = document.getElementById("investigationList");
const michlolTeam = document.getElementById("michlolTeam");
const investigationSwitcher = document.querySelector(".investigation-switcher");
const draftCreateInvestigationButton = document.getElementById("draftCreateInvestigationButton");
const draftCreateModal = document.getElementById("draftCreateModal");
const draftCreateForm = document.getElementById("draftCreateForm");
const draftInvestigationName = document.getElementById("draftInvestigationName");
const draftCreateError = document.getElementById("draftCreateError");
const draftCreateCancel = document.getElementById("draftCreateCancel");
const draftCreateSubmit = document.getElementById("draftCreateSubmit");
const promptOptionsButton = document.getElementById("promptOptionsButton");
const promptOptionsMenu = document.getElementById("promptOptionsMenu");
const workstreamRail = document.getElementById("workstreamRail");
const workstreamRailList = document.getElementById("workstreamRailList");
const workstreamRailCount = document.getElementById("workstreamRailCount");
const workstreamRailToggle = document.getElementById("workstreamRailToggle");
const playbackNextButton = document.getElementById("playbackNextButton");
const playbackResetButton = document.getElementById("playbackResetButton");
const languageToggle = document.getElementById("languageToggle");
const appHomeButton = document.getElementById("appHomeButton");
const welcomePage = document.getElementById("welcomePage");
const myInvestigationsList = document.getElementById("myInvestigationsList");
const myInvestigationsCount = document.getElementById("myInvestigationsCount");
const similarInvestigationsList = document.getElementById("similarInvestigationsList");
const welcomeActionModal = document.getElementById("welcomeActionModal");
const welcomeActionTitle = document.getElementById("welcomeActionTitle");
const welcomeActionDescription = document.getElementById("welcomeActionDescription");
const welcomeActionClose = document.getElementById("welcomeActionClose");
const intelligencePeriod = document.getElementById("intelligencePeriod");
const playbackAgentStatus = document.getElementById("playbackAgentStatus");
const workstreamComposerMode = document.getElementById("workstreamComposerMode");
const workstreamComposerCancel = document.getElementById("workstreamComposerCancel");
const selectedLayersButton = document.getElementById("selectedLayersButton");
const selectedLayersLabel = document.getElementById("selectedLayersLabel");
const selectedLayersSummary = document.getElementById("selectedLayersSummary");
const selectedLayersClear = document.getElementById("selectedLayersClear");
const recordedModal = document.getElementById("recordedModal");
const recordedClose = document.getElementById("recordedClose");
const recordedList = document.getElementById("recordedList");
const queryLayersModal = document.getElementById("queryLayersModal");
const queryLayersClose = document.getElementById("queryLayersClose");
const queryLayersList = document.getElementById("queryLayersList");
const queryLayersSubmit = document.getElementById("queryLayersSubmit");
const queryLayersError = document.getElementById("queryLayersError");
const datasetStatus = document.getElementById("datasetStatus");
const datasetStatusIndicator = document.getElementById("datasetStatusIndicator");
const agentStatus = document.getElementById("agentStatus");
const agentStatusIndicator = document.getElementById("agentStatusIndicator");
const viewRecommendation = document.getElementById("viewRecommendation");
const layerSelectorSearch = document.getElementById("layerSelectorSearch");
const layerSelectorList = document.getElementById("layerSelectorList");
const layerSelectorStatus = document.getElementById("layerSelectorStatus");
const workspace = document.querySelector(".workspace");
const chatPanelToggle = document.getElementById("chatPanelToggle");
const queryLayerName = document.getElementById("queryLayerName");
const queryToolName = document.getElementById("queryToolName");
const queryModal = document.getElementById("queryModal");

const systemStatuses = {
  dataset: { element: datasetStatus, indicator: datasetStatusIndicator, labelHe: "מאגר הנתונים", labelEn: "Dataset", he: "טוען נתונים", en: "Loading data", state: "loading" },
  agent: { element: agentStatus, indicator: agentStatusIndicator, labelHe: "Hermes", labelEn: "Hermes", he: "בודק חיבור לסוכן", en: "Checking agent connection", state: "loading" }
};

function renderSystemStatuses() {
  Object.values(systemStatuses).forEach(status => {
    const english = currentLocale() === "en";
    const detail = english ? status.en : status.he;
    if (status.element) status.element.textContent = detail;
    if (status.indicator) {
      status.indicator.dataset.state = status.state;
      status.indicator.setAttribute("aria-label", `${english ? status.labelEn : status.labelHe}: ${detail}`);
    }
  });
}

function updateSystemStatus(kind, he, en, statusState) {
  const status = systemStatuses[kind];
  if (!status) return;
  Object.assign(status, { he, en, state: statusState });
  renderSystemStatuses();
}
const queryModalTitle = document.getElementById("queryModalTitle");
const queryModalBody = document.getElementById("queryModalBody");
const queryModalClose = document.getElementById("queryModalClose");

function viewLabels() {
  return currentLocale() === "en"
    ? { map: "Map", timeline: "Timeline", evidence: "Raw events" }
    : { map: "מפה", timeline: "ציר זמן", evidence: "אירועים גולמיים" };
}

function layerQueryLabels() {
  return currentLocale() === "en"
    ? { map: "Raw events layer", timeline: "Raw events layer", evidence: "Raw events layer" }
    : { map: "שכבת אירועים גולמיים", timeline: "שכבת אירועים גולמיים", evidence: "שכבת אירועים גולמיים" };
}

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

function layerFamilyLabels() {
  return currentLocale() === "en"
    ? { entities: "Entities", locations: "Locations", events: "Events by source_type", targets: "Targets" }
    : { entities: "ישויות", locations: "מיקומים", events: "אירועים לפי source_type", targets: "מטרות" };
}

const ATTACK_TARGET_CATALOG_LAYER_ID = "attack-targets:all";
const teamMentionState = {
  textarea: null,
  range: null,
  matches: [],
  activeIndex: 0
};

function michlolAvatarHtml(member) {
  return `<span class="michlol-avatar"><span class="michlol-initial">${escapeHtml(member.initial)}</span><img src="${escapeHtml(member.avatar)}" alt="" loading="eager" onerror="this.remove()"></span>`;
}

function michlolMemberHtml(member) {
  const title = `${member.displayName} - ${member.roleLabel}`;
  const aria = `${member.displayName}, ${member.roleLabel}`;
  const active = state.activeConversationMemberId === member.id;
  return `
    <button class="michlol-member ${active ? "active" : ""}" type="button" data-member-id="${escapeHtml(member.id)}" data-member-type="${escapeHtml(member.memberType)}" title="${escapeHtml(title)}" aria-label="${escapeHtml(aria)}" aria-pressed="${active ? "true" : "false"}">
      ${michlolAvatarHtml(member)}
      <span class="michlol-name">${escapeHtml(member.displayName)}</span>
    </button>`;
}

function renderMichlolTeam() {
  if (!michlolTeam) return;
  const members = currentMembers();
  const visible = members.slice(0, 3);
  const hidden = members.slice(3);
  michlolTeam.innerHTML = `
    <span class="michlol-title">${activeLocaleText("מכלול", "Team")}</span>
    ${visible.map(michlolMemberHtml).join("")}
    ${hidden.length ? `
      <details class="michlol-more">
        <summary title="${activeLocaleText("הצג חברי מכלול נוספים", "Show more team members")}" aria-label="${activeLocaleText("הצג חברי מכלול נוספים", "Show more team members")}">...</summary>
        <div class="michlol-more-list">
          ${hidden.map(michlolMemberHtml).join("")}
        </div>
      </details>` : ""}`;
  renderPromptOptions();
}

function renderPromptOptions() {
  const option = promptOptionsMenu?.querySelector('[data-prompt-option="workstream"]');
  if (option) option.hidden = state.draftSessionActive || state.activeConversationMemberId !== MOSHE_MEMBER_ID;
}

function activeConversationMember() {
  return currentMembers().find(member => member.id === state.activeConversationMemberId) || null;
}

function updatePromptPlaceholder() {
  if (!promptInput) return;
  if (state.workstreamComposerMode) {
    promptInput.placeholder = activeLocaleText("תאר מה לעקוב אחריו ומה מטרת המעקב...", "Describe what to track and what the workstream is for...");
    return;
  }
  const member = activeConversationMember();
  promptInput.placeholder = member
    ? activeLocaleText(`כתוב אל ${member.displayName}...`, `Write to ${member.displayName}...`)
    : activeLocaleText("כתוב שאלת חקירה...", "Ask an investigation question...");
}

function memberMessageLabel(member) {
  if (member.id === MOSHE_MEMBER_ID) return MOSHE_MESSAGE_LABEL[currentLocale()];
  return `${member.displayName} · ${member.roleLabel}`;
}

function assistantMessageLabel() {
  const member = activeConversationMember();
  if (state.activeTeamMentions.some(mention => mention.id === MOSHE_MEMBER_ID)) return MOSHE_MESSAGE_LABEL[currentLocale()];
  return member ? memberMessageLabel(member) : activeLocaleText("סוכן חקירה", "Investigation Agent");
}

function resultMessageLabel(result = {}) {
  return result.responding_agent === "moshe" ? MOSHE_MESSAGE_LABEL[currentLocale()] : assistantMessageLabel();
}

function appendMemberWelcomeMessage(member) {
  conversation.querySelectorAll(".member-welcome-message").forEach(message => message.remove());
  const welcome = member.id === MOSHE_MEMBER_ID ? MOSHE_WELCOME[currentLocale()] : MICHLOL_MEMBER_WELCOME[currentLocale()];
  return appendMessage("assistant", `<p>${escapeHtml(welcome)}</p>`, {
    label: memberMessageLabel(member),
    className: "member-welcome-message",
    memberId: member.id
  });
}

function selectConversationMember(memberId) {
  const member = currentMembers().find(item => item.id === memberId);
  if (!member) return;
  if (state.activeConversationMemberId === member.id) {
    if (state.workstreamComposerMode) setWorkstreamComposerMode(false);
    state.activeConversationMemberId = null;
    state.activeTeamMentions = teamMentionsForPrompt(promptInput?.value || "");
    conversation.querySelectorAll(".member-welcome-message").forEach(message => message.remove());
    renderMichlolTeam();
    updatePromptPlaceholder();
    promptInput?.focus();
    return;
  }
  if (member.id !== MOSHE_MEMBER_ID && state.workstreamComposerMode) {
    setWorkstreamComposerMode(false);
  }
  state.activeConversationMemberId = member.id;
  renderMichlolTeam();
  updatePromptPlaceholder();
  appendMemberWelcomeMessage(member);
  conversation.scrollTop = conversation.scrollHeight;
}

function applyLocaleUi() {
  document.documentElement.lang = currentLocale();
  document.documentElement.dir = currentLocale() === "en" ? "ltr" : "rtl";
  if (languageToggle) languageToggle.checked = currentLocale() === "en";
  try {
    const url = new URL(window.location.href);
    url.searchParams.set("lang", currentLocale());
    window.history.replaceState({}, "", url);
  } catch (error) {
    // Ignore URL rewrite issues and continue applying locale in-memory.
  }
  applyLocaleAttributes();
  renderSystemStatuses();
  document.title = activeLocaleText("סביבת מודיעין", "Intelligence Workspace");
  const helpButton = document.querySelector(".help-button");
  helpButton?.setAttribute("aria-label", activeLocaleText("פתח עזרה", "Open help"));
  if (helpButton) helpButton.href = `./help.html?lang=${currentLocale()}`;
  if (appHomeButton) appHomeButton.textContent = activeLocaleText("סביבת מודיעין", "Intelligence Workspace");
  const investigationLabel = document.querySelector('.investigation-switcher label[for="investigationInput"]');
  if (investigationLabel) investigationLabel.textContent = activeLocaleText("חקירה פעילה", "Active investigation");
  if (investigationInput) {
    investigationInput.setAttribute("aria-label", activeLocaleText("בחר או צור חקירה", "Choose or create an investigation"));
  }
  if (investigationAddButton) {
    investigationAddButton.title = activeLocaleText("צור חקירה חדשה", "Create a new investigation");
    investigationAddButton.setAttribute("aria-label", investigationAddButton.title);
  }
  if (promptInput) {
    promptInput.setAttribute("aria-label", activeLocaleText("שאלת חקירה", "Investigation question"));
  }
  if (recordedList && !state.savedQuestions.length) recordedList.innerHTML = `<div class="activity-empty">${activeLocaleText("לא נמצאו שאלות שמורות.", "No saved questions found.")}</div>`;
  updatePromptPlaceholder();
  renderMichlolTeam();
  renderInvestigationSelector();
  renderDraftInvestigationUi();
  renderWelcomePage();
  renderAllViews();
  if (!state.lastResult && !state.busy) setSuggestions(DEFAULT_SUGGESTIONS[currentLocale()]);
}

function createTeamMentionMenu() {
  const menu = document.createElement("div");
  menu.id = "teamMentionMenu";
  menu.className = "team-mention-menu";
  menu.setAttribute("role", "listbox");
  menu.setAttribute("aria-label", activeLocaleText("בחירת חבר מכלול", "Choose a team member"));
  menu.hidden = true;
  document.body.appendChild(menu);
  menu.addEventListener("mousedown", event => event.preventDefault());
  menu.addEventListener("click", event => {
    const option = event.target.closest("[data-team-mention-index]");
    if (!option) return;
    chooseTeamMention(Number(option.dataset.teamMentionIndex));
  });
  return menu;
}

const teamMentionMenu = createTeamMentionMenu();

function normalizeTeamMentionText(value) {
  return String(value || "").normalize("NFKC").trim().toLocaleLowerCase(currentLocaleTag());
}

function activeMentionRange(textarea) {
  const caret = textarea.selectionStart;
  if (caret == null || textarea.selectionEnd !== caret) return null;
  const beforeCaret = textarea.value.slice(0, caret);
  const match = beforeCaret.match(/(^|[\s([{])@([^\s@]*)$/u);
  if (!match) return null;
  return {
    start: caret - match[2].length - 1,
    end: caret,
    query: match[2]
  };
}

function matchingTeamMembers(query) {
  const normalized = normalizeTeamMentionText(query);
  if (!normalized) return currentMembers();
  return currentMembers().filter(member => {
    const haystack = normalizeTeamMentionText(`${member.displayName} ${member.roleLabel} ${member.id}`);
    return haystack.includes(normalized);
  });
}

function recognizedTeamMemberByMention(rawMention) {
  const normalized = normalizeTeamMentionText(rawMention).replace(/^@/, "").replace(/[^\p{L}\p{N}_-]+$/gu, "");
  if (!normalized) return null;
  return currentMembers().find(member => normalizeTeamMentionText(member.displayName) === normalized) || null;
}

function highlightedPromptHtml(value) {
  const text = String(value || "");
  if (!text) return "";
  let html = "";
  let lastIndex = 0;
  const mentionPattern = /@([\p{L}\p{N}_-]+)/gu;
  let match;
  while ((match = mentionPattern.exec(text))) {
    html += escapeHtml(text.slice(lastIndex, match.index));
    const member = recognizedTeamMemberByMention(match[0]);
    const mention = escapeHtml(match[0]);
    html += member ? `<span class="mention-highlight-token">${mention}</span>` : mention;
    lastIndex = match.index + match[0].length;
  }
  html += escapeHtml(text.slice(lastIndex));
  return html.endsWith("\n") ? `${html}\n` : html;
}

function syncMentionHighlight(textarea) {
  const highlights = textarea?.closest(".mention-editor")?.querySelector(".mention-highlights");
  if (!highlights) return;
  highlights.innerHTML = highlightedPromptHtml(textarea.value);
  highlights.scrollTop = textarea.scrollTop;
  highlights.scrollLeft = textarea.scrollLeft;
}

function enableMentionHighlight(textarea) {
  if (!textarea || textarea.dataset.mentionHighlight === "true" || !textarea.parentNode) return;
  const wrapper = document.createElement("div");
  wrapper.className = "mention-editor";
  const highlights = document.createElement("div");
  highlights.className = "mention-highlights";
  highlights.setAttribute("aria-hidden", "true");
  textarea.parentNode.insertBefore(wrapper, textarea);
  wrapper.append(highlights, textarea);
  textarea.classList.add("mention-source");
  textarea.dataset.mentionHighlight = "true";
  textarea.addEventListener("input", () => syncMentionHighlight(textarea));
  textarea.addEventListener("scroll", () => syncMentionHighlight(textarea));
  syncMentionHighlight(textarea);
}

function textareaCaretViewportRect(textarea) {
  const style = window.getComputedStyle(textarea);
  const mirror = document.createElement("div");
  const marker = document.createElement("span");
  const beforeCaret = textarea.value.slice(0, textarea.selectionStart || 0);
  const mirrorStyles = [
    "boxSizing", "width", "minHeight", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft",
    "borderTopWidth", "borderRightWidth", "borderBottomWidth", "borderLeftWidth", "fontFamily",
    "fontSize", "fontWeight", "fontStyle", "letterSpacing", "lineHeight", "textTransform",
    "textAlign", "direction", "wordSpacing", "tabSize"
  ];
  mirrorStyles.forEach(prop => {
    mirror.style[prop] = style[prop];
  });
  mirror.style.position = "fixed";
  mirror.style.top = `${textarea.getBoundingClientRect().top}px`;
  mirror.style.left = `${textarea.getBoundingClientRect().left}px`;
  mirror.style.height = "auto";
  mirror.style.overflow = "hidden";
  mirror.style.visibility = "hidden";
  mirror.style.whiteSpace = "pre-wrap";
  mirror.style.overflowWrap = "break-word";
  mirror.style.pointerEvents = "none";
  mirror.textContent = beforeCaret || "";
  marker.textContent = "\u200b";
  mirror.appendChild(marker);
  document.body.appendChild(mirror);
  const markerRect = marker.getBoundingClientRect();
  const caretRect = {
    top: markerRect.top - textarea.scrollTop,
    right: markerRect.right - textarea.scrollLeft,
    bottom: markerRect.bottom - textarea.scrollTop,
    left: markerRect.left - textarea.scrollLeft
  };
  mirror.remove();
  return caretRect;
}

function positionTeamMentionMenu(textarea) {
  if (!teamMentionMenu || teamMentionMenu.hidden) return;
  const rect = textarea.getBoundingClientRect();
  const caretRect = textareaCaretViewportRect(textarea);
  const width = Math.min(260, Math.max(180, window.innerWidth - 24));
  teamMentionMenu.style.width = `${width}px`;
  const measuredHeight = Math.min(teamMentionMenu.offsetHeight || 186, 186);
  const anchorTop = Number.isFinite(caretRect.top) ? Math.max(rect.top, Math.min(caretRect.top, rect.bottom)) : rect.top;
  const anchorBottom = Number.isFinite(caretRect.bottom) ? Math.max(rect.top, Math.min(caretRect.bottom, rect.bottom)) : rect.bottom;
  const anchorRight = Number.isFinite(caretRect.right) ? Math.max(rect.left, Math.min(caretRect.right, rect.right)) : rect.right;
  const mobile = window.innerWidth <= 760;
  const belowTop = mobile ? rect.bottom + 8 : anchorBottom + 8;
  const aboveTop = mobile ? rect.top - measuredHeight - 8 : anchorTop - measuredHeight - 8;
  const hasRoomAbove = aboveTop >= 12;
  const hasRoomBelow = belowTop + measuredHeight <= window.innerHeight - 12;
  const top = mobile && hasRoomAbove ? aboveTop : (hasRoomBelow ? belowTop : Math.max(12, aboveTop));
  const left = Math.max(12, Math.min(anchorRight - width, window.innerWidth - width - 12));
  teamMentionMenu.style.top = `${Math.round(top)}px`;
  teamMentionMenu.style.left = `${Math.round(left)}px`;
}

function renderTeamMentionMenu() {
  if (!teamMentionMenu || !teamMentionState.textarea || !teamMentionState.matches.length) {
    closeTeamMentionMenu();
    return;
  }
  teamMentionMenu.innerHTML = teamMentionState.matches.map((member, index) => `
    <button type="button" role="option" class="team-mention-option ${index === teamMentionState.activeIndex ? "active" : ""}" data-team-mention-index="${index}" aria-selected="${index === teamMentionState.activeIndex ? "true" : "false"}">
      ${michlolAvatarHtml(member)}
      <span class="team-mention-main">
        <span class="team-mention-name">${escapeHtml(member.displayName)}</span>
        <span class="team-mention-role">${escapeHtml(member.roleLabel)}</span>
      </span>
    </button>`).join("");
  teamMentionMenu.hidden = false;
  positionTeamMentionMenu(teamMentionState.textarea);
  const activeOption = teamMentionMenu.querySelector(".team-mention-option.active");
  activeOption?.scrollIntoView({ block: "nearest" });
}

function updateTeamMentionMenu(textarea) {
  const range = activeMentionRange(textarea);
  if (!range) {
    closeTeamMentionMenu();
    return;
  }
  const matches = matchingTeamMembers(range.query);
  if (!matches.length) {
    closeTeamMentionMenu();
    return;
  }
  teamMentionState.textarea = textarea;
  teamMentionState.range = range;
  teamMentionState.matches = matches;
  teamMentionState.activeIndex = Math.min(teamMentionState.activeIndex, matches.length - 1);
  renderTeamMentionMenu();
}

function closeTeamMentionMenu() {
  if (teamMentionMenu) {
    teamMentionMenu.hidden = true;
    teamMentionMenu.innerHTML = "";
  }
  teamMentionState.textarea = null;
  teamMentionState.range = null;
  teamMentionState.matches = [];
  teamMentionState.activeIndex = 0;
}

function chooseTeamMention(index = teamMentionState.activeIndex) {
  const textarea = teamMentionState.textarea;
  const range = teamMentionState.range;
  const member = teamMentionState.matches[index];
  if (!textarea || !range || !member) return;
  const before = textarea.value.slice(0, range.start);
  const after = textarea.value.slice(range.end);
  const mentionText = `@${member.displayName}`;
  const spacing = after.startsWith(" ") || after.startsWith("\n") || !after ? " " : "";
  const nextValue = `${before}${mentionText}${spacing}${after}`;
  const caret = before.length + mentionText.length + spacing.length;
  textarea.value = nextValue;
  textarea.focus();
  textarea.setSelectionRange(caret, caret);
  state.activeTeamMentions = teamMentionsForPrompt(textarea.value);
  syncMentionHighlight(textarea);
  closeTeamMentionMenu();
}

function handleTeamMentionKeydown(event) {
  if (!teamMentionState.textarea || event.target !== teamMentionState.textarea || teamMentionMenu.hidden) return false;
  if (event.key === "ArrowDown") {
    event.preventDefault();
    teamMentionState.activeIndex = (teamMentionState.activeIndex + 1) % teamMentionState.matches.length;
    renderTeamMentionMenu();
    return true;
  }
  if (event.key === "ArrowUp") {
    event.preventDefault();
    teamMentionState.activeIndex = (teamMentionState.activeIndex - 1 + teamMentionState.matches.length) % teamMentionState.matches.length;
    renderTeamMentionMenu();
    return true;
  }
  if (event.key === "Enter" || event.key === "Tab") {
    event.preventDefault();
    chooseTeamMention();
    return true;
  }
  if (event.key === "Escape") {
    event.preventDefault();
    closeTeamMentionMenu();
    return true;
  }
  return false;
}

function attachTeamMentionAutocomplete(textarea) {
  if (!textarea) return;
  textarea.setAttribute("aria-autocomplete", "list");
  textarea.setAttribute("aria-controls", "teamMentionMenu");
  textarea.addEventListener("input", () => {
    state.activeTeamMentions = teamMentionsForPrompt(textarea.value);
    syncMentionHighlight(textarea);
    updateTeamMentionMenu(textarea);
  });
  textarea.addEventListener("click", () => updateTeamMentionMenu(textarea));
  textarea.addEventListener("keyup", event => {
    if (["ArrowDown", "ArrowUp", "Enter", "Tab", "Escape"].includes(event.key)) return;
    updateTeamMentionMenu(textarea);
  });
  textarea.addEventListener("blur", () => {
    setTimeout(() => {
      if (document.activeElement?.closest?.("#teamMentionMenu")) return;
      closeTeamMentionMenu();
    }, 100);
  });
}

function teamMentionsForPrompt(prompt) {
  const mentions = [];
  const seen = new Set();
  const mentionPattern = /@([\p{L}\p{N}_-]+)/gu;
  let match;
  while ((match = mentionPattern.exec(prompt || ""))) {
    const query = normalizeTeamMentionText(match[1]);
    const member = currentMembers().find(item => normalizeTeamMentionText(item.displayName) === query);
    if (!member || seen.has(member.id)) continue;
    seen.add(member.id);
    mentions.push({
      id: member.id,
      display_name: member.displayName,
      role_label: member.roleLabel,
      member_type: member.memberType
    });
  }
  return mentions;
}

function addressedPromptForSelectedMember(prompt) {
  const clean = String(prompt || "").trim();
  if (!clean || teamMentionsForPrompt(clean).length) return clean;
  const member = activeConversationMember();
  return member ? `@${member.displayName} ${clean}` : clean;
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  let atFieldStart = true;
  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];
    if (char === '"' && quoted && next === '"') { cell += '"'; i += 1; }
    else if (char === '"' && quoted) quoted = false;
    else if (char === '"' && atFieldStart) { quoted = true; atFieldStart = false; }
    else if (char === ',' && !quoted) { row.push(cell); cell = ""; atFieldStart = true; }
    else if ((char === '\n' || char === '\r') && !quoted) {
      if (char === '\r' && next === '\n') i += 1;
      row.push(cell);
      if (row.some(value => value !== "")) rows.push(row);
      row = [];
      cell = "";
      atFieldStart = true;
    } else {
      cell += char;
      atFieldStart = false;
    }
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
  const idsInAnswer = new Set((result.answer || "").match(/\bLOC-(?:V2-)?\d{3}\b/g) || []);
  if (idsInAnswer.size) {
    locations = locations.filter(item => idsInAnswer.has(item.location_id) || !String(item.location_id || "").match(/^LOC-(?:V2-)?\d{3}$/));
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
    const sourceType = event.source_type || "מקור לא ידוע";
    if (!grouped.has(sourceType)) grouped.set(sourceType, []);
    grouped.get(sourceType).push(event);
  });
  return [...grouped.entries()]
    .sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0], "he"))
    .map(([sourceType, items]) => ({
      dataId: layerId("events", sourceType),
      label: sourceType,
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

function buildCatalogLayer(layer, rows = []) {
  const items = layer.kind === "events"
    ? rows.map(item => ({ ...item, date: new Date(item.timestamp_utc) }))
    : rows;
  return {
    dataId: layer.id,
    label: layer.label,
    kind: layer.kind,
    visible: true,
    items,
    capabilities: layer.capabilities || { table: true, map: false, timeline: false },
    catalogLayerId: layer.id
  };
}

function buildTypedResultLayers(result = {}) {
  return (result.requested_result_layers || [])
    .filter(layer => layer && Array.isArray(layer.rows) && layer.rows.length)
    .map(layer => ({
      dataId: layer.id || layerId(layer.kind, "result"),
      label: layer.label || "תוצאות הסוכן",
      kind: layer.kind,
      visible: true,
      items: layer.kind === "events"
        ? layer.rows.map(item => ({ ...item, date: new Date(item.timestamp_utc) }))
        : layer.rows,
      capabilities: layer.capabilities || { table: true, map: false, timeline: false },
      preferredView: layer.recommended_view
    }));
}

function buildEvidenceReferenceLayers(result = {}) {
  return (result.evidence_reference_layers || [])
    .filter(layer => layer && Array.isArray(layer.rows) && layer.rows.length)
    .map(layer => ({
      dataId: layer.id || layerId(layer.kind, "evidence"),
      label: layer.label || "ראיות תומכות",
      kind: layer.kind,
      visible: true,
      items: layer.kind === "events"
        ? layer.rows.map(item => ({ ...item, date: new Date(item.timestamp_utc) }))
        : layer.rows,
      capabilities: layer.capabilities || { table: true, map: false, timeline: false },
      preferredView: layer.recommended_view
    }));
}

function evidenceLayerIdentifiers(layer) {
  const keysByKind = {
    events: ["event_id", "record_id"],
    locations: ["location_id", "key"],
    location_metadata: ["location_id"],
    entity_metadata: ["entity_id"],
    attack_targets: ["target_id"],
    time_aggregation: ["key", "sortKey", "label"],
    group_aggregation: ["key", "label"]
  };
  const keys = keysByKind[layer.kind] || ["event_id", "location_id", "entity_id", "target_id", "key"];
  return [...new Set((layer.items || []).map(item => {
    const key = keys.find(candidate => item?.[candidate] != null && String(item[candidate]).trim());
    return key ? String(item[key]).trim() : "";
  }).filter(Boolean))];
}

function evidenceLayerSourceId(result, layer) {
  return sanitizeLayerKey(`evidence:${finalSourceId(result)}:${layer.dataId}`);
}

function updateEvidenceReferenceButton(btn) {
  const sourceLayers = state.layers.filter(layer => layer.sourceId === btn.dataset.sourceId);
  const visible = sourceLayers.some(layer => layer.visible);
  btn.classList.toggle("is-visible", visible);
  btn.setAttribute("aria-pressed", visible ? "true" : "false");
  btn.title = visible ? "Hide evidence layer" : "Show evidence layer";
}

function updateEvidenceReferenceButtons() {
  document.querySelectorAll(".evidence-reference-link").forEach(updateEvidenceReferenceButton);
}

function toggleEvidenceReferenceLayer(result, layer, btn) {
  const sourceId = evidenceLayerSourceId(result, layer);
  const existing = state.layers.filter(item => item.sourceId === sourceId);
  if (existing.some(item => item.visible)) {
    existing.forEach(item => { item.visible = false; });
    updateEvidenceReferenceButton(btn);
    renderAllViews();
    return;
  }
  addResultLayers({
    sourceId,
    sourceLabel: `Evidence: ${layer.label}`,
    preferredView: layer.preferredView,
    layers: [layer]
  });
  state.rawOverlayMinimized = false;
  activateView(layer.preferredView, { reason: `Evidence layer: ${layer.label}` });
  renderAllViews();
  updateEvidenceReferenceButtons();
}

function buildEvidenceReferencesSection(result) {
  const layers = buildEvidenceReferenceLayers(result);
  if (!layers.length) return null;
  const section = document.createElement("details");
  section.className = "evidence-references";
  section.innerHTML = `
    <summary class="evidence-references-summary">Evidence IDs · ${layers.length.toLocaleString("en-US")} layers</summary>
    <ul class="evidence-reference-list"></ul>`;
  const list = section.querySelector(".evidence-reference-list");
  layers.forEach(layer => {
    const identifiers = evidenceLayerIdentifiers(layer);
    const shown = identifiers.slice(0, 14);
    const overflow = Math.max(0, identifiers.length - shown.length);
    const item = document.createElement("li");
    item.className = "evidence-reference-item";
    item.innerHTML = `
      <details class="evidence-reference-details">
        <summary class="evidence-reference-link" aria-pressed="false">
          <span class="evidence-reference-label">${escapeHtml(layer.label)}</span>
          <span class="evidence-reference-view">${layer.preferredView === "timeline" ? "Timeline" : "Map"} · ${(layer.items || []).length.toLocaleString("en-US")}</span>
        </summary>
        ${shown.length ? `<div class="evidence-reference-identifiers" dir="ltr">${shown.map(escapeHtml).join(", ")}${overflow ? ` <span dir="ltr">and ${overflow.toLocaleString("en-US")} more</span>` : ""}</div>` : ""}
      </details>`;
    const btn = item.querySelector(".evidence-reference-link");
    btn.dataset.sourceId = evidenceLayerSourceId(result, layer);
    btn.title = "Show evidence layer";
    btn.addEventListener("click", () => toggleEvidenceReferenceLayer(result, layer, btn));
    list.appendChild(item);
  });
  return section;
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
    existingSourceLayers.forEach(layer => {
      ensureLayerFilterState(layer);
      layer.visible = true;
    });
  }

  layers.forEach(layer => {
    if (layer.kind === "attack_targets") {
      const incomingIds = new Set((layer.items || []).map(item => item.target_id).filter(Boolean));
      state.layers.forEach(existingLayer => {
        if (existingLayer.kind !== "attack_targets" || existingLayer.sourceId === cleanSourceId) return;
        existingLayer.items = (existingLayer.items || []).filter(item => !incomingIds.has(item.target_id));
      });
      state.layers = state.layers.filter(existingLayer => existingLayer.kind !== "attack_targets" || existingLayer.items.length);
    }
    const dataId = layer.dataId || layer.id || layerId(layer.kind, layer.label);
    const id = `${cleanSourceId}::${sanitizeLayerKey(dataId)}`;
    const existing = state.layers.find(item => item.id === id);
    if (existing) {
      ensureLayerFilterState(existing);
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
      preferredView: layer.preferredView || preferredView,
      color: nextLayerColor(),
      visible: true
    };
    ensureLayerFilterState(next);
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

function ensureLayerFilterState(layer) {
  if (!layer) return null;
  if (!Array.isArray(layer.draftFilters)) layer.draftFilters = [];
  if (!Array.isArray(layer.appliedFilters)) layer.appliedFilters = [];
  if (typeof layer.filterError !== "string") layer.filterError = "";
  if (typeof layer.filterPanelOpen !== "boolean") layer.filterPanelOpen = false;
  return layer;
}

function createFilterId() {
  return `filter:${Date.now()}:${Math.random().toString(16).slice(2)}`;
}

function cloneFilter(filter = {}) {
  return {
    id: filter.id || createFilterId(),
    field: filter.field || "",
    value: stringifyFilterValue(filter.value)
  };
}

function cloneFilters(filters = []) {
  return filters.map(filter => cloneFilter(filter));
}

function filterFieldPathsForValue(value, prefix = "", fields = new Set(), depth = 0) {
  if (value === null || value === undefined) return fields;
  if (value instanceof Date) {
    if (prefix) fields.add(prefix);
    return fields;
  }
  if (Array.isArray(value)) {
    if (prefix) fields.add(prefix);
    return fields;
  }
  if (typeof value !== "object") {
    if (prefix) fields.add(prefix);
    return fields;
  }
  Object.keys(value).forEach(key => {
    const path = prefix ? `${prefix}.${key}` : key;
    const child = value[key];
    if (child && typeof child === "object" && !Array.isArray(child) && depth < 2) {
      filterFieldPathsForValue(child, path, fields, depth + 1);
    } else {
      fields.add(path);
    }
  });
  if (prefix && !Object.keys(value).length) fields.add(prefix);
  return fields;
}

function filterFieldsForLayer(layer) {
  ensureLayerFilterState(layer);
  const fields = new Set();
  (layer?.items || []).forEach(item => filterFieldPathsForValue(item, "", fields));
  return [...fields].sort((a, b) => a.localeCompare(b, "en"));
}

function valueForFilterField(item, field) {
  if (!field) return "";
  return String(field).split(".").reduce((value, key) => {
    if (value === null || value === undefined) return undefined;
    return value[key];
  }, item);
}

function stringifyFilterValue(value) {
  if (value === null || value === undefined) return "";
  if (value instanceof Date) return value.toISOString();
  if (Array.isArray(value)) return value.map(item => stringifyFilterValue(item)).filter(Boolean).join(" ");
  if (typeof value === "object") {
    return Object.keys(value)
      .sort((a, b) => a.localeCompare(b, "en"))
      .map(key => stringifyFilterValue(value[key]))
      .filter(Boolean)
      .join(" ");
  }
  return String(value);
}

function normalizeFilterText(value) {
  return stringifyFilterValue(value).trim().replace(/\s+/g, " ").toLocaleLowerCase("en-US");
}

function validAppliedFilters(layer) {
  ensureLayerFilterState(layer);
  return (layer?.appliedFilters || []).filter(filter => filter?.field && normalizeFilterText(filter.value));
}

function layerHasAppliedFilters(layer) {
  return validAppliedFilters(layer).length > 0;
}

function filterMatchesItem(item, filter) {
  const needle = normalizeFilterText(filter.value);
  if (!filter.field || !needle) return true;
  return normalizeFilterText(valueForFilterField(item, filter.field)).includes(needle);
}

function itemsForLayerPresentation(layer) {
  ensureLayerFilterState(layer);
  const items = layer?.items || [];
  const filters = validAppliedFilters(layer);
  if (!filters.length) return items;
  return items.filter(item => filters.every(filter => filterMatchesItem(item, filter)));
}

function targetQuantityLabel(target = {}) {
  const min = target.count_min;
  const max = target.count_max;
  const estimate = target.count_estimate;
  if (target.count_assessment === "range" && min != null && max != null) return `${Number(min).toLocaleString("en-US")}–${Number(max).toLocaleString("en-US")}`;
  if (estimate != null) return `${target.count_assessment === "approximate" ? "~" : ""}${Number(estimate).toLocaleString("en-US")}`;
  if (min != null && max != null && min !== max) return `${Number(min).toLocaleString("en-US")}–${Number(max).toLocaleString("en-US")}`;
  if (min != null) return Number(min).toLocaleString("en-US");
  if (max != null) return Number(max).toLocaleString("en-US");
  return "Undetermined";
}

function confidenceLabel(value) {
  return value === "high" ? "High" : value === "medium" ? "Medium" : (value || "-");
}

function identifiersForLayerContext(layer, items, limit = 80) {
  const idFields = layer?.kind === "entity_metadata"
    ? ["entity_id"]
    : layer?.kind === "location_metadata" || layer?.kind === "locations"
      ? ["location_id", "key"]
      : ["event_id", "location_id", "entity_id"];
  const seen = new Set();
  const ids = [];
  items.forEach(item => {
    idFields.forEach(field => {
      const value = item?.[field];
      if (!value || seen.has(value) || ids.length >= limit) return;
      seen.add(value);
      ids.push(value);
    });
  });
  return ids;
}

function selectedLayerContextForAgent() {
  return state.layers
    .filter(layer => state.promptSelectedLayerIds.has(layer.id) && layer.capabilities?.table)
    .slice(0, 8)
    .map(layer => {
      const filteredItems = itemsForLayerPresentation(layer);
      const appliedFilters = validAppliedFilters(layer).map(filter => ({
        field: filter.field,
        operator: "contains",
        value: stringifyFilterValue(filter.value)
      }));
      const firstItem = filteredItems[0] || (layer.items || [])[0] || {};
      const sourceType = layer.source_type
        || firstItem.source_type
        || (String(layer.catalogLayerId || "").startsWith("events:") ? String(layer.catalogLayerId).slice("events:".length) : "");
      return {
        id: layer.id,
        label: layer.label,
        kind: layer.kind,
        catalog_layer_id: layer.catalogLayerId || layer.dataId || "",
        source_type: sourceType,
        original_count: (layer.items || []).length,
        filtered_count: filteredItems.length,
        applied_filters: appliedFilters,
        sample_ids: identifiersForLayerContext(layer, filteredItems)
      };
    });
}

function normalizeMemoryList(value) {
  return Array.isArray(value) ? value.filter(item => item && typeof item === "object") : [];
}

function currentSavedMemory() {
  const memory = state.investigationMemory?.memory;
  return memory && typeof memory === "object" ? memory : { chat_summaries: [], layers: [] };
}

function normalizeSavedMemoryForAgent(memory = currentSavedMemory()) {
  const chatSummaries = normalizeMemoryList(memory.chat_summaries).slice(-8).map(item => ({
    id: item.id || "",
    kind: item.kind || "chat_result_summary",
    saved_at_utc: item.saved_at_utc || "",
    prompt: item.prompt || "",
    answer_summary: item.answer_summary || item.answer_preview || "",
    answer_preview: item.answer_preview || "",
    source_run_id: item.source_run_id || "",
    recommended_view: item.recommended_view || "",
    step_count: Number(item.step_count || 0),
    evidence_ids: Array.isArray(item.evidence_ids) ? item.evidence_ids.slice(0, 80) : []
  }));
  const layers = normalizeMemoryList(memory.layers).slice(-12).map(item => ({
    id: item.id || "",
    kind: item.kind || "layer_filter_state",
    saved_at_utc: item.saved_at_utc || "",
    layer_id: item.layer_id || "",
    label: item.label || "",
    layer_kind: item.layer_kind || item.kind || "",
    catalog_layer_id: item.catalog_layer_id || "",
    data_id: item.data_id || "",
    source_id: item.source_id || "",
    source_label: item.source_label || "",
    source_type: item.source_type || "",
    original_count: Number(item.original_count || 0),
    filtered_count: Number(item.filtered_count || 0),
    applied_filters: normalizeMemoryList(item.applied_filters).slice(0, 20).map(filter => ({
      field: filter.field || "",
      operator: filter.operator || "contains",
      value: stringifyFilterValue(filter.value)
    })).filter(filter => filter.field && filter.value),
    sample_ids: Array.isArray(item.sample_ids) ? item.sample_ids.slice(0, 80) : [],
    restore_status: item.restore_status || ""
  }));
  return {
    chat_summaries: chatSummaries,
    layers
  };
}

function investigationMemoryForAgent() {
  const memory = normalizeSavedMemoryForAgent();
  if (!memory.chat_summaries.length && !memory.layers.length) return null;
  return memory;
}

function filtersFromSavedMemory(savedLayer) {
  return normalizeMemoryList(savedLayer?.applied_filters).map(filter => ({
    id: createFilterId(),
    field: filter.field || "",
    value: stringifyFilterValue(filter.value)
  })).filter(filter => filter.field && normalizeFilterText(filter.value));
}

function applySavedFiltersToLayer(layer, savedLayer) {
  if (!layer) return;
  ensureLayerFilterState(layer);
  const filters = filtersFromSavedMemory(savedLayer);
  layer.appliedFilters = cloneFilters(filters);
  layer.draftFilters = cloneFilters(filters);
  layer.filterError = "";
  layer.investigation_memory_layer_id = savedLayer.id || true;
}

async function restoreMemorySavedLayers(memoryPayload, token) {
  const savedLayers = normalizeMemoryList(memoryPayload?.memory?.layers);
  if (!savedLayers.length) {
    renderAllViews();
    return;
  }
  const restoredMemoryLayers = [];
  for (const savedLayer of savedLayers) {
    if (token !== state.investigationMemoryLoadToken) return;
    const catalogLayerId = savedLayer.catalog_layer_id || "";
    if (!catalogLayerId) {
      restoredMemoryLayers.push({ ...savedLayer, restore_status: "context_only" });
      continue;
    }
    const openedLayer = await openCatalogLayer(catalogLayerId, {
      silent: true,
      savedLayer
    });
    restoredMemoryLayers.push({
      ...savedLayer,
      restore_status: openedLayer ? "opened" : "unavailable"
    });
  }
  if (token !== state.investigationMemoryLoadToken) return;
  const memory = memoryPayload.memory || {};
  state.investigationMemory = {
    ...memoryPayload,
    memory: {
      chat_summaries: normalizeMemoryList(memory.chat_summaries),
      layers: restoredMemoryLayers
    }
  };
  renderAllViews();
  renderLayerSelector();
  renderQueryLayersModal();
}

async function loadInvestigationMemory(options = {}) {
  if (!state.investigationId) return null;
  const token = ++state.investigationMemoryLoadToken;
  state.investigationMemoryLoading = true;
  state.investigationMemoryError = "";
  try {
    const response = await fetch(`/api/investigation-memory?id=${encodeURIComponent(state.investigationId)}`, { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("טעינת זיכרון החקירה נכשלה", "Failed to load investigation memory"));
    if (token !== state.investigationMemoryLoadToken) return null;
    state.investigationMemory = payload;
    if (options.restoreLayers) await restoreMemorySavedLayers(payload, token);
    return payload;
  } catch (error) {
    if (token === state.investigationMemoryLoadToken) {
      state.investigationMemoryError = error.message || activeLocaleText("טעינת זיכרון החקירה נכשלה", "Failed to load investigation memory");
      state.investigationMemory = null;
    }
    return null;
  } finally {
    if (token === state.investigationMemoryLoadToken) {
      state.investigationMemoryLoading = false;
    }
  }
}

function layerMemoryPayload(layer) {
  ensureLayerFilterState(layer);
  const filteredItems = itemsForLayerPresentation(layer);
  const appliedFilters = validAppliedFilters(layer).map(filter => ({
    field: filter.field,
    operator: "contains",
    value: stringifyFilterValue(filter.value)
  }));
  const firstItem = filteredItems[0] || (layer.items || [])[0] || {};
  const sourceType = layer.source_type
    || firstItem.source_type
    || (String(layer.catalogLayerId || "").startsWith("events:") ? String(layer.catalogLayerId).slice("events:".length) : "");
  return {
    id: layer.id,
    label: layer.label,
    kind: layer.kind,
    catalog_layer_id: layer.catalogLayerId || "",
    data_id: layer.dataId || "",
    source_id: layer.sourceId || "",
    source_label: layer.sourceLabel || "",
    source_type: sourceType,
    original_count: (layer.items || []).length,
    filtered_count: filteredItems.length,
    applied_filters: appliedFilters,
    sample_ids: identifiersForLayerContext(layer, filteredItems)
  };
}

function canSaveLayerToMemory(layer) {
  return Boolean(
    state.investigationId
    && layer
    && layer.capabilities?.table
    && layer.label
    && !layer.investigation_memory_layer_id
  );
}

async function saveLayerToInvestigationMemory(layer, button) {
  if (state.draftSessionActive) {
    openDraftCreateModal(() => saveLayerToInvestigationMemory(layer, button));
    return;
  }
  if (!canSaveLayerToMemory(layer) || state.busy || button?.dataset.memorySaving === "true") return;
  button.dataset.memorySaving = "true";
  button.title = "Saving layer to investigation memory";
  button.setAttribute("aria-label", "Saving layer to investigation memory");
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch("/api/investigation-memory/layer", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      signal: controller.signal,
      body: JSON.stringify({
        investigation_id: state.investigationId,
        name: state.investigationName,
        layer: layerMemoryPayload(layer),
      }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("שמירת השכבה לזיכרון נכשלה", "Failed to save layer to memory"));
    layer.investigation_memory_layer_id = payload.saved?.id || true;
    button.title = activeLocaleText("השכבה נשמרה בזיכרון החקירה", "Layer saved to investigation memory");
    button.setAttribute("aria-label", button.title);
    renderEvidence();
  } catch (error) {
    button.title = error.name === "AbortError"
      ? activeLocaleText("שמירת השכבה ארכה יותר מדי זמן. נסו שוב.", "Saving the layer took too long. Try again.")
      : error.message;
    button.setAttribute("aria-label", button.title);
  } finally {
    clearTimeout(timeout);
    delete button.dataset.memorySaving;
  }
}

function renderSelectedLayersButton() {
  if (!selectedLayersButton || !selectedLayersLabel || !selectedLayersSummary) return;
  const layers = state.layers.filter(layer => state.promptSelectedLayerIds.has(layer.id) && layer.capabilities?.table);
  selectedLayersButton.classList.toggle("has-layers", layers.length > 0);
  selectedLayersButton.hidden = layers.length === 0;
  if (!layers.length) {
    selectedLayersLabel.textContent = "";
    selectedLayersSummary.textContent = "";
    selectedLayersButton.title = activeLocaleText("בחר שכבות לשאילתה", "Choose layers for the query");
    return;
  }
  const preview = layers.slice(0, 2).map(layer => layer.label).join(" · ");
  const remaining = layers.length > 2 ? ` +${layers.length - 2}` : "";
  selectedLayersLabel.textContent = state.workstreamComposerMode
    ? activeLocaleText("שכבת מעקב", "Workstream layer")
    : (layers.length === 1
      ? activeLocaleText("נבחרה שכבה אחת", "1 layer selected")
      : activeLocaleText(`${layers.length.toLocaleString(currentLocaleTag())} שכבות נבחרו`, `${layers.length.toLocaleString(currentLocaleTag())} layers selected`));
  selectedLayersSummary.textContent = `${preview}${remaining}`;
  selectedLayersButton.title = activeLocaleText(
    `שנה שכבות לשאילתה: ${layers.map(layer => layer.label).join(", ")}`,
    `Change query layers: ${layers.map(layer => layer.label).join(", ")}`
  );
}

function clearPromptLayerSelection() {
  state.promptSelectedLayerIds = new Set();
  renderSelectedLayersButton();
  renderQueryLayersModal();
}

function selectedLayerContextText(layers) {
  if (!layers.length) return "";
  const lines = [
    "Interface-selected layer context:",
    "Treat these layers as context and as the filters the analyst chose before sending the question. If the question refers to the current results/layers/selection, use them to narrow the search."
  ];
  layers.forEach(layer => {
    const count = layer.applied_filters.length
      ? `${layer.filtered_count}/${layer.original_count}`
      : String(layer.original_count);
    const source = layer.source_type ? `, source_type=${layer.source_type}` : "";
    const filters = layer.applied_filters.length
      ? `, filters=${layer.applied_filters.map(filter => `${filter.field} contains ${filter.value}`).join("; ")}`
      : "";
    const ids = layer.sample_ids.length ? `, sample_ids=${layer.sample_ids.join(", ")}` : "";
    const more = layer.filtered_count > layer.sample_ids.length ? `, sample_ids_are_partial=true` : "";
    lines.push(`- ${layer.label} (${layer.kind}, ${layer.catalog_layer_id || "no-catalog-id"}): ${count} records${source}${filters}${ids}${more}`);
  });
  return lines.join("\n");
}

function promptForAgentWithSelectedLayers(prompt, selectedLayers) {
  const context = selectedLayerContextText(selectedLayers);
  return [prompt, context, TEAM_MENTION_AGENT_INSTRUCTION].filter(Boolean).join("\n\n");
}

function promptForAgent(prompt) {
  return [prompt, TEAM_MENTION_AGENT_INSTRUCTION].filter(Boolean).join("\n\n");
}

function investigationStateForPrompt(selectedLayers) {
  const savedMemory = investigationMemoryForAgent();
  if (!selectedLayers.length && !savedMemory) return null;
  const userTurns = state.history.filter(item => item.role === "user").length + 1;
  const invState = { turn: userTurns };
  if (selectedLayers.length) invState.selected_layers = selectedLayers;
  if (savedMemory) invState.saved_memory = savedMemory;
  return invState;
}

function workstreamContextForChat(messageId) {
  const workstreams = activeWorkstreams();
  if (workstreams.length !== 1) return null;
  return {
    workstream_id: workstreams[0].workstream_id,
    pending_proposal: state.pendingMosheWorkstreamProposal,
    current_turn_message_id: messageId
  };
}

function applyWorkstreamChatResult(result) {
  if (result.workstream_created) {
    result.workstream_recording = { kind: "creation", workstream: result.workstream_created };
    state.workstreams = [
      result.workstream_created,
      ...state.workstreams.filter(item => item.workstream_id !== result.workstream_created.workstream_id)
    ];
    setWorkstreamComposerMode(false);
    renderWorkstreamIndicator();
  }
  if (result.workstream_proposal) {
    state.pendingMosheWorkstreamProposal = result.workstream_proposal;
  }
  const decision = result.workstream_action?.decision;
  if (decision === "reject") state.pendingMosheWorkstreamProposal = null;
  if (decision === "correct" && result.workstream_action?.proposal) {
    state.pendingMosheWorkstreamProposal = result.workstream_action.proposal;
  }
  if (result.workstream_artifact) {
    state.pendingMosheWorkstreamProposal = null;
    result.answer = `${result.answer}\n\nThe change was saved to the workstream (revision ${result.workstream_artifact.revision}).`;
    void loadWorkstreams();
  } else if (result.workstream_conflict?.error) {
    result.answer = `${result.answer}\n\nI did not save the change: ${result.workstream_conflict.error}`;
  }
}

function normalizeInvestigationName(name) {
  return String(name || "").replace(/\s+/g, " ").trim();
}

function investigationNameKey(name) {
  return normalizeInvestigationName(name).toLocaleLowerCase("he-IL");
}

function saveInvestigationRegistry() {
  try {
    localStorage.setItem(INVESTIGATIONS_STORAGE_KEY, JSON.stringify({
      active_id: state.investigationId,
      investigations: state.investigations
    }));
  } catch (error) {
    console.warn("Could not save investigations", error);
  }
}

function createInvestigationRecord(name) {
  const safeName = normalizeInvestigationName(name) || defaultInvestigationName();
  return {
    id: createInvestigationId(),
    name: safeName,
    created_at: new Date().toISOString()
  };
}

function ensureInvestigationRecord(name) {
  const safeName = normalizeInvestigationName(name) || defaultInvestigationName();
  const existing = state.investigations.find(item => investigationNameKey(item.name) === investigationNameKey(safeName));
  if (existing) return existing;
  const created = createInvestigationRecord(safeName);
  state.investigations.push(created);
  saveInvestigationRegistry();
  void registerInvestigationRecord(created);
  return created;
}

const SIMILAR_INVESTIGATIONS = [
  {
    id: "regional-infrastructure",
    titleHe: "תשתיות קריטיות בצפון קוסובו",
    titleEn: "Critical infrastructure in North Kosovo",
    summaryHe: "מעקב אזורי אחר שיבושים, חסימות ודפוסי פעילות סביב תשתיות חיוניות.",
    summaryEn: "Regional monitoring of disruptions, roadblocks, and activity around critical infrastructure.",
    reasonHe: "חפיפה גאוגרפית גבוהה",
    reasonEn: "High geographic overlap",
    participants: 2,
    action: "request"
  },
  {
    id: "cross-border-movement",
    titleHe: "תנועות חוצות גבול במערב הבלקן",
    titleEn: "Cross-border movement in the Western Balkans",
    summaryHe: "חקירה משותפת של דיווחי תנועה, נתיבי מעבר וסימנים מקדימים להסלמה.",
    summaryEn: "A collaborative investigation of movement reports, transit routes, and escalation indicators.",
    reasonHe: "נושאים ומקורות משותפים",
    reasonEn: "Shared topics and sources",
    participants: 3,
    action: "join"
  },
  {
    id: "information-environment",
    titleHe: "סביבת המידע וההשפעה האזורית",
    titleEn: "Regional information and influence environment",
    summaryHe: "זיהוי נרטיבים מתואמים, שמועות חוזרות וקשרים בין ערוצי הפצה.",
    summaryEn: "Identifying coordinated narratives, recurring rumors, and relationships between distribution channels.",
    reasonHe: "התאמה לתחום המומחיות שלך",
    reasonEn: "Matches your expertise",
    participants: 6,
    action: "request"
  }
];

function welcomeAvatarHtml(member) {
  return `<span class="ribbon-avatar" title="${escapeHtml(`${member.displayName} · ${member.roleLabel}`)}"><span>${escapeHtml(member.initial)}</span><img src="${escapeHtml(member.avatar)}" alt="" onerror="this.remove()"></span>`;
}

function welcomeParticipantsHtml(count = currentMembers().length) {
  const participantCount = Math.max(0, Number(count) || 0);
  const members = currentMembers().slice(0, Math.min(5, participantCount));
  return `
    <div class="ribbon-participants">
      <span class="ribbon-label">${activeLocaleText("משתתפים", "Participants")}</span>
      <div class="ribbon-avatar-row">
        ${members.map(welcomeAvatarHtml).join("")}
        <span class="ribbon-participant-count">${participantCount.toLocaleString(currentLocaleTag())}</span>
      </div>
    </div>`;
}

function ownedInvestigationRibbonHtml(investigation, index) {
  const progress = Math.max(42, 68 - (index * 9));
  const openLabel = activeLocaleText(`פתח את ${investigation.name}`, `Open ${investigation.name}`);
  return `
    <article class="investigation-ribbon" data-owned-investigation-id="${escapeHtml(investigation.id)}">
      <button class="ribbon-main-action" type="button" data-open-investigation="${escapeHtml(investigation.id)}" aria-label="${escapeHtml(openLabel)}">
        <div class="ribbon-primary">
          <div class="ribbon-title-row">
            <h3 class="ribbon-title">${escapeHtml(investigation.name)}</h3>
            <span class="ribbon-status">${activeLocaleText("פעילה", "Active")}</span>
          </div>
          <p class="ribbon-summary">${activeLocaleText("חקירת המודיעין הפעילה על צפון קוסובו וסרביה.", "Active intelligence investigation covering North Kosovo and Serbia.")}</p>
          <span class="ribbon-attention"><span class="material-symbols-rounded" aria-hidden="true">priority_high</span>${activeLocaleText("2 פריטים דורשים תשומת לב", "2 items need attention")}</span>
        </div>
        ${welcomeParticipantsHtml()}
        <div class="ribbon-metrics">
          <div class="ribbon-metric"><span>${activeLocaleText("פעילות אחרונה", "Recent activity")}</span><strong>${activeLocaleText("עודכן לפני 18 דקות", "Updated 18 minutes ago")}</strong></div>
          <div class="ribbon-metric"><span>${activeLocaleText("אבן הדרך הבאה", "Next milestone")}</span><strong>${activeLocaleText("הערכת דפוסי הסלמה", "Assess escalation patterns")}</strong></div>
          <div class="ribbon-progress" role="progressbar" aria-label="${activeLocaleText("התקדמות", "Progress")}" aria-valuenow="${progress}" aria-valuemin="0" aria-valuemax="100"><span style="width:${progress}%"></span></div>
        </div>
      </button>
      <div class="ribbon-actions">
        <button class="ribbon-action" type="button" data-welcome-action="invite" data-investigation-name="${escapeHtml(investigation.name)}"><span class="material-symbols-rounded" aria-hidden="true">person_add</span>${activeLocaleText("הזמנה / הוספה", "Invite / add")}</button>
      </div>
    </article>`;
}

function similarInvestigationRibbonHtml(investigation) {
  const actionLabel = investigation.action === "join"
    ? activeLocaleText("הצטרפות", "Join")
    : activeLocaleText("בקשת הצטרפות", "Request to join");
  return `
    <article class="investigation-ribbon similar">
      <div class="ribbon-similar-content">
        <div class="ribbon-primary">
          <div class="ribbon-title-row"><h3 class="ribbon-title">${escapeHtml(activeLocaleText(investigation.titleHe, investigation.titleEn))}</h3><span class="ribbon-status">${activeLocaleText("מומלצת", "Recommended")}</span></div>
          <p class="ribbon-summary">${escapeHtml(activeLocaleText(investigation.summaryHe, investigation.summaryEn))}</p>
          <span class="ribbon-attention"><span class="material-symbols-rounded" aria-hidden="true">auto_awesome</span>${escapeHtml(activeLocaleText(investigation.reasonHe, investigation.reasonEn))}</span>
        </div>
        ${welcomeParticipantsHtml(investigation.participants)}
        <div class="ribbon-metrics">
          <div class="ribbon-metric"><span>${activeLocaleText("רמת פעילות", "Activity level")}</span><strong>${activeLocaleText("פעילות גבוהה השבוע", "High activity this week")}</strong></div>
          <div class="ribbon-metric"><span>${activeLocaleText("גישה", "Access")}</span><strong>${investigation.action === "join" ? activeLocaleText("פתוחה להשתתפות", "Open participation") : activeLocaleText("דורשת אישור בעלים", "Owner approval required")}</strong></div>
        </div>
      </div>
      <div class="ribbon-actions"><button class="ribbon-action secondary" type="button" data-welcome-action="${investigation.action}" data-investigation-name="${escapeHtml(activeLocaleText(investigation.titleHe, investigation.titleEn))}">${actionLabel}</button></div>
    </article>`;
}

function renderWelcomePage() {
  if (!myInvestigationsList || !similarInvestigationsList) return;
  const investigations = state.investigations.length ? state.investigations : [{ id: state.investigationId, name: state.investigationName }];
  myInvestigationsCount.textContent = investigations.length.toLocaleString(currentLocaleTag());
  myInvestigationsList.innerHTML = investigations.map(ownedInvestigationRibbonHtml).join("");
  similarInvestigationsList.innerHTML = SIMILAR_INVESTIGATIONS.map(similarInvestigationRibbonHtml).join("");
}

function renderDraftInvestigationUi() {
  if (!investigationSwitcher || !draftCreateInvestigationButton) return;
  const active = state.draftSessionActive && state.pageView === "workspace";
  investigationSwitcher.classList.toggle("draft-active", active);
  draftCreateInvestigationButton.hidden = !active;
}

function setPageView(view, options = {}) {
  state.pageView = view === "workspace" ? "workspace" : "welcome";
  const showingWelcome = state.pageView === "welcome";
  if (welcomePage) welcomePage.hidden = !showingWelcome;
  if (workspace) workspace.hidden = showingWelcome;
  document.body.classList.toggle("welcome-active", showingWelcome);
  renderDraftInvestigationUi();
  if (showingWelcome) {
    renderWelcomePage();
    if (options.focus !== false) document.getElementById("welcomeTitle")?.focus?.();
    return;
  }
  window.requestAnimationFrame(() => {
    state.map?.resize();
    window.requestAnimationFrame(() => state.map?.resize());
  });
  if (options.focus !== false) promptInput?.focus();
}

function openWelcomeAction(action, investigationName) {
  if (!welcomeActionModal) return;
  const title = action === "invite"
    ? activeLocaleText("הזמנת משתתפים", "Invite participants")
    : action === "join"
      ? activeLocaleText("הצטרפות לחקירה", "Join investigation")
      : activeLocaleText("בקשת הצטרפות", "Request to join");
  welcomeActionTitle.textContent = title;
  welcomeActionDescription.textContent = activeLocaleText(
    `זוהי פעולת הדגמה עבור „${investigationName}”. לא בוצע שינוי בנתונים ולא נשלחה הודעה.`,
    `This is a demo action for “${investigationName}.” No data was changed and no message was sent.`
  );
  welcomeActionModal.hidden = false;
  welcomeActionClose?.focus();
}

function closeWelcomeAction() {
  if (welcomeActionModal) welcomeActionModal.hidden = true;
}

function showDraftCreateError(message = "") {
  if (!draftCreateError) return;
  draftCreateError.textContent = message;
  draftCreateError.hidden = !message;
}

function openDraftCreateModal(pendingAction = null) {
  if (!state.draftSessionActive || !draftCreateModal) return;
  if (pendingAction && !state.pendingDraftMemoryAction) state.pendingDraftMemoryAction = pendingAction;
  showDraftCreateError();
  draftCreateModal.hidden = false;
  window.requestAnimationFrame(() => draftInvestigationName?.focus());
}

function closeDraftCreateModal() {
  if (!draftCreateModal || draftCreateSubmit?.disabled) return;
  draftCreateModal.hidden = true;
  state.pendingDraftMemoryAction = null;
  showDraftCreateError();
  draftCreateInvestigationButton?.focus();
}

async function createInvestigationFromDraft() {
  if (!state.draftSessionActive || draftCreateSubmit?.disabled) return;
  const name = normalizeInvestigationName(draftInvestigationName?.value);
  if (!name) {
    showDraftCreateError(activeLocaleText("יש להזין שם חקירה.", "Enter an investigation name."));
    draftInvestigationName?.focus();
    return;
  }
  const duplicate = state.investigations.some(item => investigationNameKey(item.name) === investigationNameKey(name));
  if (duplicate) {
    showDraftCreateError(activeLocaleText("שם החקירה כבר קיים.", "That investigation name already exists."));
    draftInvestigationName?.focus();
    return;
  }
  const investigation = { id: state.investigationId, name, created_at: new Date().toISOString() };
  draftCreateSubmit.disabled = true;
  draftCreateSubmit.textContent = activeLocaleText("יוצר...", "Creating...");
  showDraftCreateError();
  try {
    await registerInvestigationRecord(investigation);
    state.investigations.push(investigation);
    state.investigationName = name;
    state.draftSessionActive = false;
    saveInvestigationRegistry();
    draftCreateModal.hidden = true;
    renderInvestigationSelector();
    renderMichlolTeam();
    renderDraftInvestigationUi();
    renderWelcomePage();
    const pendingAction = state.pendingDraftMemoryAction;
    state.pendingDraftMemoryAction = null;
    if (pendingAction) await pendingAction();
  } catch (error) {
    showDraftCreateError(error.message || activeLocaleText("יצירת החקירה נכשלה.", "Failed to create the investigation."));
  } finally {
    draftCreateSubmit.disabled = false;
    draftCreateSubmit.textContent = activeLocaleText("צור חקירה", "Create investigation");
  }
}

async function registerInvestigationRecord(investigation) {
  if (!investigation?.id || !investigation?.name) return null;
  const response = await fetch("/api/investigations", {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({
      investigation_id: investigation.id,
      name: investigation.name,
      locale: currentLocale()
    })
  });
  if (!response.ok) throw new Error(`investigation registration unavailable (${response.status})`);
  return response.json();
}

function loadInvestigationRegistry() {
  let registry = null;
  try {
    LEGACY_INVESTIGATIONS_STORAGE_KEYS.forEach(key => localStorage.removeItem(key));
    registry = JSON.parse(localStorage.getItem(INVESTIGATIONS_STORAGE_KEY) || "null");
  } catch (error) {
    registry = null;
  }
  const seen = new Set();
  const investigations = Array.isArray(registry?.investigations)
    ? registry.investigations
        .map(item => ({
          id: String(item?.id || createInvestigationId()),
          name: normalizeInvestigationName(item?.name),
          created_at: item?.created_at || new Date().toISOString()
        }))
        .filter(item => {
          const key = item.id;
          if (!item.name || seen.has(key)) return false;
          seen.add(key);
          return true;
        })
    : [];
  if (!investigations.length) investigations.push({
    id: state.investigationId,
    name: defaultInvestigationName(),
    created_at: new Date().toISOString()
  });
  state.investigations = investigations;
  const active = investigations.find(item => item.id === registry?.active_id) || investigations[0];
  state.investigationId = active.id;
  state.investigationName = active.name;
  saveInvestigationRegistry();
  renderWelcomePage();
}

async function hydrateInvestigationRegistry() {
  try {
    const response = await fetch(buildLocaleApiUrl("/api/investigations"), { cache: "no-store" });
    if (!response.ok) throw new Error(`investigation registry unavailable (${response.status})`);
    const payload = await response.json();
    const remoteInvestigations = Array.isArray(payload?.investigations) ? payload.investigations : [];
    const localById = new Map(state.investigations.map(item => [item.id, item]));
    const hydratedInvestigations = remoteInvestigations.map(item => {
      const id = String(item?.investigation_id || item?.id || "").trim();
      const name = normalizeInvestigationName(item?.name);
      if (!id || !name) return null;
      const existing = localById.get(id);
      return {
        id,
        name,
        created_at: item?.created_at_utc || existing?.created_at || new Date().toISOString()
      };
    }).filter(Boolean);

    if (hydratedInvestigations.length) {
      state.investigations = hydratedInvestigations;
      const active = hydratedInvestigations.find(item => item.id === state.investigationId) || hydratedInvestigations[0];
      state.investigationId = active.id;
      state.investigationName = active.name;
    }

    saveInvestigationRegistry();
    renderInvestigationSelector();
    renderWelcomePage();
  } catch (error) {
    console.warn("Investigation registry hydration failed", error);
  }
}

function matchingInvestigations(query) {
  const key = investigationNameKey(query);
  if (!key) return state.investigations;
  return state.investigations.filter(item => investigationNameKey(item.name).includes(key));
}

function renderInvestigationSelector() {
  if (!investigationInput || !investigationList) return;
  if (document.activeElement !== investigationInput) {
    investigationInput.value = state.investigationName || defaultInvestigationName();
  }
  const matches = matchingInvestigations(state.investigationSearchQuery);
  investigationInput.setAttribute("aria-expanded", state.investigationSelectorOpen && matches.length ? "true" : "false");
  investigationList.hidden = !state.investigationSelectorOpen || !matches.length;
  investigationList.innerHTML = matches.map(item => `
    <button type="button" class="investigation-option ${item.id === state.investigationId ? "active" : ""}" role="option" aria-selected="${item.id === state.investigationId}" data-investigation-id="${escapeHtml(item.id)}">
      <span>${escapeHtml(item.name)}</span>
      ${item.id === state.investigationId ? `<small>${activeLocaleText("פעילה", "Active")}</small>` : ""}
    </button>
  `).join("");
}

function selectInvestigation(investigation, options = {}) {
  if (!investigation || state.busy) return;
  state.investigationId = investigation.id;
  state.investigationName = investigation.name;
  state.draftSessionActive = false;
  state.pendingDraftMemoryAction = null;
  state.investigationSelectorOpen = false;
  state.investigationSearchQuery = "";
  state.investigationMemoryLoadToken += 1;
  state.memoryUpdatePollToken += 1;
  state.investigationMemory = null;
  state.investigationMemoryError = "";
  state.investigationMemoryLoading = false;
  if (investigationInput) investigationInput.value = investigation.name;
  saveInvestigationRegistry();
  resetInvestigation({ keepInvestigation: true });
  renderInvestigationSelector();
  void loadSelectedInvestigation(investigation.id);
  if (options.focusInput) investigationInput?.focus();
}

async function loadSelectedInvestigation(investigationId) {
  await loadWorkstreams();
  if (state.investigationId !== investigationId) return;
  await loadInvestigationMemory({ restoreLayers: true });
}

function addOrSelectInvestigation() {
  const name = normalizeInvestigationName(investigationInput?.value) || defaultInvestigationName();
  const investigation = ensureInvestigationRecord(name);
  if (state.busy) {
    renderInvestigationSelector();
    return;
  }
  selectInvestigation(investigation, { focusInput: true });
}

function startDraftInvestigation(prompt) {
  const text = String(prompt || "").trim();
  if (!text || state.busy) return;
  state.investigationId = createInvestigationId();
  state.investigationName = "";
  state.draftSessionActive = true;
  state.pendingDraftMemoryAction = null;
  resetInvestigation({ keepInvestigation: true });
  setPageView("workspace", { focus: false });
  runPrompt(text);
}

function setInvestigationSelectorOpen(open) {
  state.investigationSelectorOpen = !!open;
  if (!state.investigationSelectorOpen) state.investigationSearchQuery = "";
  renderInvestigationSelector();
}

function draftFiltersForLayer(layer) {
  ensureLayerFilterState(layer);
  return (layer?.draftFilters || []).filter(filter => filter?.field || normalizeFilterText(filter?.value));
}

function activeFilterLayer() {
  const layer = activeTableLayer();
  return layer?.filterPanelOpen ? layer : null;
}

function renderLayerFilterPanel(layer) {
  const panel = document.getElementById("layerFilterPanel");
  if (!panel) return;
  if (!layer || !layer.filterPanelOpen) {
    panel.hidden = true;
    panel.innerHTML = "";
    return;
  }

  ensureLayerFilterState(layer);
  const fields = filterFieldsForLayer(layer);
  const draftFilters = draftFiltersForLayer(layer);
  const appliedFilters = validAppliedFilters(layer);
  const fieldOptionsFor = selectedField => fields.length
    ? fields.map(field => `<option value="${escapeHtml(field)}" ${field === selectedField ? "selected" : ""}>${escapeHtml(field)}</option>`).join("")
    : '<option value="">No fields available</option>';
  const draftHtml = draftFilters.length
    ? draftFilters.map((filter, index) => `
      <div class="filter-draft-row">
        <select class="layer-filter-select filter-field-select" data-filter-field data-filter-index="${index}" aria-label="Choose a filter field">
          ${fieldOptionsFor(filter.field)}
        </select>
        <span class="filter-operator">contains</span>
        <input class="layer-filter-input filter-value-input" data-filter-value data-filter-index="${index}" type="text" value="${escapeHtml(stringifyFilterValue(filter.value))}" placeholder="Value to search" aria-label="Filter value">
        <button type="button" class="filter-remove-button" data-filter-remove="${index}" aria-label="Remove filter" title="Remove filter">×</button>
      </div>`).join("")
    : "";
  const appliedHtml = appliedFilters.length
    ? appliedFilters.map(filter => `
      <span class="filter-chip">
        <span dir="ltr">${escapeHtml(filter.field)}</span>
        <span>contains</span>
        <strong>${escapeHtml(stringifyFilterValue(filter.value))}</strong>
      </span>`).join("")
    : `<span class="filter-empty inline">${escapeHtml(activeLocaleText("אין מסננים פעילים.", "No active filters."))}</span>`;
  const addDisabled = fields.length ? "" : "disabled";
  const errorHtml = layer.filterError
    ? `<div class="filter-error" role="alert">${escapeHtml(layer.filterError)}</div>`
    : "";

  panel.hidden = false;
  panel.innerHTML = `
    <div class="layer-filter-header">
      <div>
        <span class="layer-filter-kicker">${escapeHtml(activeLocaleText("מסנני שכבה", "Layer filters"))}</span>
        <h3>${escapeHtml(layer.label)}</h3>
      </div>
      <button type="button" class="layer-filter-close" data-layer-filter="${escapeHtml(layer.id)}" aria-label="${escapeHtml(activeLocaleText("סגור מסננים", "Close filters"))}" title="${escapeHtml(activeLocaleText("סגור מסננים", "Close filters"))}">×</button>
    </div>
    ${draftFilters.length ? `<div class="layer-filter-section"><div class="filter-draft-list">${draftHtml}</div>${errorHtml}</div>` : errorHtml ? `<div class="layer-filter-section">${errorHtml}</div>` : ""}
    <div class="layer-filter-actions">
      <button type="button" class="filter-add-button" data-filter-add ${addDisabled}>${escapeHtml(activeLocaleText("הוסף מסנן", "Add filter"))}</button>
      <button type="button" class="primary-filter-action" data-filter-apply>${escapeHtml(activeLocaleText("החל", "Apply"))}</button>
    </div>`;
}

function addDraftFilter(layer) {
  ensureLayerFilterState(layer);
  const [firstField] = filterFieldsForLayer(layer);
  if (!firstField) {
    layer.filterError = activeLocaleText("אין שדות זמינים לסינון בשכבה זו.", "No fields are available for filtering in this layer.");
    return;
  }
  layer.draftFilters.push({ id: createFilterId(), field: firstField, value: "" });
  layer.filterError = "";
}

function updateDraftFilterField(layer, index, field) {
  ensureLayerFilterState(layer);
  if (!layer.draftFilters[index]) return;
  layer.draftFilters[index].field = field;
  layer.filterError = "";
}

function updateDraftFilterValue(layer, index, value) {
  ensureLayerFilterState(layer);
  if (!layer.draftFilters[index]) return;
  layer.draftFilters[index].value = value;
  layer.filterError = "";
}

function removeDraftFilter(layer, index) {
  ensureLayerFilterState(layer);
  layer.draftFilters.splice(index, 1);
  layer.filterError = "";
}

function resetDraftFilters(layer) {
  ensureLayerFilterState(layer);
  layer.draftFilters = cloneFilters(validAppliedFilters(layer));
  layer.filterError = "";
}

function applyDraftFilters(layer) {
  ensureLayerFilterState(layer);
  const draftFilters = draftFiltersForLayer(layer);
  const invalid = draftFilters.find(filter => !filter.field || !normalizeFilterText(filter.value));
  if (invalid) {
    layer.filterError = activeLocaleText("יש למלא שדה וערך לפני החלת המסננים.", "Fill in a field and value before applying filters.");
    return false;
  }
  layer.appliedFilters = cloneFilters(draftFilters);
  layer.draftFilters = cloneFilters(layer.appliedFilters);
  layer.filterError = "";
  return true;
}

function isCatalogLayerOpen(layerId) {
  return state.layers.some(layer => layer.catalogLayerId === layerId);
}

function normalizeLayerSearch(value) {
  return String(value ?? "").trim().toLocaleLowerCase("en-US");
}

function layerSearchText(layer) {
    const familyLabel = layerFamilyLabels()[layer.family] || layer.family || "";
  return normalizeLayerSearch([layer.label, familyLabel, layer.kind, layer.id].filter(Boolean).join(" "));
}

function matchingCatalogLayers() {
  const query = normalizeLayerSearch(state.layerSearchQuery);
  if (!query) return [];
  return state.layerCatalog
    .filter(layer => layerSearchText(layer).includes(query))
    .slice(0, 8);
}

function renderLayerSelector() {
  if (!layerSelectorSearch || !layerSelectorList || !layerSelectorStatus) return;
  if (state.layerCatalogLoading) {
    layerSelectorStatus.textContent = activeLocaleText("טוען שכבות", "Loading layers");
  } else if (state.layerCatalogError) {
    layerSelectorStatus.textContent = state.layerCatalogError;
  } else {
    layerSelectorStatus.textContent = "";
  }

  layerSelectorSearch.value = state.layerSearchQuery;
  layerSelectorSearch.disabled = state.layerCatalogLoading && !state.layerCatalog.length;
  layerSelectorSearch.parentElement?.setAttribute("aria-expanded", state.layerSearchOpen ? "true" : "false");

  if (!state.layerSearchOpen) {
    layerSelectorList.hidden = true;
    layerSelectorList.innerHTML = "";
    return;
  }

  layerSelectorList.hidden = false;
  if (state.layerCatalogError) {
    layerSelectorList.innerHTML = `<div class="layer-selector-empty">${escapeHtml(state.layerCatalogError)}</div>`;
    return;
  }
  if (state.layerCatalogLoading && !state.layerCatalog.length) {
    layerSelectorList.innerHTML = `<div class="layer-selector-empty">${escapeHtml(activeLocaleText("טוען שכבות...", "Loading layers..."))}</div>`;
    return;
  }
  if (!state.layerCatalog.length) {
    layerSelectorList.innerHTML = `<div class="layer-selector-empty">${escapeHtml(activeLocaleText("אין שכבות זמינות.", "No layers available."))}</div>`;
    return;
  }

  if (!normalizeLayerSearch(state.layerSearchQuery)) {
    layerSelectorList.innerHTML = `<div class="layer-selector-empty">${escapeHtml(activeLocaleText("הקלד שם שכבה או סוג מקור.", "Type a layer name or source type."))}</div>`;
    return;
  }

  const matches = matchingCatalogLayers();
  if (!matches.length) {
    layerSelectorList.innerHTML = `<div class="layer-selector-empty">${escapeHtml(activeLocaleText("לא נמצאו שכבות תואמות.", "No matching layers found."))}</div>`;
    return;
  }

  layerSelectorList.innerHTML = matches.map(layer => {
    const open = isCatalogLayerOpen(layer.id);
    const loading = state.openingLayerIds.has(layer.id);
    const family = layerFamilyLabels()[layer.family] || layer.family || activeLocaleText("שכבה", "Layer");
    return `
      <button type="button" role="option" class="layer-select-option ${open ? "selected" : ""}" data-layer-select="${escapeHtml(layer.id)}" title="${escapeHtml(layer.label)}" ${loading ? "disabled" : ""}>
        <span class="layer-select-main">
          <span class="layer-select-name">${escapeHtml(layer.label)}</span>
          <span class="layer-select-family">${escapeHtml(family)}</span>
        </span>
        <span class="layer-select-meta">
          <span class="layer-select-count">${Number(layer.count || 0).toLocaleString(currentLocaleTag())}</span>
          ${open ? `<span class="layer-select-state">${escapeHtml(activeLocaleText("פתוחה", "Open"))}</span>` : ""}
        </span>
      </button>`;
  }).join("");
}

function renderQueryLayersModal() {
  if (!queryLayersModal || !queryLayersList || !queryLayersSubmit || !queryLayersError) return;
  const openLayers = state.layers.filter(layer => layer.capabilities.table);
  queryLayersError.hidden = true;
  queryLayersError.textContent = "";
  queryLayersSubmit.disabled = openLayers.length === 0;
  queryLayersSubmit.textContent = state.workstreamComposerMode
    ? activeLocaleText("צרף שכבה", "Attach layer")
    : activeLocaleText("בחר שכבות", "Choose layers");
  if (!openLayers.length) {
    queryLayersList.innerHTML = `<div class="layer-selector-empty">${escapeHtml(activeLocaleText("אין שכבות פתוחות זמינות לבחירה.", "No open layers available to choose."))}</div>`;
    return;
  }
  queryLayersList.innerHTML = openLayers.map(layer => {
    return `
    <label class="step-inject-layer-item" style="${layerColorStyle(layer)}">
      <input type="${state.workstreamComposerMode ? "radio" : "checkbox"}" name="${state.workstreamComposerMode ? "workstream-layer" : ""}" value="${escapeHtml(layer.id)}" ${state.promptSelectedLayerIds.has(layer.id) ? "checked" : ""}>
      <span class="step-inject-layer-color"></span>
      <span class="step-inject-layer-name">${escapeHtml(layer.label)}</span>
      <span class="step-inject-layer-count">${itemsForLayerPresentation(layer).length.toLocaleString("en-US")}</span>
    </label>`;
  }).join("");
}

async function loadLayerCatalog() {
  if (!layerSelectorList || !layerSelectorStatus) return;
  state.layerCatalogLoading = true;
  state.layerCatalogError = "";
  renderLayerSelector();
  try {
    const response = await fetch(buildLocaleApiUrl("/api/layers"), { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("טעינת השכבות נכשלה", "Failed to load layers"));
    state.layerCatalog = payload.layers || [];
  } catch (error) {
    state.layerCatalogError = error.message || activeLocaleText("טעינת השכבות נכשלה", "Failed to load layers");
  } finally {
    state.layerCatalogLoading = false;
    renderLayerSelector();
    renderQueryLayersModal();
  }
}

async function openCatalogLayer(layerId, options = {}) {
  const layer = state.layerCatalog.find(item => item.id === layerId);
  if (!layer || state.openingLayerIds.has(layerId)) return null;
  const existing = state.layers.find(item => item.catalogLayerId === layerId);
  if (existing) {
    existing.visible = true;
    state.activeLayerId = existing.id;
    state.rawOverlayMinimized = false;
    state.layerSearchQuery = "";
    state.layerSearchOpen = false;
    if (options.savedLayer) applySavedFiltersToLayer(existing, options.savedLayer);
    if (!options.silent) {
      renderAllViews();
      renderLayerSelector();
      renderQueryLayersModal();
    }
    return existing;
  }

    state.openingLayerIds.add(layerId);
    renderLayerSelector();
    renderQueryLayersModal();
  try {
    const response = await fetch(buildLocaleApiUrl(`/api/layers/${encodeURIComponent(layerId)}/rows`), { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("טעינת נתוני השכבה נכשלה", "Failed to load layer data"));
    const openedLayer = buildCatalogLayer(payload.layer || layer, payload.rows || []);
    const added = addResultLayers({
      sourceId: `catalog:${layerId}`,
      sourceLabel: openedLayer.label,
      preferredView: openedLayer.capabilities.map ? "map" : (openedLayer.capabilities.timeline ? "timeline" : "evidence"),
      layers: [openedLayer]
    });
    const restoredLayer = added.find(item => item.catalogLayerId === layerId)
      || state.layers.find(item => item.catalogLayerId === layerId)
      || null;
    if (restoredLayer && options.savedLayer) applySavedFiltersToLayer(restoredLayer, options.savedLayer);
    state.rawOverlayMinimized = false;
    state.layerSearchQuery = "";
    state.layerSearchOpen = false;
    if (!options.silent) showResult(
      "שכבה נפתחה",
      added.length
        ? `${openedLayer.label}: ${(openedLayer.items || []).length.toLocaleString("he-IL")} רשומות נטענו.`
        : "השכבה כבר פתוחה."
    );
    return restoredLayer;
  } catch (error) {
    state.layerCatalogError = error.message || "טעינת נתוני השכבה נכשלה";
    return null;
  } finally {
    state.openingLayerIds.delete(layerId);
    if (!options.silent) {
      renderLayerSelector();
      renderQueryLayersModal();
    }
  }
}

async function refreshOpenAttackTargetCatalogLayer() {
  const existing = state.layers.find(item => item.catalogLayerId === ATTACK_TARGET_CATALOG_LAYER_ID);
  if (!existing) return null;
  try {
    const response = await fetch(buildLocaleApiUrl(`/api/layers/${encodeURIComponent(ATTACK_TARGET_CATALOG_LAYER_ID)}/rows`), { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "רענון שכבת המטרות נכשל");
    const refreshed = buildCatalogLayer(payload.layer, payload.rows || []);
    existing.items = refreshed.items;
    existing.visible = true;
    state.layers = state.layers.filter(layer => layer.kind !== "attack_targets" || layer === existing);
    const catalogEntry = state.layerCatalog.find(item => item.id === ATTACK_TARGET_CATALOG_LAYER_ID);
    if (catalogEntry) catalogEntry.count = existing.items.length;
    ensureLayerFilterState(existing);
    ensureActiveLayer();
    renderAllViews();
    renderLayerSelector();
    renderQueryLayersModal();
    return existing;
  } catch (error) {
    state.layerCatalogError = error.message || "רענון שכבת המטרות נכשל";
    return null;
  }
}

function visibleEventItems() {
  return visibleLayers("timeline")
    .filter(layer => layer.kind === "events")
    .flatMap(layer => itemsForLayerPresentation(layer));
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

const CONVERSATION_BOTTOM_THRESHOLD_PX = 96;

function conversationIsNearBottom() {
  return conversation.scrollHeight - conversation.scrollTop - conversation.clientHeight <= CONVERSATION_BOTTOM_THRESHOLD_PX;
}

function scrollConversationToLatest() {
  conversation.scrollTop = conversation.scrollHeight;
  requestAnimationFrame(() => {
    conversation.scrollTop = conversation.scrollHeight;
  });
}

function followConversationAfterUpdate(shouldFollow) {
  if (shouldFollow) scrollConversationToLatest();
}

function appendMessage(role, html, options = {}) {
  const shouldFollow = role === "user" || conversationIsNearBottom();
  const article = document.createElement("article");
  article.className = `message ${role === "user" ? "user-message" : "assistant-message"}${options.className ? ` ${options.className}` : ""}`;
  if (options.memberId) article.dataset.conversationMemberId = options.memberId;
  article.innerHTML = `<div class="message-label">${escapeHtml(options.label || (role === "user" ? activeLocaleText("אנליסט", "Analyst") : assistantMessageLabel()))}</div>${html}`;
  conversation.appendChild(article);
  followConversationAfterUpdate(shouldFollow);
  return article;
}

function thinkingIndicatorHtml() {
  return `
    <span class="thinking-indicator" role="status" aria-label="${escapeHtml(activeLocaleText("חושב", "Thinking"))}">
      <span>${escapeHtml(activeLocaleText("חושב", "Thinking"))}</span><span class="thinking-dots" aria-hidden="true"><i></i><i></i><i></i></span>
    </span>`;
}

function activeWorkstreams() {
  return state.workstreams.filter(item => item?.status !== "archived");
}

function workstreamStatusLabels() {
  return currentLocale() === "en"
    ? { active: "Active", paused: "Paused", completed: "Completed", archived: "Archived" }
    : { active: "פעיל", paused: "מושהה", completed: "הושלם", archived: "בארכיון" };
}

function loadWorkstreamSeenState() {
  try {
    const parsed = JSON.parse(localStorage.getItem(WORKSTREAM_SEEN_STORAGE_KEY) || "{}");
    state.workstreamSeen = parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    state.workstreamSeen = {};
  }
}

function saveWorkstreamSeenState() {
  localStorage.setItem(WORKSTREAM_SEEN_STORAGE_KEY, JSON.stringify(state.workstreamSeen));
}

function workstreamSeenKey(workstreamId) {
  return `${state.investigationId || "investigation"}:${workstreamId}`;
}

function workstreamSeenMarker(workstream) {
  if (!workstream) return "";
  const activityId = String(workstream.latest_activity_id || "").trim();
  if (activityId) return `activity:${activityId}`;
  const updated = String(workstream.updated_at_utc || workstream.created_at_utc || "").trim();
  return updated ? `time:${updated}` : "";
}

function workstreamHasNewItems(workstream) {
  const marker = workstreamSeenMarker(workstream);
  if (!marker) return false;
  return state.workstreamSeen[workstreamSeenKey(workstream?.workstream_id)] !== marker;
}

function markWorkstreamSeen(workstream) {
  if (!workstream?.workstream_id) return;
  const marker = workstreamSeenMarker(workstream) || `time:${new Date().toISOString()}`;
  state.workstreamSeen[workstreamSeenKey(workstream.workstream_id)] = marker;
  saveWorkstreamSeenState();
}

function workstreamUpdatedLabel(workstream) {
  const value = workstream?.updated_at_utc || workstream?.created_at_utc;
  const date = value ? new Date(value) : null;
  if (!date || Number.isNaN(date.getTime())) return "";
  return new Intl.DateTimeFormat("en-US", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit"
  }).format(date);
}

function setWorkstreamRailCollapsed(collapsed) {
  state.workstreamRailCollapsed = Boolean(collapsed);
  workstreamRail?.classList.toggle("collapsed", state.workstreamRailCollapsed);
  document.querySelector(".workspace")?.classList.toggle("workstream-rail-collapsed", state.workstreamRailCollapsed);
  if (workstreamRailToggle) {
    workstreamRailToggle.setAttribute("aria-expanded", state.workstreamRailCollapsed ? "false" : "true");
    workstreamRailToggle.setAttribute("aria-label", state.workstreamRailCollapsed
      ? activeLocaleText("הרחב מעקבים", "Expand workstreams")
      : activeLocaleText("מזער מעקבים", "Collapse workstreams"));
    workstreamRailToggle.title = state.workstreamRailCollapsed
      ? activeLocaleText("הרחב מעקבים", "Expand workstreams")
      : activeLocaleText("מזער מעקבים", "Collapse workstreams");
    const icon = workstreamRailToggle.querySelector(".material-symbols-rounded");
    if (icon) {
      const pointsLeft = currentLocale() === "he"
        ? state.workstreamRailCollapsed
        : !state.workstreamRailCollapsed;
      icon.textContent = pointsLeft ? "chevron_left" : "chevron_right";
    }
  }
  if (state.map) setTimeout(() => state.map.resize(), 220);
}

function renderWorkstreamIndicator() {
  if (!workstreamRail || !workstreamRailList || !workstreamRailCount) return;
  const workstreams = activeWorkstreams();
  const visible = workstreams.length > 0;
  workstreamRail.hidden = !visible;
  document.querySelector(".workspace")?.classList.toggle("workstream-rail-visible", visible);
  workstreamRailCount.textContent = workstreams.length.toLocaleString("en-US");
  workstreamRailList.innerHTML = workstreams.map(item => {
    const hasNew = workstreamHasNewItems(item);
    const status = workstreamStatusLabels()[item.status] || item.status || activeLocaleText("פעיל", "Active");
    const updated = workstreamUpdatedLabel(item);
    return `
      <button type="button" class="workstream-rail-card ${hasNew ? "has-new" : ""}" role="listitem" data-workstream-show="${escapeHtml(item.workstream_id)}" title="${escapeHtml(item.title || "Workstream")}">
        <span class="workstream-card-state" aria-hidden="true"></span>
        <span class="workstream-card-body">
          <strong>${escapeHtml(item.title || "Workstream")}</strong>
          <span class="workstream-card-meta"><span>${escapeHtml(status)}</span>${updated ? `<time>${escapeHtml(updated)}</time>` : ""}</span>
        </span>
        ${hasNew ? '<span class="workstream-new-badge" aria-label="New items">New</span>' : ""}
      </button>`;
  }).join("");
  setWorkstreamRailCollapsed(state.workstreamRailCollapsed);
}

async function loadWorkstreams() {
  if (!state.investigationId) return [];
  const investigationId = state.investigationId;
  const token = ++state.workstreamLoadToken;
  state.workstreamsLoading = true;
  try {
    const response = await fetch(`/api/workstreams?investigation_id=${encodeURIComponent(investigationId)}&locale=${encodeURIComponent(currentLocale())}`, { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("טעינת המעקבים נכשלה", "Failed to load workstreams"));
    if (token !== state.workstreamLoadToken || investigationId !== state.investigationId) return [];
    state.workstreams = Array.isArray(payload.workstreams) ? payload.workstreams : [];
    renderWorkstreamIndicator();
    void fetchInvestigationPlayback().catch(() => {
      state.investigationPlayback = null;
      renderInvestigationPlayback();
    });
    return state.workstreams;
  } catch (error) {
    if (token === state.workstreamLoadToken) {
      state.workstreams = [];
      renderWorkstreamIndicator();
    }
    return [];
  } finally {
    if (token === state.workstreamLoadToken) state.workstreamsLoading = false;
  }
}

function setWorkstreamComposerMode(enabled) {
  state.workstreamComposerMode = Boolean(enabled);
  promptForm.classList.toggle("tracking-mode", state.workstreamComposerMode);
  if (workstreamComposerMode) workstreamComposerMode.hidden = !state.workstreamComposerMode;
  updatePromptPlaceholder();
  renderSelectedLayersButton();
  renderQueryLayersModal();
  setPromptOptionsOpen(false);
}

function startWorkstreamComposerMode() {
  if (state.activeConversationMemberId !== MOSHE_MEMBER_ID) return;
  setWorkstreamComposerMode(true);
  promptInput.focus();
}

function workstreamMessage(html, options = {}) {
  const article = appendMessage("assistant", html, {
    label: options.label || activeLocaleText("עדכון מעקב", "Workstream update"),
    className: `workstream-message${options.className ? ` ${options.className}` : ""}`,
    memberId: options.memberId,
  });
  scrollConversationToLatest();
  return article;
}

async function fetchWorkstream(workstreamId) {
  const response = await fetch(`/api/workstreams/${encodeURIComponent(workstreamId)}?locale=${encodeURIComponent(currentLocale())}`, { cache: "no-store" });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || activeLocaleText("טעינת המעקב נכשלה", "Failed to load workstream"));
  return payload;
}

function playbackNextStage(playback) {
  return playback?.run?.next_stage || playback?.next_stage || null;
}

function formatPlaybackTime(value) {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return String(value || "");
  return parsed.toLocaleString(currentLocaleTag(), {
    timeZone: "UTC",
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

async function reloadOpenCatalogLayers() {
  const catalogLayerIds = [...new Set(
    state.layers.map(layer => layer.catalogLayerId).filter(Boolean)
  )];
  if (!catalogLayerIds.length) return;
  for (const layerId of catalogLayerIds) {
    const existingLayers = state.layers.filter(layer => layer.catalogLayerId === layerId);
    const wasVisible = existingLayers.some(layer => layer.visible);
    const savedFilters = existingLayers[0] ? {
      draftFilters: existingLayers[0].draftFilters,
      appliedFilters: existingLayers[0].appliedFilters,
    } : null;
    state.layers = state.layers.filter(layer => layer.catalogLayerId !== layerId);
    const restored = await openCatalogLayer(layerId, { silent: true, savedLayer: savedFilters });
    if (restored) restored.visible = wasVisible;
  }
  ensureActiveLayer();
  renderAllViews();
  renderLayerSelector();
  renderQueryLayersModal();
}

function renderInvestigationPlayback() {
  if (!playbackNextButton || !playbackResetButton || !intelligencePeriod) return;
  const playback = state.investigationPlayback;
  renderWorkstreamIndicator();
  const timeframe = playback?.run?.visible_timeframe || playback?.full_timeframe;
  intelligencePeriod.textContent = timeframe?.from && timeframe?.to
    ? `${formatPlaybackTime(timeframe.from)}–${formatPlaybackTime(timeframe.to)}`
    : "";
  const next = playbackNextStage(state.investigationPlayback);
  const reevaluation = playback?.run?.reevaluation;
  const processing = reevaluation?.status === "running";
  if (playbackAgentStatus) {
    playbackAgentStatus.hidden = !processing && reevaluation?.status !== "failed";
    playbackAgentStatus.classList.toggle("failed", reevaluation?.status === "failed");
    playbackAgentStatus.textContent = processing
      ? activeLocaleText("משה מעבד…", "Moshe is processing…")
      : activeLocaleText("העיבוד של משה נכשל", "Moshe processing failed");
    playbackAgentStatus.title = reevaluation?.error || "";
  }
  playbackNextButton.hidden = !next?.timeframe;
  playbackNextButton.disabled = processing;
  playbackResetButton.hidden = !playback?.run;
  playbackResetButton.disabled = processing;
  if (!next?.timeframe) return;
  const nextTimeframe = next.timeframe;
  const tooltip = `${activeLocaleText("הטווח הבא", "Next range")}: ${formatPlaybackTime(nextTimeframe.from)}–${formatPlaybackTime(nextTimeframe.to)}`;
  playbackNextButton.title = tooltip;
  playbackNextButton.setAttribute("aria-label", activeLocaleText(`השלב הבא. ${tooltip}`, `Next step. ${tooltip}`));
}
async function fetchInvestigationPlayback() {
  const investigationId = String(state.investigationId || "").trim();
  if (!investigationId) return null;
  const response = await fetch(
    `/api/playback?investigation_id=${encodeURIComponent(investigationId)}&locale=${encodeURIComponent(currentLocale())}`,
    { cache: "no-store" }
  );
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || activeLocaleText("טעינת מצב הניגון נכשלה", "Failed to load playback state"));
  state.investigationPlayback = payload;
  renderInvestigationPlayback();
  if (payload?.run?.reevaluation?.status === "running") {
    void pollMoshePlaybackReevaluation();
  }
  handleInvestigationMemoryUpdate(payload?.run);
  return payload;
}

async function initializeStagedPlayback({ reset = false } = {}) {
  const investigationId = String(state.investigationId || "").trim();
  if (!investigationId) return null;
  const response = await fetch("/api/playback/mode", {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({
      investigation_id: investigationId,
      mode: "real_time",
      reset,
      locale: currentLocale(),
    }),
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "Failed to initialize staged playback");
  state.investigationPlayback = payload;
  renderInvestigationPlayback();
  await reloadOpenCatalogLayers();
  return payload;
}

async function pollMoshePlaybackReevaluation() {
  const token = ++state.playbackPollToken;
  const investigationId = String(state.investigationId || "").trim();
  while (token === state.playbackPollToken && investigationId === String(state.investigationId || "").trim()) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    if (token !== state.playbackPollToken) return;
    try {
      const response = await fetch(
        `/api/playback?investigation_id=${encodeURIComponent(investigationId)}&locale=${encodeURIComponent(currentLocale())}`,
        { cache: "no-store" }
      );
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || activeLocaleText("טעינת מצב התרחיש נכשלה", "Failed to load playback state"));
      state.investigationPlayback = payload;
      renderInvestigationPlayback();
      const status = payload?.run?.reevaluation?.status;
      if (status !== "running") {
        if (status === "completed") {
          const answer = String(payload.run.reevaluation?.assessment?.answer || "").trim();
          if (payload.run.reevaluation?.assessment?.workstream_updates?.length) {
            await loadWorkstreams();
          }
          if (answer) {
            appendMoshePlaybackAssessment(payload.run.reevaluation.assessment);
          } else {
            workstreamMessage(`<p>${activeLocaleText("משה סיים לעבד את פרוסת המידע החדשה.", "Moshe finished processing the new information slice.")}</p>`);
          }
        } else if (status === "failed") {
          workstreamMessage(`<p>${activeLocaleText("טווח הזמן עודכן, אך העיבוד של משה נכשל.", "The timeframe was updated, but Moshe's processing failed.")}</p><div class="answer-callout">${escapeHtml(payload.run.reevaluation.error || "")}</div>`);
        }
        return;
      }
    } catch (error) {
      if (token === state.playbackPollToken && playbackAgentStatus) {
        playbackAgentStatus.hidden = false;
        playbackAgentStatus.classList.add("failed");
        playbackAgentStatus.textContent = activeLocaleText("לא ניתן לבדוק את הסטטוס של משה", "Unable to check Moshe's status");
      }
      return;
    }
  }
}

function appendMoshePlaybackAssessment(assessment = {}) {
  const result = {
    ...assessment,
    run_id: assessment.run_id || `playback:${Date.now()}`
  };
  const hasRequestedResults = buildTypedResultLayers(result).length > 0;
  const article = workstreamMessage(
    `<div class="answer-body">
      ${answerHtml(cleanAssistantAnswer(String(assessment.answer || "")))}
      ${hasRequestedResults ? `<div class="final-answer-actions">
        <button type="button" class="final-answer-show-btn layers-hidden" data-source-id="${escapeHtml(finalSourceId(result))}" title="${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}" aria-label="${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}" aria-pressed="false">
          <span class="final-answer-show-label">${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}</span>
        </button>
      </div>` : ""}
    </div>`,
    { label: MOSHE_MESSAGE_LABEL[currentLocale()], memberId: MOSHE_MEMBER_ID }
  );
  const button = article.querySelector(".final-answer-show-btn");
  if (button) {
    button.addEventListener("click", () => {
      toggleFinalAnswerVisibility(result, "", button);
    });
    updateSourceVisibilityBtn(button);
  }
  return article;
}

function investigationMemoryUpdateKey(run = {}) {
  return `${run.run_id || "playback"}:${run.revision || 0}:${state.investigationId || "investigation"}`;
}

function investigationMemoryUpdateLabel() {
  return activeLocaleText("עדכון חקירה", "Investigation update");
}

function findMemoryUpdateProcessingMessage(key) {
  return [...conversation.querySelectorAll("[data-memory-update-processing]")]
    .find(element => element.dataset.memoryUpdateProcessing === key) || null;
}

function removeMemoryUpdateProcessingMessage(key) {
  findMemoryUpdateProcessingMessage(key)?.remove();
}

function handleInvestigationMemoryUpdate(run = {}) {
  const update = run?.memory_update;
  if (!update) return;
  const key = investigationMemoryUpdateKey(run);
  const status = String(update.status || "");
  if (status === "running") {
    if (!state.renderedMemoryUpdateKeys.has(key) && !findMemoryUpdateProcessingMessage(key)) {
      const article = appendMessage(
        "assistant",
        `<p>${activeLocaleText("סוכן החקירה בוחן את פרוסת המידע החדשה מול זיכרון החקירה.", "The investigation agent is checking the new information slice against the investigation memory.")}</p>`,
        { label: investigationMemoryUpdateLabel(), className: "memory-update-message" }
      );
      article.dataset.memoryUpdateProcessing = key;
    }
    void pollInvestigationMemoryUpdate();
    return;
  }
  if (state.renderedMemoryUpdateKeys.has(key)) return;
  removeMemoryUpdateProcessingMessage(key);
  state.renderedMemoryUpdateKeys.add(key);
  if (status === "completed") {
    const answer = String(update.assessment?.answer || "").trim();
    if (answer) {
      appendMessage(
        "assistant",
        `<div class="answer-body">${answerHtml(cleanAssistantAnswer(answer))}</div>`,
        { label: investigationMemoryUpdateLabel(), className: "memory-update-message" }
      );
    }
  } else if (status === "failed") {
    appendMessage(
      "assistant",
      `<p>${activeLocaleText("עדכון החקירה נכשל.", "The investigation update failed.")}</p><div class="answer-callout">${escapeHtml(update.error || "")}</div>`,
      { label: investigationMemoryUpdateLabel(), className: "memory-update-message" }
    );
  }
}

async function pollInvestigationMemoryUpdate() {
  const token = ++state.memoryUpdatePollToken;
  const investigationId = String(state.investigationId || "").trim();
  while (token === state.memoryUpdatePollToken && investigationId === String(state.investigationId || "").trim()) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    if (token !== state.memoryUpdatePollToken) return;
    try {
      const response = await fetch(
        `/api/playback?investigation_id=${encodeURIComponent(investigationId)}&locale=${encodeURIComponent(currentLocale())}`,
        { cache: "no-store" }
      );
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || activeLocaleText("טעינת מצב התרחיש נכשלה", "Failed to load playback state"));
      state.investigationPlayback = payload;
      renderInvestigationPlayback();
      handleInvestigationMemoryUpdate(payload?.run);
      if (payload?.run?.memory_update?.status !== "running") return;
    } catch {
      return;
    }
  }
}

async function advanceInvestigationPlayback() {
  if (!playbackNextButton || playbackNextButton.disabled) return;
  const playback = state.investigationPlayback || await fetchInvestigationPlayback();
  const run = playback?.run;
  playbackNextButton.disabled = true;
  playbackNextButton.textContent = "…";
  try {
    const response = await fetch("/api/playback/next", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify({
        investigation_id: state.investigationId,
        expected_revision: run?.revision,
        idempotency_key: `playback:${state.investigationId}:${run?.revision || 0}:${Date.now()}`,
        locale: currentLocale(),
      }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Failed to advance playback");
    state.investigationPlayback = {
      ...state.investigationPlayback,
      investigation_id: state.investigationId,
      mode: "real_time",
      run: result.run,
    };
    renderInvestigationPlayback();
    await reloadOpenCatalogLayers();
    handleInvestigationMemoryUpdate(result.run);
    if (result.moshe_triggered) {
      workstreamMessage(`<p>${activeLocaleText("טווח הזמן עודכן. משה מעבד עכשיו את פרוסת המידע החדשה מול המעקבים הפעילים.", "The timeframe was updated. Moshe is now processing the new information slice against the active workstreams.")}</p>`);
    } else if (result.moshe_skipped_reason === "initial_baseline") {
      workstreamMessage(`<p>${activeLocaleText("טווח הבסיס הופעל. משה לא הופעל עד שתגיע פרוסת המידע הבאה.", "The baseline timeframe is active. Moshe will not be triggered until the next information slice arrives.")}</p>`);
    } else if (result.moshe_skipped_reason === "no_active_workstreams") {
      workstreamMessage(`<p>${activeLocaleText("טווח הזמן עודכן. אין מעקבים פעילים, ולכן משה לא הופעל.", "The timeframe was updated. There are no active workstreams, so Moshe was not triggered.")}</p>`);
    }
    if (result.run?.reevaluation?.status === "running") {
      void pollMoshePlaybackReevaluation();
    }
  } catch (error) {
    workstreamMessage(
      `<p>I couldn't advance to the next step.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`
    );
  } finally {
    playbackNextButton.innerHTML = '<span class="material-symbols-rounded" aria-hidden="true">skip_next</span>';
    renderInvestigationPlayback();
  }
}

async function changeIntelligenceMode() {
  try {
    await initializeStagedPlayback();
  } catch (error) {
    renderInvestigationPlayback();
    workstreamMessage(
      `<p>${activeLocaleText("לא הצלחתי להפעיל את הניגון המדורג.", "I couldn't initialize staged playback.")}</p><div class="answer-callout">${escapeHtml(error.message)}</div>`
    );
  }
}

function workstreamAgent(workstream) {
  return (workstream.participants || []).find(item => item.kind === "agent") || null;
}

const WORKSTREAM_ARTIFACT_STATUS_LABELS = {
  active: "Active",
  ready_for_assessment: "Ready for assessment",
  rejected: "Rejected",
  closed: "Closed"
};

const INDICATION_ROLE_LABELS = {
  supports: "Supports",
  contradicts: "Contradicts",
  context: "Context"
};

function workstreamArtifactHtml(workstream) {
  const artifacts = Array.isArray(workstream.artifacts) ? workstream.artifacts : [];
  const artifact = artifacts.find(item => item.artifact_type === "target_assessment_lead"
    && !["closed", "rejected"].includes(item.status))
    || artifacts.find(item => item.artifact_type === "target_assessment_lead");
  if (!artifact) return `<p class="workstream-message-meta">${escapeHtml(activeLocaleText("עדיין אין הובלה להערכה במעקב.", "There is no assessment lead in this workstream yet."))}</p>`;
  const content = artifact.content || {};
  const activeIndications = (content.indications || []).filter(item => item.state !== "removed");
  const indications = activeIndications.length
    ? `<ul>${activeIndications.map(item => {
        const reference = item.source_reference || {};
        const detail = item.annotation || item.relevance || item.observed_claim || "";
        return `<li><strong>${escapeHtml(reference.record_id || "")}</strong> · ${escapeHtml(INDICATION_ROLE_LABELS[item.role] || item.role || activeLocaleText("הקשר", "Context"))}${detail ? ` — ${escapeHtml(detail)}` : ""}</li>`;
      }).join("")}</ul>`
    : `<p>${escapeHtml(activeLocaleText("אין אינדיקציות פעילות.", "No active indications."))}</p>`;
  const gaps = (content.gaps || []).length
    ? `<p><strong>${escapeHtml(activeLocaleText("פערים:", "Gaps:"))}</strong> ${escapeHtml(content.gaps.join(" · "))}</p>`
    : `<p><strong>${escapeHtml(activeLocaleText("פערים:", "Gaps:"))}</strong> ${escapeHtml(activeLocaleText("לא נרשמו", "None recorded"))}</p>`;
  const questions = (content.assessment_questions || []).length
    ? `<p><strong>${escapeHtml(activeLocaleText("שאלות להערכה:", "Assessment questions:"))}</strong> ${escapeHtml(content.assessment_questions.join(" · "))}</p>`
    : "";
  return `
    <section class="workstream-artifact-summary">
      <p><strong>${escapeHtml(activeLocaleText("הובלה להערכה:", "Assessment lead:"))}</strong> ${escapeHtml(content.lead_statement || activeLocaleText("ללא ניסוח", "No wording"))}</p>
      <p class="workstream-message-meta">${escapeHtml(activeLocaleText("סטטוס", "Status"))}: ${escapeHtml(WORKSTREAM_ARTIFACT_STATUS_LABELS[artifact.status] || artifact.status || activeLocaleText("לא ידוע", "Unknown"))} · ${escapeHtml(activeLocaleText("גרסה", "Revision"))}: ${Number(artifact.revision || 0).toLocaleString(currentLocaleTag())}</p>
      <p><strong>${escapeHtml(activeLocaleText("אינדיקציות:", "Indications:"))}</strong></p>
      ${indications}
      ${gaps}
      ${questions}
    </section>`;
}

function normalizedWorkstreamSummaryText(value) {
  return String(value || "").replace(/\s+/g, " ").trim().toLocaleLowerCase(currentLocaleTag());
}

function workstreamResultSourceId(workstreamId) {
  return sanitizeLayerKey(`workstream:${workstreamId}`);
}

function workstreamHasPresentation(workstream) {
  const artifacts = Array.isArray(workstream.artifacts) ? workstream.artifacts : [];
  return artifacts.some(artifact =>
    artifact.artifact_type === "target_assessment_lead"
    && !["closed", "rejected"].includes(artifact.status)
    && (artifact.content?.indications || []).some(item => item.state !== "removed")
  );
}

async function toggleWorkstreamResultVisibility(workstreamId, btn) {
  const sourceId = workstreamResultSourceId(workstreamId);
  const sourceLayers = state.layers.filter(layer => layer.sourceId === sourceId);
  if (sourceLayers.some(layer => layer.visible)) {
    sourceLayers.forEach(layer => { layer.visible = false; });
    updateSourceVisibilityBtn(btn);
    renderAllViews();
    return;
  }
  await showWorkstreamResultVisibility(workstreamId, btn);
}

async function resetInvestigationPlayback() {
  if (!playbackResetButton || playbackResetButton.disabled) return;
  state.playbackPollToken += 1;
  playbackResetButton.disabled = true;
  playbackResetButton.innerHTML = '<span class="material-symbols-rounded" aria-hidden="true">progress_activity</span>';
  try {
    await initializeStagedPlayback({ reset: true });
  } catch (error) {
    workstreamMessage(
      `<p>${activeLocaleText("לא הצלחתי לאפס לפרוסת הזמן הראשונה.", "I couldn't reset to the initial time slice.")}</p><div class="answer-callout">${escapeHtml(error.message)}</div>`
    );
  } finally {
    playbackResetButton.innerHTML = '<span class="material-symbols-rounded" aria-hidden="true">refresh</span>';
    renderInvestigationPlayback();
  }
}

async function fetchWorkstreamPresentation(workstreamId) {
  const response = await fetch(
    `/api/workstreams/${encodeURIComponent(workstreamId)}/presentation?locale=${encodeURIComponent(currentLocale())}`,
    { cache: "no-store" }
  );
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || activeLocaleText("טעינת תוצאות המעקב נכשלה", "Failed to load workstream results"));
  return result;
}

async function showWorkstreamResultVisibility(workstreamId, btn) {
  const sourceId = workstreamResultSourceId(workstreamId);
  if (btn) btn.disabled = true;
  try {
    const result = await fetchWorkstreamPresentation(workstreamId);
    state.layers = state.layers.filter(layer => layer.sourceId !== sourceId);
    const layers = buildTypedResultLayers(result);
    if (!layers.length) throw new Error(activeLocaleText("אין למעקב תוצאות שניתן להציג", "This workstream has no results that can be displayed"));
    addResultLayers({
      sourceId,
      sourceLabel: result.title || activeLocaleText("תוצאות מעקב", "Workstream results"),
      preferredView: "map",
      layers
    });
    state.rawOverlayMinimized = false;
    activateView("map", { reason: activeLocaleText("תוצאות המעקב", "Workstream results") });
    renderAllViews();
  } catch (error) {
    workstreamMessage(
      `<p>${escapeHtml(activeLocaleText("לא הצלחתי להציג את תוצאות המעקב.", "I couldn't display the workstream results."))}</p><div class="answer-callout">${escapeHtml(error.message)}</div>`
    );
  } finally {
    if (btn) btn.disabled = false;
    updateSourceVisibilityBtn(btn);
  }
}

async function showRecordedWorkstreamPresentation(recording, btn = null) {
  let presentation = recording?.presentation;
  const workstreamId = recording?.workstream?.workstream_id || presentation?.workstream_id;
  if (!presentation && workstreamId) {
    try {
      presentation = await fetchWorkstreamPresentation(workstreamId);
    } catch (error) {
      if (btn) btn.remove();
      return;
    }
  }
  if (!presentation) {
    if (btn) btn.remove();
    return;
  }
  const sourceId = workstreamResultSourceId(workstreamId || "recorded");
  state.layers = state.layers.filter(layer => layer.sourceId !== sourceId);
  const layers = buildTypedResultLayers(presentation);
  if (!layers.length) {
    if (btn) btn.remove();
    return;
  }
  addResultLayers({
    sourceId,
    sourceLabel: presentation.title || recording?.workstream?.title || activeLocaleText("תוצאות מעקב", "Workstream results"),
    preferredView: layers[0]?.preferredView || "map",
    layers
  });
  state.rawOverlayMinimized = false;
  activateView(layers[0]?.preferredView || "map", { reason: activeLocaleText("תוצאות מעקב מוקלטות", "Recorded workstream results") });
  renderAllViews();
  if (btn) updateSourceVisibilityBtn(btn);
}

function toggleRecordedWorkstreamResultVisibility(btn) {
  const sourceId = btn?.dataset.sourceId;
  if (!sourceId) return;
  const sourceLayers = state.layers.filter(layer => layer.sourceId === sourceId);
  if (!sourceLayers.length) return;
  const anyVisible = sourceLayers.some(layer => layer.visible);
  sourceLayers.forEach(layer => { layer.visible = !anyVisible; });
  updateSourceVisibilityBtn(btn);
  renderAllViews();
}

const workstreamRecordingSnapshots = new Map();

function appendWorkstreamUpdate(workstream, options = {}) {
  conversation.querySelectorAll("[data-workstream-update-id]").forEach(message => {
    if (message.dataset.workstreamUpdateId === workstream.workstream_id) message.remove();
  });
  const agent = workstreamAgent(workstream);
  const assignment = (workstream.assignments || []).find(item => item.status === "active")
    || (workstream.assignments || [])[0];
  const title = String(workstream.title || activeLocaleText("מעקב", "Workstream")).trim();
  const objective = String(workstream.objective || "").trim();
  const responsibility = String(assignment?.responsibility || "").trim();
  const renderedValues = new Set([normalizedWorkstreamSummaryText(title)]);
  const distinctDetail = (value, html) => {
    const normalized = normalizedWorkstreamSummaryText(value);
    if (!normalized || renderedValues.has(normalized)) return "";
    renderedValues.add(normalized);
    return html(value);
  };
  const objectiveHtml = distinctDetail(objective, value => `<p>${escapeHtml(value)}</p>`);
  const responsibilityHtml = distinctDetail(
    responsibility,
    value => `<p class="workstream-message-meta">${escapeHtml(activeLocaleText("אחריות", "Responsibility"))}: ${escapeHtml(value)}</p>`
  );
  const hasRecordedPresentation = options.recorded
    && (Boolean(options.recording?.presentation) || workstreamHasPresentation(workstream));
  const message = workstreamMessage(`
    <p class="workstream-message-title">${escapeHtml(activeLocaleText("עדכון מעקב", "Workstream update"))} — ${escapeHtml(title)}</p>
    ${objectiveHtml}
    ${responsibilityHtml}
    ${workstreamArtifactHtml(workstream)}
    <div class="workstream-message-actions">
      ${!options.recorded && workstreamHasPresentation(workstream) ? `<button type="button" class="final-answer-show-btn layers-hidden" data-workstream-results="${escapeHtml(workstream.workstream_id)}" data-source-id="${escapeHtml(workstreamResultSourceId(workstream.workstream_id))}" title="${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}" aria-label="${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}" aria-pressed="false"><span class="final-answer-show-label">${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}</span></button>` : ""}
      ${hasRecordedPresentation ? `<button type="button" class="final-answer-show-btn layers-hidden" data-recorded-workstream-results data-source-id="${escapeHtml(workstreamResultSourceId(workstream.workstream_id))}" title="${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}" aria-label="${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}" aria-pressed="false"><span class="final-answer-show-label">${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}</span></button>` : ""}
      <button type="button" class="final-answer-save-btn" data-workstream-save="${escapeHtml(workstream.workstream_id)}" ${options.recorded ? "disabled" : ""}>${options.recorded ? activeLocaleText("נשמר", "Saved") : activeLocaleText("שמור הקלטה", "Save recording")}</button>
      ${!options.recorded ? `<button type="button" class="danger-button" data-workstream-archive="${escapeHtml(workstream.workstream_id)}">${escapeHtml(activeLocaleText("העברה לארכיון", "Archive"))}</button>` : ""}
    </div>`, {
      label: agent ? `${agent.display_name} · ${activeLocaleText("עדכון מעקב", "Workstream update")}` : activeLocaleText("עדכון מעקב", "Workstream update"),
      memberId: agent?.participant_id,
    });
  message.dataset.workstreamUpdateId = workstream.workstream_id;
  if (!options.recorded) workstreamRecordingSnapshots.set(workstream.workstream_id, workstream);
  const resultsButton = message.querySelector("[data-workstream-results]");
  if (resultsButton) updateSourceVisibilityBtn(resultsButton);
  return message;
}

async function showWorkstreamUpdate(workstreamId) {
  try {
    const workstream = await fetchWorkstream(workstreamId);
    markWorkstreamSeen(workstream);
    renderWorkstreamIndicator();
    const message = appendWorkstreamUpdate(workstream);
    if (workstreamHasPresentation(workstream)) {
      await showWorkstreamResultVisibility(
        workstreamId,
        message.querySelector("[data-workstream-results]")
      );
    }
  } catch (error) {
    workstreamMessage(`<p>${escapeHtml(activeLocaleText("לא הצלחתי לטעון את עדכון המעקב.", "I couldn't load the workstream update."))}</p><div class="answer-callout">${escapeHtml(error.message)}</div>`);
  }
}

async function archiveWorkstreamFromChat(workstreamId) {
  try {
    const response = await fetch(`/api/workstreams/${encodeURIComponent(workstreamId)}/archive?locale=${encodeURIComponent(currentLocale())}`, { method: "POST" });
    const archived = await response.json();
    if (!response.ok) throw new Error(archived.error || activeLocaleText("העברת המעקב לארכיון נכשלה", "Failed to archive workstream"));
    state.workstreams = state.workstreams.map(item => item.workstream_id === workstreamId ? archived : item);
    renderWorkstreamIndicator();
    workstreamMessage(`<p>${escapeHtml(activeLocaleText("המעקב", "The workstream"))} <strong>${escapeHtml(archived.title || "")}</strong> ${escapeHtml(activeLocaleText("הועבר לארכיון.", "was archived."))}</p>`);
  } catch (error) {
    workstreamMessage(`<p>${escapeHtml(activeLocaleText("לא הצלחתי להעביר את המעקב לארכיון.", "I couldn't archive the workstream."))}</p><div class="answer-callout">${escapeHtml(error.message)}</div>`);
  }
}

function startAssistantResearchMessage(message = "") {
  const shouldFollow = conversationIsNearBottom();
  const article = document.createElement("article");
  article.className = "message assistant-message";
  article.innerHTML = `
    <div class="message-label">${escapeHtml(assistantMessageLabel())}</div>
    <section class="research-process research-process-live">
      <h3>${escapeHtml(activeLocaleText("תהליך המחקר", "Research process"))}</h3>
      <ol class="activity-list"></ol>
      <div class="activity-empty">${message ? escapeHtml(message) : thinkingIndicatorHtml()}</div>
    </section>`;
  conversation.appendChild(article);
  state.activeAssistantMessage = article;
  state.activeActivityEmpty = article.querySelector(".activity-empty");
  state.activeActivityList = article.querySelector(".activity-list");
  followConversationAfterUpdate(shouldFollow);
  return article;
}

function ensureAssistantResearchMessage(message) {
  if (!state.activeAssistantMessage || !state.activeActivityList || !state.activeActivityEmpty) {
    startAssistantResearchMessage(message);
  }
}

function setActiveResearchMessage(message) {
  const shouldFollow = conversationIsNearBottom();
  ensureAssistantResearchMessage(message);
  state.activeActivityList.innerHTML = "";
  state.activeActivityEmpty.hidden = false;
  state.activeActivityEmpty.textContent = message;
  followConversationAfterUpdate(shouldFollow);
}

function finalizeAssistantMessage(answer, options = {}) {
  const shouldFollow = conversationIsNearBottom();
  ensureAssistantResearchMessage();
  const article = state.activeAssistantMessage;
  const label = article.querySelector(".message-label");
  if (label && options.result) label.textContent = resultMessageLabel(options.result);
  const existingList = state.activeActivityList;
  const stepsCount = existingList ? existingList.children.length : 0;
  const research = article.querySelector(".research-process");
  const details = document.createElement("details");
  details.className = "research-steps-toggle";
  details.innerHTML = `<summary>${escapeHtml(activeLocaleText("תהליך המחקר", "Research process"))}${stepsCount ? ` · ${stepsCount} ${escapeHtml(activeLocaleText("צעדים", "steps"))}` : ""}</summary>`;
  if (existingList && stepsCount) {
    details.appendChild(existingList);
  } else {
    const empty = document.createElement("div");
    empty.className = "activity-empty";
    empty.textContent = activeLocaleText("לא התקבל פירוט צעדי מחקר.", "No research-step details were received.");
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
    const finalId = finalSourceId(options.result);
    const hasRequestedResults = buildTypedResultLayers(options.result).length > 0;
    actions.innerHTML = `
      ${hasRequestedResults ? `<button type="button" class="final-answer-show-btn layers-hidden" data-source-id="${escapeHtml(finalId)}" title="${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}" aria-label="${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}" aria-pressed="false">
        <span class="final-answer-show-label">${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}</span>
      </button>` : ""}
      <button type="button" class="final-answer-save-btn" ${options.result.saved_question_id ? "disabled" : ""}>${options.result.saved_question_id ? activeLocaleText("נשמר", "Saved") : activeLocaleText("שמור הקלטה", "Save run")}</button>
      <button type="button" class="final-answer-memory-btn" ${options.result.investigation_memory_summary_id ? "disabled" : ""}>${options.result.investigation_memory_summary_id ? activeLocaleText("נשמר בזיכרון", "Saved to memory") : activeLocaleText("שמור לזיכרון", "Save to memory")}</button>
    `;
    const finalShowBtn = actions.querySelector(".final-answer-show-btn");
    if (finalShowBtn) {
      finalShowBtn.addEventListener("click", () => {
        toggleFinalAnswerVisibility(options.result, options.prompt || "", finalShowBtn);
      });
    }
    actions.querySelector(".final-answer-save-btn").addEventListener("click", event => {
      saveResultQuestion(options.result, options.prompt || "", event.currentTarget);
    });
    actions.querySelector(".final-answer-memory-btn").addEventListener("click", event => {
      saveResultToInvestigationMemory(options.result, options.prompt || "", event.currentTarget);
    });
    let evidenceToggle = answerBody.querySelector(".evidence-ids-toggle");
    const evidenceReferences = buildEvidenceReferencesSection(options.result);
    if (evidenceReferences && evidenceToggle) {
      evidenceToggle.remove();
      evidenceToggle = null;
    }
    if (evidenceToggle) {
      answerBody.insertBefore(actions, evidenceToggle);
    } else {
      answerBody.appendChild(actions);
    }
    if (evidenceReferences) answerBody.appendChild(evidenceReferences);
    if (finalShowBtn) updateSourceVisibilityBtn(finalShowBtn);
    updateEvidenceReferenceButtons();
  }
  state.activeAssistantMessage = null;
  state.activeActivityList = null;
  state.activeActivityEmpty = null;
  followConversationAfterUpdate(shouldFollow);
}

function showFinalAnswerResult(result, prompt) {
  if (!result) return;
  applyAgentResult(result, prompt, { keepRenderedSteps: true, restoreOnly: true });
}

function toggleFinalAnswerVisibility(result, prompt, btn) {
  const sourceId = sanitizeLayerKey(btn?.dataset.sourceId || finalSourceId(result));
  const sourceLayers = state.layers.filter(layer => layer.sourceId === sourceId);
  const anyVisible = sourceLayers.some(layer => layer.visible);
  if (!sourceLayers.length || !anyVisible) {
    showFinalAnswerResult(result, prompt);
    return;
  }
  sourceLayers.forEach(layer => { layer.visible = false; });
  updateSourceVisibilityBtn(btn);
  renderAllViews();
}

const TOOL_LABELS = {
  classify_question_intent: "Question intent classification",
  resolve_location: "Location resolution",
  resolve_event_reference: "Anchor event identification",
  search_events: "Focused dataset search",
  semantic_search_events: "Semantic dataset search",
  get_objects: "Object retrieval",
  find_actor_history: "Actor history check",
  aggregate_events: "Cluster identification",
  explain_linkage: "Evidence bridge check",
  build_event_sequence: "Event sequence building",
  resolve_entity: "Name and alias resolution",
  trace_identifier: "Recurring identifier trace",
  trace_semantic_clues: "Semantic clue tracing",
  plan_next_investigation_step: "Investigation flow control",
  find_related_events: "Evidence expansion",
  challenge_hypothesis: "Hypothesis challenge",
  prepare_target_candidate: "Target candidate preparation",
  find_duplicate_target_candidates: "Target duplicate check",
  search_target_candidates: "Target candidate search",
  get_target_candidate: "Target candidate retrieval",
  create_target_candidate: "Target candidate creation",
  update_target_candidate: "Target candidate update",
  attach_target_evidence: "Attach evidence to target"
};

function humanToolLabel(tool) {
  const clean = String(tool || "").replace(/^\d+\.\s*/, "");
  if (TOOL_LABELS[clean]) return TOOL_LABELS[clean];
  const readable = clean.replace(/[_-]+/g, " ").trim();
  return readable ? readable.charAt(0).toUpperCase() + readable.slice(1) : "Investigation action";
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

function resolveFinalResultView(result = {}, layers = []) {
  const requestedView = ["map", "timeline"].includes(result.recommended_view)
    ? result.recommended_view
    : layers.find(layer => ["map", "timeline"].includes(layer.preferredView))?.preferredView;
  if (["map", "timeline"].includes(requestedView)) return requestedView;
  if (layers.some(layer => layer.capabilities?.map)) return "map";
  if (layers.some(layer => layer.capabilities?.timeline)) return "timeline";
  return "map";
}

function presentFinalAgentResult(result, prompt, options = {}) {
  const typedLayers = buildTypedResultLayers(result);
  const requestedView = resolveFinalResultView(result, typedLayers);
  state.queryContext = buildFinalQueryContext(result, prompt);
  const addedLayers = addResultLayers({
    sourceId: finalSourceId(result),
    sourceLabel: result.responding_agent === "moshe" ? activeLocaleText("תשובת משה", "Moshe response") : activeLocaleText("תשובת הסוכן", "Agent response"),
    preferredView: requestedView,
    layers: typedLayers
  });
  if (options.showSummary) {
    showResult(
      activeLocaleText("ממצאי הסוכן", "Agent findings"),
      localizedRestoreOnlySummary(addedLayers.length)
    );
  }
  activateView(requestedView, {
    automatic: true,
    reason: result.view_reason || activeLocaleText("הנתונים נבחרו כתשובה לבקשת המשתמש", "Data selected as the answer to the user's request")
  });
  renderAllViews();
  renderQueryInspector();
  return addedLayers;
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
      tool: activeLocaleText("אין שאילתה פעילה", "No active query"),
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
  if (queryLayerName) queryLayerName.textContent = layerQueryLabels()[layer] || activeLocaleText("שכבת אירועים גולמיים", "Raw events layer");
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

// ── Step Inject (Continue from here) ────────────────────────────────────────

const stepInjectModal = document.getElementById("stepInjectModal");
const stepInjectTitle = document.getElementById("stepInjectTitle");
const stepInjectPrompt = document.getElementById("stepInjectPrompt");
const stepInjectLayers = document.getElementById("stepInjectLayers");
const stepInjectLayersGroup = document.getElementById("stepInjectLayersGroup");
const stepInjectSubmit = document.getElementById("stepInjectSubmit");
const stepInjectClose = document.getElementById("stepInjectClose");
const stepInjectError = document.getElementById("stepInjectError");

function openStepInjectModal(stepLabel, stepNumber) {
  stepInjectModal.dataset.fromStep = stepNumber;
  stepInjectTitle.textContent = activeLocaleText(`צעד ${stepNumber}: ${stepLabel}`, `Step ${stepNumber}: ${stepLabel}`);
  stepInjectPrompt.value = "";
  syncMentionHighlight(stepInjectPrompt);
  stepInjectError.hidden = true;
  stepInjectError.textContent = "";

  const visibleLayers_ = state.layers.filter(l => l.visible && l.capabilities?.table);
  stepInjectLayersGroup.hidden = visibleLayers_.length === 0;
  stepInjectLayers.innerHTML = visibleLayers_.map(layer => `
    <label class="step-inject-layer-item" style="${layerColorStyle(layer)}">
      <input type="checkbox" value="${escapeHtml(layer.id)}" checked>
      <span class="step-inject-layer-color"></span>
      <span class="step-inject-layer-name">${escapeHtml(layer.label)}</span>
      <span class="step-inject-layer-count">${itemsForLayerPresentation(layer).length.toLocaleString("en-US")}</span>
    </label>`).join("");

  stepInjectSubmit.disabled = false;
  stepInjectSubmit.textContent = activeLocaleText("שלח להמשך חקירה", "Send to continue investigation");
  stepInjectModal.hidden = false;
  stepInjectPrompt.focus();
}

function closeStepInjectModal() {
  if (stepInjectModal) stepInjectModal.hidden = true;
}

function originalClassificationContext(steps) {
  const classificationStep = (steps || []).find(step => step?.tool === "classify_question_intent");
  if (!classificationStep) return null;
  const text = [classificationStep.action, classificationStep.result].filter(Boolean).join(" ");
  return {
    action: classificationStep.action || "",
    result: classificationStep.result || "",
    summary: text
  };
}

function buildContinuationPrompt(instruction, selectedLayers, classificationContext = null) {
  const lines = [`User instruction: ${instruction}`];
  if (classificationContext?.summary) {
    lines.push(
      "\nOriginal investigation frame to preserve:",
      classificationContext.summary,
      "Do not reclassify the question. Continue with the same recommended_mode and tool_budget set by the original classification."
    );
  }
  if (selectedLayers.length) {
    lines.push("\nLayers selected for continuation:");
    selectedLayers.forEach(layer => {
      const items = itemsForLayerPresentation(layer);
      const eventIds = items.map(item => item.event_id).filter(Boolean).slice(0, 100);
      lines.push(`- ${layer.label}: ${items.length} records${eventIds.length ? `, IDs: ${eventIds.join(", ")}` : ""}`);
    });
  }
  return lines.join("\n");
}

async function submitStepInject() {
  const instruction = stepInjectPrompt.value.trim();
  if (!instruction) {
    stepInjectError.textContent = "Enter an instruction for the agent.";
    stepInjectError.hidden = false;
    return;
  }
  if (state.busy) {
    stepInjectError.textContent = "An investigation is already running — wait for it to finish.";
    stepInjectError.hidden = false;
    return;
  }

  const checkedIds = new Set(
    [...stepInjectLayers.querySelectorAll("input[type=checkbox]:checked")].map(cb => cb.value)
  );
  const selectedLayers = state.layers.filter(l => checkedIds.has(l.id));

  stepInjectSubmit.disabled = true;
  stepInjectSubmit.textContent = "Sending...";
  stepInjectError.hidden = true;
  closeStepInjectModal();

  state.busy = true;
  sendButton.disabled = true;
  sendButton.textContent = "↑";

  // Snapshot only steps up to (and including) the step that triggered the continuation
  const fromStep = parseInt(stepInjectModal.dataset.fromStep, 10) || 0;
  const allPriorSteps = state.lastResult?.investigation_steps || [];
  const priorSteps = fromStep > 0 ? allPriorSteps.slice(0, fromStep) : allPriorSteps;
  const priorResult = state.lastResult;
  const baseStepCount = priorSteps.length;
  const classificationContext = originalClassificationContext(priorSteps.length ? priorSteps : allPriorSteps);
  const addressedInstruction = addressedPromptForSelectedMember(instruction);
  state.activeTeamMentions = teamMentionsForPrompt(addressedInstruction);
  const continuationPrompt = buildContinuationPrompt(addressedInstruction, selectedLayers, classificationContext);
  const agentContinuationPrompt = promptForAgent(continuationPrompt);

  // Start a new labeled continuation bubble
  startAssistantResearchMessage();
  // Mark the article so CSS can show the ↩ continuation kicker
  if (state.activeAssistantMessage) {
    state.activeAssistantMessage.dataset.continuation = "true";
  }

  // Render all prior steps first so the analyst has full context in one place
  if (priorResult && priorSteps.length) {
    renderActivitySteps(priorSteps, priorResult);
  }

  let progressTimer = null;
  let liveStepCount = 0;

  const pollContinuationSteps = async () => {
    try {
      const response = await fetch(liveStepsUrl(addressedInstruction), { cache: "no-store" });
      if (!response.ok) return;
      const live = await response.json();
      const steps = live.investigation_steps || [];
      if (steps.length > liveStepCount) {
        steps.slice(liveStepCount).forEach((step, i) => {
          const num = baseStepCount + liveStepCount + i + 1;
          addActivity(step.tool, step.action, step.result, {
            stepNumber: num,
            bridgeSummary: step.bridge_summary,
            rationale: step.rationale || step.decision,
            technical: step.technical,
            isError: step.technical?.is_error,
            stepData: step,
            sourceId: stepSourceId(state.investigationId, num),
            sourceLabel: `Step ${num}: ${humanToolLabel(step.tool)}`
          });
        });
        liveStepCount = steps.length;
      }
    } catch (_) {}
  };

  try {
    progressTimer = setInterval(pollContinuationSteps, 1800);
    setTimeout(pollContinuationSteps, 900);
    const response = await fetch("/api/investigate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt: agentContinuationPrompt,
        routing_prompt: addressedInstruction,
        history: state.history,
        investigation_id: state.investigationId,
        investigation_state: investigationStateForPrompt(selectedLayerContextForAgent()),
        continuation_context: {
          original_classification: classificationContext,
          from_step: fromStep || null
        },
        is_continuation: true,
        locale: currentLocale()
      })
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Hermes request failed");
    result.answer = cleanAssistantAnswer(result.answer);
    state.history.push({ role: "user", content: continuationPrompt }, { role: "assistant", content: result.answer });
    // Merge prior steps with new steps so the full chain is in state
    const newSteps = result.investigation_steps || [];
    result.investigation_steps = [...priorSteps, ...newSteps];
    applyAgentResult(result, continuationPrompt, { keepRenderedSteps: true });
  } catch (error) {
    addActivity("connection_error", "Unable to complete the investigation continuation.", error.message);
    finalizeAssistantMessage(`<p>I couldn't complete the investigation continuation.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`, { html: true });
  } finally {
    if (progressTimer) clearInterval(progressTimer);
    state.busy = false;
    sendButton.disabled = false;
    sendButton.textContent = "↑";
  }
}

if (stepInjectClose) stepInjectClose.addEventListener("click", closeStepInjectModal);
if (stepInjectModal) stepInjectModal.addEventListener("click", e => { if (e.target === stepInjectModal) closeStepInjectModal(); });
if (stepInjectSubmit) stepInjectSubmit.addEventListener("click", submitStepInject);
if (stepInjectPrompt) stepInjectPrompt.addEventListener("keydown", e => {
  if (handleTeamMentionKeydown(e)) return;
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) submitStepInject();
});

// ── End Step Inject ──────────────────────────────────────────────────────────

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

  // Build a synthetic result object compatible with the shared agent visualization path.
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
      summary: `${Number(group.count || 0).toLocaleString("en-US")} events`
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
    sourceLabel: step.__sourceLabel || `Step ${step.__stepNumber || ""}: ${label}`.trim(),
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
    `Step: ${label}`,
    hasData
      ? `${addedLayers.length.toLocaleString("en-US")} layers were added or shown from this step.`
      : "This step did not return data that can be displayed."
  );

  if (state.aggregateTimeline.length) {
    activateView("timeline", { automatic: true, reason: "Step with time data" });
  } else if (state.aggregateLocations.length || state.locationMetadata.length || state.entityMetadata.length || state.current.some(e => e.location_id)) {
    activateView("map", { automatic: true, reason: "Step with location data" });
  } else {
    activateView("map", { automatic: true, reason: "Step with records" });
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
  const label = btn.querySelector(".step-visibility-label, .final-answer-show-label");
  const actionLabel = label
    ? (anyVisible ? activeLocaleText("הסתר תוצאות", "Hide results") : activeLocaleText("הצג תוצאות", "Show results"))
    : (anyVisible ? activeLocaleText("הסתר שכבות", "Hide layers") : activeLocaleText("הצג שכבות", "Show layers"));
  btn.title = actionLabel;
  btn.setAttribute("aria-label", actionLabel);
  btn.setAttribute("aria-pressed", anyVisible ? "true" : "false");
  if (label) label.textContent = actionLabel;
}

function updateStepVisibilityButtons() {
  document.querySelectorAll(".step-visibility-btn").forEach(updateSourceVisibilityBtn);
}

function updateResultVisibilityButtons() {
  updateStepVisibilityButtons();
  document.querySelectorAll(".final-answer-show-btn").forEach(updateSourceVisibilityBtn);
  updateEvidenceReferenceButtons();
}

function resolvedStepSourceId(step) {
  if (step.__sourceId) {
    const sourceId = sanitizeLayerKey(step.__sourceId);
    const oldLiveBase = sanitizeLayerKey(state.investigationId);
    if (state.lastResult?.run_id && oldLiveBase && sourceId.includes(oldLiveBase)) {
      return sanitizeLayerKey(stepSourceId(state.lastResult, step.__stepNumber));
    }
    return sourceId;
  }
  if (state.lastResult && step.__stepNumber) {
    return sanitizeLayerKey(stepSourceId(state.lastResult, step.__stepNumber));
  }
  return sanitizeLayerKey(stepSourceId(state.lastResult || state.investigationId, step.__stepNumber));
}

function toggleStepVisibility(step, btn) {
  const sourceId = sanitizeLayerKey(btn?.dataset.sourceId || resolvedStepSourceId(step));
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
  const shouldFollow = options.manageConversationScroll !== false && conversationIsNearBottom();
  ensureAssistantResearchMessage();
  const item = document.createElement("li");
  item.className = "activity-item";
  const stepNumber = options.stepNumber || state.activeActivityList.children.length + 1;
  const cleanTool = String(tool || "").replace(/^\d+\.\s*/, "");
  const bridgeSummary = options.bridgeSummary || options.rationale || activeLocaleText("הסוכן ממשיך בצעד הזה כדי לצמצם את השאלה לפי ההקשר שנאסף עד כה.", "The agent continues with this step to narrow the question using the context gathered so far.");
  const baseStepData = options.stepData || {
    tool: cleanTool,
    action: detail,
    result,
    technical: options.technical || { tool: cleanTool, arguments: {} }
  };
  const stepData = {
    ...baseStepData,
    __sourceId: options.sourceId || baseStepData.__sourceId || stepSourceId(state.lastResult || state.investigationId, stepNumber),
    __sourceLabel: options.sourceLabel || baseStepData.__sourceLabel || `Step ${stepNumber}: ${humanToolLabel(cleanTool)}`,
    __stepNumber: stepNumber
  };
  const hasStepData = Boolean(stepData);
  const sourceId = sanitizeLayerKey(stepData.__sourceId);
  const label = humanToolLabel(cleanTool);
  const queryDetails = stepQueryDetails(stepData, label);
  item.innerHTML = `
    <details class="activity-disclosure">
      <summary class="activity-card-summary" aria-label="${escapeHtml(activeLocaleText(`פתח פרטי שלב ${stepNumber}: ${label}`, `Expand step ${stepNumber}: ${label}`))}">
        <span class="activity-step-number">${stepNumber}</span>
        <strong class="activity-step-title">${escapeHtml(label)}</strong>
        <span class="material-symbols-rounded activity-expand-icon" aria-hidden="true">expand_more</span>
      </summary>
      <div class="activity-expanded">
        <div class="activity-card-meta">
          <span class="activity-tool">${escapeHtml(cleanTool)}</span>
          <span class="activity-status ${options.isError ? "error" : "success"}">${options.isError ? activeLocaleText("נכשל", "Failed") : activeLocaleText("הושלם", "Completed")}</span>
        </div>
        <div class="activity-flow">
          <section class="activity-section rationale-section">
            <div class="activity-section-label">${activeLocaleText("ניתוח הסוכן והחלטת הצעד הבא", "Agent analysis and next-step decision")}</div>
            <p class="activity-rationale">${escapeHtml(bridgeSummary)}</p>
          </section>
          <section class="activity-section">
            <div class="activity-section-label">${activeLocaleText("מה נבדק", "What was checked")}</div>
            <p class="activity-detail">${escapeHtml(detail)}</p>
          </section>
          <section class="activity-section result-section">
            <div class="activity-section-label">${activeLocaleText("מה חזר", "What came back")}</div>
            <p class="activity-result">${escapeHtml(result)}</p>
          </section>
        </div>
        ${hasStepData ? `
          <div class="activity-step-actions">
            <button type="button" class="step-visibility-btn layers-hidden" data-source-id="${escapeHtml(sourceId)}" title="${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}" aria-label="${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}" aria-pressed="false">
              <span class="step-visibility-label">${escapeHtml(activeLocaleText("הצג תוצאות", "Show results"))}</span>
            </button>
            <button type="button" class="step-query-btn" title="${escapeHtml(activeLocaleText("הצג שאילתה", "Show query"))}">${activeLocaleText("הצג שאילתה", "Show query")}</button>
            <button type="button" class="step-continue-btn" title="${escapeHtml(activeLocaleText("המשך מהשלב הזה", "Continue from this step"))}">${activeLocaleText("המשך מכאן", "Continue from here")}</button>
          </div>` : ""}
      </div>
    </details>`;
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
    const continueBtn = item.querySelector(".step-continue-btn");
    continueBtn.addEventListener("click", () => openStepInjectModal(label, stepNumber));
  }
  state.activeActivityList.appendChild(item);
  followConversationAfterUpdate(shouldFollow);
}

function setSuggestions(items) {
  suggestions.innerHTML = items.map(item => `<button type="button" data-prompt="${item}">${item}</button>`).join("");
}

function localizedRestoreOnlySummary(layerCount) {
  return layerCount
    ? activeLocaleText(
        `${layerCount.toLocaleString(currentLocaleTag())} שכבות נוספו או הוצגו כתשובה.`,
        `${layerCount.toLocaleString(currentLocaleTag())} layers were added or shown as the answer.`
      )
    : activeLocaleText("לא נבחרו נתונים להצגה.", "No data was selected for display.");
}

function eventText(event) {
  return `${event.event_summary} ${event.entity_name || event.entity_id || ""} ${event.location_name}`;
}

function answerHtml(text) {
  const normalized = String(text || "")
    .replace(/(^|\n)(\s*(?:Evidence|Event)\s+IDs\s*:)/m, "\n\n$2")
    .trim();
  const escaped = escapeHtml(normalized);
  if (!escaped) return "<p></p>";
  return escaped.split(/\n{2,}/).map(block => {
    const trimmed = block.trim();
    const evidenceMatch = trimmed.match(/^(?:Evidence|Event)\s+IDs\s*:\s*(.+)$/s);
    if (evidenceMatch) {
      return `<details class="evidence-ids-toggle"><summary>Evidence IDs</summary><p>${evidenceMatch[1].replace(/\n/g, "<br>")}</p></details>`;
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
    .replace(/^\s*Investigation step\s*:.*(?:\r?\n|$)/gm, "")
    .trim();
}

function inferRecommendedView(prompt, answer) {
  const text = `${prompt || ""}\n${answer || ""}`;
  const scores = { map: 0, timeline: 0, evidence: 0 };
  const scoreTerms = (view, terms, weight = 1) => terms.forEach(term => {
    if (text.includes(term)) scores[view] += weight;
  });

  scoreTerms("map", ["map", "route", "movement path", "location", "area", "distance", "west", "east", "road", "crossing"], 2);
  scoreTerms("timeline", ["sequence", "time order", "timeline", "before", "after", "timing", "at", "minutes", "started", "ended"], 2);
  scoreTerms("evidence", ["raw events", "records", "sources", "evidence", "quote", "verification", "check", "evidence ids"], 2);

  if (/\b\d{2}:\d{2}\b/.test(text)) scores.timeline += 2;
  if ((answer || "").match(EVENT_ID_PATTERN)?.length >= 6) scores.evidence += 1;
  const view = Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0];
  const reasons = {
    map: "Locations and movement route are central to the answer",
    timeline: "Event sequence and timing are central to the answer",
    evidence: "Evidence and records are central to the answer"
  };
  return { view, reason: reasons[view] };
}

function visibleActivitySteps(steps) {
  const internalWorkstreamTools = new Set([
    "prepare_workstream_creation",
    "prepare_workstream_indication_proposal",
    "decide_workstream_indication_proposal"
  ]);
  return (steps || []).filter(step => !internalWorkstreamTools.has(step.tool));
}

function renderActivitySteps(steps, sourceBase = null) {
  const shouldFollow = conversationIsNearBottom();
  ensureAssistantResearchMessage();
  state.activeActivityList.innerHTML = "";
  visibleActivitySteps(steps).forEach((step, index) => {
    const explanation = step.model_explanation || {};
    const number = index + 1;
    addActivity(step.tool, step.action, step.result, {
      stepNumber: number,
      bridgeSummary: explanation.bridge_summary || step.bridge_summary,
      rationale: explanation.decision || step.rationale || step.decision,
      technical: step.technical,
      isError: step.technical?.is_error,
      manageConversationScroll: false,
      stepData: step,
      sourceId: stepSourceId(sourceBase || state.lastResult || state.investigationId, number),
      sourceLabel: `Step ${number}: ${humanToolLabel(step.tool)}`
    });
  });
  followConversationAfterUpdate(shouldFollow);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const SAVED_REPLAY_STEP_DELAY_MS = 2000;

async function replaySavedResult(result, prompt) {
  const steps = visibleActivitySteps(result.investigation_steps || []);
  if (!steps.length) {
    applyAgentResult(result, prompt);
    return;
  }
  startAssistantResearchMessage();
  for (let index = 0; index < steps.length; index += 1) {
    if (index > 0) await sleep(SAVED_REPLAY_STEP_DELAY_MS);
    renderActivitySteps(steps.slice(0, index + 1), result);
  }
  await sleep(SAVED_REPLAY_STEP_DELAY_MS);
  applyAgentResult(result, prompt, { keepRenderedSteps: true });
}

function canSaveResult(result, prompt) {
  return Boolean(
    prompt
    && result
    && result.answer
    && !result.demo_replay
    && !result.recorded_id
    && !result.saved_question_id
  );
}

function canSaveResultToMemory(result, prompt) {
  return Boolean(
    state.investigationId
    && prompt
    && result
    && result.answer
    && !result.demo_replay
    && !result.recorded_id
    && !result.investigation_memory_summary_id
  );
}

function formatSavedTime(value) {
  if (!value) return activeLocaleText("זמן השמירה לא ידוע", "Save time unknown");
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString(currentLocaleTag(), {
    dateStyle: "short",
    timeStyle: "short",
  });
}

async function saveResultQuestion(result, prompt, button) {
  if (!canSaveResult(result, prompt) || state.busy || button?.disabled) return;
  button.disabled = true;
  button.textContent = activeLocaleText("שומר...", "Saving...");
  button.title = activeLocaleText("שומר את תוצאת החקירה", "Saving the investigation result");
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const title = prompt.trim().slice(0, 60);
    const response = await fetch("/api/saved-question", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      signal: controller.signal,
      body: JSON.stringify({
        title,
        question: prompt,
        result,
      }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("שמירת השאלה נכשלה", "Failed to save question"));
    result.saved_question_id = payload.id;
    if (state.lastResult === result) state.lastResult = result;
    button.textContent = activeLocaleText("נשמר", "Saved");
    button.title = activeLocaleText("תוצאת החקירה נשמרה", "Investigation result saved");
    if (!recordedModal.hidden) loadRecordedQuestions();
  } catch (error) {
    const message = error.name === "AbortError"
      ? activeLocaleText("שמירת השאלה ארכה יותר מדי זמן. נסו שוב.", "Saving the question took too long. Try again.")
      : error.message;
    button.textContent = activeLocaleText("נכשל", "Failed");
    button.title = message;
    setTimeout(() => {
      if (!result.saved_question_id) {
        button.disabled = false;
        button.textContent = activeLocaleText("שמור הקלטה", "Save run");
        button.title = activeLocaleText("שמור את ריצת החקירה", "Save the investigation run");
      }
    }, 2500);
  } finally {
    clearTimeout(timeout);
  }
}

async function saveResultToInvestigationMemory(result, prompt, button) {
  if (state.draftSessionActive) {
    openDraftCreateModal(() => saveResultToInvestigationMemory(result, prompt, button));
    return;
  }
  if (!canSaveResultToMemory(result, prompt) || state.busy || button?.disabled) return;
  button.disabled = true;
  button.textContent = activeLocaleText("שומר לזיכרון...", "Saving to memory...");
  button.title = activeLocaleText("שומר את הממצא לזיכרון החקירה", "Saving the finding to investigation memory");
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch("/api/investigation-memory/chat-summary", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      signal: controller.signal,
      body: JSON.stringify({
        investigation_id: state.investigationId,
        name: state.investigationName,
        prompt,
        result,
      }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("שמירה לזיכרון החקירה נכשלה", "Failed to save to investigation memory"));
    result.investigation_memory_summary_id = payload.saved?.id || true;
    if (state.lastResult === result) state.lastResult = result;
    button.textContent = activeLocaleText("נשמר בזיכרון", "Saved to memory");
    button.title = activeLocaleText("הממצא נשמר בזיכרון החקירה", "Finding saved to investigation memory");
  } catch (error) {
    const message = error.name === "AbortError"
      ? activeLocaleText("השמירה לזיכרון ארכה יותר מדי זמן. נסו שוב.", "Saving to memory took too long. Try again.")
      : error.message;
    button.textContent = activeLocaleText("נכשל", "Failed");
    button.title = message;
    setTimeout(() => {
      if (!result.investigation_memory_summary_id) {
        button.disabled = false;
        button.textContent = activeLocaleText("שמור לזיכרון", "Save to memory");
        button.title = activeLocaleText("שמור את הממצא לזיכרון החקירה", "Save the finding to investigation memory");
      }
    }, 2500);
  } finally {
    clearTimeout(timeout);
  }
}

async function deleteSavedQuestion(savedId) {
  if (!savedId || state.busy) return;
  try {
    const response = await fetch(`/api/saved-question?id=${encodeURIComponent(savedId)}`, { method: "DELETE" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("מחיקת השאלה נכשלה", "Failed to delete question"));
    state.savedQuestions = state.savedQuestions.filter(item => item.id !== savedId);
    loadRecordedQuestions();
  } catch (error) {
    recordedList.innerHTML = `<div class="activity-empty">${activeLocaleText("מחיקת השאלה השמורה נכשלה", "Failed to delete saved question")}: ${escapeHtml(error.message)}</div>`;
  }
}

function applyAgentResult(result, prompt, options = {}) {
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
      document.querySelectorAll(".step-visibility-btn").forEach(btn => {
        if (btn.dataset.sourceId && btn.dataset.sourceId.includes(oldBase)) {
          btn.dataset.sourceId = btn.dataset.sourceId.replace(oldBase, newBase);
        }
      });
    }
    state.lastResult = result;
    state.lastPrompt = prompt;
    state.rawOverlayMinimized = false;
    state.rawOverlayHeight = 28;
  }

  if (options.restoreOnly) {
    presentFinalAgentResult(result, prompt, { showSummary: true });
    return;
  }
  if (!options.keepRenderedSteps) renderActivitySteps(result.investigation_steps || [], result);
  if (!options.keepRenderedSteps && !(result.investigation_steps || []).length) {
    const started = (result.events || []).filter(event => event.event === "tool.started");
    started.forEach((event, index) => {
      const tool = (event.tool || "MCP").replace(/^mcp_(?:serbia_events_poc|intelligence_events_poc)_/, "");
      const input = event.preview ? `Input sent to the tool: ${event.preview}` : "Hermes did not return the input details for this action.";
      addActivity(tool, input, "The tool completed without error; result details were not included in the Hermes log.", {
        stepNumber: index + 1,
        observedClue: "Hermes reported that the agent chose to run a tool, but did not return a detailed clue for this step.",
        rationale: "The agent chose this tool to keep reducing uncertainty in the investigation.",
        expectedValue: "Get more evidence or validate a candidate that already surfaced.",
        technical: { tool, preview: event.preview || null },
        sourceId: stepSourceId(result, index + 1),
        sourceLabel: `Step ${index + 1}: ${humanToolLabel(tool)}`
      });
    });
  }
  if (!options.keepRenderedSteps && !(result.investigation_steps || []).length && !(result.events || []).some(event => event.event === "tool.started")) {
    addActivity("Hermes", `Investigation question sent: ${prompt}`, `A response was received in run ${result.run_id}, without a detailed tool log.`);
  }

  finalizeAssistantMessage(result.answer, { result, prompt });
  presentFinalAgentResult(result, prompt);
  if (buildTypedResultLayers(result).some(layer => layer.kind === "attack_targets")) {
    void refreshOpenAttackTargetCatalogLayer();
  }
  updateResultVisibilityButtons();
  renderQueryInspector();
  setSuggestions(FOLLOWUP_SUGGESTIONS[currentLocale()]);
}

async function runSavedQuestion(savedId) {
  if (state.busy) return;
  closeRecordedModal();
  state.busy = true;
  sendButton.disabled = true;
  promptOptionsButton.disabled = true;
  sendButton.textContent = "↑";
  try {
    const response = await fetch(`/api/saved-question?id=${encodeURIComponent(savedId)}`, { cache: "no-store" });
    const saved = await response.json();
    if (!response.ok) throw new Error(saved.error || activeLocaleText("טעינת השאלה השמורה נכשלה", "Failed to load saved question"));
    const result = {
      ...(saved.result || {}),
      saved_question_id: saved.id,
      source_run_id: saved.source_run_id || saved.result?.run_id,
    };
    const prompt = (saved.question || "").trim();
    appendMessage("user", `<p>${highlightedPromptHtml(prompt)}</p>`);
    state.history.push({ role: "user", content: prompt }, { role: "assistant", content: result.answer || "" });
    if (result.workstream_recording?.kind === "detail" && result.workstream_recording?.workstream) {
      const message = appendWorkstreamUpdate(result.workstream_recording.workstream, {
        recorded: true,
        recording: result.workstream_recording,
      });
      await showRecordedWorkstreamPresentation(
        result.workstream_recording,
        message.querySelector("[data-recorded-workstream-results]")
      );
    } else {
      await replaySavedResult(result, prompt);
    }
  } catch (error) {
    startAssistantResearchMessage(activeLocaleText("טעינת השאלה השמורה נכשלה.", "Loading saved question failed."));
    finalizeAssistantMessage(`<p>${activeLocaleText("לא הצלחתי להציג את השאלה השמורה.", "I couldn't display the saved question.")}</p><div class="answer-callout">${escapeHtml(error.message)}</div>`, { html: true });
  } finally {
    state.busy = false;
    sendButton.disabled = false;
    promptOptionsButton.disabled = false;
    sendButton.textContent = "↑";
  }
}

function setPromptOptionsOpen(open) {
  state.promptOptionsOpen = Boolean(open);
  if (promptOptionsMenu) promptOptionsMenu.hidden = !state.promptOptionsOpen;
  if (promptOptionsButton) promptOptionsButton.setAttribute("aria-expanded", state.promptOptionsOpen ? "true" : "false");
}

function openRecordedModal() {
  setPromptOptionsOpen(false);
  recordedModal.hidden = false;
  loadRecordedQuestions();
}

function closeRecordedModal() {
  recordedModal.hidden = true;
}

function openQueryLayersModal() {
  setPromptOptionsOpen(false);
  queryLayersModal.hidden = false;
  renderQueryLayersModal();
}

function closeQueryLayersModal() {
  if (queryLayersModal) queryLayersModal.hidden = true;
}

function submitQueryLayerSelection() {
  const checkedIds = new Set(
    [...queryLayersList.querySelectorAll("input[type=checkbox]:checked")].map(cb => cb.value)
  );
  const selectedLayers = state.layers.filter(layer => checkedIds.has(layer.id));
  if (!selectedLayers.length) {
    queryLayersError.textContent = activeLocaleText("בחר לפחות שכבה אחת.", "Choose at least one layer.");
    queryLayersError.hidden = false;
    return;
  }
  if (state.workstreamComposerMode && selectedLayers.length !== 1) {
    queryLayersError.textContent = activeLocaleText("בחר שכבה אחת למעקב.", "Choose one layer for the workstream.");
    queryLayersError.hidden = false;
    return;
  }
  state.promptSelectedLayerIds = checkedIds;
  const firstTableLayer = selectedLayers.find(layer => layer.capabilities.table);
  if (firstTableLayer) state.activeLayerId = firstTableLayer.id;
  state.rawOverlayMinimized = false;
  closeQueryLayersModal();
  renderAllViews();
}

async function loadRecordedQuestions() {
  recordedList.innerHTML = `<div class="activity-empty">${activeLocaleText("טוען שאלות שמורות...", "Loading saved questions...")}</div>`;
  try {
    const response = await fetch("/api/saved-questions", { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("השאלות השמורות אינן זמינות", "Saved questions unavailable"));
    state.savedQuestions = payload.saved_questions || [];
    if (!state.savedQuestions.length) {
      recordedList.innerHTML = `<div class="activity-empty">${activeLocaleText("לא נמצאו שאלות שמורות.", "No saved questions found.")}</div>`;
      return;
    }
    recordedList.innerHTML = state.savedQuestions.map(item => `
      <article class="recorded-question saved-question-card">
        <div class="saved-question-main">
          <strong>${escapeHtml(item.title || item.question || activeLocaleText("שאלה שמורה", "Saved question"))}</strong>
          <p>${escapeHtml(item.question || "")}</p>
          <span>${escapeHtml(formatSavedTime(item.saved_at_utc))} · ${item.recording_type === "workstream_message" ? activeLocaleText("מעקב", "Workstream") : escapeHtml(viewLabels()[item.recommended_view] || item.recommended_view || activeLocaleText("תצוגה", "View"))} · ${Number(item.step_count || 0)} ${activeLocaleText("צעדים", "steps")}</span>
        </div>
        <div class="saved-question-actions">
          <button type="button" data-saved-id="${escapeHtml(item.id)}">${activeLocaleText("פתח", "Open")}</button>
          <button type="button" class="danger-button" data-saved-delete="${escapeHtml(item.id)}">${activeLocaleText("מחק", "Delete")}</button>
        </div>
      </article>
    `).join("");
  } catch (error) {
    recordedList.innerHTML = `<div class="activity-empty">${activeLocaleText("לא הצלחתי לטעון את השאלות השמורות", "Failed to load saved questions")}: ${escapeHtml(error.message)}</div>`;
  }
}

async function runPrompt(prompt, options = {}) {
  const clean = prompt.trim();
  if (!clean || state.busy) return;
  const workstreamCreationRequested = options.workstreamCreation === true;
  const addressedPrompt = addressedPromptForSelectedMember(clean);
  const selectedLayers = selectedLayerContextForAgent();
  state.activeTeamMentions = teamMentionsForPrompt(addressedPrompt);
  const workstreamInstruction = workstreamCreationRequested
    ? "The user is in workstream-creation flow. Conduct a natural conversation: if essential information is missing, ask a short question; once the objective and responsibility are clear, use the workstream creation tool."
    : "";
  const agentPrompt = promptForAgentWithSelectedLayers(
    [addressedPrompt, workstreamInstruction].filter(Boolean).join("\n\n"),
    selectedLayers
  );
  const investigationState = investigationStateForPrompt(selectedLayers);
  const currentTurnMessageId = globalThis.crypto?.randomUUID?.()
    || `turn_${Date.now()}_${Math.random().toString(16).slice(2)}`;
  const clientStarted = performance.now();
  let firstLiveStepAt = null;
  appendMessage("user", `<p>${highlightedPromptHtml(clean)}</p>`);
  startAssistantResearchMessage();
  state.busy = true;
  sendButton.disabled = true;
  sendButton.textContent = "↑";
  suggestions.innerHTML = "";
  let liveStepCount = 0;
  let progressTimer = null;
  const pollLiveSteps = async () => {
    try {
      const response = await fetch(liveStepsUrl(addressedPrompt), { cache: "no-store" });
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
        prompt: agentPrompt,
        routing_prompt: addressedPrompt,
        history: state.history,
        investigation_id: state.investigationId,
        investigation_state: investigationState,
        workstream_context: workstreamContextForChat(currentTurnMessageId),
        workstream_creation_requested: workstreamCreationRequested,
        locale: currentLocale()
      })
    });
    progressTimer = setInterval(pollLiveSteps, 1800);
    setTimeout(pollLiveSteps, 900);
    const response = await investigationRequest;
    const responseReceivedAt = performance.now();
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Hermes request failed");
    applyWorkstreamChatResult(result);
    result.answer = cleanAssistantAnswer(result.answer);
    state.history.push({ role: "user", content: clean }, { role: "assistant", content: result.answer });
    const renderStarted = performance.now();
    applyAgentResult(result, clean);
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
    addActivity("connection_error", activeLocaleText("לא ניתן היה להשלים את ריצת Hermes.", "Unable to complete the Hermes run."), error.message);
    finalizeAssistantMessage(`<p>${activeLocaleText("לא הצלחתי להשלים את ריצת הסוכן האמיתית.", "I couldn't complete the real agent run.")}</p><div class="answer-callout">${escapeHtml(error.message)}</div>`, { html: true });
    updateSystemStatus("agent", "Hermes אינו זמין", "Hermes unavailable", "error");
  } finally {
    if (progressTimer) clearInterval(progressTimer);
    state.busy = false;
    sendButton.disabled = false;
    sendButton.textContent = "↑";
  }
}

function showResult(title, subtitle) {
  if (resultTitle) resultTitle.textContent = title;
  if (resultSubtitle) resultSubtitle.textContent = subtitle;
  if (resultCount) {
    const visibleEvents = visibleEventItems().length;
    const visibleLocationLayers = visibleLayers("map").filter(layer => layer.kind === "locations").reduce((sum, layer) => sum + itemsForLayerPresentation(layer).length, 0);
    const visibleTimeGroups = visibleLayers("timeline").filter(layer => layer.kind === "time_aggregation").reduce((sum, layer) => sum + itemsForLayerPresentation(layer).length, 0);
    resultCount.textContent = visibleEvents
      ? activeLocaleText(`${visibleEvents} אירועים`, `${visibleEvents} events`)
      : (visibleTimeGroups ? activeLocaleText(`${visibleTimeGroups} נקודות זמן`, `${visibleTimeGroups} time points`) : activeLocaleText(`${visibleLocationLayers} מיקומים`, `${visibleLocationLayers} locations`));
  }
  renderAllViews();
}

function renderAllViews() {
  renderMap();
  renderTimeline();
  renderEvidence();
  renderSelectedLayersButton();
  updateResultVisibilityButtons();
}

function activateView(view, options = {}) {
  const requestedView = view === "evidence" ? "map" : view;
  const safeView = viewLabels()[requestedView] ? requestedView : "map";
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
    viewRecommendation.textContent = activeLocaleText(`הסוכן בחר: ${viewLabels()[safeView]} · ${options.reason}`, `Agent selected: ${viewLabels()[safeView]} · ${options.reason}`);
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

function setChatPanelCollapsed(collapsed) {
  state.chatPanelCollapsed = Boolean(collapsed);
  workspace.classList.toggle("chat-panel-collapsed", state.chatPanelCollapsed);
  if (chatPanelToggle) {
    const label = state.chatPanelCollapsed ? "Show chat" : "Collapse chat";
    chatPanelToggle.title = label;
    chatPanelToggle.setAttribute("aria-label", label);
    chatPanelToggle.setAttribute("aria-expanded", state.chatPanelCollapsed ? "false" : "true");
    const icon = chatPanelToggle.querySelector(".material-symbols-rounded");
    if (icon) icon.textContent = state.chatPanelCollapsed ? "chevron_left" : "chevron_right";
  }
  if (state.map) {
    setTimeout(() => {
      state.map.resize();
      renderMap();
    }, 220);
  }
}

function initPanelResizers() {
  document.querySelectorAll(".panel-resizer").forEach(handle => {
    handle.addEventListener("pointerdown", event => {
      if (event.target.closest(".chat-panel-toggle") || state.chatPanelCollapsed) return;
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
  chatPanelToggle?.addEventListener("click", event => {
    event.preventDefault();
    event.stopPropagation();
    setChatPanelCollapsed(!state.chatPanelCollapsed);
  });
}

function clearMarkers() {
  state.markers.forEach(marker => marker.remove());
  state.markers = [];
  state.focusedEventPopup?.remove();
  state.focusedEventPopup = null;
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
    const items = itemsForLayerPresentation(layer);
    if (layer.kind === "events") {
      const counts = {};
      items.forEach(event => { counts[event.location_id] = (counts[event.location_id] || 0) + 1; });
      Object.entries(counts).forEach(([locationId, count]) => addLocationCount(locationId, count, layer.label, null, layer.color));
    } else if (layer.kind === "locations") {
      items.forEach(item => addLocationCount(item.location_id, item.count || 1, layer.label, item, layer.color));
    } else if (layer.kind === "location_metadata") {
      items.forEach(item => addLocationCount(item.location_id, item.event_count || item.count || 1, item.location_name || layer.label, item, layer.color));
    } else if (layer.kind === "entity_metadata") {
      items.forEach(entity => {
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
    element.setAttribute("aria-label", activeLocaleText(`${location.name}: ${item.count.toLocaleString("he-IL")} פריטים`, `${location.name}: ${item.count.toLocaleString("en-US")} items`));
    element.innerHTML = `<span class="map-marker-dot"></span>${item.count > 1 ? `<span class="map-marker-count">${item.count.toLocaleString(currentLocaleTag())}</span>` : ""}`;
    const popupHtml = `
      <div class="map-popup" dir="${currentLocale() === "en" ? "ltr" : "rtl"}">
        <strong>${escapeHtml(location.name)}</strong>
        <span>${escapeHtml(activeLocaleText(`${item.count.toLocaleString("he-IL")} פריטים`, `${item.count.toLocaleString("en-US")} items`))}</span>
        <em>${escapeHtml([...item.labels].join(" · "))}</em>
      </div>`;
    const popup = new maplibregl.Popup({ offset: 18, closeButton: true, closeOnClick: true }).setHTML(popupHtml);
    const marker = new maplibregl.Marker({ element, anchor: "center" }).setLngLat([location.lon, location.lat]).setPopup(popup).addTo(state.map);
    state.markers.push(marker);
    bounds.extend([location.lon, location.lat]);
  });
  const targetLocationIndexes = new Map();
  visibleLayers("map").filter(layer => layer.kind === "attack_targets").forEach(layer => {
    itemsForLayerPresentation(layer).forEach(target => {
      const canonical = LOCATIONS[target.location_id] || null;
      const lon = canonical?.lon ?? target.longitude;
      const lat = canonical?.lat ?? target.latitude;
      if (lon == null || lat == null) return;
      const locationKey = target.location_id || `${lon}:${lat}`;
      const index = targetLocationIndexes.get(locationKey) || 0;
      targetLocationIndexes.set(locationKey, index + 1);
      const angle = index * 2.399963;
      const radius = index ? 0.0018 * Math.ceil(index / 6 + 1) : 0;
      const markerLon = Number(lon) + Math.cos(angle) * radius;
      const markerLat = Number(lat) + Math.sin(angle) * radius;
      const element = document.createElement("div");
      element.className = "map-marker attack-target-marker";
      element.style.setProperty("--layer-color", layer.color || "#ffb347");
      element.setAttribute("role", "button");
      element.setAttribute("aria-label", activeLocaleText(`מועמד מטרה: ${target.title || target.target_id}, ${target.location_name || target.location_id}`, `Target candidate: ${target.title || target.target_id}, ${target.location_name || target.location_id}`));
      element.innerHTML = '<span class="map-marker-dot"></span>';
      const popupHtml = `<div class="map-popup target-map-popup" dir="${currentLocale() === "en" ? "ltr" : "rtl"}">
        <strong>${escapeHtml(String(target.title || target.target_id || activeLocaleText("מועמד מטרה", "Target candidate")))}</strong>
        <span>${escapeHtml(String(target.object_class || "-"))} · ${escapeHtml(String(target.entity_name || target.entity_id || activeLocaleText("ללא ישות", "No entity")))}</span>
        <span>${escapeHtml(activeLocaleText("ביטחון", "Confidence"))} ${escapeHtml(String(confidenceLabel(target.confidence)))} · ${escapeHtml(activeLocaleText("כמות", "Quantity"))} ${escapeHtml(String(targetQuantityLabel(target)))}</span>
        <p>${escapeHtml(String(target.summary || ""))}</p>
        <span class="target-raw-references"><b>${escapeHtml(activeLocaleText("אסמכתאות גולמיות:", "Raw references:"))}</b> ${(target.raw_data_references || []).length
          ? (target.raw_data_references || []).map(recordId => `<code dir="ltr">${escapeHtml(String(recordId || "-"))}</code>`).join(" · ")
          : escapeHtml(activeLocaleText("לא נטענו אסמכתאות בתוצאה זו", "No raw references were loaded in this result"))}</span>
      </div>`;
      const popup = new maplibregl.Popup({ offset: 20, closeButton: true, closeOnClick: true }).setHTML(popupHtml);
      const marker = new maplibregl.Marker({ element, anchor: "center" }).setLngLat([markerLon, markerLat]).setPopup(popup).addTo(state.map);
      state.markers.push(marker);
      bounds.extend([markerLon, markerLat]);
    });
  });
  if (!bounds.isEmpty()) state.map.fitBounds(bounds, { padding: 110, maxZoom: 10.2, duration: 450 });
}

function eventMapCoordinates(event = {}) {
  const locationId = event.location_id || event.key;
  const requestedName = String(event.location_name || event.name || event.label || "").trim().toLowerCase();
  const canonical = LOCATIONS[locationId] || Object.values(LOCATIONS).find(location => (
    requestedName && String(location.name || "").trim().toLowerCase() === requestedName
  )) || null;
  const lon = canonical?.lon ?? event.longitude ?? event.lon;
  const lat = canonical?.lat ?? event.latitude ?? event.lat;
  if (lon == null || lat == null || !Number.isFinite(Number(lon)) || !Number.isFinite(Number(lat))) return null;
  return { lon: Number(lon), lat: Number(lat) };
}

function mapSelectionKey(layerId, kind, itemId) {
  return `${String(layerId)}:${String(kind)}:${String(itemId)}`;
}

function isMapItemSelected(layerId, kind, itemId) {
  return state.focusedMapSelection === mapSelectionKey(layerId, kind, itemId);
}

function mapItemId(item = {}, kind = "event") {
  if (kind === "target") return String(item.target_id || item.id || "");
  if (kind === "location") return String(item.location_id || item.key || item.id || "");
  return String(item.record_id || item.event_id || item.id || "");
}

function mapActionButton(layerId, kind, itemId, item) {
  const selected = isMapItemSelected(layerId, kind, itemId);
  const available = Boolean(eventMapCoordinates(item));
  const label = selected
    ? activeLocaleText("בטל בחירה במפה", "Clear map selection")
    : activeLocaleText("הצג במפה", "Show on map");
  return `<button type="button" class="result-map-action ${selected ? "active" : ""}" data-result-map-kind="${escapeHtml(kind)}" data-result-map-item="${escapeHtml(itemId)}" data-result-map-layer="${escapeHtml(String(layerId))}" title="${escapeHtml(label)}" aria-label="${escapeHtml(label)}" aria-pressed="${selected ? "true" : "false"}" ${available ? "" : "disabled"}><span class="material-symbols-rounded" aria-hidden="true">${selected ? "location_off" : "location_on"}</span></button>`;
}

function mapItemPopupHtml(item, kind) {
  if (kind === "target") return `<div class="map-popup target-map-popup" dir="${currentLocale() === "en" ? "ltr" : "rtl"}"><strong>${escapeHtml(String(item.title || item.target_id || activeLocaleText("מועמד מטרה", "Target candidate")))}</strong><span>${escapeHtml(String(item.object_class || "-"))} · ${escapeHtml(String(item.entity_name || item.entity_id || "-"))}</span><span>${escapeHtml(activeLocaleText("ביטחון", "Confidence"))} ${escapeHtml(String(confidenceLabel(item.confidence)))}</span><p>${escapeHtml(String(item.summary || ""))}</p></div>`;
  if (kind === "location") return `<div class="map-popup" dir="${currentLocale() === "en" ? "ltr" : "rtl"}"><strong>${escapeHtml(String(item.location_name || item.name || item.label || item.location_id || item.key || "-"))}</strong><span dir="ltr">${escapeHtml(String(item.location_id || item.key || "-"))}</span><span>${escapeHtml(activeLocaleText("כמות", "Count"))}: ${Number(item.event_count || item.count || 0).toLocaleString(currentLocaleTag())}</span>${item.municipality ? `<em>${escapeHtml(String(item.municipality))}</em>` : ""}</div>`;
  const recordId = String(item.record_id || item.event_id || "-");
  return `<div class="map-popup event-map-popup" dir="${currentLocale() === "en" ? "ltr" : "rtl"}"><strong dir="ltr">${escapeHtml(recordId)}</strong><span dir="ltr">${escapeHtml(String(item.timestamp_utc || "-"))}</span><span>${escapeHtml(String(item.entity_name || item.entity_id || "-"))}</span><em>${escapeHtml(String(item.location_name || item.location_id || "-"))}</em><p>${escapeHtml(String(item.event_summary || ""))}</p></div>`;
}

function toggleMapItem(layerId, kind, itemId) {
  const layer = state.layers.find(item => String(item.id) === String(layerId));
  const selectedEvent = (layer?.items || []).find(item => mapItemId(item, kind) === String(itemId || ""));
  const coordinates = eventMapCoordinates(selectedEvent);
  if (!selectedEvent || !coordinates) return;
  const selectionKey = mapSelectionKey(layerId, kind, itemId);
  if (state.focusedMapSelection === selectionKey) {
    state.focusedMapSelection = null;
    state.focusedEventPopup?.remove();
    state.focusedEventPopup = null;
    renderEvidence();
    return;
  }
  state.focusedEventPopup?.remove();
  state.focusedEventPopup = null;
  state.focusedMapSelection = selectionKey;
  renderEvidence();

  activateView("map");
  setTimeout(() => {
    if (!state.mapReady || !state.map) return;
    state.map.easeTo({
      center: [coordinates.lon, coordinates.lat],
      zoom: Math.max(Number(state.map.getZoom?.() || 0), kind === "location" ? 12 : 13),
      duration: 450
    });
    state.focusedEventPopup = new maplibregl.Popup({ offset: 20, closeButton: true, closeOnClick: false })
      .setLngLat([coordinates.lon, coordinates.lat])
      .setHTML(mapItemPopupHtml(selectedEvent, kind))
      .addTo(state.map);
  }, 0);
}

function renderTimeline() {
  const timeline = document.getElementById("timeline");
  const eventTimelineItems = visibleLayers("timeline")
    .filter(layer => layer.kind === "events")
    .flatMap(layer => itemsForLayerPresentation(layer).map(event => ({ type: "event", layer, event, sort: event.date })));
  const aggregateTimelineItems = visibleLayers("timeline")
    .filter(layer => layer.kind === "time_aggregation")
    .flatMap(layer => itemsForLayerPresentation(layer).map(item => ({ type: "aggregation", layer, item, sort: item.sortKey })));
  if (!eventTimelineItems.length && !aggregateTimelineItems.length) { timeline.className = "timeline empty-state"; timeline.textContent = activeLocaleText("לא נבחרו שכבות עם ציר זמן להצגה.", "No timeline layers were selected for display."); return; }
  timeline.className = "timeline";
  const aggregationHtml = aggregateTimelineItems.map(({ layer, item }) => `
    <article class="timeline-item" style="${layerColorStyle(layer)}">
      <span class="timeline-dot"></span>
      <div class="timeline-time">${escapeHtml(item.timeLabel)}</div>
      <div class="timeline-title">${escapeHtml(layer.label)} · ${escapeHtml(activeLocaleText(`${item.count.toLocaleString("he-IL")} אירועים`, `${item.count.toLocaleString("en-US")} events`))}</div>
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

function resultTableControl(layerId) {
  const key = String(layerId || "default");
  if (!state.resultTableControls.has(key)) {
    state.resultTableControls.set(key, {
      filters: {},
      sortColumn: null,
      sortDirection: "asc",
      openFilterColumn: null
    });
  }
  return state.resultTableControls.get(key);
}

function normalizedTableCellText(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

function resultTableSortValue(value) {
  const text = normalizedTableCellText(value);
  const numeric = Number(text.replace(/[,%\s]/g, ""));
  if (text && Number.isFinite(numeric)) return { type: "number", value: numeric };
  const timestamp = /^\d{4}-\d{2}-\d{2}(?:T|\s)/.test(text) ? Date.parse(text) : NaN;
  if (Number.isFinite(timestamp)) return { type: "number", value: timestamp };
  return { type: "text", value: text };
}

function applyResultTableControls(layerId) {
  const head = document.getElementById("evidenceHead");
  const body = document.getElementById("evidenceRows");
  if (!head || !body) return;
  const control = resultTableControl(layerId);
  const rows = [...body.querySelectorAll("tr:not(.result-table-no-match)")]
    .filter(row => !row.querySelector(".empty-cell"));
  rows.forEach((row, originalIndex) => {
    if (!row.dataset.resultTableOriginalIndex) row.dataset.resultTableOriginalIndex = String(originalIndex);
    const visible = Object.entries(control.filters).every(([column, filter]) => {
      if (!filter) return true;
      const cell = row.cells[Number(column)];
      return normalizedTableCellText(cell?.textContent).toLocaleLowerCase("he")
        .includes(normalizedTableCellText(filter).toLocaleLowerCase("he"));
    });
    row.hidden = !visible;
  });

  if (Number.isInteger(control.sortColumn)) {
    const direction = control.sortDirection === "desc" ? -1 : 1;
    rows.sort((a, b) => {
      const left = resultTableSortValue(a.cells[control.sortColumn]?.textContent);
      const right = resultTableSortValue(b.cells[control.sortColumn]?.textContent);
      if (left.type === "number" && right.type === "number") return (left.value - right.value) * direction;
      return String(left.value).localeCompare(String(right.value), "he", {
        numeric: true,
        sensitivity: "base"
      }) * direction;
    });
    rows.forEach(row => body.appendChild(row));
  }

  body.querySelector(".result-table-no-match")?.remove();
  if (rows.length && !rows.some(row => !row.hidden)) {
    const noMatch = document.createElement("tr");
    noMatch.className = "result-table-no-match";
    noMatch.innerHTML = `<td colspan="${head.querySelectorAll("th").length}" class="empty-cell">No results match the filters.</td>`;
    body.appendChild(noMatch);
  }
}

function enhanceResultsTable(layer) {
  const head = document.getElementById("evidenceHead");
  if (!head || !layer) return;
  const control = resultTableControl(layer.id);
  [...head.querySelectorAll("th")].forEach((cell, column) => {
    if (cell.dataset.resultActionColumn === "true") return;
    const label = normalizedTableCellText(cell.textContent);
    const activeSort = control.sortColumn === column;
    const filterValue = String(control.filters[column] || "");
    const filterOpen = control.openFilterColumn === column;
    const directionLabel = activeSort
      ? (control.sortDirection === "asc" ? activeLocaleText("ממויין בסדר עולה", "Sorted ascending") : activeLocaleText("ממויין בסדר יורד", "Sorted descending"))
      : activeLocaleText("לא ממוין", "Not sorted");
    cell.setAttribute("aria-sort", activeSort ? (control.sortDirection === "asc" ? "ascending" : "descending") : "none");
    cell.innerHTML = `
      <div class="result-column-header">
        <button type="button" class="result-column-sort" data-result-sort="${column}" data-result-layer="${escapeHtml(String(layer.id))}" title="${escapeHtml(activeLocaleText(`מיין לפי ${label}. ${directionLabel}`, `Sort by ${label}. ${directionLabel}`))}">
          <span>${escapeHtml(label)}</span>
          <span class="material-symbols-rounded" aria-hidden="true">${activeSort ? (control.sortDirection === "asc" ? "arrow_upward" : "arrow_downward") : "unfold_more"}</span>
        </button>
        <button type="button" class="result-column-filter-toggle ${filterValue ? "active" : ""}" data-result-filter-toggle="${column}" data-result-layer="${escapeHtml(String(layer.id))}" title="${escapeHtml(activeLocaleText(`סנן לפי ${label}`, `Filter by ${label}`))}" aria-label="${escapeHtml(activeLocaleText(`סנן לפי ${label}`, `Filter by ${label}`))}" aria-expanded="${filterOpen ? "true" : "false"}">
          <span class="material-symbols-rounded" aria-hidden="true">filter_alt</span>
        </button>
      </div>
      ${filterOpen ? `
        <div class="result-column-filter-popover">
          <input type="search" class="result-column-filter" data-result-filter="${column}" data-result-layer="${escapeHtml(String(layer.id))}" value="${escapeHtml(filterValue)}" placeholder="${escapeHtml(activeLocaleText(`סנן ${label}`, `Filter ${label}`))}" aria-label="${escapeHtml(activeLocaleText(`סנן ${label}`, `Filter ${label}`))}">
          ${filterValue ? `<button type="button" class="result-column-filter-clear" data-result-filter-clear="${column}" data-result-layer="${escapeHtml(String(layer.id))}" title="${escapeHtml(activeLocaleText("נקה מסנן", "Clear filter"))}" aria-label="${escapeHtml(activeLocaleText("נקה מסנן", "Clear filter"))}"><span class="material-symbols-rounded" aria-hidden="true">close</span></button>` : ""}
        </div>` : ""}`;
  });
  applyResultTableControls(layer.id);
  if (Number.isInteger(control.openFilterColumn)) {
    head.querySelector(`.result-column-filter[data-result-filter="${control.openFilterColumn}"]`)?.focus();
  }
}

function renderEvidence() {
  const overlay = document.getElementById("rawEventsOverlay");
  const viewStack = overlay?.closest(".view-stack");
  const tabs = document.getElementById("rawEventsTabs");
  const head = document.getElementById("evidenceHead");
  const body = document.getElementById("evidenceRows");
  const filterPanel = document.getElementById("layerFilterPanel");
  if (!overlay || !tabs || !head || !body) return;

  const tableLayers = state.layers.filter(layer => layer.capabilities.table);
  tableLayers.forEach(layer => ensureLayerFilterState(layer));
  if (!tableLayers.length) {
    overlay.hidden = true;
    tabs.innerHTML = "";
    head.innerHTML = "";
    body.innerHTML = "";
    if (filterPanel) {
      filterPanel.hidden = true;
      filterPanel.innerHTML = "";
    }
    return;
  }

  if (!tableLayers.some(layer => layer.id === state.activeLayerId)) state.activeLayerId = tableLayers[0].id;
  const activeLayer = activeTableLayer();

  overlay.hidden = false;
  overlay.classList.toggle("minimized", state.rawOverlayMinimized);
  overlay.classList.toggle("filter-panel-open", Boolean(activeLayer?.filterPanelOpen));
  overlay.style.setProperty("--raw-overlay-height", `${state.rawOverlayHeight}%`);
  if (viewStack) viewStack.style.setProperty("--raw-overlay-height", `${state.rawOverlayHeight}%`);
  const minimizeButton = document.getElementById("rawEventsMinimize");
  if (minimizeButton) {
    minimizeButton.textContent = state.rawOverlayMinimized ? "□" : "−";
    minimizeButton.title = state.rawOverlayMinimized ? activeLocaleText("הרחב", "Expand") : activeLocaleText("מזער", "Minimize");
    minimizeButton.setAttribute("aria-label", state.rawOverlayMinimized
      ? activeLocaleText("הרחב טבלת תוצאות", "Expand results table")
      : activeLocaleText("מזער טבלת תוצאות", "Minimize results table"));
  }
  tabs.innerHTML = tableLayers.map(layer => {
    const filteredCount = itemsForLayerPresentation(layer).length;
    const originalCount = (layer.items || []).length;
    const countLabel = layerHasAppliedFilters(layer)
      ? `${filteredCount.toLocaleString(currentLocaleTag())}/${originalCount.toLocaleString(currentLocaleTag())}`
      : originalCount.toLocaleString(currentLocaleTag());
    return `
    <button type="button" class="raw-source-tab ${layer.id === activeLayer?.id ? "active" : ""} ${layer.visible ? "" : "hidden-source"}" style="${layerColorStyle(layer)}" data-layer-id="${escapeHtml(layer.id)}" role="tab" aria-selected="${layer.id === activeLayer?.id}" title="${escapeHtml(layer.sourceLabel || layer.label)}">
      <span class="raw-source-color"></span>
      <span class="raw-source-name">${escapeHtml(layer.label)}</span>
      <strong>${countLabel}</strong>
      <span class="raw-source-filter ${layer.filterPanelOpen ? "active" : ""} ${validAppliedFilters(layer).length ? "has-filters" : ""}" data-layer-filter="${escapeHtml(layer.id)}" title="${escapeHtml(activeLocaleText("פתח מסננים", "Open filters"))}" aria-label="${escapeHtml(activeLocaleText("פתח מסננים", "Open filters"))}" aria-pressed="${layer.filterPanelOpen ? "true" : "false"}">
        <span class="filter-funnel-icon" aria-hidden="true"></span>
      </span>
      <span class="raw-source-memory ${layer.investigation_memory_layer_id ? "saved" : ""}" data-layer-memory="${escapeHtml(layer.id)}" title="${escapeHtml(layer.investigation_memory_layer_id ? activeLocaleText("השכבה נשמרה בזיכרון החקירה", "Layer saved to investigation memory") : activeLocaleText("שמור שכבה לזיכרון החקירה", "Save layer to investigation memory"))}" aria-label="${escapeHtml(layer.investigation_memory_layer_id ? activeLocaleText("השכבה נשמרה בזיכרון החקירה", "Layer saved to investigation memory") : activeLocaleText("שמור שכבה לזיכרון החקירה", "Save layer to investigation memory"))}" aria-pressed="${layer.investigation_memory_layer_id ? "true" : "false"}">
        <span class="memory-bookmark-icon" aria-hidden="true"></span>
      </span>
        <span class="raw-source-eye" data-layer-visibility="${escapeHtml(layer.id)}" title="${escapeHtml(layer.visible ? activeLocaleText("הסתר שכבה", "Hide layer") : activeLocaleText("הצג שכבה", "Show layer"))}" aria-label="${escapeHtml(layer.visible ? activeLocaleText("הסתר שכבה", "Hide layer") : activeLocaleText("הצג שכבה", "Show layer"))}" aria-pressed="${layer.visible ? "true" : "false"}">
          <span class="visibility-eye-icon ${layer.visible ? "" : "off"}" aria-hidden="true"></span>
        </span>
      <span class="raw-source-close" data-layer-close="${escapeHtml(layer.id)}" title="${escapeHtml(activeLocaleText("סגור שכבה", "Close layer"))}" aria-label="${escapeHtml(activeLocaleText("סגור שכבה", "Close layer"))}">×</span>
    </button>`;
  }).join("");

  if (!activeLayer) return;
  ensureLayerFilterState(activeLayer);
  renderLayerFilterPanel(activeLayer);
  const activeItems = activeLayer.visible ? itemsForLayerPresentation(activeLayer) : [];
  if (activeLayer.kind === "attack_targets") {
    head.innerHTML = `<tr><th class="result-map-action-column" data-result-action-column="true"></th><th>${escapeHtml(activeLocaleText("מטרה", "Target"))}</th><th>${escapeHtml(activeLocaleText("סוג אובייקט", "Object type"))}</th><th>${escapeHtml(activeLocaleText("ישות", "Entity"))}</th><th>${escapeHtml(activeLocaleText("מיקום קנוני", "Canonical location"))}</th><th>${escapeHtml(activeLocaleText("ביטחון", "Confidence"))}</th><th>${escapeHtml(activeLocaleText("כמות", "Quantity"))}</th><th>${escapeHtml(activeLocaleText("סיכום", "Summary"))}</th><th>${escapeHtml(activeLocaleText("סוגי מקור", "Source types"))}</th><th>${escapeHtml(activeLocaleText("רשומות גולמיות", "Raw records"))}</th></tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(item => {
      const itemId = mapItemId(item, "target");
      const selected = isMapItemSelected(activeLayer.id, "target", itemId);
      return `
      <tr class="attack-target-row ${selected ? "map-selected-row" : ""}">
        <td class="result-map-action-cell">${mapActionButton(activeLayer.id, "target", itemId, item)}</td>
        <td><strong>${escapeHtml(String(item.title || item.target_id || "-"))}</strong><small dir="ltr">${escapeHtml(String(item.target_id || "-"))}</small></td>
        <td>${escapeHtml(String(item.object_class || "-"))}</td>
        <td>${escapeHtml(String(item.entity_name || item.entity_id || "-"))}</td>
        <td>${escapeHtml(String(item.location_name || item.location_id || "-"))}</td>
        <td>${escapeHtml(String(confidenceLabel(item.confidence)))}</td>
        <td>${escapeHtml(String(targetQuantityLabel(item)))}</td>
        <td>${escapeHtml(String(item.summary || "-"))}</td>
        <td>${(item.source_types || []).length ? (item.source_types || []).map(sourceType => `<span class="target-source-type">${escapeHtml(String(sourceType))}</span>`).join("<br>") : "-"}</td>
        <td><strong>${Number(item.evidence_count || (item.raw_data_references || []).length || 0).toLocaleString(currentLocaleTag())}</strong></td>
      </tr>`;
    }).join("") : `<tr><td colspan="10" class="empty-cell">${escapeHtml(activeLocaleText("לא נמצאו מועמדי מטרה להצגה.", "No target candidates found for display."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "location_metadata") {
    head.innerHTML = `<tr><th class="result-map-action-column" data-result-action-column="true"></th><th>${escapeHtml(activeLocaleText("מיקום", "Location"))}</th><th>${escapeHtml(activeLocaleText("אירועים", "Events"))}</th><th>${escapeHtml(activeLocaleText("רשות", "Municipality"))}</th><th>${escapeHtml(activeLocaleText("סוג", "Type"))}</th><th>${escapeHtml(activeLocaleText("דיוק", "Precision"))}</th><th>ID</th></tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(item => {
      const itemId = mapItemId(item, "location");
      const selected = isMapItemSelected(activeLayer.id, "location", itemId);
      return `
      <tr class="${selected ? "map-selected-row" : ""}">
        <td class="result-map-action-cell">${mapActionButton(activeLayer.id, "location", itemId, item)}</td>
        <td>${escapeHtml(item.location_name || item.name || item.location_id || "-")}</td>
        <td>${Number(item.event_count || item.count || 0).toLocaleString(currentLocaleTag())}</td>
        <td>${escapeHtml(item.municipality || "-")}</td>
        <td>${escapeHtml(item.type || "-")}</td>
        <td>${escapeHtml(item.precision || "-")}</td>
        <td dir="ltr">${escapeHtml(item.location_id || "-")}</td>
      </tr>`;
    }).join("") : `<tr><td colspan="7" class="empty-cell">${escapeHtml(activeLocaleText("השכבה מוסתרת או ריקה.", "Layer is hidden or empty."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "entity_metadata") {
    head.innerHTML = `<tr><th>${escapeHtml(activeLocaleText("ישות", "Entity"))}</th><th>${escapeHtml(activeLocaleText("אירועים", "Events"))}</th><th>${escapeHtml(activeLocaleText("סוג", "Type"))}</th><th>${escapeHtml(activeLocaleText("ערכי שחקן", "Actor values"))}</th><th>${escapeHtml(activeLocaleText("מוקדים מובילים", "Leading hotspots"))}</th><th>ID</th></tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(item => {
      const aliases = (item.aliases || []).slice(0, 4).join(", ");
      const topLocations = (item.top_locations || []).slice(0, 4).map(location => `${location.location_name || location.location_id} (${Number(location.count || 0).toLocaleString("en-US")})`).join(", ");
      return `
      <tr>
        <td>${escapeHtml(item.canonical_name || item.entity_id || "-")}</td>
        <td>${Number(item.event_count || item.count || 0).toLocaleString("en-US")}</td>
        <td>${escapeHtml(item.entity_type || "-")}</td>
        <td>${escapeHtml(aliases || "-")}</td>
        <td>${escapeHtml(topLocations || "-")}</td>
        <td dir="ltr">${escapeHtml(item.entity_id || "-")}</td>
      </tr>`;
    }).join("") : `<tr><td colspan="6" class="empty-cell">${escapeHtml(activeLocaleText("השכבה מוסתרת או ריקה.", "Layer is hidden or empty."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "locations") {
    head.innerHTML = `<tr><th class="result-map-action-column" data-result-action-column="true"></th><th>${escapeHtml(activeLocaleText("מיקום", "Location"))}</th><th>${escapeHtml(activeLocaleText("כמות", "Count"))}</th><th>ID</th><th>${escapeHtml(activeLocaleText("סוג שכבה", "Layer type"))}</th></tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(item => {
      const itemId = mapItemId(item, "location");
      const selected = isMapItemSelected(activeLayer.id, "location", itemId);
      return `
      <tr class="${selected ? "map-selected-row" : ""}">
        <td class="result-map-action-cell">${mapActionButton(activeLayer.id, "location", itemId, item)}</td>
        <td>${escapeHtml(item.location_name || item.label || item.key || item.location_id || "-")}</td>
        <td>${Number(item.count || 0).toLocaleString(currentLocaleTag())}</td>
        <td dir="ltr">${escapeHtml(item.location_id || item.key || "-")}</td>
        <td>${escapeHtml(activeLayer.label)}</td>
      </tr>`;
    }).join("") : `<tr><td colspan="5" class="empty-cell">${escapeHtml(activeLocaleText("השכבה מוסתרת או ריקה.", "Layer is hidden or empty."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "time_aggregation") {
    head.innerHTML = `<tr><th>${escapeHtml(activeLocaleText("זמן", "Time"))}</th><th>${escapeHtml(activeLocaleText("כמות", "Count"))}</th><th>${escapeHtml(activeLocaleText("סוג קיבוץ", "Grouping type"))}</th><th>${escapeHtml(activeLocaleText("סיכום", "Summary"))}</th></tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(item => `
      <tr>
        <td>${escapeHtml(item.timeLabel || item.label || "-")}</td>
        <td>${Number(item.count || 0).toLocaleString(currentLocaleTag())}</td>
        <td>${escapeHtml(item.group_by === "hour" ? activeLocaleText("שעה", "Hour") : activeLocaleText("תאריך", "Date"))}</td>
        <td>${escapeHtml(item.summary || "-")}</td>
      </tr>`).join("") : `<tr><td colspan="4" class="empty-cell">${escapeHtml(activeLocaleText("השכבה מוסתרת או ריקה.", "Layer is hidden or empty."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "group_aggregation") {
    head.innerHTML = `<tr><th>${escapeHtml(activeLocaleText("קבוצה", "Group"))}</th><th>${escapeHtml(activeLocaleText("כמות", "Count"))}</th><th>${escapeHtml(activeLocaleText("סוג קיבוץ", "Grouping type"))}</th><th>${escapeHtml(activeLocaleText("אירוע ראשון", "First event"))}</th><th>${escapeHtml(activeLocaleText("אירוע אחרון", "Last event"))}</th></tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(item => `
      <tr>
        <td>${escapeHtml(item.label || item.key || "-")}</td>
        <td>${Number(item.count || 0).toLocaleString(currentLocaleTag())}</td>
        <td>${escapeHtml(item.group_by || "-")}</td>
        <td dir="ltr">${escapeHtml(item.first_event_id || item.first_event_time || "-")}</td>
        <td dir="ltr">${escapeHtml(item.last_event_id || item.last_event_time || "-")}</td>
      </tr>`).join("") : `<tr><td colspan="5" class="empty-cell">${escapeHtml(activeLocaleText("השכבה מוסתרת או ריקה.", "Layer is hidden or empty."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  head.innerHTML = `<tr><th class="result-map-action-column" data-result-action-column="true" aria-label="${escapeHtml(activeLocaleText("פעולות", "Actions"))}"></th><th>${escapeHtml(activeLocaleText("מזהה רשומה", "Record ID"))}</th><th>${escapeHtml(activeLocaleText("זמן", "Time"))}</th><th>${escapeHtml(activeLocaleText("אמינות", "Reliability"))}</th><th>${escapeHtml(activeLocaleText("ודאות", "Certainty"))}</th><th>${escapeHtml(activeLocaleText("גורם", "Actor"))}</th><th>${escapeHtml(activeLocaleText("מיקום", "Location"))}</th><th>${escapeHtml(activeLocaleText("תקציר", "Summary"))}</th></tr>`;
  body.innerHTML = activeItems.length ? activeItems.map(event => {
    const eventId = String(event.record_id || event.event_id || "");
    const selected = isMapItemSelected(activeLayer.id, "event", eventId);
    return `
    <tr class="${selected ? "map-selected-row" : ""}">
      <td class="result-map-action-cell">${mapActionButton(activeLayer.id, "event", eventId, event)}</td>
      <td dir="ltr">${escapeHtml(event.record_id || event.event_id || "-")}</td>
      <td dir="ltr">${escapeHtml(event.timestamp_utc)}</td>
      <td>${escapeHtml(event.source_reliability_label || event.source_reliability || "-")}</td>
      <td>${escapeHtml(event.certainty_level || "-")}</td>
      <td>${escapeHtml(event.entity_name || event.entity_id || "-")}</td>
      <td>${escapeHtml(event.location_name || "-")}</td>
      <td>${escapeHtml(event.event_summary || "-")}</td>
    </tr>`;
  }).join("") : `<tr><td colspan="8" class="empty-cell">${escapeHtml(activeLocaleText("השכבה מוסתרת או ריקה.", "Layer is hidden or empty."))}</td></tr>`;
  enhanceResultsTable(activeLayer);
}

function resetInvestigation(options = {}) {
  state.current = [];
  state.stage = 0;
  state.aggregateLocations = [];
  state.aggregateTimeline = [];
  state.aggregateGroups = [];
  state.locationMetadata = [];
  state.entityMetadata = [];
  state.layers = [];
  state.promptSelectedLayerIds = new Set();
  state.activeLayerId = null;
  state.rawOverlayMinimized = false;
  state.rawOverlayHeight = 28;
  state.resultTableControls.clear();
  state.focusedMapSelection = null;
  state.history = [];
  state.workstreamLoadToken += 1;
  state.workstreams = [];
  state.workstreamsLoading = false;
  state.investigationPlayback = null;
  state.memoryUpdatePollToken += 1;
  state.pendingMosheWorkstreamProposal = null;
  state.workstreamComposerMode = false;
  if (!options.keepInvestigation) {
    const investigation = ensureInvestigationRecord(defaultInvestigationName());
    state.investigationId = investigation.id;
    state.investigationName = investigation.name;
    saveInvestigationRegistry();
  }
  state.activeAssistantMessage = null;
  state.activeActivityList = null;
  state.activeActivityEmpty = null;
  state.lastResult = null;
  state.lastPrompt = null;
  state.queryContext = null;
  state.investigationMemory = null;
  state.investigationMemoryError = "";
  state.investigationMemoryLoading = false;
  state.layerSearchQuery = "";
  state.layerSearchOpen = false;
  state.activeConversationMemberId = null;
  setPromptOptionsOpen(false);
  promptForm.classList.remove("tracking-mode");
  if (workstreamComposerMode) workstreamComposerMode.hidden = true;
  renderWorkstreamIndicator();
  closeQueryLayersModal();
  conversation.innerHTML = `<article class="message assistant-message"><div class="message-label">${activeLocaleText("סוכן חקירה", "Investigation Agent")}</div><p>${activeLocaleText("אפשר להתחיל בשאלה פתוחה. אשתמש בכלי החיפוש, הזמן והמפה כדי לבנות תשובה שניתן לבדוק מול האירועים הגולמיים.", "You can start with an open question. I’ll use search, time, and map tools to build an answer you can verify against the raw events.")}</p></article>`;
  updatePromptPlaceholder();
  if (resultTitle) resultTitle.textContent = activeLocaleText("טרם בוצעה חקירה", "No investigation yet");
  if (resultSubtitle) resultSubtitle.textContent = activeLocaleText("תוצאות, המחשות וראיות יופיעו כאן לאחר השאלה הראשונה.", "Results, visuals, and evidence will appear here after the first question.");
  if (resultCount) resultCount.textContent = activeLocaleText("0 אירועים", "0 events");
  activateView("map");
  setSuggestions(currentLocale() === "en"
    ? ["Which blockage reports appeared first?", "Is the border crossing claim supported by a reliable source?", "Where are the main reporting clusters?"]
    : ["אילו דיווחים על חסימות הופיעו ראשונים?", "האם הטענה על חציית גבול מגובה במקור אמין?", "איפה יש ריכוזי דיווחים מרכזיים?"]);
  renderAllViews();
  renderLayerSelector();
  renderQueryLayersModal();
  renderQueryInspector();
  renderInvestigationSelector();
  renderMichlolTeam();
  if (state.map) setTimeout(() => state.map.resize(), 0);
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[char]);
}

document.addEventListener("input", event => {
  const filter = event.target.closest(".result-column-filter[data-result-filter]");
  if (!filter) return;
  const control = resultTableControl(filter.dataset.resultLayer);
  control.filters[Number(filter.dataset.resultFilter)] = filter.value;
  applyResultTableControls(filter.dataset.resultLayer);
});

document.addEventListener("click", event => {
  const resultMapEvent = event.target.closest(".result-map-action[data-result-map-item]");
  if (resultMapEvent) {
    toggleMapItem(resultMapEvent.dataset.resultMapLayer, resultMapEvent.dataset.resultMapKind, resultMapEvent.dataset.resultMapItem);
    return;
  }
  const columnFilterToggle = event.target.closest(".result-column-filter-toggle[data-result-filter-toggle]");
  if (columnFilterToggle) {
    const layerId = columnFilterToggle.dataset.resultLayer;
    const column = Number(columnFilterToggle.dataset.resultFilterToggle);
    const control = resultTableControl(layerId);
    control.openFilterColumn = control.openFilterColumn === column ? null : column;
    renderEvidence();
    return;
  }
  const filterClear = event.target.closest(".result-column-filter-clear[data-result-filter-clear]");
  if (filterClear) {
    const layerId = filterClear.dataset.resultLayer;
    const column = Number(filterClear.dataset.resultFilterClear);
    const control = resultTableControl(layerId);
    control.filters[column] = "";
    control.openFilterColumn = null;
    renderEvidence();
    return;
  }
  const resultSort = event.target.closest(".result-column-sort[data-result-sort]");
  if (resultSort) {
    const layerId = resultSort.dataset.resultLayer;
    const column = Number(resultSort.dataset.resultSort);
    const control = resultTableControl(layerId);
    if (control.sortColumn === column) {
      control.sortDirection = control.sortDirection === "asc" ? "desc" : "asc";
    } else {
      control.sortColumn = column;
      control.sortDirection = "asc";
    }
    const layer = state.layers.find(item => String(item.id) === String(layerId));
    if (layer) renderEvidence();
    return;
  }
  const michlolMember = event.target.closest(".michlol-member[data-member-id]");
  if (michlolMember) {
    selectConversationMember(michlolMember.dataset.memberId);
    return;
  }
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
  if (!event.target.closest(".investigation-switcher") && state.investigationSelectorOpen) {
    setInvestigationSelectorOpen(false);
  }
  const promptOption = event.target.closest("[data-prompt-option]");
  if (promptOption) {
    event.stopPropagation();
    if (promptOption.dataset.promptOption === "recordings") openRecordedModal();
    if (promptOption.dataset.promptOption === "layers") openQueryLayersModal();
    if (promptOption.dataset.promptOption === "workstream") startWorkstreamComposerMode();
    return;
  }
  const showWorkstream = event.target.closest("[data-workstream-show]");
  if (showWorkstream) {
    const workstreamId = showWorkstream.dataset.workstreamShow;
    showWorkstreamUpdate(workstreamId);
    return;
  }
  const archiveWorkstream = event.target.closest("[data-workstream-archive]");
  if (archiveWorkstream) {
    void archiveWorkstreamFromChat(archiveWorkstream.dataset.workstreamArchive);
    return;
  }
  const saveWorkstream = event.target.closest("[data-workstream-save]");
  if (saveWorkstream) {
    const workstreamId = saveWorkstream.dataset.workstreamSave;
    const workstream = workstreamRecordingSnapshots.get(workstreamId)
      || state.workstreams.find(item => item.workstream_id === workstreamId);
    if (workstream) {
      const prompt = `${activeLocaleText("עדכון מעקב", "Workstream update")} — ${workstream.title || activeLocaleText("מעקב", "Workstream")}`;
      void (async () => {
        let presentation = null;
        if (workstreamHasPresentation(workstream)) {
          try {
            presentation = await fetchWorkstreamPresentation(workstreamId);
          } catch (error) {
            saveWorkstream.textContent = activeLocaleText("נכשל", "Failed");
            saveWorkstream.title = error.message;
            setTimeout(() => {
              saveWorkstream.textContent = activeLocaleText("שמור הקלטה", "Save recording");
              saveWorkstream.title = activeLocaleText("שמור את הקלטת המעקב", "Save the workstream recording");
            }, 2500);
            return;
          }
        }
        await saveResultQuestion({
          answer: prompt,
          investigation_steps: [],
          workstream_recording: { kind: "detail", workstream, presentation }
        }, prompt, saveWorkstream);
      })();
    }
    return;
  }
  const workstreamResults = event.target.closest("[data-workstream-results]");
  if (workstreamResults) {
    void toggleWorkstreamResultVisibility(
      workstreamResults.dataset.workstreamResults,
      workstreamResults
    );
    return;
  }
  const recordedWorkstreamResults = event.target.closest("[data-recorded-workstream-results]");
  if (recordedWorkstreamResults) {
    toggleRecordedWorkstreamResultVisibility(recordedWorkstreamResults);
    return;
  }
  const viewButton = event.target.closest("[data-view]");
  if (viewButton) activateView(viewButton.dataset.view);
  const layerSelect = event.target.closest("[data-layer-select]");
  if (layerSelect) {
    state.layerSearchQuery = "";
    state.layerSearchOpen = false;
    openCatalogLayer(layerSelect.dataset.layerSelect);
    return;
  }
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
  const addFilter = event.target.closest("[data-filter-add]");
  if (addFilter) {
    event.stopPropagation();
    const layer = activeFilterLayer();
    if (layer) {
      addDraftFilter(layer);
      renderEvidence();
    }
    return;
  }
  const removeFilter = event.target.closest("[data-filter-remove]");
  if (removeFilter) {
    event.stopPropagation();
    const layer = activeFilterLayer();
    if (layer) {
      removeDraftFilter(layer, Number(removeFilter.dataset.filterRemove));
      renderEvidence();
    }
    return;
  }
  const cancelFilters = event.target.closest("[data-filter-cancel]");
  if (cancelFilters) {
    event.stopPropagation();
    const layer = activeFilterLayer();
    if (layer) {
      resetDraftFilters(layer);
      renderEvidence();
    }
    return;
  }
  const applyFilters = event.target.closest("[data-filter-apply]");
  if (applyFilters) {
    event.stopPropagation();
    const layer = activeFilterLayer();
    if (layer) {
      const applied = applyDraftFilters(layer);
      applied ? renderAllViews() : renderEvidence();
    }
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
  const memoryToggle = event.target.closest("[data-layer-memory]");
  if (memoryToggle) {
    event.stopPropagation();
    const layer = state.layers.find(item => item.id === memoryToggle.dataset.layerMemory);
    if (layer) saveLayerToInvestigationMemory(layer, memoryToggle);
    return;
  }
  const filterToggle = event.target.closest("[data-layer-filter]");
  if (filterToggle) {
    event.stopPropagation();
    const layer = state.layers.find(item => item.id === filterToggle.dataset.layerFilter);
    if (layer) {
      ensureLayerFilterState(layer);
      const nextOpen = !layer.filterPanelOpen || state.activeLayerId !== layer.id;
      state.layers.forEach(item => { item.filterPanelOpen = false; });
      layer.filterPanelOpen = nextOpen;
      state.activeLayerId = layer.id;
      state.rawOverlayMinimized = false;
    }
    renderEvidence();
    return;
  }
  const closeLayer = event.target.closest("[data-layer-close]");
  if (closeLayer) {
    event.stopPropagation();
    const layerIdToClose = closeLayer.dataset.layerClose;
    state.promptSelectedLayerIds.delete(layerIdToClose);
    state.layers = state.layers.filter(item => item.id !== layerIdToClose);
    if (state.activeLayerId === layerIdToClose) {
      state.activeLayerId = state.layers.find(layer => layer.capabilities.table && layer.visible)?.id
        || state.layers.find(layer => layer.capabilities.table)?.id
        || null;
    }
    renderAllViews();
    renderLayerSelector();
    renderQueryLayersModal();
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
    state.promptSelectedLayerIds = new Set();
    state.activeLayerId = null;
    state.current = [];
    state.aggregateLocations = [];
    state.aggregateTimeline = [];
    state.locationMetadata = [];
    state.entityMetadata = [];
    state.queryContext = null;
    renderAllViews();
    renderLayerSelector();
    renderQueryInspector();
  }
  if (!event.target.closest(".layer-selector") && state.layerSearchOpen) {
    state.layerSearchOpen = false;
    renderLayerSelector();
  }
  if (!event.target.closest(".prompt-options") && state.promptOptionsOpen) {
    setPromptOptionsOpen(false);
  }
  if (event.target === recordedModal) closeRecordedModal();
  if (event.target === queryLayersModal) closeQueryLayersModal();
});

document.addEventListener("input", event => {
  if (event.target.matches("[data-filter-value]")) {
    const layer = activeFilterLayer();
    if (layer) updateDraftFilterValue(layer, Number(event.target.dataset.filterIndex), event.target.value);
    return;
  }
  if (event.target !== layerSelectorSearch) return;
  state.layerSearchQuery = event.target.value;
  state.layerSearchOpen = true;
  renderLayerSelector();
});

document.addEventListener("change", event => {
  if (!event.target.matches("[data-filter-field]")) return;
  const layer = activeFilterLayer();
  if (!layer) return;
  updateDraftFilterField(layer, Number(event.target.dataset.filterIndex), event.target.value);
  renderEvidence();
});

document.addEventListener("focusin", event => {
  if (event.target !== layerSelectorSearch) return;
  state.layerSearchOpen = true;
  renderLayerSelector();
});

document.addEventListener("keydown", event => {
  if (state.promptOptionsOpen && event.key === "Escape") {
    setPromptOptionsOpen(false);
    promptOptionsButton?.focus();
    return;
  }
  if (event.target.matches("[data-filter-value]") && event.key === "Enter") {
    event.preventDefault();
    const layer = activeFilterLayer();
    if (layer) {
      const applied = applyDraftFilters(layer);
      applied ? renderAllViews() : renderEvidence();
    }
    return;
  }
  if (event.target !== layerSelectorSearch) return;
  if (event.key === "Escape") {
    state.layerSearchOpen = false;
    renderLayerSelector();
    layerSelectorSearch.blur();
    return;
  }
  if (event.key === "Enter") {
    const [firstMatch] = matchingCatalogLayers();
    if (firstMatch) {
      event.preventDefault();
      state.layerSearchQuery = "";
      state.layerSearchOpen = false;
      openCatalogLayer(firstMatch.id);
    }
  }
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
    stack.style.setProperty("--raw-overlay-height", `${state.rawOverlayHeight}%`);
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
  if (state.workstreamComposerMode) {
    if (!prompt.trim()) return;
    promptInput.value = "";
    syncMentionHighlight(promptInput);
    closeTeamMentionMenu();
    runPrompt(prompt, { workstreamCreation: true });
    return;
  }
  promptInput.value = "";
  syncMentionHighlight(promptInput);
  closeTeamMentionMenu();
  runPrompt(prompt);
});

welcomePromptForm?.addEventListener("submit", event => {
  event.preventDefault();
  const prompt = welcomePromptInput?.value || "";
  if (!prompt.trim()) {
    welcomePromptInput?.focus();
    return;
  }
  welcomePromptInput.value = "";
  startDraftInvestigation(prompt);
});

welcomePromptInput?.addEventListener("keydown", event => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    welcomePromptForm?.requestSubmit();
  }
});

welcomePromptOptionsButton?.addEventListener("click", () => {
  if (state.busy) return;
  state.investigationId = createInvestigationId();
  state.investigationName = "";
  state.draftSessionActive = true;
  state.pendingDraftMemoryAction = null;
  resetInvestigation({ keepInvestigation: true });
  setPageView("workspace", { focus: false });
  promptInput.value = welcomePromptInput?.value || "";
  syncMentionHighlight(promptInput);
  promptOptionsButton?.click();
});

promptInput.addEventListener("keydown", event => {
  if (handleTeamMentionKeydown(event)) return;
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    promptForm.requestSubmit();
  }
});

investigationInput?.addEventListener("focus", () => {
  state.investigationSearchQuery = "";
  setInvestigationSelectorOpen(true);
  investigationInput.select();
});
investigationInput?.addEventListener("input", () => {
  state.investigationSearchQuery = investigationInput.value;
  setInvestigationSelectorOpen(true);
});
investigationInput?.addEventListener("keydown", event => {
  if (event.key === "Enter") {
    event.preventDefault();
    const name = normalizeInvestigationName(investigationInput.value);
    const existing = state.investigations.find(item => investigationNameKey(item.name) === investigationNameKey(name));
    if (existing) selectInvestigation(existing);
    else addOrSelectInvestigation();
  }
  if (event.key === "Escape") setInvestigationSelectorOpen(false);
});
investigationAddButton?.addEventListener("click", addOrSelectInvestigation);
investigationList?.addEventListener("mousedown", event => event.preventDefault());
investigationList?.addEventListener("click", event => {
  const option = event.target.closest("[data-investigation-id]");
  if (!option) return;
  const investigation = state.investigations.find(item => item.id === option.dataset.investigationId);
  selectInvestigation(investigation, { focusInput: true });
});
document.addEventListener("pointerdown", event => {
  document.querySelectorAll("details.michlol-more[open]").forEach(details => {
    if (!details.contains(event.target)) details.removeAttribute("open");
  });
  if (!event.target.closest("#teamMentionMenu") && event.target !== teamMentionState.textarea) {
    closeTeamMentionMenu();
  }
});
window.addEventListener("resize", () => {
  if (teamMentionState.textarea) positionTeamMentionMenu(teamMentionState.textarea);
});
document.addEventListener("scroll", () => {
  if (teamMentionState.textarea) positionTeamMentionMenu(teamMentionState.textarea);
}, true);
promptOptionsButton.addEventListener("click", event => {
  event.stopPropagation();
  setPromptOptionsOpen(!state.promptOptionsOpen);
});
workstreamRailToggle?.addEventListener("click", () => setWorkstreamRailCollapsed(!state.workstreamRailCollapsed));
playbackNextButton?.addEventListener("click", advanceInvestigationPlayback);
playbackResetButton?.addEventListener("click", resetInvestigationPlayback);
languageToggle?.addEventListener("change", () => {
  state.locale = languageToggle.checked ? "en" : "he";
  try {
    localStorage.setItem(LOCALE_STORAGE_KEY, state.locale);
  } catch (error) {
    // Ignore localStorage failures and still apply the locale for this session.
  }
  const url = new URL(window.location.href);
  url.searchParams.set("lang", state.locale);
  window.location.assign(url.toString());
});
appHomeButton?.addEventListener("click", () => setPageView("welcome"));
welcomePage?.addEventListener("click", event => {
  const action = event.target.closest("[data-welcome-action]");
  if (action) {
    openWelcomeAction(action.dataset.welcomeAction, action.dataset.investigationName || "");
    return;
  }
  const opener = event.target.closest("[data-open-investigation]");
  if (!opener) return;
  const investigation = state.investigations.find(item => item.id === opener.dataset.openInvestigation);
  if (investigation && investigation.id !== state.investigationId) selectInvestigation(investigation);
  setPageView("workspace");
});
welcomeActionClose?.addEventListener("click", closeWelcomeAction);
welcomeActionModal?.addEventListener("click", event => {
  if (event.target === welcomeActionModal) closeWelcomeAction();
});
draftCreateInvestigationButton?.addEventListener("click", () => openDraftCreateModal());
draftCreateCancel?.addEventListener("click", closeDraftCreateModal);
draftCreateForm?.addEventListener("submit", event => {
  event.preventDefault();
  void createInvestigationFromDraft();
});
draftCreateModal?.addEventListener("click", event => {
  if (event.target === draftCreateModal) closeDraftCreateModal();
});
document.addEventListener("keydown", event => {
  if (event.key === "Escape" && welcomeActionModal && !welcomeActionModal.hidden) {
    closeWelcomeAction();
  }
  if (event.key === "Escape" && draftCreateModal && !draftCreateModal.hidden) {
    closeDraftCreateModal();
  }
});
workstreamComposerCancel?.addEventListener("click", () => setWorkstreamComposerMode(false));
selectedLayersButton.addEventListener("click", openQueryLayersModal);
selectedLayersClear.addEventListener("click", event => {
  event.preventDefault();
  event.stopPropagation();
  clearPromptLayerSelection();
});
selectedLayersClear.addEventListener("keydown", event => {
  if (event.key !== "Enter" && event.key !== " ") return;
  event.preventDefault();
  event.stopPropagation();
  clearPromptLayerSelection();
});
recordedClose.addEventListener("click", closeRecordedModal);
queryLayersClose.addEventListener("click", closeQueryLayersModal);
queryLayersSubmit.addEventListener("click", submitQueryLayerSelection);
renderMichlolTeam();
applyLocaleUi();
updatePromptPlaceholder();
enableMentionHighlight(promptInput);
enableMentionHighlight(stepInjectPrompt);
attachTeamMentionAutocomplete(promptInput);
attachTeamMentionAutocomplete(stepInjectPrompt);
initPanelResizers();
loadInvestigationRegistry();
loadWorkstreamSeenState();
renderInvestigationSelector();
renderWelcomePage();
setPageView("welcome", { focus: false });

async function boot() {
  initMap();
  await hydrateInvestigationRegistry();
  await loadLayerCatalog();
  await loadWorkstreams();
  await loadInvestigationMemory({ restoreLayers: true });
  let runtimeStatus = null;
  try {
    runtimeStatus = await fetch(buildLocaleApiUrl("/api/status"), { cache: "no-store" }).then(response => response.json());
    if (runtimeStatus.locations_url) {
      const runtimeLocations = await fetch(runtimeStatus.locations_url, { cache: "no-store" }).then(response => response.json());
      Object.entries(runtimeLocations).forEach(([locationId, location]) => {
        LOCATIONS[locationId] = {
          name: location.name || locationId,
          type: location.type || "",
          lat: Number(location.latitude),
          lon: Number(location.longitude)
        };
      });
      renderEvidence();
    }
    const datasetUrl = runtimeStatus.dataset_url || "./data/serbia_kosovo_events_projection.csv";
    const response = await fetch(datasetUrl, { cache: "no-store" });
    if (!response.ok) throw new Error("dataset unavailable");
    state.events = parseCsv(await response.text()).map(enrich);
    const versionLabel = runtimeStatus.dataset_version ? ` · ${runtimeStatus.dataset_version.toUpperCase()}` : "";
    updateSystemStatus("dataset",
      `${state.events.length.toLocaleString("he-IL")} אירועים זמינים במאגר${versionLabel}`,
      `${state.events.length.toLocaleString("en-US")} events available in the dataset${versionLabel}`,
      "ready"
    );
  } catch (error) {
    updateSystemStatus("dataset", "טעינת הנתונים נכשלה", "Failed to load data", "error");
  }
  try {
    const status = runtimeStatus || await fetch(buildLocaleApiUrl("/api/status"), { cache: "no-store" }).then(response => response.json());
    if (!status.configured) throw new Error("not configured");
    updateSystemStatus("agent", "Hermes + MCP מחוברים", "Hermes + MCP connected", "ready");
  } catch (error) {
    updateSystemStatus("agent", "מצב הדגמה מקומי", "Local demo mode", "error");
  }
}

boot();
