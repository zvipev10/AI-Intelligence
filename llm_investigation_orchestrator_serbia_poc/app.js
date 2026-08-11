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
  return /(^|[^\p{L}\p{N}_])@משה(?![\p{L}\p{N}_])/u.test(String(currentPrompt || ""))
    ? "/api/live-steps?agent=moshe"
    : "/api/live-steps?agent=general";
}

const INVESTIGATIONS_STORAGE_KEY = "serbia-poc-investigations-v2";
const LEGACY_INVESTIGATIONS_STORAGE_KEYS = ["serbia-poc-investigations-v1"];
const DEFAULT_INVESTIGATION_NAME = "חקירה חדשה";
const TEAM_MENTION_AGENT_INSTRUCTION = [
  "הנחיית ממשק קבועה:",
  "סימוני @ לפני שמות חברי מכלול, כגון @משה או @טליה, הם פנייה פנימית של המשתמש לצוות העבודה.",
  "אל תתייחס לשמות חברי המכלול כאל ישויות מודיעיניות, אנשים לחקירה, מקורות, מיקומים או מילות מפתח, אלא אם המשתמש מבקש במפורש לנתח את חברי המכלול עצמם."
].join("\n");

const MICHLOL_MEMBERS = [
  { id: "moshe-targets-officer", displayName: "משה", roleLabel: "קצין מטרות", memberType: "user", avatar: "./assets/michlol/moshe.png", initial: "מ" },
  { id: "talia-tama-officer", displayName: "טליה", roleLabel: "קצינת תמא", memberType: "user", avatar: "./assets/michlol/talia.png", initial: "ט" },
  { id: "naama-field-officer", displayName: "נעמה", roleLabel: "קצינת שטח", memberType: "user", avatar: "./assets/michlol/naama.png", initial: "נ" },
  { id: "gadi-collection-officer", displayName: "גדי", roleLabel: "קצין איסוף", memberType: "user", avatar: "./assets/michlol/gadi.png", initial: "ג" },
  { id: "yahli-processing-officer", displayName: "יהלי", roleLabel: "קצין עיבוד", memberType: "user", avatar: "./assets/michlol/yahli.png", initial: "י" }
];

const MICHLOL_MEMBER_WELCOME = "אני מחובר עכשיו לשיחה הזו. שלח לי את המשימה או השאלה הבאה, ובשלב הבא נחבר כאן סוכן ייעודי לחבר המכלול.";
const MOSHE_MEMBER_ID = "moshe-targets-officer";
const WORKSTREAM_SEEN_STORAGE_KEY = "serbia-poc-workstream-seen-v1";
const MOSHE_MESSAGE_LABEL = "משה - קצין מטרות";
const MOSHE_WELCOME = "אני משה, קצין המטרות. אפשר לשאול אותי על אינדיקציות ומטרות, או לפתוח מעקב חדש.";

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
  investigationName: DEFAULT_INVESTIGATION_NAME,
  investigations: [],
  investigationMemory: null,
  investigationMemoryLoading: false,
  investigationMemoryError: "",
  investigationMemoryLoadToken: 0,
  datasetVersion: "",
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
const resultTitle = document.getElementById("resultTitle");
const resultSubtitle = document.getElementById("resultSubtitle");
const resultCount = document.getElementById("resultCount");
const sendButton = document.getElementById("sendButton");
const investigationInput = document.getElementById("investigationInput");
const investigationAddButton = document.getElementById("investigationAddButton");
const investigationList = document.getElementById("investigationList");
const michlolTeam = document.getElementById("michlolTeam");
const promptOptionsButton = document.getElementById("promptOptionsButton");
const promptOptionsMenu = document.getElementById("promptOptionsMenu");
const workstreamRail = document.getElementById("workstreamRail");
const workstreamRailList = document.getElementById("workstreamRailList");
const workstreamRailCount = document.getElementById("workstreamRailCount");
const workstreamRailToggle = document.getElementById("workstreamRailToggle");
const playbackNextButton = document.getElementById("playbackNextButton");
const intelligenceModeSelect = document.getElementById("intelligenceModeSelect");
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
const agentStatus = document.getElementById("agentStatus");
const viewRecommendation = document.getElementById("viewRecommendation");
const layerSelectorSearch = document.getElementById("layerSelectorSearch");
const layerSelectorList = document.getElementById("layerSelectorList");
const layerSelectorStatus = document.getElementById("layerSelectorStatus");
const workspace = document.querySelector(".workspace");
const chatPanelToggle = document.getElementById("chatPanelToggle");
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

const LAYER_FAMILY_LABELS = {
  entities: "ישויות",
  locations: "מיקומים",
  events: "אירועים לפי source_type",
  targets: "מטרות"
};

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
  const visible = MICHLOL_MEMBERS.slice(0, 3);
  const hidden = MICHLOL_MEMBERS.slice(3);
  michlolTeam.innerHTML = `
    <span class="michlol-title">מכלול</span>
    ${visible.map(michlolMemberHtml).join("")}
    ${hidden.length ? `
      <details class="michlol-more">
        <summary title="הצג חברי מכלול נוספים" aria-label="הצג חברי מכלול נוספים">...</summary>
        <div class="michlol-more-list">
          ${hidden.map(michlolMemberHtml).join("")}
        </div>
      </details>` : ""}`;
  renderPromptOptions();
}

function renderPromptOptions() {
  const option = promptOptionsMenu?.querySelector('[data-prompt-option="workstream"]');
  if (option) option.hidden = state.activeConversationMemberId !== MOSHE_MEMBER_ID;
}

function activeConversationMember() {
  return MICHLOL_MEMBERS.find(member => member.id === state.activeConversationMemberId) || null;
}

function updatePromptPlaceholder() {
  if (!promptInput) return;
  if (state.workstreamComposerMode) {
    promptInput.placeholder = "תאר מה לעקוב אחריו ומה מטרת המעקב...";
    return;
  }
  const member = activeConversationMember();
  promptInput.placeholder = member ? `כתוב אל ${member.displayName}...` : "כתוב שאלת חקירה...";
}

function memberMessageLabel(member) {
  if (member.id === MOSHE_MEMBER_ID) return MOSHE_MESSAGE_LABEL;
  return `${member.displayName} · ${member.roleLabel}`;
}

function assistantMessageLabel() {
  const member = activeConversationMember();
  if (state.activeTeamMentions.some(mention => mention.id === MOSHE_MEMBER_ID)) return MOSHE_MESSAGE_LABEL;
  return member ? memberMessageLabel(member) : "סוכן חקירה";
}

function resultMessageLabel(result = {}) {
  return result.responding_agent === "moshe" ? MOSHE_MESSAGE_LABEL : assistantMessageLabel();
}

function appendMemberWelcomeMessage(member) {
  conversation.querySelectorAll(".member-welcome-message").forEach(message => message.remove());
  const welcome = member.id === MOSHE_MEMBER_ID ? MOSHE_WELCOME : MICHLOL_MEMBER_WELCOME;
  return appendMessage("assistant", `<p>${escapeHtml(welcome)}</p>`, {
    label: memberMessageLabel(member),
    className: "member-welcome-message",
    memberId: member.id
  });
}

function selectConversationMember(memberId) {
  const member = MICHLOL_MEMBERS.find(item => item.id === memberId);
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

function createTeamMentionMenu() {
  const menu = document.createElement("div");
  menu.id = "teamMentionMenu";
  menu.className = "team-mention-menu";
  menu.setAttribute("role", "listbox");
  menu.setAttribute("aria-label", "בחירת חבר מכלול");
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
  return String(value || "").normalize("NFKC").trim().toLocaleLowerCase("he-IL");
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
  if (!normalized) return MICHLOL_MEMBERS;
  return MICHLOL_MEMBERS.filter(member => {
    const haystack = normalizeTeamMentionText(`${member.displayName} ${member.roleLabel} ${member.id}`);
    return haystack.includes(normalized);
  });
}

function recognizedTeamMemberByMention(rawMention) {
  const normalized = normalizeTeamMentionText(rawMention).replace(/^@/, "").replace(/[^\p{L}\p{N}_-]+$/gu, "");
  if (!normalized) return null;
  return MICHLOL_MEMBERS.find(member => normalizeTeamMentionText(member.displayName) === normalized) || null;
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
    const member = MICHLOL_MEMBERS.find(item => normalizeTeamMentionText(item.displayName) === query);
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
  btn.title = visible ? "הסתר שכבת ראיות" : "הצג שכבת ראיות";
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
    sourceLabel: `ראיות: ${layer.label}`,
    preferredView: layer.preferredView,
    layers: [layer]
  });
  state.rawOverlayMinimized = false;
  activateView(layer.preferredView, { reason: `שכבת ראיות: ${layer.label}` });
  renderAllViews();
  updateEvidenceReferenceButtons();
}

function buildEvidenceReferencesSection(result) {
  const layers = buildEvidenceReferenceLayers(result);
  if (!layers.length) return null;
  const section = document.createElement("details");
  section.className = "evidence-references";
  section.innerHTML = `
    <summary class="evidence-references-summary">מזהי ראיות · ${layers.length.toLocaleString("he-IL")} שכבות</summary>
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
          <span class="evidence-reference-view">${layer.preferredView === "timeline" ? "ציר זמן" : "מפה"} · ${(layer.items || []).length.toLocaleString("he-IL")}</span>
        </summary>
        ${shown.length ? `<div class="evidence-reference-identifiers" dir="ltr">${shown.map(escapeHtml).join(", ")}${overflow ? ` <span dir="rtl">ועוד ${overflow.toLocaleString("he-IL")}</span>` : ""}</div>` : ""}
      </details>`;
    const btn = item.querySelector(".evidence-reference-link");
    btn.dataset.sourceId = evidenceLayerSourceId(result, layer);
    btn.title = "הצג שכבת ראיות";
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
  return [...fields].sort((a, b) => a.localeCompare(b, "he"));
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
      .sort((a, b) => a.localeCompare(b, "he"))
      .map(key => stringifyFilterValue(value[key]))
      .filter(Boolean)
      .join(" ");
  }
  return String(value);
}

function normalizeFilterText(value) {
  return stringifyFilterValue(value).trim().replace(/\s+/g, " ").toLocaleLowerCase("he-IL");
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
  if (target.count_assessment === "range" && min != null && max != null) return `${Number(min).toLocaleString("he-IL")}–${Number(max).toLocaleString("he-IL")}`;
  if (estimate != null) return `${target.count_assessment === "approximate" ? "כ־" : ""}${Number(estimate).toLocaleString("he-IL")}`;
  if (min != null && max != null && min !== max) return `${Number(min).toLocaleString("he-IL")}–${Number(max).toLocaleString("he-IL")}`;
  if (min != null) return Number(min).toLocaleString("he-IL");
  if (max != null) return Number(max).toLocaleString("he-IL");
  return "לא הוכרע";
}

function confidenceLabel(value) {
  return value === "high" ? "גבוה" : value === "medium" ? "בינוני" : (value || "-");
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
    reconstruction: item.reconstruction && typeof item.reconstruction === "object" ? {
      type: item.reconstruction.type || "",
      layer_kind: item.reconstruction.layer_kind || "",
      dataset_version: item.reconstruction.dataset_version || "",
      locale: item.reconstruction.locale || ""
    } : null,
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
    if (savedLayer.reconstruction?.record_ids?.length) {
      const restored = await presentMemorySavedLayer(savedLayer.id, { silent: true });
      restoredMemoryLayers.push({
        ...savedLayer,
        restore_status: restored?.restore_status || "unavailable"
      });
      continue;
    }
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

async function presentMemorySavedLayer(memoryLayerId, options = {}) {
  const query = new URLSearchParams({
    investigation_id: state.investigationId,
    locale: document.documentElement.lang || "he"
  });
  try {
    const response = await fetch(
      `/api/investigation-memory/layers/${encodeURIComponent(memoryLayerId)}/presentation?${query}`,
      { cache: "no-store" }
    );
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "טעינת השכבה השמורה נכשלה");
    if (payload.restore_status === "unavailable") {
      throw new Error(payload.reason || "השכבה השמורה אינה זמינה במאגר הנוכחי");
    }
    const layers = buildTypedResultLayers(payload);
    if (!layers.length) throw new Error("לא נמצאו רשומות זמינות לשחזור השכבה");
    const sourceId = sanitizeLayerKey(`memory:${memoryLayerId}`);
    state.layers = state.layers.filter(layer => layer.sourceId !== sourceId);
    const addedLayers = addResultLayers({
      sourceId,
      sourceLabel: payload.label || "שכבה מזיכרון החקירה",
      preferredView: layers[0]?.preferredView || "map",
      layers
    });
    addedLayers.forEach(layer => applySavedFiltersToLayer(layer, {
      id: memoryLayerId,
      applied_filters: payload.applied_filters || []
    }));
    state.rawOverlayMinimized = false;
    activateView(layers[0]?.preferredView || "map", { reason: payload.label || "שכבה מזיכרון החקירה" });
    renderAllViews();
    if (payload.restore_status === "partially_restored" && !options.silent) {
      workstreamMessage(`<p>השכבה שוחזרה חלקית: ${Number(payload.restored_count || 0).toLocaleString("he-IL")} מתוך ${Number(payload.requested_count || 0).toLocaleString("he-IL")} רשומות זמינות.</p>`);
    }
    return payload;
  } catch (error) {
    if (!options.silent) {
      workstreamMessage(`<p>לא הצלחתי להציג את השכבה השמורה.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`);
    }
    return { restore_status: "unavailable", error: error.message };
  }
}

async function applyMemoryLayerActions(result = {}) {
  const actions = Array.isArray(result.memory_layer_actions) ? result.memory_layer_actions : [];
  for (const action of actions) {
    if (action?.action !== "present" || !action.memory_layer_id) continue;
    await presentMemorySavedLayer(action.memory_layer_id);
  }
}

async function loadInvestigationMemory(options = {}) {
  if (!state.investigationId) return null;
  const token = ++state.investigationMemoryLoadToken;
  state.investigationMemoryLoading = true;
  state.investigationMemoryError = "";
  try {
    const response = await fetch(`/api/investigation-memory?id=${encodeURIComponent(state.investigationId)}`, { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "טעינת זיכרון החקירה נכשלה");
    if (token !== state.investigationMemoryLoadToken) return null;
    state.investigationMemory = payload;
    if (options.restoreLayers) await restoreMemorySavedLayers(payload, token);
    return payload;
  } catch (error) {
    if (token === state.investigationMemoryLoadToken) {
      state.investigationMemoryError = error.message || "טעינת זיכרון החקירה נכשלה";
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
  const reconstructionIds = evidenceLayerIdentifiers({ ...layer, items: filteredItems });
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
    sample_ids: identifiersForLayerContext(layer, filteredItems),
    reconstruction: reconstructionIds.length ? {
      type: "typed_ids",
      layer_kind: layer.kind,
      record_ids: reconstructionIds,
      dataset_version: state.datasetVersion || "",
      locale: document.documentElement.lang || "he"
    } : null
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
  if (!canSaveLayerToMemory(layer) || state.busy || button?.dataset.memorySaving === "true") return;
  button.dataset.memorySaving = "true";
  button.title = "שומר שכבה לזיכרון החקירה";
  button.setAttribute("aria-label", "שומר שכבה לזיכרון החקירה");
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
    if (!response.ok) throw new Error(payload.error || "שמירת השכבה לזיכרון נכשלה");
    layer.investigation_memory_layer_id = payload.saved?.id || true;
    button.title = "השכבה נשמרה לזיכרון החקירה";
    button.setAttribute("aria-label", "השכבה נשמרה לזיכרון החקירה");
    renderEvidence();
  } catch (error) {
    button.title = error.name === "AbortError" ? "שמירת השכבה נמשכה יותר מדי זמן. נסה שוב." : error.message;
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
    selectedLayersButton.title = "בחר שכבות לשאילתה";
    return;
  }
  const preview = layers.slice(0, 2).map(layer => layer.label).join(" · ");
  const remaining = layers.length > 2 ? ` +${layers.length - 2}` : "";
  selectedLayersLabel.textContent = state.workstreamComposerMode
    ? "שכבת מעקב"
    : (layers.length === 1 ? "שכבה אחת נבחרה" : `${layers.length.toLocaleString("he-IL")} שכבות נבחרו`);
  selectedLayersSummary.textContent = `${preview}${remaining}`;
  selectedLayersButton.title = `שנה שכבות לשאילתה: ${layers.map(layer => layer.label).join(", ")}`;
}

function clearPromptLayerSelection() {
  state.promptSelectedLayerIds = new Set();
  renderSelectedLayersButton();
  renderQueryLayersModal();
}

function selectedLayerContextText(layers) {
  if (!layers.length) return "";
  const lines = [
    "הקשר שכבות שנבחרו בממשק:",
    "התייחס לשכבות אלה כהקשר ולמסננים שהאנליסט בחר לפני שליחת השאלה. אם השאלה מתייחסת לתוצאות/שכבות/הבחירה הנוכחית, השתמש בהן כדי לצמצם את החיפוש."
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
    lines.push(`- ${layer.label} (${layer.kind}, ${layer.catalog_layer_id || "no-catalog-id"}): ${count} רשומות${source}${filters}${ids}${more}`);
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
    result.answer = `${result.answer}\n\nהשינוי נשמר במעקב (גרסה ${result.workstream_artifact.revision}).`;
    void loadWorkstreams();
  } else if (result.workstream_conflict?.error) {
    result.answer = `${result.answer}\n\nלא שמרתי את השינוי: ${result.workstream_conflict.error}`;
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
  const safeName = normalizeInvestigationName(name) || DEFAULT_INVESTIGATION_NAME;
  return {
    id: createInvestigationId(),
    name: safeName,
    created_at: new Date().toISOString()
  };
}

function ensureInvestigationRecord(name) {
  const safeName = normalizeInvestigationName(name) || DEFAULT_INVESTIGATION_NAME;
  const existing = state.investigations.find(item => investigationNameKey(item.name) === investigationNameKey(safeName));
  if (existing) return existing;
  const created = createInvestigationRecord(safeName);
  state.investigations.push(created);
  saveInvestigationRegistry();
  return created;
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
          const key = investigationNameKey(item.name);
          if (!item.name || seen.has(key)) return false;
          seen.add(key);
          return true;
        })
    : [];
  if (!investigations.length) investigations.push({
    id: state.investigationId,
    name: DEFAULT_INVESTIGATION_NAME,
    created_at: new Date().toISOString()
  });
  state.investigations = investigations;
  const active = investigations.find(item => item.id === registry?.active_id) || investigations[0];
  state.investigationId = active.id;
  state.investigationName = active.name;
  saveInvestigationRegistry();
}

async function hydrateInvestigationRegistry() {
  try {
    const response = await fetch("/api/investigations", { cache: "no-store" });
    if (!response.ok) throw new Error(`investigation registry unavailable (${response.status})`);
    const payload = await response.json();
    const remoteInvestigations = Array.isArray(payload?.investigations) ? payload.investigations : [];
    const localById = new Map(state.investigations.map(item => [item.id, item]));
    const localByName = new Map(state.investigations.map(item => [investigationNameKey(item.name), item]));

    remoteInvestigations.forEach(item => {
      const id = String(item?.investigation_id || item?.id || "").trim();
      const name = normalizeInvestigationName(item?.name);
      if (!id || !name) return;
      const existing = localById.get(id) || localByName.get(investigationNameKey(name));
      const hydrated = {
        id,
        name,
        created_at: item?.created_at_utc || existing?.created_at || new Date().toISOString()
      };
      if (existing) {
        const index = state.investigations.indexOf(existing);
        state.investigations[index] = hydrated;
        if (state.investigationId === existing.id) {
          state.investigationId = hydrated.id;
          state.investigationName = hydrated.name;
        }
      } else {
        state.investigations.push(hydrated);
      }
      localById.set(id, hydrated);
      localByName.set(investigationNameKey(name), hydrated);
    });

    saveInvestigationRegistry();
    renderInvestigationSelector();
  } catch (error) {
    console.warn("Could not hydrate investigations from server", error);
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
    investigationInput.value = state.investigationName || DEFAULT_INVESTIGATION_NAME;
  }
  const matches = matchingInvestigations(state.investigationSearchQuery);
  investigationInput.setAttribute("aria-expanded", state.investigationSelectorOpen && matches.length ? "true" : "false");
  investigationList.hidden = !state.investigationSelectorOpen || !matches.length;
  investigationList.innerHTML = matches.map(item => `
    <button type="button" class="investigation-option ${item.id === state.investigationId ? "active" : ""}" role="option" aria-selected="${item.id === state.investigationId}" data-investigation-id="${escapeHtml(item.id)}">
      <span>${escapeHtml(item.name)}</span>
      ${item.id === state.investigationId ? "<small>פעילה</small>" : ""}
    </button>
  `).join("");
}

function selectInvestigation(investigation, options = {}) {
  if (!investigation || state.busy) return;
  state.investigationId = investigation.id;
  state.investigationName = investigation.name;
  state.investigationSelectorOpen = false;
  state.investigationSearchQuery = "";
  state.investigationMemoryLoadToken += 1;
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
  const name = normalizeInvestigationName(investigationInput?.value) || DEFAULT_INVESTIGATION_NAME;
  const investigation = ensureInvestigationRecord(name);
  if (state.busy) {
    renderInvestigationSelector();
    return;
  }
  selectInvestigation(investigation, { focusInput: true });
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
  const fieldOptionsFor = selectedField => {
    const availableFields = selectedField && !fields.includes(selectedField)
      ? [selectedField, ...fields]
      : fields;
    return availableFields.length
    ? availableFields.map(field => `<option value="${escapeHtml(field)}" ${field === selectedField ? "selected" : ""}>${escapeHtml(field)}</option>`).join("")
    : '<option value="">אין שדות זמינים</option>';
  };
  const draftHtml = draftFilters.length
    ? draftFilters.map((filter, index) => `
      <div class="filter-draft-row">
        <select class="layer-filter-select filter-field-select" data-filter-field data-filter-index="${index}" aria-label="בחר שדה מסנן">
          ${fieldOptionsFor(filter.field)}
        </select>
        <span class="filter-operator">contains</span>
        <input class="layer-filter-input filter-value-input" data-filter-value data-filter-index="${index}" type="text" value="${escapeHtml(stringifyFilterValue(filter.value))}" placeholder="ערך לחיפוש" aria-label="ערך מסנן">
        <button type="button" class="filter-remove-button" data-filter-remove="${index}" aria-label="הסר מסנן" title="הסר מסנן">×</button>
      </div>`).join("")
    : "";
  const appliedHtml = appliedFilters.length
    ? appliedFilters.map(filter => `
      <span class="filter-chip">
        <span dir="ltr">${escapeHtml(filter.field)}</span>
        <span>contains</span>
        <strong>${escapeHtml(stringifyFilterValue(filter.value))}</strong>
      </span>`).join("")
    : '<span class="filter-empty inline">אין מסננים פעילים.</span>';
  const addDisabled = fields.length ? "" : "disabled";
  const errorHtml = layer.filterError
    ? `<div class="filter-error" role="alert">${escapeHtml(layer.filterError)}</div>`
    : "";

  panel.hidden = false;
  panel.innerHTML = `
    <div class="layer-filter-header">
      <div>
        <span class="layer-filter-kicker">מסנני שכבה</span>
        <h3>${escapeHtml(layer.label)}</h3>
      </div>
      <button type="button" class="layer-filter-close" data-layer-filter="${escapeHtml(layer.id)}" aria-label="סגור מסננים" title="סגור מסננים">×</button>
    </div>
    ${draftFilters.length ? `<div class="layer-filter-section"><div class="filter-draft-list">${draftHtml}</div>${errorHtml}</div>` : errorHtml ? `<div class="layer-filter-section">${errorHtml}</div>` : ""}
    <div class="layer-filter-actions">
      <button type="button" class="filter-add-button" data-filter-add ${addDisabled}>הוסף מסנן</button>
      <button type="button" class="primary-filter-action" data-filter-apply>החל</button>
    </div>`;
}

function addDraftFilter(layer) {
  ensureLayerFilterState(layer);
  const [firstField] = filterFieldsForLayer(layer);
  if (!firstField) {
    layer.filterError = "אין שדות זמינים לסינון בשכבה הזו.";
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
    layer.filterError = "יש למלא שדה וערך לפני החלת המסננים.";
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
  return String(value ?? "").trim().toLocaleLowerCase("he-IL");
}

function layerSearchText(layer) {
  const familyLabel = LAYER_FAMILY_LABELS[layer.family] || layer.family || "";
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
    layerSelectorStatus.textContent = "טוען שכבות";
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
    layerSelectorList.innerHTML = '<div class="layer-selector-empty">טוען שכבות...</div>';
    return;
  }
  if (!state.layerCatalog.length) {
    layerSelectorList.innerHTML = '<div class="layer-selector-empty">אין שכבות זמינות.</div>';
    return;
  }

  if (!normalizeLayerSearch(state.layerSearchQuery)) {
    layerSelectorList.innerHTML = '<div class="layer-selector-empty">הקלד שם שכבה או סוג מקור.</div>';
    return;
  }

  const matches = matchingCatalogLayers();
  if (!matches.length) {
    layerSelectorList.innerHTML = '<div class="layer-selector-empty">לא נמצאו שכבות תואמות.</div>';
    return;
  }

  layerSelectorList.innerHTML = matches.map(layer => {
    const open = isCatalogLayerOpen(layer.id);
    const loading = state.openingLayerIds.has(layer.id);
    const family = LAYER_FAMILY_LABELS[layer.family] || layer.family || "שכבה";
    return `
      <button type="button" role="option" class="layer-select-option ${open ? "selected" : ""}" data-layer-select="${escapeHtml(layer.id)}" title="${escapeHtml(layer.label)}" ${loading ? "disabled" : ""}>
        <span class="layer-select-main">
          <span class="layer-select-name">${escapeHtml(layer.label)}</span>
          <span class="layer-select-family">${escapeHtml(family)}</span>
        </span>
        <span class="layer-select-meta">
          <span class="layer-select-count">${Number(layer.count || 0).toLocaleString("he-IL")}</span>
          ${open ? '<span class="layer-select-state">פתוחה</span>' : ""}
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
  queryLayersSubmit.textContent = state.workstreamComposerMode ? "צרף שכבה" : "בחר שכבות";
  if (!openLayers.length) {
    queryLayersList.innerHTML = '<div class="layer-selector-empty">אין שכבות פתוחות לבחירה.</div>';
    return;
  }
  queryLayersList.innerHTML = openLayers.map(layer => {
    return `
    <label class="step-inject-layer-item" style="${layerColorStyle(layer)}">
      <input type="${state.workstreamComposerMode ? "radio" : "checkbox"}" name="${state.workstreamComposerMode ? "workstream-layer" : ""}" value="${escapeHtml(layer.id)}" ${state.promptSelectedLayerIds.has(layer.id) ? "checked" : ""}>
      <span class="step-inject-layer-color"></span>
      <span class="step-inject-layer-name">${escapeHtml(layer.label)}</span>
      <span class="step-inject-layer-count">${itemsForLayerPresentation(layer).length.toLocaleString("he-IL")}</span>
    </label>`;
  }).join("");
}

async function loadLayerCatalog() {
  if (!layerSelectorList || !layerSelectorStatus) return;
  state.layerCatalogLoading = true;
  state.layerCatalogError = "";
  renderLayerSelector();
  try {
    const response = await fetch("/api/layers", { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "טעינת השכבות נכשלה");
    state.layerCatalog = payload.layers || [];
  } catch (error) {
    state.layerCatalogError = error.message || "טעינת השכבות נכשלה";
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
    const response = await fetch(`/api/layers/${encodeURIComponent(layerId)}/rows`, { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "טעינת נתוני השכבה נכשלה");
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
    const response = await fetch(`/api/layers/${encodeURIComponent(ATTACK_TARGET_CATALOG_LAYER_ID)}/rows`, { cache: "no-store" });
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
  article.innerHTML = `<div class="message-label">${escapeHtml(options.label || (role === "user" ? "אנליסט" : assistantMessageLabel()))}</div>${html}`;
  conversation.appendChild(article);
  followConversationAfterUpdate(shouldFollow);
  return article;
}

function thinkingIndicatorHtml() {
  return `
    <span class="thinking-indicator" role="status" aria-label="חושב">
      <span>חושב</span><span class="thinking-dots" aria-hidden="true"><i></i><i></i><i></i></span>
    </span>`;
}

function activeWorkstreams() {
  if (state.investigationPlayback?.mode !== "real_time") return [];
  return state.workstreams.filter(item => item?.status !== "archived");
}

const WORKSTREAM_STATUS_LABELS = {
  active: "פעיל",
  paused: "מושהה",
  completed: "הושלם",
  archived: "בארכיון"
};

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

function workstreamHasNewItems(workstream) {
  const updated = Date.parse(workstream?.updated_at_utc || workstream?.created_at_utc || "");
  const seen = Date.parse(state.workstreamSeen[workstreamSeenKey(workstream?.workstream_id)] || "");
  return Number.isFinite(updated) && (!Number.isFinite(seen) || updated > seen);
}

function markWorkstreamSeen(workstream) {
  if (!workstream?.workstream_id) return;
  const listedWorkstream = state.workstreams.find(
    item => item?.workstream_id === workstream.workstream_id
  );
  const seenAt = [
    workstream.updated_at_utc,
    workstream.created_at_utc,
    listedWorkstream?.updated_at_utc,
    listedWorkstream?.created_at_utc,
  ].reduce((latest, value) => {
    const timestamp = Date.parse(value || "");
    return Number.isFinite(timestamp) && timestamp > latest ? timestamp : latest;
  }, 0);
  state.workstreamSeen[workstreamSeenKey(workstream.workstream_id)] =
    seenAt ? new Date(seenAt).toISOString() : new Date().toISOString();
  saveWorkstreamSeenState();
}

function workstreamUpdatedLabel(workstream) {
  const value = workstream?.updated_at_utc || workstream?.created_at_utc;
  const date = value ? new Date(value) : null;
  if (!date || Number.isNaN(date.getTime())) return "";
  return new Intl.DateTimeFormat("he-IL", {
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
    workstreamRailToggle.setAttribute("aria-label", state.workstreamRailCollapsed ? "הרחב מעקבים" : "מזער מעקבים");
    workstreamRailToggle.title = state.workstreamRailCollapsed ? "הרחב מעקבים" : "מזער מעקבים";
    const icon = workstreamRailToggle.querySelector(".material-symbols-rounded");
    if (icon) icon.textContent = state.workstreamRailCollapsed ? "chevron_right" : "chevron_left";
  }
  if (state.map) setTimeout(() => state.map.resize(), 220);
}

function renderWorkstreamIndicator() {
  if (!workstreamRail || !workstreamRailList || !workstreamRailCount) return;
  const workstreams = activeWorkstreams();
  const visible = workstreams.length > 0 && state.investigationPlayback?.mode === "real_time";
  workstreamRail.hidden = !visible;
  document.querySelector(".workspace")?.classList.toggle("workstream-rail-visible", visible);
  workstreamRailCount.textContent = workstreams.length.toLocaleString("he-IL");
  workstreamRailList.innerHTML = workstreams.map(item => {
    const hasNew = workstreamHasNewItems(item);
    const status = WORKSTREAM_STATUS_LABELS[item.status] || item.status || "פעיל";
    const updated = workstreamUpdatedLabel(item);
    return `
      <button type="button" class="workstream-rail-card ${hasNew ? "has-new" : ""}" role="listitem" data-workstream-show="${escapeHtml(item.workstream_id)}" title="${escapeHtml(item.title || "מעקב")}">
        <span class="workstream-card-state" aria-hidden="true"></span>
        <span class="workstream-card-body">
          <strong>${escapeHtml(item.title || "מעקב")}</strong>
          <span class="workstream-card-meta"><span>${escapeHtml(status)}</span>${updated ? `<time>${escapeHtml(updated)}</time>` : ""}</span>
        </span>
        ${hasNew ? '<span class="workstream-new-badge" aria-label="פריטים חדשים">חדש</span>' : ""}
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
    const response = await fetch(`/api/workstreams?investigation_id=${encodeURIComponent(investigationId)}`, { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "טעינת המעקבים נכשלה");
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
    label: options.label || "עדכון מעקב",
    className: `workstream-message${options.className ? ` ${options.className}` : ""}`,
    memberId: options.memberId,
  });
  scrollConversationToLatest();
  return article;
}

async function fetchWorkstream(workstreamId) {
  const response = await fetch(`/api/workstreams/${encodeURIComponent(workstreamId)}`, { cache: "no-store" });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "טעינת המעקב נכשלה");
  return payload;
}

function playbackNextStage(playback) {
  return playback?.run?.next_stage || playback?.next_stage || null;
}

function formatPlaybackTime(value) {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return String(value || "");
  return parsed.toLocaleString("he-IL", {
    timeZone: "UTC",
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function renderInvestigationPlayback() {
  if (!playbackNextButton || !intelligenceModeSelect || !intelligencePeriod) return;
  const playback = state.investigationPlayback;
  const mode = playback?.mode || "historical";
  intelligenceModeSelect.value = mode;
  renderWorkstreamIndicator();
  const timeframe = mode === "real_time"
    ? playback?.run?.visible_timeframe
    : playback?.full_timeframe;
  intelligencePeriod.textContent = timeframe?.from && timeframe?.to
    ? `${formatPlaybackTime(timeframe.from)}–${formatPlaybackTime(timeframe.to)}`
    : "";
  const next = playbackNextStage(state.investigationPlayback);
  const reevaluation = playback?.run?.reevaluation;
  const processing = reevaluation?.status === "running";
  if (playbackAgentStatus) {
    playbackAgentStatus.hidden = !processing && reevaluation?.status !== "failed";
    playbackAgentStatus.classList.toggle("failed", reevaluation?.status === "failed");
    playbackAgentStatus.textContent = processing ? "משה מעבד…" : "העיבוד של משה נכשל";
    playbackAgentStatus.title = reevaluation?.error || "";
  }
  playbackNextButton.hidden = mode !== "real_time" || !next?.timeframe;
  playbackNextButton.disabled = processing;
  if (!next?.timeframe) return;
  const nextTimeframe = next.timeframe;
  const tooltip = `פרק הזמן של השלב הבא: ${formatPlaybackTime(nextTimeframe.from)}–${formatPlaybackTime(nextTimeframe.to)}`;
  playbackNextButton.title = tooltip;
  playbackNextButton.setAttribute("aria-label", `השלב הבא. ${tooltip}`);
}

async function fetchInvestigationPlayback() {
  const investigationId = String(state.investigationId || "").trim();
  if (!investigationId) return null;
  const response = await fetch(
    `/api/playback?investigation_id=${encodeURIComponent(investigationId)}`,
    { cache: "no-store" }
  );
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "טעינת מצב התרחיש נכשלה");
  state.investigationPlayback = payload;
  renderInvestigationPlayback();
  if (payload?.run?.reevaluation?.status === "running") {
    void pollMoshePlaybackReevaluation();
  }
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
        `/api/playback?investigation_id=${encodeURIComponent(investigationId)}`,
        { cache: "no-store" }
      );
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || "טעינת מצב התרחיש נכשלה");
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
            workstreamMessage("<p>משה סיים לעבד את פרוסת המידע החדשה.</p>");
          }
        } else if (status === "failed") {
          workstreamMessage(`<p>הטווח עודכן, אך העיבוד של משה נכשל.</p><div class="answer-callout">${escapeHtml(payload.run.reevaluation.error || "")}</div>`);
        }
        return;
      }
    } catch (error) {
      if (token === state.playbackPollToken && playbackAgentStatus) {
        playbackAgentStatus.hidden = false;
        playbackAgentStatus.classList.add("failed");
        playbackAgentStatus.textContent = "לא ניתן לבדוק את מצב משה";
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
        <button type="button" class="final-answer-show-btn layers-hidden" data-source-id="${escapeHtml(finalSourceId(result))}" title="הצג תוצאות" aria-label="הצג תוצאות" aria-pressed="false">
          <span class="final-answer-show-label">הצג תוצאות</span>
        </button>
      </div>` : ""}
    </div>`,
    { label: MOSHE_MESSAGE_LABEL, memberId: MOSHE_MEMBER_ID }
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
      }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "התקדמות התרחיש נכשלה");
    state.investigationPlayback = {
      ...state.investigationPlayback,
      investigation_id: state.investigationId,
      mode: "real_time",
      run: result.run,
    };
    renderInvestigationPlayback();
    if (result.moshe_triggered) {
      workstreamMessage("<p>הטווח עודכן. משה מעבד כעת את פרוסת המידע החדשה מול המעקבים הפעילים.</p>");
    } else if (result.moshe_skipped_reason === "no_active_workstreams") {
      workstreamMessage("<p>הטווח עודכן. אין מעקבים פעילים, לכן לא הופעל עיבוד של משה.</p>");
    }
    if (result.run?.reevaluation?.status === "running") {
      void pollMoshePlaybackReevaluation();
    }
  } catch (error) {
    workstreamMessage(
      `<p>לא הצלחתי להתקדם לשלב הבא.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`
    );
  } finally {
    playbackNextButton.innerHTML = '<span class="material-symbols-rounded" aria-hidden="true">skip_next</span>';
    renderInvestigationPlayback();
  }
}

async function changeIntelligenceMode() {
  if (!intelligenceModeSelect) return;
  const mode = intelligenceModeSelect.value;
  if (mode !== "real_time") state.playbackPollToken += 1;
  intelligenceModeSelect.disabled = true;
  try {
    const response = await fetch("/api/playback/mode", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify({
        investigation_id: state.investigationId,
        mode,
      }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "שינוי מצב המידע נכשל");
    state.investigationPlayback = payload;
    renderInvestigationPlayback();
  } catch (error) {
    renderInvestigationPlayback();
    workstreamMessage(
      `<p>לא הצלחתי לשנות את מצב המידע.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`
    );
  } finally {
    intelligenceModeSelect.disabled = false;
  }
}

function workstreamAgent(workstream) {
  return (workstream.participants || []).find(item => item.kind === "agent") || null;
}

const WORKSTREAM_ARTIFACT_STATUS_LABELS = {
  active: "פעיל",
  ready_for_assessment: "מוכן להערכה",
  rejected: "נדחה",
  closed: "סגור"
};

const INDICATION_ROLE_LABELS = {
  supports: "תומכת",
  contradicts: "סותרת",
  context: "הקשר"
};

function workstreamArtifactHtml(workstream) {
  const artifacts = Array.isArray(workstream.artifacts) ? workstream.artifacts : [];
  const artifact = artifacts.find(item => item.artifact_type === "target_assessment_lead"
    && !["closed", "rejected"].includes(item.status))
    || artifacts.find(item => item.artifact_type === "target_assessment_lead");
  if (!artifact) return '<p class="workstream-message-meta">עדיין אין הובלה להערכה במעקב.</p>';
  const content = artifact.content || {};
  const activeIndications = (content.indications || []).filter(item => item.state !== "removed");
  const indications = activeIndications.length
    ? `<ul>${activeIndications.map(item => {
        const reference = item.source_reference || {};
        const detail = item.annotation || item.relevance || item.observed_claim || "";
        return `<li><strong>${escapeHtml(reference.record_id || "")}</strong> · ${escapeHtml(INDICATION_ROLE_LABELS[item.role] || item.role || "הקשר")}${detail ? ` — ${escapeHtml(detail)}` : ""}</li>`;
      }).join("")}</ul>`
    : "<p>אין אינדיקציות פעילות.</p>";
  const gaps = (content.gaps || []).length
    ? `<p><strong>פערים:</strong> ${escapeHtml(content.gaps.join(" · "))}</p>`
    : "<p><strong>פערים:</strong> לא נרשמו</p>";
  const questions = (content.assessment_questions || []).length
    ? `<p><strong>שאלות להערכה:</strong> ${escapeHtml(content.assessment_questions.join(" · "))}</p>`
    : "";
  return `
    <section class="workstream-artifact-summary">
      <p><strong>הובלה להערכה:</strong> ${escapeHtml(content.lead_statement || "ללא ניסוח")}</p>
      <p class="workstream-message-meta">סטטוס: ${escapeHtml(WORKSTREAM_ARTIFACT_STATUS_LABELS[artifact.status] || artifact.status || "לא ידוע")} · גרסה: ${Number(artifact.revision || 0).toLocaleString("he-IL")}</p>
      <p><strong>אינדיקציות:</strong></p>
      ${indications}
      ${gaps}
      ${questions}
    </section>`;
}

function normalizedWorkstreamSummaryText(value) {
  return String(value || "").replace(/\s+/g, " ").trim().toLocaleLowerCase("he-IL");
}

function workstreamResultSourceId(workstreamId) {
  return sanitizeLayerKey(`workstream:${workstreamId}`);
}

function workstreamHasPresentation(workstream) {
  const targetIds = Array.isArray(workstream.target_ids) ? workstream.target_ids : [];
  if (targetIds.some(targetId => String(targetId || "").trim())) return true;
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

async function showWorkstreamResultVisibility(workstreamId, btn) {
  const sourceId = workstreamResultSourceId(workstreamId);
  if (btn) btn.disabled = true;
  try {
    const response = await fetch(
      `/api/workstreams/${encodeURIComponent(workstreamId)}/presentation`,
      { cache: "no-store" }
    );
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "טעינת תוצאות המעקב נכשלה");
    state.layers = state.layers.filter(layer => layer.sourceId !== sourceId);
    const layers = buildTypedResultLayers(result);
    if (!layers.length) throw new Error("אין למעקב תוצאות שניתן להציג");
    addResultLayers({
      sourceId,
      sourceLabel: result.title || "תוצאות מעקב",
      preferredView: "map",
      layers
    });
    state.rawOverlayMinimized = false;
    activateView("map", { reason: "תוצאות המעקב" });
    renderAllViews();
  } catch (error) {
    workstreamMessage(
      `<p>לא הצלחתי להציג את תוצאות המעקב.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`
    );
  } finally {
    if (btn) btn.disabled = false;
    updateSourceVisibilityBtn(btn);
  }
}

function appendWorkstreamUpdate(workstream) {
  conversation.querySelectorAll("[data-workstream-update-id]").forEach(message => {
    if (message.dataset.workstreamUpdateId === workstream.workstream_id) message.remove();
  });
  const agent = workstreamAgent(workstream);
  const assignment = (workstream.assignments || []).find(item => item.status === "active")
    || (workstream.assignments || [])[0];
  const title = String(workstream.title || "מעקב").trim();
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
    value => `<p class="workstream-message-meta">אחריות: ${escapeHtml(value)}</p>`
  );
  const message = workstreamMessage(`
    <p class="workstream-message-title">עדכון מעקב — ${escapeHtml(title)}</p>
    ${objectiveHtml}
    ${responsibilityHtml}
    ${workstreamArtifactHtml(workstream)}
    <div class="workstream-message-actions">
      ${workstreamHasPresentation(workstream) ? `<button type="button" class="final-answer-show-btn layers-hidden" data-workstream-results="${escapeHtml(workstream.workstream_id)}" data-source-id="${escapeHtml(workstreamResultSourceId(workstream.workstream_id))}" title="הצג תוצאות" aria-label="הצג תוצאות" aria-pressed="false"><span class="final-answer-show-label">הצג תוצאות</span></button>` : ""}
      <button type="button" class="danger-button" data-workstream-archive="${escapeHtml(workstream.workstream_id)}">העברה לארכיון</button>
    </div>`, {
      label: agent ? `${agent.display_name} · עדכון מעקב` : "עדכון מעקב",
      memberId: agent?.participant_id,
    });
  message.dataset.workstreamUpdateId = workstream.workstream_id;
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
    workstreamMessage(`<p>לא הצלחתי לטעון את עדכון המעקב.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`);
  }
}

async function archiveWorkstreamFromChat(workstreamId) {
  try {
    const response = await fetch(`/api/workstreams/${encodeURIComponent(workstreamId)}/archive`, { method: "POST" });
    const archived = await response.json();
    if (!response.ok) throw new Error(archived.error || "העברת המעקב לארכיון נכשלה");
    state.workstreams = state.workstreams.map(item => item.workstream_id === workstreamId ? archived : item);
    renderWorkstreamIndicator();
    workstreamMessage(`<p>המעקב <strong>${escapeHtml(archived.title || "")}</strong> הועבר לארכיון.</p>`);
  } catch (error) {
    workstreamMessage(`<p>לא הצלחתי להעביר את המעקב לארכיון.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`);
  }
}

function startAssistantResearchMessage(message = "") {
  const shouldFollow = conversationIsNearBottom();
  const article = document.createElement("article");
  article.className = "message assistant-message";
  article.innerHTML = `
    <div class="message-label">${escapeHtml(assistantMessageLabel())}</div>
    <section class="research-process research-process-live">
      <h3>תהליך המחקר</h3>
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
    const finalId = finalSourceId(options.result);
    const hasRequestedResults = buildTypedResultLayers(options.result).length > 0;
    actions.innerHTML = `
      ${hasRequestedResults ? `<button type="button" class="final-answer-show-btn layers-hidden" data-source-id="${escapeHtml(finalId)}" title="הצג תוצאות" aria-label="הצג תוצאות" aria-pressed="false">
        <span class="final-answer-show-label">הצג תוצאות</span>
      </button>` : ""}
      <button type="button" class="final-answer-save-btn" ${options.result.saved_question_id ? "disabled" : ""}>${options.result.saved_question_id ? "נשמר" : "שמור הקלטה"}</button>
      <button type="button" class="final-answer-memory-btn" ${options.result.investigation_memory_summary_id ? "disabled" : ""}>${options.result.investigation_memory_summary_id ? "נשמר בזיכרון" : "שמור לזיכרון"}</button>
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
  classify_question_intent: "סיווג כוונת השאלה",
  resolve_location: "הבנת המקום",
  resolve_event_reference: "זיהוי אירוע העוגן",
  search_events: "חיפוש ממוקד במאגר",
  semantic_search_events: "חיפוש סמנטי במאגר",
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
  challenge_hypothesis: "בדיקת ההשערה מול חלופות",
  prepare_target_candidate: "הכנת מועמד מטרה",
  find_duplicate_target_candidates: "בדיקת כפילות מטרה",
  search_target_candidates: "חיפוש מועמדי מטרות",
  get_target_candidate: "שליפת מועמד מטרה",
  create_target_candidate: "יצירת מועמד מטרה",
  update_target_candidate: "עדכון מועמד מטרה",
  attach_target_evidence: "צירוף ראיות למטרה"
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
  stepInjectTitle.textContent = `צעד ${stepNumber}: ${stepLabel}`;
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
      <span class="step-inject-layer-count">${itemsForLayerPresentation(layer).length.toLocaleString("he-IL")}</span>
    </label>`).join("");

  stepInjectSubmit.disabled = false;
  stepInjectSubmit.textContent = "שלח להמשך חקירה";
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
  const lines = [`הוראה מהמשתמש: ${instruction}`];
  if (classificationContext?.summary) {
    lines.push(
      "\nמסגרת החקירה המקורית לשימור:",
      classificationContext.summary,
      "אין לסווג מחדש את השאלה. המשך לפי אותו recommended_mode ואותו tool_budget שנקבעו בסיווג המקורי."
    );
  }
  if (selectedLayers.length) {
    lines.push("\nשכבות שנבחרו להמשך:");
    selectedLayers.forEach(layer => {
      const items = itemsForLayerPresentation(layer);
      const eventIds = items.map(item => item.event_id).filter(Boolean).slice(0, 100);
      lines.push(`- ${layer.label}: ${items.length} רשומות${eventIds.length ? `, מזהים: ${eventIds.join(", ")}` : ""}`);
    });
  }
  return lines.join("\n");
}

async function submitStepInject() {
  const instruction = stepInjectPrompt.value.trim();
  if (!instruction) {
    stepInjectError.textContent = "יש להזין הוראה לסוכן.";
    stepInjectError.hidden = false;
    return;
  }
  if (state.busy) {
    stepInjectError.textContent = "חקירה כבר פעילה — המתן לסיומה.";
    stepInjectError.hidden = false;
    return;
  }

  const checkedIds = new Set(
    [...stepInjectLayers.querySelectorAll("input[type=checkbox]:checked")].map(cb => cb.value)
  );
  const selectedLayers = state.layers.filter(l => checkedIds.has(l.id));

  stepInjectSubmit.disabled = true;
  stepInjectSubmit.textContent = "שולח...";
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
            sourceLabel: `צעד ${num}: ${humanToolLabel(step.tool)}`
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
        is_continuation: true
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
    addActivity("connection_error", "לא ניתן היה להשלים את המשך החקירה.", error.message);
    finalizeAssistantMessage(`<p>לא הצלחתי להשלים את המשך החקירה.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`, { html: true });
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
  const label = btn.querySelector(".step-visibility-label, .final-answer-show-label");
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
        <button type="button" class="step-continue-btn" title="המשך מצעד זה">המשך מכאן</button>
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
    const continueBtn = item.querySelector(".step-continue-btn");
    continueBtn.addEventListener("click", () => openStepInjectModal(label, stepNumber));
  }
  state.activeActivityList.appendChild(item);
  followConversationAfterUpdate(shouldFollow);
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
      return `<details class="evidence-ids-toggle"><summary>מזהי ראיות</summary><p>${evidenceMatch[1].replace(/\n/g, "<br>")}</p></details>`;
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
  const shouldFollow = conversationIsNearBottom();
  ensureAssistantResearchMessage();
  state.activeActivityList.innerHTML = "";
  const internalWorkstreamTools = new Set([
    "prepare_workstream_creation",
    "prepare_workstream_indication_proposal",
    "decide_workstream_indication_proposal"
  ]);
  (steps || []).filter(step => !internalWorkstreamTools.has(step.tool)).forEach((step, index) => {
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
      sourceLabel: `צעד ${number}: ${humanToolLabel(step.tool)}`
    });
  });
  followConversationAfterUpdate(shouldFollow);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
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
  if (!value) return "זמן שמירה לא ידוע";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString("he-IL", {
    dateStyle: "short",
    timeStyle: "short",
  });
}

async function saveResultQuestion(result, prompt, button) {
  if (!canSaveResult(result, prompt) || state.busy || button?.disabled) return;
  button.disabled = true;
  button.textContent = "שומר...";
  button.title = "שומר את תוצאת החקירה";
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
    if (!response.ok) throw new Error(payload.error || "שמירת השאלה נכשלה");
    result.saved_question_id = payload.id;
    if (state.lastResult === result) state.lastResult = result;
    button.textContent = "נשמר";
    button.title = "תוצאת החקירה נשמרה";
    if (!recordedModal.hidden) loadRecordedQuestions();
  } catch (error) {
    const message = error.name === "AbortError" ? "שמירת השאלה נמשכה יותר מדי זמן. נסה שוב." : error.message;
    button.textContent = "נכשל";
    button.title = message;
    setTimeout(() => {
      if (!result.saved_question_id) {
        button.disabled = false;
        button.textContent = "שמור הקלטה";
        button.title = "שמור את הקלטת החקירה";
      }
    }, 2500);
  } finally {
    clearTimeout(timeout);
  }
}

async function saveResultToInvestigationMemory(result, prompt, button) {
  if (!canSaveResultToMemory(result, prompt) || state.busy || button?.disabled) return;
  button.disabled = true;
  button.textContent = "שומר לזיכרון...";
  button.title = "שומר את הממצא לזיכרון החקירה";
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
    if (!response.ok) throw new Error(payload.error || "שמירה לזיכרון החקירה נכשלה");
    result.investigation_memory_summary_id = payload.saved?.id || true;
    if (state.lastResult === result) state.lastResult = result;
    button.textContent = "נשמר בזיכרון";
    button.title = "הממצא נשמר לזיכרון החקירה";
  } catch (error) {
    const message = error.name === "AbortError" ? "שמירה לזיכרון נמשכה יותר מדי זמן. נסה שוב." : error.message;
    button.textContent = "נכשל";
    button.title = message;
    setTimeout(() => {
      if (!result.investigation_memory_summary_id) {
        button.disabled = false;
        button.textContent = "שמור לזיכרון";
        button.title = "שמור את הממצא לזיכרון החקירה";
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
    if (!response.ok) throw new Error(payload.error || "מחיקת השאלה נכשלה");
    state.savedQuestions = state.savedQuestions.filter(item => item.id !== savedId);
    loadRecordedQuestions();
  } catch (error) {
    recordedList.innerHTML = `<div class="activity-empty">מחיקת השאלה השמורה נכשלה: ${escapeHtml(error.message)}</div>`;
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
    state.queryContext = buildFinalQueryContext(result, prompt);
    const typedLayers = buildTypedResultLayers(result);
    const requestedView = typedLayers[0]?.preferredView || result.recommended_view || "map";
    const addedLayers = addResultLayers({
      sourceId: finalSourceId(result),
      sourceLabel: result.responding_agent === "moshe" ? "תשובת משה" : "תשובת הסוכן",
      preferredView: requestedView,
      layers: typedLayers
    });
    showResult(
      "ממצאי הסוכן",
      addedLayers.length
        ? `נוספו או הוצגו ${addedLayers.length.toLocaleString("he-IL")} שכבות שנבחרו כתשובה.`
        : "לא נבחרו נתונים להצגה."
    );
    activateView(requestedView, { reason: result.view_reason || "נתונים שנבחרו כתשובה לבקשת המשתמש" });
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
  if (buildTypedResultLayers(result).some(layer => layer.kind === "attack_targets")) {
    void refreshOpenAttackTargetCatalogLayer();
  }
  updateResultVisibilityButtons();
  renderQueryInspector();
  setSuggestions(["אילו הסברים תמימים יכולים להתאים לאותן ראיות?", "מה חסר כדי להעלות את רמת הביטחון?", "הצג את רצף האירועים לפי סדר הזמן"]);
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
    if (!response.ok) throw new Error(saved.error || "טעינת השאלה השמורה נכשלה");
    const result = {
      ...(saved.result || {}),
      saved_question_id: saved.id,
      source_run_id: saved.source_run_id || saved.result?.run_id,
    };
    const prompt = (saved.question || "").trim();
    appendMessage("user", `<p>${highlightedPromptHtml(prompt)}</p>`);
    state.history.push({ role: "user", content: prompt }, { role: "assistant", content: result.answer || "" });
    applyAgentResult(result, prompt);
  } catch (error) {
    startAssistantResearchMessage("טעינת שאלה שמורה נכשלה.");
    finalizeAssistantMessage(`<p>לא הצלחתי להציג את השאלה השמורה.</p><div class="answer-callout">${escapeHtml(error.message)}</div>`, { html: true });
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
    queryLayersError.textContent = "יש לבחור לפחות שכבה אחת.";
    queryLayersError.hidden = false;
    return;
  }
  if (state.workstreamComposerMode && selectedLayers.length !== 1) {
    queryLayersError.textContent = "יש לבחור שכבה אחת למעקב.";
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

async function runPrompt(prompt, options = {}) {
  const clean = prompt.trim();
  if (!clean || state.busy) return;
  const workstreamCreationRequested = options.workstreamCreation === true;
  const addressedPrompt = addressedPromptForSelectedMember(clean);
  const selectedLayers = selectedLayerContextForAgent();
  state.activeTeamMentions = teamMentionsForPrompt(addressedPrompt);
  const workstreamInstruction = workstreamCreationRequested
    ? "המשתמש נמצא בזרימת יצירת מעקב. נהל שיחה טבעית: אם חסר מידע חיוני שאל שאלה קצרה; כאשר המטרה והאחריות ברורות, השתמש בכלי יצירת המעקב."
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
        workstream_creation_requested: workstreamCreationRequested
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
    await applyMemoryLayerActions(result);
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
      ? `${visibleEvents} אירועים`
      : (visibleTimeGroups ? `${visibleTimeGroups} נקודות זמן` : `${visibleLocationLayers} מיקומים`);
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

function setChatPanelCollapsed(collapsed) {
  state.chatPanelCollapsed = Boolean(collapsed);
  workspace.classList.toggle("chat-panel-collapsed", state.chatPanelCollapsed);
  if (chatPanelToggle) {
    const label = state.chatPanelCollapsed ? "הצג שיחה" : "מזער שיחה";
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
      element.setAttribute("aria-label", `מועמד מטרה: ${target.title || target.target_id}, ${target.location_name || target.location_id}`);
      element.innerHTML = '<span class="map-marker-dot"></span>';
      const popupHtml = `<div class="map-popup target-map-popup" dir="rtl">
        <strong>${escapeHtml(String(target.title || target.target_id || "מועמד מטרה"))}</strong>
        <span>${escapeHtml(String(target.object_class || "-"))} · ${escapeHtml(String(target.entity_name || target.entity_id || "ללא ישות"))}</span>
        <span>ביטחון ${escapeHtml(String(confidenceLabel(target.confidence)))} · כמות ${escapeHtml(String(targetQuantityLabel(target)))}</span>
        <p>${escapeHtml(String(target.summary || ""))}</p>
        <span class="target-raw-references"><b>אסמכתאות גולמיות:</b> ${(target.raw_data_references || []).length
          ? (target.raw_data_references || []).map(recordId => `<code dir="ltr">${escapeHtml(String(recordId || "-"))}</code>`).join(" · ")
          : "לא נטענו אסמכתאות בתוצאה זו"}</span>
      </div>`;
      const popup = new maplibregl.Popup({ offset: 20, closeButton: true, closeOnClick: true }).setHTML(popupHtml);
      const marker = new maplibregl.Marker({ element, anchor: "center" }).setLngLat([markerLon, markerLat]).setPopup(popup).addTo(state.map);
      state.markers.push(marker);
      bounds.extend([markerLon, markerLat]);
    });
  });
  if (!bounds.isEmpty()) state.map.fitBounds(bounds, { padding: 110, maxZoom: 10.2, duration: 450 });
}

function renderTimeline() {
  const timeline = document.getElementById("timeline");
  const eventTimelineItems = visibleLayers("timeline")
    .filter(layer => layer.kind === "events")
    .flatMap(layer => itemsForLayerPresentation(layer).map(event => ({ type: "event", layer, event, sort: event.date })));
  const aggregateTimelineItems = visibleLayers("timeline")
    .filter(layer => layer.kind === "time_aggregation")
    .flatMap(layer => itemsForLayerPresentation(layer).map(item => ({ type: "aggregation", layer, item, sort: item.sortKey })));
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
    noMatch.innerHTML = `<td colspan="${head.querySelectorAll("th").length}" class="empty-cell">לא נמצאו תוצאות התואמות למסננים.</td>`;
    body.appendChild(noMatch);
  }
}

function enhanceResultsTable(layer) {
  const head = document.getElementById("evidenceHead");
  if (!head || !layer) return;
  const control = resultTableControl(layer.id);
  [...head.querySelectorAll("th")].forEach((cell, column) => {
    const label = normalizedTableCellText(cell.textContent);
    const activeSort = control.sortColumn === column;
    const filterValue = String(control.filters[column] || "");
    const filterOpen = control.openFilterColumn === column;
    const directionLabel = activeSort
      ? (control.sortDirection === "asc" ? "ממוין בסדר עולה" : "ממוין בסדר יורד")
      : "לא ממוין";
    cell.setAttribute("aria-sort", activeSort ? (control.sortDirection === "asc" ? "ascending" : "descending") : "none");
    cell.innerHTML = `
      <div class="result-column-header">
        <button type="button" class="result-column-sort" data-result-sort="${column}" data-result-layer="${escapeHtml(String(layer.id))}" title="מיון לפי ${escapeHtml(label)}. ${directionLabel}">
          <span>${escapeHtml(label)}</span>
          <span class="material-symbols-rounded" aria-hidden="true">${activeSort ? (control.sortDirection === "asc" ? "arrow_upward" : "arrow_downward") : "unfold_more"}</span>
        </button>
        <button type="button" class="result-column-filter-toggle ${filterValue ? "active" : ""}" data-result-filter-toggle="${column}" data-result-layer="${escapeHtml(String(layer.id))}" title="סינון לפי ${escapeHtml(label)}" aria-label="סינון לפי ${escapeHtml(label)}" aria-expanded="${filterOpen ? "true" : "false"}">
          <span class="material-symbols-rounded" aria-hidden="true">filter_alt</span>
        </button>
      </div>
      ${filterOpen ? `
        <div class="result-column-filter-popover">
          <input type="search" class="result-column-filter" data-result-filter="${column}" data-result-layer="${escapeHtml(String(layer.id))}" value="${escapeHtml(filterValue)}" placeholder="סינון ${escapeHtml(label)}" aria-label="סינון ${escapeHtml(label)}">
          ${filterValue ? `<button type="button" class="result-column-filter-clear" data-result-filter-clear="${column}" data-result-layer="${escapeHtml(String(layer.id))}" title="נקה סינון" aria-label="נקה סינון"><span class="material-symbols-rounded" aria-hidden="true">close</span></button>` : ""}
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
    minimizeButton.title = state.rawOverlayMinimized ? "הגדל" : "מזער";
    minimizeButton.setAttribute("aria-label", state.rawOverlayMinimized ? "הגדל טבלת תוצאות" : "מזער טבלת תוצאות");
  }
  tabs.innerHTML = tableLayers.map(layer => {
    const filteredCount = itemsForLayerPresentation(layer).length;
    const originalCount = (layer.items || []).length;
    const countLabel = layerHasAppliedFilters(layer)
      ? `${filteredCount.toLocaleString("he-IL")}/${originalCount.toLocaleString("he-IL")}`
      : originalCount.toLocaleString("he-IL");
    return `
    <button type="button" class="raw-source-tab ${layer.id === activeLayer?.id ? "active" : ""} ${layer.visible ? "" : "hidden-source"}" style="${layerColorStyle(layer)}" data-layer-id="${escapeHtml(layer.id)}" role="tab" aria-selected="${layer.id === activeLayer?.id}" title="${escapeHtml(layer.sourceLabel || layer.label)}">
      <span class="raw-source-color"></span>
      <span class="raw-source-name">${escapeHtml(layer.label)}</span>
      <strong>${countLabel}</strong>
      <span class="raw-source-filter ${layer.filterPanelOpen ? "active" : ""} ${validAppliedFilters(layer).length ? "has-filters" : ""}" data-layer-filter="${escapeHtml(layer.id)}" title="פתח מסננים" aria-label="פתח מסננים" aria-pressed="${layer.filterPanelOpen ? "true" : "false"}">
        <span class="filter-funnel-icon" aria-hidden="true"></span>
      </span>
      <span class="raw-source-memory ${layer.investigation_memory_layer_id ? "saved" : ""}" data-layer-memory="${escapeHtml(layer.id)}" title="${layer.investigation_memory_layer_id ? "השכבה נשמרה לזיכרון החקירה" : "שמור שכבה לזיכרון החקירה"}" aria-label="${layer.investigation_memory_layer_id ? "השכבה נשמרה לזיכרון החקירה" : "שמור שכבה לזיכרון החקירה"}" aria-pressed="${layer.investigation_memory_layer_id ? "true" : "false"}">
        <span class="memory-bookmark-icon" aria-hidden="true"></span>
      </span>
        <span class="raw-source-eye" data-layer-visibility="${escapeHtml(layer.id)}" title="${layer.visible ? "הסתר שכבה" : "הצג שכבה"}" aria-label="${layer.visible ? "הסתר שכבה" : "הצג שכבה"}" aria-pressed="${layer.visible ? "true" : "false"}">
          <span class="visibility-eye-icon ${layer.visible ? "" : "off"}" aria-hidden="true"></span>
        </span>
      <span class="raw-source-close" data-layer-close="${escapeHtml(layer.id)}" title="סגור שכבה" aria-label="סגור שכבה">×</span>
    </button>`;
  }).join("");

  if (!activeLayer) return;
  ensureLayerFilterState(activeLayer);
  renderLayerFilterPanel(activeLayer);
  const activeItems = activeLayer.visible ? itemsForLayerPresentation(activeLayer) : [];
  if (activeLayer.kind === "attack_targets") {
    head.innerHTML = "<tr><th>מטרה</th><th>סוג אובייקט</th><th>ישות</th><th>מיקום קנוני</th><th>ביטחון</th><th>כמות</th><th>תקציר</th><th>סוגי מקור</th><th>רשומות גולמיות</th></tr>";
    body.innerHTML = activeItems.length ? activeItems.map(item => `
      <tr class="attack-target-row">
        <td><strong>${escapeHtml(String(item.title || item.target_id || "-"))}</strong><small dir="ltr">${escapeHtml(String(item.target_id || "-"))}</small></td>
        <td>${escapeHtml(String(item.object_class || "-"))}</td>
        <td>${escapeHtml(String(item.entity_name || item.entity_id || "-"))}</td>
        <td>${escapeHtml(String(item.location_name || item.location_id || "-"))}</td>
        <td>${escapeHtml(String(confidenceLabel(item.confidence)))}</td>
        <td>${escapeHtml(String(targetQuantityLabel(item)))}</td>
        <td>${escapeHtml(String(item.summary || "-"))}</td>
        <td>${(item.source_types || []).length ? (item.source_types || []).map(sourceType => `<span class="target-source-type">${escapeHtml(String(sourceType))}</span>`).join("<br>") : "-"}</td>
        <td><strong>${Number(item.evidence_count || (item.raw_data_references || []).length || 0).toLocaleString("he-IL")}</strong></td>
      </tr>`).join("") : '<tr><td colspan="9" class="empty-cell">לא נמצאו מועמדי מטרות להצגה.</td></tr>';
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "location_metadata") {
    head.innerHTML = "<tr><th>מיקום</th><th>אירועים</th><th>רשות</th><th>סוג</th><th>דיוק</th><th>מזהה</th></tr>";
    body.innerHTML = activeItems.length ? activeItems.map(item => `
      <tr>
        <td>${escapeHtml(item.location_name || item.name || item.location_id || "-")}</td>
        <td>${Number(item.event_count || item.count || 0).toLocaleString("he-IL")}</td>
        <td>${escapeHtml(item.municipality || "-")}</td>
        <td>${escapeHtml(item.type || "-")}</td>
        <td>${escapeHtml(item.precision || "-")}</td>
        <td dir="ltr">${escapeHtml(item.location_id || "-")}</td>
      </tr>`).join("") : '<tr><td colspan="6" class="empty-cell">השכבה מוסתרת או ריקה.</td></tr>';
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "entity_metadata") {
    head.innerHTML = "<tr><th>ישות</th><th>אירועים</th><th>סוג</th><th>ערכי actor</th><th>מוקדים מובילים</th><th>מזהה</th></tr>";
    body.innerHTML = activeItems.length ? activeItems.map(item => {
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
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "locations") {
    head.innerHTML = "<tr><th>מיקום</th><th>כמות</th><th>מזהה</th><th>סוג שכבה</th></tr>";
    body.innerHTML = activeItems.length ? activeItems.map(item => `
      <tr>
        <td>${escapeHtml(item.location_name || item.label || item.key || item.location_id || "-")}</td>
        <td>${Number(item.count || 0).toLocaleString("he-IL")}</td>
        <td dir="ltr">${escapeHtml(item.location_id || item.key || "-")}</td>
        <td>${escapeHtml(activeLayer.label)}</td>
      </tr>`).join("") : '<tr><td colspan="4" class="empty-cell">השכבה מוסתרת או ריקה.</td></tr>';
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "time_aggregation") {
    head.innerHTML = "<tr><th>זמן</th><th>כמות</th><th>סוג קיבוץ</th><th>תקציר</th></tr>";
    body.innerHTML = activeItems.length ? activeItems.map(item => `
      <tr>
        <td>${escapeHtml(item.timeLabel || item.label || "-")}</td>
        <td>${Number(item.count || 0).toLocaleString("he-IL")}</td>
        <td>${escapeHtml(item.group_by === "hour" ? "שעה" : "תאריך")}</td>
        <td>${escapeHtml(item.summary || "-")}</td>
      </tr>`).join("") : '<tr><td colspan="4" class="empty-cell">השכבה מוסתרת או ריקה.</td></tr>';
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "group_aggregation") {
    head.innerHTML = "<tr><th>קבוצה</th><th>כמות</th><th>סוג קיבוץ</th><th>אירוע ראשון</th><th>אירוע אחרון</th></tr>";
    body.innerHTML = activeItems.length ? activeItems.map(item => `
      <tr>
        <td>${escapeHtml(item.label || item.key || "-")}</td>
        <td>${Number(item.count || 0).toLocaleString("he-IL")}</td>
        <td>${escapeHtml(item.group_by || "-")}</td>
        <td dir="ltr">${escapeHtml(item.first_event_id || item.first_event_time || "-")}</td>
        <td dir="ltr">${escapeHtml(item.last_event_id || item.last_event_time || "-")}</td>
      </tr>`).join("") : '<tr><td colspan="5" class="empty-cell">השכבה מוסתרת או ריקה.</td></tr>';
    enhanceResultsTable(activeLayer);
    return;
  }
  head.innerHTML = "<tr><th>מזהה רשומה</th><th>זמן</th><th>אמינות</th><th>ודאות</th><th>גורם</th><th>מיקום</th><th>תקציר</th></tr>";
  body.innerHTML = activeItems.length ? activeItems.map(event => `
    <tr>
      <td dir="ltr">${escapeHtml(event.record_id || event.event_id || "-")}</td>
      <td dir="ltr">${escapeHtml(event.timestamp_utc)}</td>
      <td>${escapeHtml(event.source_reliability_label || event.source_reliability || "-")}</td>
      <td>${escapeHtml(event.certainty_level || "-")}</td>
      <td>${escapeHtml(event.entity_name || event.entity_id || "-")}</td>
      <td>${escapeHtml(event.location_name || "-")}</td>
      <td>${escapeHtml(event.event_summary || "-")}</td>
    </tr>`).join("") : '<tr><td colspan="7" class="empty-cell">השכבה מוסתרת או ריקה.</td></tr>';
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
  state.history = [];
  state.workstreamLoadToken += 1;
  state.workstreams = [];
  state.workstreamsLoading = false;
  state.investigationPlayback = null;
  state.pendingMosheWorkstreamProposal = null;
  state.workstreamComposerMode = false;
  if (!options.keepInvestigation) {
    const investigation = ensureInvestigationRecord(DEFAULT_INVESTIGATION_NAME);
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
  conversation.innerHTML = '<article class="message assistant-message"><div class="message-label">סוכן חקירה</div><p>אפשר להתחיל בשאלה פתוחה. אשתמש בכלי החיפוש, הזמן והמפה כדי לבנות תשובה שניתן לבדוק מול האירועים הגולמיים.</p></article>';
  updatePromptPlaceholder();
  if (resultTitle) resultTitle.textContent = "טרם בוצעה חקירה";
  if (resultSubtitle) resultSubtitle.textContent = "תוצאות, המחשות וראיות יופיעו כאן לאחר השאלה הראשונה.";
  if (resultCount) resultCount.textContent = "0 אירועים";
  activateView("map");
  setSuggestions(["אילו דיווחים על חסימות הופיעו ראשונים?", "האם הטענה על חציית גבול מגובה במקור אמין?", "איפה יש ריכוזי דיווחים מרכזיים?"]);
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
  const workstreamResults = event.target.closest("[data-workstream-results]");
  if (workstreamResults) {
    void toggleWorkstreamResultVisibility(
      workstreamResults.dataset.workstreamResults,
      workstreamResults
    );
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
intelligenceModeSelect?.addEventListener("change", changeIntelligenceMode);
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
updatePromptPlaceholder();
enableMentionHighlight(promptInput);
enableMentionHighlight(stepInjectPrompt);
attachTeamMentionAutocomplete(promptInput);
attachTeamMentionAutocomplete(stepInjectPrompt);
initPanelResizers();
loadInvestigationRegistry();
loadWorkstreamSeenState();
renderInvestigationSelector();

async function boot() {
  initMap();
  await hydrateInvestigationRegistry();
  await loadLayerCatalog();
  await loadWorkstreams();
  await loadInvestigationMemory({ restoreLayers: true });
  let runtimeStatus = null;
  try {
    runtimeStatus = await fetch("/api/status", { cache: "no-store" }).then(response => response.json());
    state.datasetVersion = runtimeStatus.dataset_version || "";
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
    }
    const datasetUrl = runtimeStatus.dataset_url || "./data/serbia_kosovo_events_projection.csv";
    const response = await fetch(datasetUrl, { cache: "no-store" });
    if (!response.ok) throw new Error("dataset unavailable");
    state.events = parseCsv(await response.text()).map(enrich);
    const versionLabel = runtimeStatus.dataset_version ? ` · ${runtimeStatus.dataset_version.toUpperCase()}` : "";
    document.getElementById("datasetStatus").textContent = `${state.events.length.toLocaleString("he-IL")} אירועים זמינים במאגר${versionLabel}`;
    document.querySelector(".status-dot").classList.add("ready");
  } catch (error) {
    document.getElementById("datasetStatus").textContent = "טעינת הנתונים נכשלה";
  }
  try {
    const status = runtimeStatus || await fetch("/api/status", { cache: "no-store" }).then(response => response.json());
    if (!status.configured) throw new Error("not configured");
    agentStatus.textContent = "Hermes + MCP מחוברים";
    agentStatus.className = "agent-live";
  } catch (error) {
    agentStatus.textContent = "מצב הדגמה מקומי";
    agentStatus.className = "agent-error";
  }
}

boot();
