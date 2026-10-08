const demoRuntime = window.DEMO_RUNTIME || null;
const scenarioStorage = window.DEMO_STORAGE || localStorage;
﻿const LOCATIONS = {
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

const MIL_STD_VERSION = "MIL-STD-2525E Change 1";
const MIL_STD_ORGANIZATIONS = Object.freeze({
  "ENT-SAF-2BRIGADE": { affiliation: "friendly", icon: "II" },
  "ENT-SAF-21-INF": { affiliation: "friendly", icon: "●" },
  "ENT-SAF-22-INF": { affiliation: "friendly", icon: "●" },
  "ENT-SAF-27-MECH": { affiliation: "friendly", icon: "↗" },
  "ENT-SAF-28-MECH": { affiliation: "friendly", icon: "↗" },
  "ENT-SAF-210-ENG": { affiliation: "friendly", icon: "E" },
  "ENT-SAF-3BRIGADE": { affiliation: "friendly", icon: "II" },
  "ENT-KFOR-RCE": { affiliation: "hostile", icon: "HQ" },
  "ENT-KFOR-KTRBN": { affiliation: "hostile", icon: "●" },
  "ENT-KFOR-MSU": { affiliation: "hostile", icon: "●" },
  "ENT-KFOR-AVIATION": { affiliation: "hostile", icon: "✈" },
  "ENT-NATO-RESERVE": { affiliation: "hostile", icon: "●" }
});
const MIL_STD_UAV_OBJECTS = Object.freeze({
  "רכב משוריין": { code: "armored-vehicle", icon: "▰", he: "רכב משוריין", en: "Armored vehicle" },
  "Armored vehicle": { code: "armored-vehicle", icon: "▰", he: "רכב משוריין", en: "Armored vehicle" },
  "משאית לוגיסטית": { code: "logistics-truck", icon: "▱", he: "משאית לוגיסטית", en: "Logistics truck" },
  "Logistics truck": { code: "logistics-truck", icon: "▱", he: "משאית לוגיסטית", en: "Logistics truck" },
  "שיירת כלי רכב": { code: "vehicle-convoy", icon: "•••", he: "שיירת כלי רכב", en: "Vehicle convoy" },
  "Vehicle convoy": { code: "vehicle-convoy", icon: "•••", he: "שיירת כלי רכב", en: "Vehicle convoy" },
  "מסוק": { code: "helicopter", icon: "⌁", he: "מסוק", en: "Helicopter" },
  "Helicopter": { code: "helicopter", icon: "⌁", he: "מסוק", en: "Helicopter" }
});

function milStdConfidence(value) {
  const normalized = String(value || "").trim().toLowerCase();
  if (["גבוהה", "high", "confirmed"].includes(normalized)) return "high";
  if (["בינונית", "medium", "likely"].includes(normalized)) return "medium";
  return "low";
}

function milStdClaimLabel(status) {
  if (status === "observed") return activeLocaleText("נצפה", "Observed");
  if (status === "assessed") return activeLocaleText("מוערך", "Assessed");
  return activeLocaleText("מדווח", "Reported");
}

function milStdOrganizationDescriptors(layer) {
  return (itemsForLayerPresentation(layer) || []).flatMap(entity => {
    const mapping = MIL_STD_ORGANIZATIONS[entity.entity_id];
    if (!mapping) return [];
    return (entity.top_locations || []).filter(location => location.presence_claim !== false).map(location => ({
      kind: "organization",
      id: entity.entity_id,
      name: entity.canonical_name || entity.entity_id,
      locationId: location.location_id,
      longitude: location.longitude,
      latitude: location.latitude,
      count: Number(location.presence_evidence_count || location.count || 0),
      evidenceIds: location.evidence_record_ids || [],
      latestTimestamp: location.latest_timestamp_utc || "",
      status: location.assessment_status || "reported",
      confidence: milStdConfidence(location.confidence || entity.confidence),
      affiliation: mapping.affiliation,
      icon: mapping.icon,
      symbolCode: `organization:${entity.entity_id}`
    }));
  });
}

function milStdObservationDescriptor(event) {
  if (event.collection_family !== "airborne_isr_video_exploitation") return null;
  const mapping = MIL_STD_UAV_OBJECTS[event.object_class || event.observed_object_class];
  if (!mapping || !event.location_id) return null;
  const entityAffiliation = MIL_STD_ORGANIZATIONS[event.entity_id]?.affiliation || "unknown";
  return {
    kind: "record",
    id: event.record_id || event.event_id,
    name: activeLocaleText(mapping.he, mapping.en),
    locationId: event.location_id,
    count: Number(event.estimated_object_count || 1),
    evidenceIds: [event.record_id || event.event_id].filter(Boolean),
    latestTimestamp: event.timestamp_utc || "",
    status: "observed",
    confidence: milStdConfidence(event.identification_confidence || event.certainty_level),
    affiliation: entityAffiliation,
    icon: mapping.icon,
    symbolCode: `observation:${mapping.code}`
  };
}

function milStdEntityEventDescriptor(event) {
  const mapping = MIL_STD_ORGANIZATIONS[event.entity_id];
  if (!mapping || !event.location_id) return null;
  return {
    kind: "record",
    id: event.record_id || event.event_id,
    name: event.entity_name || event.entity_id,
    locationId: event.location_id,
    count: 1,
    evidenceIds: [event.record_id || event.event_id].filter(Boolean),
    latestTimestamp: event.timestamp_utc || "",
    status: "reported",
    confidence: milStdConfidence(event.certainty_level),
    affiliation: mapping.affiliation,
    icon: mapping.icon,
    symbolCode: `organization-report:${event.entity_id}`
  };
}

function milStdEventDescriptor(event) {
  return milStdObservationDescriptor(event) || milStdEntityEventDescriptor(event);
}

function milStdEvidenceDescriptor(evidence) {
  const locationId = (evidence.location_ids || [])[0];
  if (!locationId) return null;
  const entityId = (evidence.subject_entity_ids || [])[0];
  const object = MIL_STD_UAV_OBJECTS[evidence.object_class];
  const organization = MIL_STD_ORGANIZATIONS[entityId];
  return {
    kind: "evidence",
    id: evidence.evidence_id,
    name: object ? activeLocaleText(object.he, object.en) : (entityId || activeLocaleText("ראיה", "Evidence")),
    locationId,
    count: Number(evidence.quantity?.estimate || evidence.source_record_ids?.length || 1),
    evidenceIds: evidence.source_record_ids || [],
    latestTimestamp: evidence.valid_to || evidence.valid_from || "",
    status: evidence.evidence_status === "fused" ? "assessed" : evidence.evidence_status,
    confidence: milStdConfidence(evidence.confidence),
    affiliation: organization?.affiliation || "unknown",
    icon: object?.icon || organization?.icon || "E",
    symbolCode: `evidence:${evidence.claim_type || "claim"}`
  };
}

function coalesceEvidenceDescriptors(descriptors, maximum = 400) {
  const confidenceRank = { low: 1, medium: 2, high: 3 };
  const groups = new Map();
  const passthrough = [];
  descriptors.forEach(descriptor => {
    if (descriptor.kind !== "evidence") {
      passthrough.push(descriptor);
      return;
    }
    const key = [descriptor.locationId, descriptor.symbolCode, descriptor.icon, descriptor.affiliation].join("|");
    const current = groups.get(key);
    if (!current) {
      groups.set(key, { ...descriptor, evidenceIds: [...descriptor.evidenceIds], groupedObjects: 1 });
      return;
    }
    current.count += Number(descriptor.count || 0);
    current.groupedObjects += 1;
    current.viewerEligible = false;
    current.evidenceIds = [...new Set([...current.evidenceIds, ...descriptor.evidenceIds])].slice(0, 25);
    if (descriptor.status === "assessed") current.status = "assessed";
    if ((confidenceRank[descriptor.confidence] || 0) > (confidenceRank[current.confidence] || 0)) current.confidence = descriptor.confidence;
    if (String(descriptor.latestTimestamp || "") > String(current.latestTimestamp || "")) current.latestTimestamp = descriptor.latestTimestamp;
  });
  const evidence = [...groups.values()]
    .sort((left, right) => Number(right.status === "assessed") - Number(left.status === "assessed") || Number(right.count || 0) - Number(left.count || 0))
    .slice(0, maximum);
  return [...passthrough, ...evidence];
}

function milStdMarkerElement(descriptor) {
  const element = document.createElement("button");
  element.type = "button";
  element.className = `milstd-marker ${descriptor.affiliation} confidence-${descriptor.confidence} status-${descriptor.status}`;
  if (descriptor.viewerEligible !== false) {
    element.dataset.viewerKind = descriptor.kind;
    element.dataset.viewerId = descriptor.id;
    element.setAttribute("aria-haspopup", "dialog");
  }
  element.setAttribute("aria-label", `${descriptor.name}, ${milStdClaimLabel(descriptor.status)}, ${descriptor.count} ${activeLocaleText("רשומות", "records")}`);
  element.innerHTML = `<span class="milstd-frame"><span class="milstd-icon" aria-hidden="true">${escapeHtml(descriptor.icon)}</span></span><span class="milstd-status">${escapeHtml(milStdClaimLabel(descriptor.status))}</span>${descriptor.count > 1 ? `<span class="milstd-count">${descriptor.count.toLocaleString(currentLocaleTag())}</span>` : ""}`;
  return element;
}

function milStdPopupHtml(descriptor, locationName) {
  const evidence = descriptor.evidenceIds.length
    ? descriptor.evidenceIds.slice(0, 5).map(id => `<code dir="ltr">${escapeHtml(id)}</code>`).join(" · ")
    : escapeHtml(activeLocaleText("מזהי הראיות זמינים במציג הישות", "Evidence IDs are available in the entity viewer"));
  return `<div class="map-popup milstd-popup" dir="${currentLocale() === "en" ? "ltr" : "rtl"}">
    <span class="milstd-version">${MIL_STD_VERSION}</span>
    <strong>${escapeHtml(descriptor.name)}</strong>
    <span>${escapeHtml(milStdClaimLabel(descriptor.status))} · ${escapeHtml(locationName)} · ${escapeHtml(descriptor.confidence)}</span>
    ${descriptor.latestTimestamp ? `<time dir="ltr">${escapeHtml(descriptor.latestTimestamp)}</time>` : ""}
    <span><b>${escapeHtml(activeLocaleText("ראיות", "Evidence"))}:</b> ${evidence}</span>
    ${descriptor.viewerEligible === false ? "" : `<button type="button" class="object-viewer-open" data-viewer-kind="${descriptor.kind}" data-viewer-id="${escapeHtml(descriptor.id)}">${escapeHtml(activeLocaleText("פתח פרטים", "Open details"))}</button>`}
  </div>`;
}

function createInvestigationId() {
  const random = crypto?.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  return `investigation-${random}`;
}

// The investigation list lives on the server (GET/POST /api/investigations). The browser only
// remembers which investigation was active last; the old local registries are discarded.
const ACTIVE_INVESTIGATION_STORAGE_KEY = "serbia-poc-active-investigation-v1";
const LEGACY_INVESTIGATIONS_STORAGE_KEYS = ["serbia-poc-investigations-v1", "serbia-poc-investigations-v2", "serbia-poc-workstream-seen-v2"];

const MICHLOL_MEMBERS = {
  he: [
    { id: "naama-field-officer", displayName: "נעמה", roleLabel: "קצינת סיגינט", memberType: "user", workspaceRole: "sigint", avatar: "./assets/michlol/naama.png", initial: "נ" },
    { id: "gadi-collection-officer", displayName: "גדי", roleLabel: "קצין ויזינט", memberType: "user", workspaceRole: "visint", avatar: "./assets/michlol/gadi.png", initial: "ג" },
    { id: "moshe-targets-officer", displayName: "משה", roleLabel: "קצין מטרות", memberType: "user", avatar: "./assets/michlol/moshe.png", initial: "מ" },
    { id: "talia-tama-officer", displayName: "טליה", roleLabel: "קצינת תמא", memberType: "user", avatar: "./assets/michlol/talia.png", initial: "ט" },
    { id: "yahli-processing-officer", displayName: "יהלי", roleLabel: "קצין עיבוד", memberType: "user", avatar: "./assets/michlol/yahli.png", initial: "י" }
  ],
  en: [
    { id: "naama-field-officer", displayName: "Naama", roleLabel: "SIGINT Officer", memberType: "user", workspaceRole: "sigint", avatar: "./assets/michlol/naama.png", initial: "N" },
    { id: "gadi-collection-officer", displayName: "Gadi", roleLabel: "VISINT Officer", memberType: "user", workspaceRole: "visint", avatar: "./assets/michlol/gadi.png", initial: "G" },
    { id: "moshe-targets-officer", displayName: "Moshe", roleLabel: "Targets Officer", memberType: "user", avatar: "./assets/michlol/moshe.png", initial: "M" },
    { id: "talia-tama-officer", displayName: "Talia", roleLabel: "Enemy Assessment Officer", memberType: "user", avatar: "./assets/michlol/talia.png", initial: "T" },
    { id: "yahli-processing-officer", displayName: "Yahli", roleLabel: "Processing Officer", memberType: "user", avatar: "./assets/michlol/yahli.png", initial: "Y" }
  ]
};

const ROLE_WORKSPACES = {
  sigint: {
    allowedCatalogLayerIds: new Set([
      "events:ADINT",
      "events:IPDR",
      "events:Cellular Geolocations",
      "events:Cellular Calls"
    ]),
    defaultCatalogLayerId: "events:Cellular Calls",
    defaultView: "timeline",
    openDefaultCall: true
  },
  visint: {
    allowedCatalogLayerIds: new Set([
      "events:CCTV",
      "events:Satellite"
    ]),
    defaultCatalogLayerId: "events:Satellite",
    defaultView: "map",
    openDefaultCall: false
  }
};

// Catalog layer ids follow the dataset locale; the calls source has a Hebrew and an English id.
const CATALOG_LAYER_ALIASES = { "events:שיחות סלולר": "events:Cellular Calls" };

function canonicalCatalogLayerId(layerId) {
  const id = String(layerId || "");
  return CATALOG_LAYER_ALIASES[id] || id;
}

function resolveCatalogLayerId(layerId) {
  const canonical = canonicalCatalogLayerId(layerId);
  return state.layerCatalog.find(layer => layer.id === layerId)?.id
    || state.layerCatalog.find(layer => canonicalCatalogLayerId(layer.id) === canonical)?.id
    || layerId;
}

function normalizeLocale(value) {
  const locale = String(value || "").trim().toLowerCase();
  return locale === "en" ? "en" : "he";
}

// The app runs in English only; the Hebrew strings remain in the code but are no longer selectable.
const INITIAL_LOCALE = "en";

function currentLocale() {
  return state.locale === "en" ? "en" : "he";
}

function currentLocaleTag() {
  return currentLocale() === "en" ? "en-US" : "he-IL";
}

function currentMembers() {
  return MICHLOL_MEMBERS[currentLocale()];
}

function roleWorkspaceSelectionAvailable() {
  return state.pageView === "workspace" && !state.draftSessionActive;
}

function activeRoleWorkspaceProfile() {
  return ROLE_WORKSPACES[state.activeRoleWorkspace] || null;
}

function roleWorkspaceAllowsCatalogLayer(layerId) {
  const profile = activeRoleWorkspaceProfile();
  return !profile || profile.allowedCatalogLayerIds.has(canonicalCatalogLayerId(layerId));
}

function roleWorkspaceAllowsLayer(layer) {
  return Boolean(layer?.memoryPresentationOpen) || roleWorkspaceAllowsCatalogLayer(layer?.catalogLayerId);
}

function roleWorkspaceLayers(layers = state.layers) {
  return layers.filter(roleWorkspaceAllowsLayer);
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
  entityMetadata: [],
  entityDirectory: [],
  map: null,
  mapReady: false,
  markers: [],
  assessmentMapArtifacts: [],
  cellularCallMapArtifacts: [],
  focusedEventPopup: null,
  focusedEventMarker: null,
  focusedMapSelection: null,
  focusedViewerRecordId: null,
  investigationId: "",
  investigationName: "",
  draftSessionActive: false,
  pendingDraftMemoryAction: null,
  investigations: [],
  investigationMemory: null,
  investigationMemoryLoading: false,
  investigationMemoryError: "",
  investigationMemoryLoadToken: 0,
  investigationSelectorOpen: false,
  investigationSearchQuery: "",
  layerCatalog: [],
  layerCatalogLoading: false,
  layerCatalogError: "",
  layerSearchQuery: "",
  layerSearchOpen: false,
  activeTeamMemberId: null,
  activeRoleWorkspace: null,
  openingLayerIds: new Set(),
  layers: [],
  activeLayerId: null,
  rawOverlayMinimized: false,
  rawOverlayHeight: 28,
  resultTableControls: new Map()
};

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
const appHomeButton = document.getElementById("appHomeButton");
const welcomePage = document.getElementById("welcomePage");
const myInvestigationsList = document.getElementById("myInvestigationsList");
const myInvestigationsCount = document.getElementById("myInvestigationsCount");
const invitedInvestigationsList = document.getElementById("invitedInvestigationsList");
const invitedInvestigationsCount = document.getElementById("invitedInvestigationsCount");
const similarInvestigationsList = document.getElementById("similarInvestigationsList");
const similarInvestigationsCount = document.getElementById("similarInvestigationsCount");
const welcomeActionModal = document.getElementById("welcomeActionModal");
const welcomeActionTitle = document.getElementById("welcomeActionTitle");
const welcomeActionDescription = document.getElementById("welcomeActionDescription");
const welcomeActionClose = document.getElementById("welcomeActionClose");
const welcomeDraftButton = document.getElementById("welcomeDraftButton");
const datasetStatus = document.getElementById("datasetStatus");
const datasetStatusIndicator = document.getElementById("datasetStatusIndicator");
const layerSelectorSearch = document.getElementById("layerSelectorSearch");
const layerSelectorList = document.getElementById("layerSelectorList");
const layerSelectorStatus = document.getElementById("layerSelectorStatus");
const workspace = document.querySelector(".workspace");
const memoryButton = document.getElementById("memoryButton");
const memoryModal = document.getElementById("memoryModal");
const memoryModalBody = document.getElementById("memoryModalBody");
const memoryCommentModal = document.getElementById("memoryCommentModal");
const memoryCommentForm = document.getElementById("memoryCommentForm");
const memoryCommentInput = document.getElementById("memoryCommentInput");
const memoryCommentSubject = document.getElementById("memoryCommentSubject");
const memoryCommentError = document.getElementById("memoryCommentError");
let pendingMemoryCommentAction = null;
let memoryReturnFocus = null;
const polygonActionMenu = document.getElementById("polygonActionMenu");
const collectionRequestModal = document.getElementById("collectionRequestModal");
const collectionRequestForm = document.getElementById("collectionRequestForm");
const collectionRequestTarget = document.getElementById("collectionRequestTarget");
const collectionRequestTypes = document.getElementById("collectionRequestTypes");
const collectionExtractionObjects = document.getElementById("collectionExtractionObjects");
const collectionRequestError = document.getElementById("collectionRequestError");
const adintTaskModal = document.getElementById("adintTaskModal");
const sigintTaskModal = document.getElementById("sigintTaskModal");
const cellularCallsTaskModal = document.getElementById("cellularCallsTaskModal");
const cctvTaskModal = document.getElementById("cctvTaskModal");
let pendingPolygonAction = null;
let pendingCollectionRequest = null;
let collectionTaskReturnFocus = null;
let adintTaskMap = null;
let cctvTaskMap = null;
let pendingAdintTaskTarget = null;
let pendingDemoCollectionType = null;

const systemStatuses = {
  dataset: { element: datasetStatus, indicator: datasetStatusIndicator, labelHe: "מאגר הנתונים", labelEn: "Dataset", he: "טוען נתונים", en: "Loading data", state: "loading" }
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

function viewLabels() {
  return currentLocale() === "en"
    ? { map: "Map", timeline: "Timeline", table: "Table", evidence: "Table" }
    : { map: "מפה", timeline: "ציר זמן", table: "טבלה", evidence: "טבלה" };
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
    ? { entities: "Entities", locations: "Locations", events: "Events by source_type", targets: "Targets", evidence: "Evidence" }
    : { entities: "ישויות", locations: "מיקומים", events: "אירועים לפי source_type", targets: "מטרות", evidence: "ראיות" };
}

function michlolAvatarHtml(member) {
  return `<span class="michlol-avatar"><span class="michlol-initial">${escapeHtml(member.initial)}</span><img src="${escapeHtml(member.avatar)}" alt="" loading="eager" onerror="this.remove()"></span>`;
}

function michlolMemberHtml(member) {
  const title = `${member.displayName} - ${member.roleLabel}`;
  const aria = `${member.displayName}, ${member.roleLabel}`;
  const active = state.activeTeamMemberId === member.id;
  return `
    <button class="michlol-member ${active ? "active" : ""}" type="button" data-member-id="${escapeHtml(member.id)}" data-member-type="${escapeHtml(member.memberType)}" title="${escapeHtml(title)}" aria-label="${escapeHtml(aria)}" aria-pressed="${active ? "true" : "false"}">
      ${michlolAvatarHtml(member)}
      <span class="michlol-name">${escapeHtml(member.displayName)}</span>
    </button>`;
}

function renderMichlolTeam() {
  if (!michlolTeam) return;
  const available = roleWorkspaceSelectionAvailable();
  michlolTeam.hidden = !available;
  if (!available) {
    michlolTeam.innerHTML = "";
    return;
  }
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
}

function defaultCallRecordId(layer) {
  return [...(layer?.items || [])]
    .filter(isCellularCallRecord)
    .sort((left, right) => String(right.call_started_at_utc || right.timestamp_utc || "").localeCompare(String(left.call_started_at_utc || left.timestamp_utc || "")))[0]?.event_id || "";
}

async function applyRoleWorkspace(member) {
  const role = member?.workspaceRole;
  const profile = ROLE_WORKSPACES[role] || null;
  state.activeRoleWorkspace = profile ? role : null;
  state.layers.forEach(layer => { layer.memoryPresentationOpen = false; });
  closeObjectViewer();
  ensureActiveLayer();
  renderLayerSelector();
  renderAllViews();
  if (!profile) return;

  const openedLayer = await openCatalogLayer(resolveCatalogLayerId(profile.defaultCatalogLayerId), { silent: true, roleDefault: true });
  if (!openedLayer || state.activeTeamMemberId !== member.id || state.activeRoleWorkspace !== role) return;

  state.rawOverlayMinimized = false;
  state.activeLayerId = openedLayer.capabilities.table ? openedLayer.id : state.activeLayerId;
  activateView(profile.defaultView);
  renderAllViews();

  if (profile.openDefaultCall) {
    const recordId = defaultCallRecordId(openedLayer);
    if (recordId) openObjectViewer("record", recordId, document.getElementById("timeline"));
  }
}

// Team members are presentational. Selecting a specialist (SIGINT / VISINT) scopes the workspace to
// that role's layers; selecting the same member again returns to the full workspace.
function selectTeamMember(memberId) {
  if (!roleWorkspaceSelectionAvailable()) return;
  const member = currentMembers().find(item => item.id === memberId);
  if (!member) return;
  if (state.activeTeamMemberId === member.id) {
    state.activeTeamMemberId = null;
    void applyRoleWorkspace(null);
    renderMichlolTeam();
    return;
  }
  state.activeTeamMemberId = member.id;
  void applyRoleWorkspace(member);
  renderMichlolTeam();
}

function applyLocaleUi() {
  document.documentElement.lang = currentLocale();
  document.documentElement.dir = currentLocale() === "en" ? "ltr" : "rtl";
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
  renderMichlolTeam();
  renderInvestigationSelector();
  renderDraftInvestigationUi();
  renderWelcomePage();
  renderAllViews();
  document.documentElement.dataset.appReady = "true";
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

function layerId(kind, label) {
  return `${kind}:${String(label || "unknown").replace(/\s+/g, "-")}`;
}

function buildCatalogLayer(layer, rows = []) {
  const items = layer.kind === "events"
    ? rows.map(item => ({ ...item, date: new Date(item.timestamp_utc) }))
    : layer.kind === "evidence"
      ? rows.map(item => ({ ...item, date: new Date(item.valid_from || 0) }))
    : rows;
  return {
    dataId: layer.id,
    label: layer.label,
    kind: layer.kind,
    visible: true,
    items,
    capabilities: layer.capabilities || { table: true, map: false, timeline: false },
    catalogLayerId: layer.id,
    catalogFilters: layer.catalog_filters || {}
  };
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
  const scopedLayers = roleWorkspaceLayers();
  const activeStillExists = scopedLayers.some(layer => layer.id === state.activeLayerId);
  if (!activeStillExists) {
    state.activeLayerId = scopedLayers.find(layer => layer.capabilities.table && layer.visible)?.id
      || scopedLayers.find(layer => layer.capabilities.table)?.id
      || null;
  }
  if (!scopedLayers.some(layer => layer.id === state.activeLayerId && layer.visible && layer.capabilities.table)) {
    state.activeLayerId = scopedLayers.find(layer => layer.capabilities.table && layer.visible)?.id
      || scopedLayers.find(layer => layer.capabilities.table)?.id
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

function layerColorStyle(layer) {
  return `--layer-color:${escapeHtml(layer?.color || "#8ab4f8")}`;
}

function visibleLayers(capability = null) {
  return roleWorkspaceLayers().filter(layer => layer.visible && (!capability || layer.capabilities[capability]));
}

function activeTableLayer() {
  const scopedLayers = roleWorkspaceLayers();
  return scopedLayers.find(layer => layer.id === state.activeLayerId && layer.capabilities.table)
    || scopedLayers.find(layer => layer.capabilities.table)
    || null;
}

function focusedTimelineLayers() {
  const layer = activeTableLayer();
  return layer?.visible && layer.capabilities.timeline ? [layer] : [];
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
  if (layer?.items?.length && layer.items.every(isIpdrRecord)) {
    for (const field of ["entity_id", "entity_name", "location_id", "location_name", "location_type", "location_accuracy_m"]) fields.delete(field);
  }
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

function normalizeMemoryList(value) {
  return Array.isArray(value) ? value.filter(item => item && typeof item === "object") : [];
}

function currentSavedMemory() {
  const memory = state.investigationMemory?.memory;
  return memory && typeof memory === "object" ? memory : { layers: [], artifacts: [], collection_requests: [] };
}

function memoryCommentValue(value) {
  return String(value || "").replace(/\s+/g, " ").trim().slice(0, 1200);
}

function openMemoryCommentDialog(options) {
  if (!state.investigationId || !memoryCommentModal) return;
  pendingMemoryCommentAction = options;
  memoryReturnFocus = options.trigger || document.activeElement;
  memoryCommentSubject.textContent = options.label || "";
  memoryCommentInput.value = "";
  memoryCommentError.hidden = true;
  memoryCommentError.textContent = "";
  memoryCommentModal.hidden = false;
  memoryCommentInput.focus();
}

function closeMemoryCommentDialog() {
  pendingMemoryCommentAction = null;
  memoryCommentModal.hidden = true;
  memoryReturnFocus?.focus?.();
  memoryReturnFocus = null;
}

const COLLECTION_TYPES = [
  { id: "adint", he: "ADINT", en: "ADINT", descriptionHe: "איסוף נתוני מכשירים ופרסומות באזור", descriptionEn: "Collect device and advertising observations in the area" },
  { id: "cellular_geolocations", he: "מיקומי סלולר", en: "Cellular geolocations", descriptionHe: "איסוף מיקומי מכשירים", descriptionEn: "Collect device location observations" },
  { id: "cellular_calls", he: "שיחות סלולר", en: "Cellular calls", descriptionHe: "איסוף רשומות שיחות", descriptionEn: "Collect call-detail records" },
  { id: "satellite", he: "לוויין", en: "Satellite", descriptionHe: "בקשת צילום לווייני", descriptionEn: "Request satellite imagery" },
  { id: "cctv", he: "CCTV", en: "CCTV", descriptionHe: "בקשת וידאו ממצלמות", descriptionEn: "Request camera video" }
];
const COLLECTION_LAYER_PRESENTATIONS = {
  adint: { layerId: "events:ADINT", view: "map" },
  cellular_geolocations: { layerId: "events:Cellular Geolocations", view: "map" },
  cellular_calls: { layerId: "events:Cellular Calls", view: "timeline" },
  satellite: { layerId: "events:Satellite", view: "map" },
  cctv: { layerId: "events:CCTV", view: "map" }
};
const COLLECTION_EXTRACTION_OBJECTS = [
  { id: "convoy", he: "שיירה", en: "Convoy" },
  { id: "vehicles", he: "כלי רכב", en: "Vehicles" },
  { id: "personnel", he: "כוח אדם", en: "Personnel" },
  { id: "equipment", he: "ציוד", en: "Equipment" },
  { id: "infrastructure", he: "תשתיות", en: "Infrastructure" }
];

function collectionTypesForRole() {
  if (state.activeRoleWorkspace === "sigint") return COLLECTION_TYPES.filter(item => ["cellular_geolocations", "cellular_calls"].includes(item.id));
  if (state.activeRoleWorkspace === "visint") return COLLECTION_TYPES.filter(item => ["satellite", "cctv"].includes(item.id));
  return COLLECTION_TYPES;
}

async function openRequestedCollectionLayer(collectionType) {
  const presentation = COLLECTION_LAYER_PRESENTATIONS[collectionType];
  if (!presentation) return null;
  const layer = await openCatalogLayer(resolveCatalogLayerId(presentation.layerId));
  if (layer) activateView(presentation.view);
  return layer;
}

function collectionImeiButton(value) {
  const imei = String(value || "").trim();
  if (!imei || imei === "-" || imei === "—" || /unknown/i.test(imei)) return escapeHtml(imei || "—");
  return `<button type="button" class="collection-imei" data-collection-imei="${escapeHtml(imei)}" title="${escapeHtml(activeLocaleText("בקשת איסוף עבור IMEI", "Request collection for this IMEI"))}">${escapeHtml(imei)}</button>`;
}

function closePolygonActionMenu() {
  pendingPolygonAction = null;
  polygonActionMenu.hidden = true;
}

function closeCollectionRequestDialog() {
  pendingCollectionRequest = null;
  collectionRequestModal.hidden = true;
  collectionRequestError.hidden = true;
}

function updateCollectionSourceSelectionAction() {
  const submit = document.getElementById("collectionRequestSubmit");
  const type = collectionRequestForm?.querySelector('input[name="collectionType"]:checked')?.value;
  const target = pendingCollectionRequest;
  const opensDemoTask = (target?.type === "polygon" && ["adint", "cctv"].includes(type)) || (target?.type === "imei" && ["cellular_geolocations", "cellular_calls"].includes(type));
  if (submit) submit.textContent = activeLocaleText(opensDemoTask ? "המשך" : "שלח בקשה", opensDemoTask ? "Continue" : "Submit request");
}

function closeCollectionTaskDialog(modal) {
  if (!modal) return;
  if (modal === adintTaskModal) {
    adintTaskMap?.remove();
    adintTaskMap = null;
    pendingAdintTaskTarget = null;
  }
  if (modal === cctvTaskModal) {
    cctvTaskMap?.remove();
    cctvTaskMap = null;
  }
  modal.hidden = true;
  collectionTaskReturnFocus?.focus?.();
  collectionTaskReturnFocus = null;
  pendingDemoCollectionType = null;
}

async function completeDemoCollectionTask(modal, fallbackType) {
  const type = pendingDemoCollectionType || fallbackType;
  closeCollectionTaskDialog(modal);
  await openRequestedCollectionLayer(type);
}

function polygonTaskSummary(coordinates) {
  const ring = Array.isArray(coordinates) ? coordinates : [];
  const points = ring.length > 1 && ring[0]?.[0] === ring.at(-1)?.[0] && ring[0]?.[1] === ring.at(-1)?.[1] ? ring.slice(0, -1) : ring;
  if (points.length < 3) return "No drawn location";
  const [lon, lat] = points.reduce((total, point) => [total[0] + Number(point[0] || 0), total[1] + Number(point[1] || 0)], [0, 0]).map(total => total / points.length);
  return `${points.length} vertices · centroid ${lon.toFixed(4)}, ${lat.toFixed(4)}`;
}

function renderAdintLocationMap(coordinates) {
  const container = document.getElementById("adintLocationMap");
  adintTaskMap?.remove();
  adintTaskMap = null;
  if (!container || typeof maplibregl === "undefined") return;
  const ring = (Array.isArray(coordinates) ? coordinates : []).filter(point => Array.isArray(point) && Number.isFinite(Number(point[0])) && Number.isFinite(Number(point[1])));
  const points = ring.length > 1 && ring[0][0] === ring.at(-1)[0] && ring[0][1] === ring.at(-1)[1] ? ring.slice(0, -1) : ring;
  if (points.length < 3) { container.textContent = "Location map unavailable"; return; }
  container.textContent = "";
  const map = new maplibregl.Map({
    container,
    style: "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
    center: points[0],
    zoom: 10,
    interactive: false,
    attributionControl: false
  });
  adintTaskMap = map;
  map.on("load", () => {
    if (map !== adintTaskMap) return;
    if (state.basemapMode !== "street") {
      const baseLayers = map.getStyle().layers.map(layer => JSON.parse(JSON.stringify(layer)));
      const firstLabel = baseLayers.find(layer => layer.type === "symbol")?.id;
      map.addSource("task-satellite-imagery", {
        type: "raster",
        tiles: ["https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],
        tileSize: 256,
        maxzoom: 19,
        attribution: "Imagery © Esri, Vantor, Earthstar Geographics"
      });
      map.addLayer({ id: "task-satellite-imagery", type: "raster", source: "task-satellite-imagery" }, firstLabel);
      for (const layer of baseLayers) {
        if (!map.getLayer(layer.id)) continue;
        if (satelliteReferenceLayer(layer)) {
          map.setPaintProperty(layer.id, "line-color", layer["source-layer"] === "boundary" ? "rgba(255,255,255,0.82)" : "rgba(255,215,112,0.82)");
          map.setPaintProperty(layer.id, "line-opacity", layer["source-layer"] === "boundary" ? 0.72 : 0.68);
        } else if (layer.type !== "symbol") {
          map.setLayoutProperty(layer.id, "visibility", "none");
        } else if (layer.layout?.["text-field"]) {
          map.setPaintProperty(layer.id, "text-color", "#ffffff");
          map.setPaintProperty(layer.id, "text-halo-color", "#202b35");
          map.setPaintProperty(layer.id, "text-halo-width", 1.5);
        }
      }
    }
    const bounds = new maplibregl.LngLatBounds();
    points.forEach(point => bounds.extend(point));
    map.addSource("drawn-collection-area", { type: "geojson", data: { type: "Feature", properties: {}, geometry: { type: "Polygon", coordinates: [[...points, points[0]]] } } });
    map.addLayer({ id: "drawn-collection-area-fill", type: "fill", source: "drawn-collection-area", paint: { "fill-color": "#8ab4f8", "fill-opacity": 0.24 } });
    map.addLayer({ id: "drawn-collection-area-outline", type: "line", source: "drawn-collection-area", paint: { "line-color": "#8ab4f8", "line-width": 2.5 } });
    map.fitBounds(bounds, { padding: 22, maxZoom: 13, duration: 0 });
    map.resize();
  });
}

function renderCctvLocationMap(coordinates) {
  const container = document.getElementById("cctvLocationMap");
  cctvTaskMap?.remove();
  cctvTaskMap = null;
  if (!container || typeof maplibregl === "undefined") return;
  const ring = (Array.isArray(coordinates) ? coordinates : []).filter(point => Array.isArray(point) && Number.isFinite(Number(point[0])) && Number.isFinite(Number(point[1])));
  const points = ring.length > 1 && ring[0][0] === ring.at(-1)[0] && ring[0][1] === ring.at(-1)[1] ? ring.slice(0, -1) : ring;
  if (points.length < 3) { container.textContent = "Location map unavailable"; return; }
  container.textContent = "";
  const map = new maplibregl.Map({ container, style: "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json", center: points[0], zoom: 10, interactive: false, attributionControl: false });
  cctvTaskMap = map;
  map.on("load", () => {
    if (map !== cctvTaskMap) return;
    const bounds = new maplibregl.LngLatBounds();
    points.forEach(point => bounds.extend(point));
    map.addSource("cctv-collection-area", { type: "geojson", data: { type: "Feature", properties: {}, geometry: { type: "Polygon", coordinates: [[...points, points[0]]] } } });
    map.addLayer({ id: "cctv-collection-area-fill", type: "fill", source: "cctv-collection-area", paint: { "fill-color": "#8ab4f8", "fill-opacity": 0.24 } });
    map.addLayer({ id: "cctv-collection-area-outline", type: "line", source: "cctv-collection-area", paint: { "line-color": "#8ab4f8", "line-width": 2.5 } });
    map.fitBounds(bounds, { padding: 22, maxZoom: 13, duration: 0 });
    map.resize();
  });
}

function openAdintTaskDialog(target, trigger = document.activeElement) {
  collectionTaskReturnFocus = trigger;
  pendingAdintTaskTarget = target;
  const summary = document.getElementById("adintLocationSummary");
  if (summary) summary.textContent = polygonTaskSummary(target?.coordinates);
  adintTaskModal.hidden = false;
  requestAnimationFrame(() => renderAdintLocationMap(pendingAdintTaskTarget?.coordinates));
  adintTaskModal.querySelector("button")?.focus();
}

function openSigintTaskDialog(trigger = document.activeElement) {
  collectionTaskReturnFocus = trigger;
  sigintTaskModal.hidden = false;
  sigintTaskModal.querySelector("button")?.focus();
}

function openCellularCallsTaskDialog(target, trigger = document.activeElement) {
  collectionTaskReturnFocus = trigger;
  const imei = document.getElementById("cellularCallsImei");
  if (imei && target?.imei) imei.value = target.imei;
  cellularCallsTaskModal.hidden = false;
  cellularCallsTaskModal.querySelector("button")?.focus();
}

function openCctvTaskDialog(target, trigger = document.activeElement) {
  collectionTaskReturnFocus = trigger;
  const summary = document.getElementById("cctvLocationSummary");
  if (summary) summary.textContent = polygonTaskSummary(target?.coordinates);
  cctvTaskModal.hidden = false;
  requestAnimationFrame(() => renderCctvLocationMap(target?.coordinates));
  cctvTaskModal.querySelector("button")?.focus();
}

function openPolygonActionMenu(polygon) {
  if (!polygon?.coordinates || state.pageView !== "workspace") return;
  pendingPolygonAction = polygon;
  const minimumMargin = 8;
  const menuWidth = 213;
  const menuHeight = 82;
  const x = Math.min(Math.max(polygon.position?.x ?? window.innerWidth / 2, minimumMargin), window.innerWidth - menuWidth - minimumMargin);
  const y = Math.min(Math.max(polygon.position?.y ?? window.innerHeight / 2, minimumMargin), window.innerHeight - menuHeight - minimumMargin);
  polygonActionMenu.style.left = `${x}px`;
  polygonActionMenu.style.top = `${y}px`;
  polygonActionMenu.hidden = false;
}

function openCollectionRequestDialog(target, trigger = document.activeElement) {
  if (state.draftSessionActive) { openDraftCreateModal(() => openCollectionRequestDialog(target, trigger)); return; }
  if (!state.investigationId || !target) return;
  pendingCollectionRequest = { ...target, trigger };
  const isImei = target.type === "imei";
  collectionRequestTarget.textContent = isImei
    ? `IMEI: ${target.imei}`
    : activeLocaleText("אזור מסומן במפה", "Marked area on the map");
  const types = collectionTypesForRole();
  const defaultType = target.type === "imei" ? "cellular_geolocations" : "adint";
  collectionRequestTypes.innerHTML = `<legend>${escapeHtml(activeLocaleText("סוג איסוף", "Collection type"))}</legend>${types.map((item, index) => `<label class="collection-option"><input type="radio" name="collectionType" value="${item.id}" ${item.id === defaultType || (index === 0 && !types.some(option => option.id === defaultType)) ? "checked" : ""}><span><strong>${escapeHtml(activeLocaleText(item.he, item.en))}</strong><small>${escapeHtml(activeLocaleText(item.descriptionHe, item.descriptionEn))}</small></span></label>`).join("")}`;
  const visint = state.activeRoleWorkspace === "visint";
  collectionExtractionObjects.hidden = !visint;
  collectionExtractionObjects.innerHTML = visint ? `<legend>${escapeHtml(activeLocaleText("אובייקטים לחילוץ", "Objects to extract"))}</legend>${COLLECTION_EXTRACTION_OBJECTS.map((item, index) => `<label class="collection-option"><input type="checkbox" name="collectionObject" value="${item.id}" ${index === 0 ? "checked" : ""}><span><strong>${escapeHtml(activeLocaleText(item.he, item.en))}</strong></span></label>`).join("")}` : "";
  collectionRequestError.hidden = true;
  collectionRequestModal.hidden = false;
  updateCollectionSourceSelectionAction();
  collectionRequestTypes.querySelector("input")?.focus();
}

async function submitCollectionRequest() {
  const target = pendingCollectionRequest;
  const type = collectionRequestForm.querySelector('input[name="collectionType"]:checked')?.value;
  if (!target || !type) return;
  if (target.type === "polygon" && type === "adint") {
    const trigger = target.trigger;
    pendingDemoCollectionType = type;
    closeCollectionRequestDialog();
    openAdintTaskDialog(target, trigger);
    return;
  }
  if (target.type === "polygon" && type === "cctv") {
    const trigger = target.trigger;
    pendingDemoCollectionType = type;
    closeCollectionRequestDialog();
    openCctvTaskDialog(target, trigger);
    return;
  }
  if (target.type === "imei" && type === "cellular_geolocations") {
    const trigger = target.trigger;
    pendingDemoCollectionType = type;
    closeCollectionRequestDialog();
    openSigintTaskDialog(trigger);
    return;
  }
  if (target.type === "imei" && type === "cellular_calls") {
    const trigger = target.trigger;
    pendingDemoCollectionType = type;
    closeCollectionRequestDialog();
    openCellularCallsTaskDialog(target, trigger);
    return;
  }
  const objects = [...collectionRequestForm.querySelectorAll('input[name="collectionObject"]:checked')].map(input => input.value);
  const response = await fetch("/api/collection-request", {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({
      investigation_id: state.investigationId,
      name: state.investigationName,
      role: state.activeRoleWorkspace || "general",
      target: target.type === "imei" ? { type: "imei", imei: target.imei } : { type: "polygon", geometry: { type: "Polygon", coordinates: [target.coordinates] } },
      collection_type: type,
      extraction_objects: objects,
      instructions: ""
    })
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || activeLocaleText("שליחת בקשת האיסוף נכשלה", "Could not submit collection request"));
  await loadInvestigationMemory();
  closeCollectionRequestDialog();
  const openedLayer = await openRequestedCollectionLayer(type);
  if (!openedLayer) target.trigger?.focus?.();
}

function renderMemoryScreen() {
  if (!memoryModalBody) return;
  const memory = currentSavedMemory();
  const groups = [
    ["layers", activeLocaleText("שכבות", "Layers"), memory.layers || [], item => item.label || "—", true],
    ["artifacts", activeLocaleText("אובייקטים", "Objects"), (memory.artifacts || []).filter(item => item.kind === "object"), item => item.label || item.object_id || "—", true],
    ["artifacts", activeLocaleText("אזורים", "Areas"), (memory.artifacts || []).filter(item => item.kind === "polygon"), item => item.label || activeLocaleText("אזור שמור", "Saved area"), true],
    ["collection_requests", activeLocaleText("בקשות איסוף", "Collection requests"), memory.collection_requests || [], item => item.label || item.collection_type || "—", false]
  ];
  const html = groups.filter(([, , items]) => items.length).map(([group, title, items, label, openable]) => `<section class="memory-group"><h3>${escapeHtml(title)}</h3>${items.slice().reverse().map(item => `<article class="memory-entry"><div class="memory-entry-heading">${openable ? `<button type="button" class="memory-entry-open" data-memory-open-group="${group}" data-memory-open-id="${escapeHtml(item.id)}"><strong>${escapeHtml(label(item))}</strong></button>` : `<strong>${escapeHtml(label(item))}</strong>`}<button type="button" class="memory-entry-delete" data-memory-delete-group="${group}" data-memory-delete-id="${escapeHtml(item.id)}" title="${escapeHtml(activeLocaleText("הסר מהזיכרון", "Remove from memory"))}" aria-label="${escapeHtml(activeLocaleText("הסר מהזיכרון", "Remove from memory"))}"><span class="material-symbols-rounded" aria-hidden="true">delete</span></button></div><span class="memory-entry-meta">${escapeHtml(formatSavedTime(item.saved_at_utc))}${item.object_id ? ` · ${escapeHtml(item.object_id)}` : ""}</span>${item.analyst_comment ? `<p class="memory-entry-comment">${escapeHtml(item.analyst_comment)}</p>` : ""}</article>`).join("")}</section>`).join("");
  memoryModalBody.innerHTML = html || `<div class="activity-empty">${escapeHtml(activeLocaleText("עדיין לא נשמרו פריטים לחקירה זו.", "No items have been saved to this investigation yet."))}</div>`;
}

function savedMemoryEntry(group, id) {
  return normalizeMemoryList(currentSavedMemory()[group]).find(item => item.id === id) || null;
}

function memoryPresentationView(value, fallback = "table") {
  return ["map", "timeline", "table"].includes(value) ? value : fallback;
}

function currentPresentationView() {
  return memoryPresentationView(document.querySelector(".view-tab.active")?.dataset.view, "map");
}

async function openSavedMemoryLayer(item, trigger) {
  if (!item) return;
  let layer = state.layers.find(candidate => candidate.investigation_memory_layer_id === item.id);
  if (!layer && item.catalog_layer_id) layer = await openCatalogLayer(item.catalog_layer_id, { silent: true, savedLayer: item, memoryRestore: true });
  if (!layer) return;
  layer.memoryPresentationOpen = true;
  applySavedFiltersToLayer(layer, item);
  layer.visible = true;
  state.activeLayerId = layer.id;
  activateView(memoryPresentationView(item.presentation_view, layer.preferredView || "table"));
  renderAllViews();
  closeMemoryScreen();
  trigger?.focus?.();
}

function openSavedMemoryPolygon(item, trigger) {
  const geometry = item?.geometry;
  const ring = geometry?.type === "Polygon" ? geometry.coordinates?.[0] : null;
  if (!Array.isArray(ring) || ring.length < 4) return;
  activateView("map");
  const show = () => {
    if (!state.map?.isStyleLoaded?.()) return;
    const data = { type: "Feature", properties: { memory_id: item.id }, geometry };
    const source = state.map.getSource("memory-polygon-focus");
    if (source) source.setData(data);
    else {
      state.map.addSource("memory-polygon-focus", { type: "geojson", data });
      state.map.addLayer({ id: "memory-polygon-focus-fill", type: "fill", source: "memory-polygon-focus", paint: { "fill-color": "#58a6ff", "fill-opacity": 0.18 } });
      state.map.addLayer({ id: "memory-polygon-focus-line", type: "line", source: "memory-polygon-focus", paint: { "line-color": "#9adaff", "line-width": 3 } });
    }
    const bounds = new maplibregl.LngLatBounds();
    ring.forEach(point => bounds.extend(point));
    state.map.fitBounds(bounds, { padding: 70, maxZoom: 14, duration: 0 });
  };
  requestAnimationFrame(show);
  closeMemoryScreen();
  trigger?.focus?.();
}

async function openMemoryEntry(group, id, trigger) {
  const item = savedMemoryEntry(group, id);
  if (!item) return;
  if (group === "layers") return openSavedMemoryLayer(item, trigger);
  if (group === "artifacts" && item.kind === "object") {
    const opened = openObjectViewer(item.object_kind, item.object_id, trigger);
    if (opened) closeMemoryScreen();
    return;
  }
  if (group === "artifacts" && item.kind === "polygon") openSavedMemoryPolygon(item, trigger);
}

async function deleteMemoryEntry(group, id) {
  if (!state.investigationId) return;
  const response = await fetch("/api/investigation-memory/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({ investigation_id: state.investigationId, group, item_id: id })
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || activeLocaleText("מחיקת פריט הזיכרון נכשלה", "Failed to delete memory item"));
  if (group === "layers") {
    const layer = state.layers.find(candidate => candidate.investigation_memory_layer_id === id);
    if (layer) delete layer.investigation_memory_layer_id;
  }
  await loadInvestigationMemory();
}

function openMemoryScreen(trigger = memoryButton) {
  if (!state.investigationId || state.draftSessionActive) return;
  memoryReturnFocus = trigger;
  renderMemoryScreen();
  memoryModal.hidden = false;
  document.getElementById("memoryModalClose")?.focus();
}

function closeMemoryScreen() {
  memoryModal.hidden = true;
  memoryReturnFocus?.focus?.();
  memoryReturnFocus = null;
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
      savedLayer,
      memoryRestore: true
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
      layers: restoredMemoryLayers,
      artifacts: normalizeMemoryList(memory.artifacts),
      collection_requests: normalizeMemoryList(memory.collection_requests)
    }
  };
  renderAllViews();
  renderLayerSelector();
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
    if (!memoryModal?.hidden) renderMemoryScreen();
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
    catalog_filters: layer.catalogFilters || {},
    data_id: layer.dataId || "",
    source_id: layer.sourceId || "",
    source_label: layer.sourceLabel || "",
    source_type: sourceType,
    presentation_view: currentPresentationView(),
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

async function saveLayerToInvestigationMemory(layer, button, comment = "", confirmed = false) {
  if (state.draftSessionActive) {
    openDraftCreateModal(() => saveLayerToInvestigationMemory(layer, button));
    return;
  }
  if (!canSaveLayerToMemory(layer) || button?.dataset.memorySaving === "true") return;
  if (!confirmed) {
    openMemoryCommentDialog({ label: layer.label, trigger: button, onSave: value => saveLayerToInvestigationMemory(layer, button, value, true) });
    return;
  }
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
        comment: memoryCommentValue(comment),
      }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("שמירת השכבה לזיכרון נכשלה", "Failed to save layer to memory"));
    layer.investigation_memory_layer_id = payload.saved?.id || true;
    await loadInvestigationMemory();
    button.title = activeLocaleText("השכבה נשמרה בזיכרון החקירה", "Layer saved to investigation memory");
    button.setAttribute("aria-label", button.title);
    renderEvidence();
  } catch (error) {
    button.title = error.name === "AbortError"
      ? activeLocaleText("שמירת השכבה ארכה יותר מדי זמן. נסו שוב.", "Saving the layer took too long. Try again.")
      : error.message;
    button.setAttribute("aria-label", button.title);
    if (confirmed) throw error;
  } finally {
    clearTimeout(timeout);
    delete button.dataset.memorySaving;
  }
}

function normalizeInvestigationName(name) {
  return String(name || "").replace(/\s+/g, " ").trim();
}

function investigationNameKey(name) {
  return normalizeInvestigationName(name).toLocaleLowerCase("he-IL");
}

function saveActiveInvestigation() {
  try {
    if (state.investigationId && !state.draftSessionActive) scenarioStorage.setItem(ACTIVE_INVESTIGATION_STORAGE_KEY, state.investigationId);
  } catch (error) {
    console.warn("Could not remember the active investigation", error);
  }
}

function storedActiveInvestigationId() {
  try {
    return scenarioStorage.getItem(ACTIVE_INVESTIGATION_STORAGE_KEY) || "";
  } catch (error) {
    return "";
  }
}

function investigationFromServer(item) {
  const id = String(item?.investigation_id || item?.id || "").trim();
  const name = normalizeInvestigationName(item?.name);
  if (!id || !name) return null;
  return {
    id,
    name,
    created_at: item?.created_at_utc || "",
    updated_at: item?.updated_at_utc || "",
    layer_count: Number(item?.layer_count || 0),
    artifact_count: Number(item?.artifact_count || 0),
    collection_request_count: Number(item?.collection_request_count || 0),
    status: String(item?.status || "").trim(),
    activity_level: String(item?.activity_level || "").trim(),
    research_question: String(item?.research_question || "").trim(),
    next_milestone: String(item?.next_milestone || "").trim()
  };
}

function findInvestigationByName(name) {
  const key = investigationNameKey(name);
  return key ? state.investigations.find(item => investigationNameKey(item.name) === key) || null : null;
}

// Creates the investigation on the server (the source of truth) and adds it to the local list.
async function createInvestigation(name, id = createInvestigationId()) {
  const safeName = normalizeInvestigationName(name) || defaultInvestigationName();
  const payload = await registerInvestigationRecord({ id, name: safeName });
  const created = investigationFromServer(payload?.investigation || payload) || { id, name: safeName, created_at: new Date().toISOString() };
  state.investigations = [...state.investigations.filter(item => item.id !== created.id), created];
  renderWelcomePage();
  return created;
}

async function ensureInvestigationRecord(name) {
  const safeName = normalizeInvestigationName(name) || defaultInvestigationName();
  return findInvestigationByName(safeName) || createInvestigation(safeName);
}

const SERBIA_SIMILAR_INVESTIGATIONS = [
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

const SYRIA_INVITED_INVESTIGATIONS = [
  {
    id: "suspicious-military-convoy",
    titleHe: "שיירה צבאית חשודה",
    titleEn: "Suspicious military convoy",
    summaryHe: "חקירה משותפת של תצפיות על שיירה, תנועת כלי רכב ומקורות חזותיים תומכים.",
    summaryEn: "A collaborative investigation of convoy observations, vehicle movement, and supporting visual sources.",
    reasonHe: "הוזמנת על ידי צוות הוויזינט",
    reasonEn: "Invited by the VISINT team",
    participants: 3,
    action: "join",
    invited: true
  }
];

const SYRIA_PROPOSED_INVESTIGATIONS = [
  {
    id: "unidentified-call-counterpart",
    titleHe: "זיהוי צד לא מזוהה בשיחות סלולר",
    titleEn: "Unidentified counterpart in cellular calls",
    summaryHe: "בדיקת דפוסי שיחה, מיקום ומזהי מכשיר סביב הצד הלא מזוהה בשיחות שנאספו.",
    summaryEn: "Review call, location, and device-identifier patterns around the unidentified party in collected calls.",
    reasonHe: "חפיפה גבוהה למזהים ולשיחות בחקירה שלך",
    reasonEn: "High overlap with identifiers and calls in your investigation",
    participants: 2,
    action: "request"
  },
  {
    id: "damascus-cellular-movement",
    titleHe: "תנועת מכשירים סלולריים סביב דמשק",
    titleEn: "Cellular device movement around Damascus",
    summaryHe: "השוואת אירועי מיקום סלולריים לאורך זמן כדי לזהות דפוסי תנועה משותפים.",
    summaryEn: "Compare cellular geolocation events over time to identify shared movement patterns.",
    reasonHe: "התאמה גבוהה למקור ולמרחב הגאוגרפי",
    reasonEn: "Strong source and geographic match",
    participants: 4,
    action: "join"
  }
];

const INVITED_INVESTIGATIONS = demoRuntime?.scenario_id === "syria" ? SYRIA_INVITED_INVESTIGATIONS : [];
const SIMILAR_INVESTIGATIONS = demoRuntime?.scenario_id === "syria" ? SYRIA_PROPOSED_INVESTIGATIONS : SERBIA_SIMILAR_INVESTIGATIONS;

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

function formatInvestigationTime(value) {
  const date = value ? new Date(value) : null;
  if (!date || Number.isNaN(date.getTime())) return "—";
  return date.toLocaleString(currentLocaleTag(), { dateStyle: "medium", timeStyle: "short" });
}

function ownedInvestigationRibbonHtml(investigation) {
  const openLabel = activeLocaleText(`פתח את ${investigation.name}`, `Open ${investigation.name}`);
  const count = value => Number(value || 0).toLocaleString(currentLocaleTag());
  const savedSummary = activeLocaleText(
    `${count(investigation.layer_count)} שכבות · ${count(investigation.artifact_count)} פריטים · ${count(investigation.collection_request_count)} בקשות איסוף`,
    `${count(investigation.layer_count)} layers · ${count(investigation.artifact_count)} items · ${count(investigation.collection_request_count)} collection requests`
  );
  return `
    <article class="investigation-ribbon" data-owned-investigation-id="${escapeHtml(investigation.id)}">
      <button class="ribbon-main-action" type="button" data-open-investigation="${escapeHtml(investigation.id)}" aria-label="${escapeHtml(openLabel)}">
        <div class="ribbon-primary">
          <div class="ribbon-title-row">
            <h3 class="ribbon-title">${escapeHtml(investigation.name)}</h3>
            ${investigation.id === state.investigationId ? `<span class="ribbon-status">${activeLocaleText("פעילה", "Active")}</span>` : ""}
          </div>
          <p class="ribbon-summary">${escapeHtml(savedSummary)}</p>
        </div>
        ${welcomeParticipantsHtml()}
        <div class="ribbon-metrics">
          <div class="ribbon-metric"><span>${activeLocaleText("עודכנה", "Updated")}</span><strong>${escapeHtml(formatInvestigationTime(investigation.updated_at || investigation.created_at))}</strong></div>
          <div class="ribbon-metric"><span>${activeLocaleText("נוצרה", "Created")}</span><strong>${escapeHtml(formatInvestigationTime(investigation.created_at))}</strong></div>
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
  const actionIcon = investigation.action === "join" ? "group_add" : "person_add";
  return `
    <article class="investigation-ribbon similar">
      <div class="ribbon-similar-content">
        <div class="ribbon-primary">
            <div class="ribbon-title-row"><h3 class="ribbon-title">${escapeHtml(activeLocaleText(investigation.titleHe, investigation.titleEn))}</h3><span class="ribbon-status">${investigation.invited ? activeLocaleText("הוזמנת", "Invited") : activeLocaleText("מומלצת", "Recommended")}</span></div>
          <p class="ribbon-summary">${escapeHtml(activeLocaleText(investigation.summaryHe, investigation.summaryEn))}</p>
          <span class="ribbon-attention"><span class="material-symbols-rounded" aria-hidden="true">auto_awesome</span>${escapeHtml(activeLocaleText(investigation.reasonHe, investigation.reasonEn))}</span>
        </div>
        ${welcomeParticipantsHtml(investigation.participants)}
        <div class="ribbon-metrics">
          <div class="ribbon-metric"><span>${activeLocaleText("רמת פעילות", "Activity level")}</span><strong>${escapeHtml(investigation.activityLevel || activeLocaleText("פעילות גבוהה השבוע", "High activity this week"))}</strong></div>
          <div class="ribbon-metric"><span>${activeLocaleText("גישה", "Access")}</span><strong>${investigation.action === "join" ? activeLocaleText("פתוחה להשתתפות", "Open participation") : activeLocaleText("דורשת אישור בעלים", "Owner approval required")}</strong></div>
        </div>
      </div>
      <div class="ribbon-actions"><button class="ribbon-action" type="button" data-welcome-action="${investigation.action}" data-invited-investigation="${investigation.invited ? "true" : "false"}" data-invitation-id="${escapeHtml(investigation.id)}" data-investigation-name="${escapeHtml(activeLocaleText(investigation.titleHe, investigation.titleEn))}"><span class="material-symbols-rounded" aria-hidden="true">${actionIcon}</span>${actionLabel}</button></div>
    </article>`;
}

// When the investigations come from an i360 type (APP_INVESTIGATION_TYPE), its status field picks the
// welcome section: "invited" and "recommended" go to their sections, anything else is the user's own.
// Without i360 statuses the scenario's built-in demo lists are shown, as before.
const WELCOME_STATUS_SECTIONS = { invited: "invited", recommended: "recommended" };

function welcomeStatusSection(investigation) {
  return WELCOME_STATUS_SECTIONS[String(investigation?.status || "").trim().toLowerCase()] || "";
}

function welcomeSectionsFromI360() {
  return state.investigations.some(investigation => investigation.status);
}

function welcomeRibbonFromI360(investigation, section) {
  const summary = investigation.research_question || activeLocaleText("אין שאלת מחקר", "No research question");
  const reason = investigation.next_milestone
    ? activeLocaleText(`אבן הדרך הבאה: ${investigation.next_milestone}`, `Next milestone: ${investigation.next_milestone}`)
    : activeLocaleText("מתוך i360", "From i360");
  return {
    id: investigation.id,
    titleHe: investigation.name,
    titleEn: investigation.name,
    summaryHe: summary,
    summaryEn: summary,
    reasonHe: reason,
    reasonEn: reason,
    activityLevel: investigation.activity_level,
    participants: 2,
    action: section === "invited" ? "join" : "request",
    invited: section === "invited",
    fromI360: true
  };
}

function welcomeInvitedInvestigations() {
  if (!welcomeSectionsFromI360()) return INVITED_INVESTIGATIONS;
  return state.investigations.filter(item => welcomeStatusSection(item) === "invited").map(item => welcomeRibbonFromI360(item, "invited"));
}

function welcomeSimilarInvestigations() {
  if (!welcomeSectionsFromI360()) return SIMILAR_INVESTIGATIONS;
  return state.investigations.filter(item => welcomeStatusSection(item) === "recommended").map(item => welcomeRibbonFromI360(item, "recommended"));
}

function isInvitedWelcomeInvestigation(investigation) {
  if (welcomeSectionsFromI360() && typeof investigation === "object") return Boolean(welcomeStatusSection(investigation));
  const name = typeof investigation === "string" ? investigation : investigation?.name;
  return INVITED_INVESTIGATIONS.some(invitation => [invitation.titleHe, invitation.titleEn].some(title => investigationNameKey(title) === investigationNameKey(name)));
}

function invitedInvestigationById(id) {
  return welcomeInvitedInvestigations().find(investigation => investigation.id === id) || null;
}

async function joinInvitedInvestigation(invitation) {
  if (!invitation) return;
  if (invitation.fromI360) {
    const existing = state.investigations.find(item => item.id === invitation.id);
    if (existing) {
      selectInvestigation(existing);
      setPageView("workspace");
      return;
    }
  }
  const name = activeLocaleText(invitation.titleHe, invitation.titleEn);
  try {
    const investigation = await ensureInvestigationRecord(name);
    selectInvestigation(investigation);
    setPageView("workspace");
  } catch (error) {
    openWelcomeActionMessage(activeLocaleText("ההצטרפות נכשלה", "Could not join"), error.message || "");
  }
}

function renderWelcomePage() {
  if (!myInvestigationsList || !myInvestigationsCount || !invitedInvestigationsList || !invitedInvestigationsCount || !similarInvestigationsList || !similarInvestigationsCount) return;
  const investigations = state.investigations;
  const ownedInvestigations = investigations.filter(investigation => !isInvitedWelcomeInvestigation(investigation));
  myInvestigationsCount.textContent = ownedInvestigations.length.toLocaleString(currentLocaleTag());
  myInvestigationsList.innerHTML = ownedInvestigations.length
    ? ownedInvestigations.map(ownedInvestigationRibbonHtml).join("")
    : `<p class="welcome-empty-investigations">${escapeHtml(state.investigationsError
      ? activeLocaleText(`לא ניתן לטעון את החקירות: ${state.investigationsError}`, `Could not load investigations: ${state.investigationsError}`)
      : activeLocaleText("אין עדיין חקירות. התחילו חקירת טיוטה או צרו חקירה בכפתור + שבכותרת.", "No investigations yet. Start a draft investigation, or create one with the + button in the header."))}</p>`;
  const invitedInvestigations = welcomeInvitedInvestigations();
  const similarInvestigations = welcomeSimilarInvestigations();
  invitedInvestigationsCount.textContent = invitedInvestigations.length.toLocaleString(currentLocaleTag());
  invitedInvestigationsList.innerHTML = invitedInvestigations.map(similarInvestigationRibbonHtml).join("");
  similarInvestigationsCount.textContent = similarInvestigations.length.toLocaleString(currentLocaleTag());
  similarInvestigationsList.innerHTML = similarInvestigations.map(similarInvestigationRibbonHtml).join("");
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
  renderMichlolTeam();
  renderInvestigationSelector();
  if (showingWelcome) {
    renderWelcomePage();
    if (options.focus !== false) document.getElementById("welcomeTitle")?.focus?.();
    return;
  }
  window.requestAnimationFrame(() => {
    state.map?.resize();
    window.requestAnimationFrame(() => state.map?.resize());
  });
  if (options.focus !== false) layerSelectorSearch?.focus();
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

function openWelcomeActionMessage(title, description) {
  if (!welcomeActionModal) return;
  welcomeActionTitle.textContent = title;
  welcomeActionDescription.textContent = description;
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
  const duplicate = Boolean(findInvestigationByName(name));
  if (duplicate) {
    showDraftCreateError(activeLocaleText("שם החקירה כבר קיים.", "That investigation name already exists."));
    draftInvestigationName?.focus();
    return;
  }
  draftCreateSubmit.disabled = true;
  draftCreateSubmit.textContent = activeLocaleText("יוצר...", "Creating...");
  showDraftCreateError();
  try {
    const investigation = await createInvestigation(name, state.investigationId);
    state.investigationId = investigation.id;
    state.investigationName = investigation.name;
    state.draftSessionActive = false;
    saveActiveInvestigation();
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
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || activeLocaleText(`יצירת החקירה נכשלה (${response.status})`, `Could not save the investigation (${response.status})`));
  return payload;
}

// GET /api/investigations is the source of truth for the user's investigation list.
async function loadInvestigations() {
  try {
    LEGACY_INVESTIGATIONS_STORAGE_KEYS.forEach(key => scenarioStorage.removeItem(key));
  } catch (error) {
    // Old browser state is optional.
  }
  try {
    const response = await fetch(buildLocaleApiUrl("/api/investigations"), { cache: "no-store" });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(payload.error || `investigations unavailable (${response.status})`);
    const seen = new Set();
    state.investigations = (Array.isArray(payload?.investigations) ? payload.investigations : [])
      .map(investigationFromServer)
      .filter(item => item && !seen.has(item.id) && seen.add(item.id));
    state.investigationsError = "";
  } catch (error) {
    state.investigations = [];
    state.investigationsError = error.message || activeLocaleText("טעינת החקירות נכשלה", "Failed to load investigations");
  }
  const remembered = storedActiveInvestigationId();
  const active = state.investigations.find(item => item.id === remembered) || state.investigations[0] || null;
  state.investigationId = active?.id || "";
  state.investigationName = active?.name || "";
  state.draftSessionActive = false;
  renderInvestigationSelector();
  renderWelcomePage();
}

function matchingInvestigations(query) {
  const key = investigationNameKey(query);
  if (!key) return state.investigations;
  return state.investigations.filter(item => investigationNameKey(item.name).includes(key));
}

function renderInvestigationSelector() {
  if (!investigationInput || !investigationList) return;
  if (memoryButton) memoryButton.hidden = !roleWorkspaceSelectionAvailable() || !state.investigationId;
  if (document.activeElement !== investigationInput) {
    investigationInput.value = state.investigationName || "";
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
  if (!investigation) return;
  state.investigationId = investigation.id;
  state.investigationName = investigation.name;
  state.draftSessionActive = false;
  state.pendingDraftMemoryAction = null;
  state.investigationSelectorOpen = false;
  state.investigationSearchQuery = "";
  state.investigationMemoryLoadToken += 1;
  state.investigationMemory = null;
  state.investigationMemoryError = "";
  state.investigationMemoryLoading = false;
  if (investigationInput) investigationInput.value = investigation.name;
  saveActiveInvestigation();
  resetInvestigation();
  renderInvestigationSelector();
  void loadInvestigationMemory({ restoreLayers: true });
  if (options.focusInput) investigationInput?.focus();
}

async function addOrSelectInvestigation() {
  const name = normalizeInvestigationName(investigationInput?.value) || defaultInvestigationName();
  if (investigationAddButton?.disabled) return;
  if (investigationAddButton) investigationAddButton.disabled = true;
  try {
    const investigation = await ensureInvestigationRecord(name);
    selectInvestigation(investigation, { focusInput: true });
  } catch (error) {
    if (investigationInput) investigationInput.title = error.message || "";
    console.warn("Could not create the investigation", error);
    renderInvestigationSelector();
  } finally {
    if (investigationAddButton) investigationAddButton.disabled = false;
  }
}

// A draft is an unsaved workspace: the analyst can open layers and look around, and is asked to
// name (create) the investigation before anything is saved to memory.
function startDraftInvestigation() {
  state.investigationId = createInvestigationId();
  state.investigationName = "";
  state.draftSessionActive = true;
  state.pendingDraftMemoryAction = null;
  resetInvestigation();
  setPageView("workspace", { focus: false });
  layerSelectorSearch?.focus();
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
    .filter(layer => roleWorkspaceAllowsCatalogLayer(layer.id))
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
  }
}

async function openCatalogLayer(layerId, options = {}) {
  if (!options.roleDefault && !options.memoryRestore && !roleWorkspaceAllowsCatalogLayer(layerId)) return null;
  const layer = state.layerCatalog.find(item => item.id === layerId);
  const filters = options.filters || options.savedLayer?.catalog_filters || {};
  const scopeKey = JSON.stringify(Object.fromEntries(Object.keys(filters).sort().map(key =>
    [key, Array.isArray(filters[key]) ? [...filters[key]].sort() : filters[key]])));
  if (!layer || state.openingLayerIds.has(layerId)) return null;
  const existing = state.layers.find(item => item.catalogLayerId === layerId && (item.catalogScopeKey || "{}") === scopeKey);
  if (existing) {
    existing.visible = true;
    state.activeLayerId = existing.id;
    state.rawOverlayMinimized = false;
    state.layerSearchQuery = "";
    state.layerSearchOpen = false;
    if (options.savedLayer) applySavedFiltersToLayer(existing, options.savedLayer);
    if (!options.silent && existing.kind === "events" && !existing.capabilities.map) activateView("table");
    if (!options.silent) {
      renderAllViews();
      renderLayerSelector();
    }
    return existing;
  }

    state.openingLayerIds.add(layerId);
    renderLayerSelector();
  try {
    const url = new URL(buildLocaleApiUrl(`/api/layers/${encodeURIComponent(layerId)}/rows`), window.location.href);
    if (scopeKey !== "{}") url.searchParams.set("filters", scopeKey);
    const response = await fetch(url.toString(), { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("טעינת נתוני השכבה נכשלה", "Failed to load layer data"));
    const openedLayer = buildCatalogLayer(payload.layer || layer, payload.rows || []);
    openedLayer.catalogFilters = filters;
    openedLayer.catalogScopeKey = scopeKey;
    if (scopeKey !== "{}") {
      openedLayer.dataId = `${layerId}:${scopeKey}`;
      openedLayer.label += activeLocaleText(" · מסונן", " · filtered");
    }
    const added = addResultLayers({
      sourceId: `catalog:${layerId}:${scopeKey}`,
      sourceLabel: openedLayer.label,
      preferredView: isCallsLayer(openedLayer) ? "timeline" : ["entity_metadata", "person_entities"].includes(openedLayer.kind) ? "table" : openedLayer.capabilities.map ? "map" : (openedLayer.kind === "events" ? "table" : (openedLayer.capabilities.timeline ? "timeline" : "table")),
      layers: [openedLayer]
    });
    const restoredLayer = added.find(item => item.catalogLayerId === layerId && item.catalogScopeKey === scopeKey)
      || state.layers.find(item => item.catalogLayerId === layerId && item.catalogScopeKey === scopeKey)
      || null;
    if (restoredLayer && options.savedLayer) applySavedFiltersToLayer(restoredLayer, options.savedLayer);
    state.rawOverlayMinimized = false;
    state.layerSearchQuery = "";
    state.layerSearchOpen = false;
    if (!options.silent && isCallsLayer(openedLayer)) activateView("timeline");
    else if (!options.silent && ["entity_metadata", "person_entities"].includes(openedLayer.kind)) activateView("table");
    else if (!options.silent && !openedLayer.capabilities.map) activateView(openedLayer.kind === "events" ? "table" : (openedLayer.capabilities.timeline ? "timeline" : "table"));
    if (!options.silent) renderAllViews();
    return restoredLayer;
  } catch (error) {
    console.error(`Failed to open catalog layer ${layerId}: ${error?.stack || error}`);
    state.layerCatalogError = error.message || "טעינת נתוני השכבה נכשלה";
    return null;
  } finally {
    state.openingLayerIds.delete(layerId);
    if (!options.silent) {
      renderLayerSelector();
    }
  }
}

function satelliteReferenceLayer(layer) {
  return layer?.type === "line" && ["transportation", "boundary"].includes(layer["source-layer"]);
}

function setMapBasemap(mode) {
  if (!state.map?.getLayer("satellite-imagery")) return;
  const satellite = mode === "satellite";
  state.basemapMode = satellite ? "satellite" : "street";
  for (const layer of state.basemapLayers || []) {
    if (!state.map.getLayer(layer.id)) continue;
    if (satelliteReferenceLayer(layer)) {
      state.map.setLayoutProperty(layer.id, "visibility", layer.layout?.visibility || "visible");
      const boundary = layer["source-layer"] === "boundary";
      state.map.setPaintProperty(layer.id, "line-color", satellite
        ? (boundary ? "rgba(255,255,255,0.82)" : "rgba(255,215,112,0.82)")
        : layer.paint?.["line-color"]);
      state.map.setPaintProperty(layer.id, "line-opacity", satellite
        ? (boundary ? 0.72 : 0.68)
        : layer.paint?.["line-opacity"]);
    } else if (layer.type !== "symbol") {
      state.map.setLayoutProperty(layer.id, "visibility", satellite ? "none" : (layer.layout?.visibility || "visible"));
    } else if (layer.layout?.["text-field"]) {
      state.map.setPaintProperty(layer.id, "text-color", satellite ? "#ffffff" : (layer.paint?.["text-color"] ?? "#000000"));
      state.map.setPaintProperty(layer.id, "text-halo-color", satellite ? "#202b35" : (layer.paint?.["text-halo-color"] ?? "rgba(0,0,0,0)"));
      state.map.setPaintProperty(layer.id, "text-halo-width", satellite ? 1.5 : (layer.paint?.["text-halo-width"] ?? 0));
    }
  }
  state.map.setLayoutProperty("satellite-imagery", "visibility", satellite ? "visible" : "none");
  document.querySelectorAll("[data-basemap]").forEach(button => {
    button.disabled = false;
    button.setAttribute("aria-pressed", String(button.dataset.basemap === state.basemapMode));
  });
  const status = document.getElementById("basemapStatus");
  if (status) status.hidden = true;
}

function initMap() {
  state.map = new maplibregl.Map({
    container: "map",
    style: "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
    center: demoRuntime?.demo_profile?.map.center || [20.82, 42.92],
    zoom: demoRuntime?.demo_profile?.map.zoom ?? 8.4,
    minZoom: demoRuntime?.demo_profile?.map.minZoom ?? 6.0,
    maxZoom: 15,
    maxBounds: demoRuntime?.demo_profile?.map.maxBounds || [[19.0, 41.0], [22.2, 44.0]],
    attributionControl: true
  });
  state.map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-left");
  state.map.on("style.load", () => {
    state.basemapLayers = state.map.getStyle().layers.map(layer => JSON.parse(JSON.stringify(layer)));
    state.map.addSource("satellite-imagery", {
      type: "raster",
      tiles: ["https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],
      tileSize: 256,
      maxzoom: 19,
      attribution: 'Imagery &copy; <a href="https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9" target="_blank" rel="noopener">Esri</a>, Vantor, Earthstar Geographics, GIS User Community'
    });
    const firstLabel = state.basemapLayers.find(layer => layer.type === "symbol")?.id;
    state.map.addLayer({ id: "satellite-imagery", type: "raster", source: "satellite-imagery", layout: { visibility: "none" } }, firstLabel);
    // Keep the style's vector road and administrative-boundary references above
    // the imagery while leaving terrain, land use, and water below it.
    for (const layer of state.basemapLayers.filter(satelliteReferenceLayer)) {
      state.map.moveLayer(layer.id, firstLabel);
    }
    // Override zoom-dependent native labels so English stays selected when zooming in.
    for (const layer of state.map.getStyle().layers) {
      if (layer.type !== "symbol" || !JSON.stringify(layer.layout?.["text-field"] || "").includes("name")) continue;
      state.map.setLayoutProperty(layer.id, "text-field", ["coalesce",
        ["case", ["!=", ["get", "name_en"], ""], ["get", "name_en"], null],
        ["get", "name:en"], ["get", "name:latin"], ["get", "name"]]);
    }
    setMapBasemap(state.basemapMode || "satellite");
  });
  document.querySelectorAll("[data-basemap]").forEach(button => {
    button.addEventListener("click", () => setMapBasemap(button.dataset.basemap));
  });
  state.map.on("error", event => {
    if (event.sourceId !== "satellite-imagery" || state.basemapMode !== "satellite") return;
    setMapBasemap("street");
    const status = document.getElementById("basemapStatus");
    if (status) {
      status.textContent = activeLocaleText("תצלומי הלוויין אינם זמינים כרגע. מוצגת מפת רחובות.", "Satellite imagery is currently unavailable. Showing Street map.");
      status.hidden = false;
    }
  });
  state.polygonDraw = new PolygonDrawControl(state.map, document.getElementById("polygonDrawButton"), document.getElementById("polygonDrawHint"), { onContextMenu: polygon => openPolygonActionMenu(polygon) });
  const overlay = document.getElementById("rawEventsOverlay");
  const positionDrawControl = () => {
    const height = !overlay.hidden && getComputedStyle(overlay).display !== "none" ? overlay.getBoundingClientRect().height : 0;
    document.getElementById("mapView").style.setProperty("--draw-bottom", `${height + 34}px`);
  };
  new ResizeObserver(positionDrawControl).observe(overlay);
  new MutationObserver(positionDrawControl).observe(overlay, {attributes:true,attributeFilter:["hidden","class","style"]});
  state.map.on("load", () => { state.mapReady = true; renderMap(); });
}

let objectViewerReturnFocus = null;
let objectViewerDockTarget = null;

function viewerObjects() {
  const objects = new Map();
  state.events.forEach(item => objects.set(`record:${item.record_id || item.event_id}`, item));
  const addEntity = item => {
    if (!item?.entity_id) return;
    const kind = isPersonEntity(item) ? "person" : "organization";
    objects.set(`${kind}:${item.entity_id}`, item);
  };
  state.entityDirectory.forEach(addEntity);
  state.entityMetadata.forEach(addEntity);
  state.layers.forEach(layer => {
    if (layer.kind === "events") (layer.items || []).forEach(item => objects.set(`record:${item.record_id || item.event_id}`, item));
    if (layer.kind === "evidence") (layer.items || []).forEach(item => {
      if (item.evidence_type === "ipdr_package") objects.set(`ipdr_package:${item.package_id}`, item);
      else objects.set(`evidence:${item.evidence_id}`, item);
    });
    if (layer.kind === "assessments") (layer.items || []).forEach(item => objects.set(`assessment:${item.assessment_id}`, item));
    if (["entity_metadata", "person_entities"].includes(layer.kind)) (layer.items || []).forEach(addEntity);
  });
  return objects;
}

function safeMediaUrl(value) {
  const text = String(value || "").trim();
  if (!text) return "";
  try {
    const url = new URL(text, window.location.href);
    return ["http:", "https:"].includes(url.protocol) || (url.origin === window.location.origin && url.protocol === window.location.protocol) ? url.href : "";
  } catch { return ""; }
}

function viewerMedia(item) {
  const candidates = [
    ["video", item.video_url || item.media?.video_url],
    ["audio", item.audio_url || item.media?.audio_url],
    ["image", item.image_url || item.media?.image_url]
  ];
  return candidates.map(([type, value]) => ({ type, url: safeMediaUrl(value) })).find(media => media.url) || null;
}

function isUavVideoRecord(item) {
  return item.collection_family === "airborne_isr_video_exploitation" || Boolean(item.video_segment_id);
}

function isCellularCallRecord(item) {
  return item.collection_family === "scenario_cellular_call_collection" || Boolean(item.call_id);
}

function isVisualCollectionRecord(item) {
  const source = String(item?.source_type || "").trim().toLowerCase();
  return source === "satellite" || source === "cctv";
}

function cellularCallPartyHtml(item, side) {
  const prefix = side === "a" ? "side_a" : "side_b";
  const label = side === "a" ? activeLocaleText("צד א׳", "Side A") : activeLocaleText("צד ב׳", "Side B");
  const location = item[`${prefix}_location_name`] || item[`${prefix}_location_id`] || activeLocaleText("לא ידוע", "Unknown");
  const number = item[`${prefix}_sim`] || item[`${prefix}_number`] || activeLocaleText("לא ידוע", "Unknown");
  const imei = item[`${prefix}_imei`] || activeLocaleText("לא ידוע", "Unknown");
  const person = item[`${prefix}_entity_name`] || "";
  return `<article class="cellular-call-party cellular-call-party-${side}">
    <span class="cellular-call-party-label">${escapeHtml(label)}</span>${person ? `<strong class="cellular-call-party-person">${escapeHtml(person)}</strong>` : ""}
    <dl><div><dt>${escapeHtml((item[`${prefix}_sim`] ? "SIM" : activeLocaleText("מספר", "Number")))}</dt><dd dir="ltr">${escapeHtml(number)}</dd></div>
    <div><dt>IMEI</dt><dd dir="ltr">${escapeHtml(imei)}</dd></div>
    <div><dt>${escapeHtml(activeLocaleText("מיקום", "Location"))}</dt><dd>${escapeHtml(location)}</dd></div></dl>
  </article>`;
}

let cellularViewerMap = null;
let entityViewerMap = null;

function cellularCallHtml(item) {
  if (!isCellularCallRecord(item)) return "";
  const audioUrl = safeMediaUrl(item.audio_url || item.media?.audio_url);
  const original = item.call_transcript_original || item.call_transcript || "";
  const translations = String(item.call_transcript_en || "").split(/\n\s*\n/).filter(Boolean);
  const paragraphs = String(original).split(/\n\s*\n/).filter(Boolean);
  const bubbles = paragraphs.map((text, index) => {
    const match = text.match(/^([^:]+):\s*([\s\S]*)$/);
    const speaker = match ? match[1] : "";
    const side = speaker.startsWith("IMEI") ? "a" : speaker ? "b" : "note";
    const translated = translations[index] || "";
    const translation = translated.replace(/^[^:]+:\s*/, "");
    const transcriptLanguage = /arabic|persian/i.test(item.call_language || "") ? "ar" : "en";
    return `<article class="call-bubble call-bubble-${side}">${speaker ? `<header>${escapeHtml(speaker)}</header>` : ""}<p lang="${transcriptLanguage}" dir="auto">${escapeHtml(match ? match[2] : text)}</p>${translation && translation !== (match ? match[2] : text) ? `<p class="call-translation" lang="en" dir="ltr">${escapeHtml(translation)}</p>` : ""}</article>`;
  }).join("");
  const duration = Number(item.call_duration_seconds || 0);
  const callLocation = cellularCallMapLocation(item, "a");
  const callLocationLabel = callLocation
    ? `${callLocation.name} · ${callLocation.lat.toFixed(6)}, ${callLocation.lon.toFixed(6)}`
    : activeLocaleText("מיקום שיחה לא ידוע", "Call location unavailable");
  const summary = String(item.event_summary || "").trim();
  return `<section class="call-workspace" aria-label="Cellular call analysis">
    <div class="call-main"><section class="call-map-panel"><div id="callViewerMap" aria-label="Call location map"></div><div class="call-map-caption"><span class="material-symbols-rounded">location_on</span><span dir="ltr">${escapeHtml(callLocationLabel)}</span><button type="button" id="callFitMap">Fit location</button></div></section>
    <section class="call-conversation"><header class="call-conversation-heading"><span class="material-symbols-rounded">forum</span><h3>Conversation</h3><span class="call-conversation-id" dir="ltr">${escapeHtml(item.event_id || item.record_id)} · ${duration ? `${duration.toFixed(1)}s` : "—"}</span><label><input id="callTranslationToggle" type="checkbox" checked> English translation</label></header>${summary ? `<section class="call-summary"><h4>${escapeHtml(activeLocaleText("סיכום שיחה", "Call summary"))}</h4><p>${escapeHtml(summary)}</p></section>` : ""}
    <div class="call-transcript-scroll">${bubbles || '<p class="call-empty">No transcript supplied for this call.</p>'}</div><p class="call-timing-note">${paragraphs.length ? 'Transcript order is preserved. Per-line timestamps were not supplied.' : 'Open Call 1 to view its supplied recording and transcripts.'}</p></section></div>
    <footer class="call-player"><div><span class="material-symbols-rounded">graphic_eq</span><strong>${audioUrl ? 'Supplied recording' : 'Recording unavailable'}</strong></div>${audioUrl ? `<audio controls autoplay preload="auto" src="${escapeHtml(audioUrl.endsWith("/call-1.mp3") ? audioUrl.replace(/\.mp3$/, ".wav") : audioUrl)}" aria-label="Call recording"></audio>` : '<p>No audio attached to this record.</p>'}</footer>
    <p class="call-provenance">${escapeHtml(item.call_media_origin || 'Scenario collection record.')}</p>
  </section>`;
}

function startCellularCallAudio() {
  const audio = document.querySelector("#objectViewer .call-player audio");
  if (!audio) return;
  const playback = audio.play();
  if (playback?.catch) playback.catch(() => {
    audio.dataset.autoplayBlocked = "true";
  });
}

function initializeCellularViewer(item) {
  const toggle = document.getElementById("callTranslationToggle");
  toggle?.addEventListener("change", () => document.querySelectorAll(".call-translation").forEach(el => { el.hidden = !toggle.checked; }));
  const points = ["a","b"].map(side => ({side,...cellularCallMapLocation(item,side)})).filter(p => Number.isFinite(p.lon) && Number.isFinite(p.lat));
  const container = document.getElementById("callViewerMap");
  if (!points.length || typeof maplibregl === "undefined") { container.textContent = "Location map unavailable"; return; }
  const map = new maplibregl.Map({container,style:{version:8,sources:{imagery:{type:"raster",tiles:["https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],tileSize:256,attribution:"Imagery © Esri, Vantor, Earthstar Geographics"}},layers:[{id:"imagery",type:"raster",source:"imagery"}]},center:[points[0].lon,points[0].lat],zoom:8});
  cellularViewerMap = map;
  map.addControl(new maplibregl.NavigationControl({showCompass:false}),"top-left");
  const bounds = new maplibregl.LngLatBounds();
  for (const point of points) {
    bounds.extend([point.lon,point.lat]);
    const marker = document.createElement("button");marker.type="button";marker.className=`cellular-call-map-endpoint cellular-call-map-endpoint-${point.side}`;marker.textContent=point.side.toUpperCase();marker.setAttribute("aria-label",`Side ${point.side.toUpperCase()}: ${point.name}`);
    new maplibregl.Marker({element:marker}).setLngLat([point.lon,point.lat]).setPopup(new maplibregl.Popup().setText(`Side ${point.side.toUpperCase()} · ${point.name}`)).addTo(map);
  }
  const fit=()=>map.fitBounds(bounds,{padding:Math.max(12,Math.min(48,container.clientHeight / 4,container.clientWidth / 4)),maxZoom:13,duration:0});
  map.on("load",()=>{map.resize();fit();});
  document.getElementById("callFitMap")?.addEventListener("click",fit);
}

function viewerMediaHtml(item) {
  if (isCellularCallRecord(item)) return "";
  let series = item.image_series || [];
  if (typeof series === "string") {
    try { series = JSON.parse(series); } catch { series = []; }
  }
  if (!Array.isArray(series)) series = [];
  const demoMedia = item.demo_media === true || item.demo_media === "true";
  const disclaimer = demoMedia ? `<p class="object-viewer-media-context">${escapeHtml(activeLocaleText("מדיית הדגמה.", "Demo media."))}</p>` : "";
  const fullscreenButton = isVisualCollectionRecord(item)
    ? `<button type="button" class="visual-media-fullscreen" data-visual-media-fullscreen title="${escapeHtml(activeLocaleText("הרחב מדיה למסך מלא", "Expand media to full screen"))}" aria-label="${escapeHtml(activeLocaleText("הרחב מדיה למסך מלא", "Expand media to full screen"))}"><span class="material-symbols-rounded" aria-hidden="true">open_in_full</span></button>`
    : "";
  const images = series.map(capture => {
    const url = safeMediaUrl(capture?.image_url);
    if (!url) return "";
    const pair = [{url, timestamp: capture.timestamp_utc, location: capture.location_id}];
    const captures = pair.map(entry => `<div><div class="object-viewer-media"><img loading="lazy" src="${escapeHtml(entry.url)}" alt="${escapeHtml(activeLocaleText("תמונת לוויין", "Satellite capture"))}">${fullscreenButton}</div><small>${escapeHtml(entry.location || "")} · <time>${escapeHtml(entry.timestamp || "")}</time></small></div>`).join("");
    return `<figure><figcaption><strong>${escapeHtml(capture.pair_id || "")}</strong><p>${escapeHtml(capture.description || "")}</p></figcaption><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px">${captures}</div>${capture.paired_record_id ? `<small>${escapeHtml(activeLocaleText("רשומה תואמת", "Paired record"))}: ${escapeHtml(capture.paired_record_id)}</small>` : ""}</figure>`;
  }).join("");
  if (images) return `<section class="object-viewer-source-media"><h3>${escapeHtml(series.length === 1 ? activeLocaleText("תמונת לוויין", "Satellite image") : activeLocaleText("תמונות לוויין לאורך זמן", "Satellite captures over time"))}</h3>${disclaimer}${images}</section>`;
  const media = viewerMedia(item);
  const mediaElement = media?.type === "video"
    ? `<video controls preload="metadata" src="${escapeHtml(media.url)}"></video>`
    : media?.type === "audio"
      ? `<audio controls preload="metadata" src="${escapeHtml(media.url)}"></audio>`
      : media?.type === "image"
        ? `<img src="${escapeHtml(media.url)}" alt="">`
        : "";
  if (!isUavVideoRecord(item)) return mediaElement ? `${disclaimer}<div class="object-viewer-media">${mediaElement}${fullscreenButton}</div>` : "";

  const mission = item.mission_id || activeLocaleText("משימה לא מזוהה", "Unidentified mission");
  const segment = item.video_segment_id || activeLocaleText("מקטע לא מזוהה", "Unidentified segment");
  return `<section class="object-viewer-source-media" aria-labelledby="objectViewerMediaTitle">
    <div class="object-viewer-section-heading">
      <div><span class="eyebrow">${escapeHtml(activeLocaleText("תצוגת מקור", "Source visualization"))}</span><h3 id="objectViewerMediaTitle">${escapeHtml(activeLocaleText("זרם וידאו מכטב״ם", "UAV video stream"))}</h3></div>
      <span class="object-viewer-live-badge"><i></i>${escapeHtml(activeLocaleText("הצגה", "Display"))}</span>
    </div>
    <div class="object-viewer-media object-viewer-simulated-media"><canvas id="objectViewerUavCanvas" width="720" height="405" role="img" aria-label="${escapeHtml(activeLocaleText("תצוגת וידאו אווירי", "Aerial-video visualization"))}"></canvas><span class="uav-simulation-label">ISR</span></div>
    <div class="object-viewer-media-context"><span><b>${escapeHtml(activeLocaleText("משימה", "Mission"))}</b><code dir="ltr">${escapeHtml(mission)}</code></span><span><b>${escapeHtml(activeLocaleText("מקטע", "Segment"))}</b><code dir="ltr">${escapeHtml(segment)}</code></span></div>
    <p>${escapeHtml(activeLocaleText("תצוגה חזותית למשימת האיסוף. הרשומה היא תצפית אנליטית שנגזרה ממקור הווידאו.", "Collection-mission visualization. The record is an analytical observation derived from the video source."))}</p>
  </section>`;
}

// Media URLs carried on rows may be stale (the bundled demo media was removed). When a viewer's media
// is missing or fails to load, ask the platform for the record's files (signed URLs) and use those;
// if there are none, show the viewer's missing-media state instead of a broken player.
const recordFilesRequests = new Map();

function recordFileUrls(recordId) {
  const id = String(recordId || "").trim();
  if (!id) return Promise.resolve([]);
  if (!recordFilesRequests.has(id)) {
    recordFilesRequests.set(id, fetch(`/api/records/${encodeURIComponent(id)}/files`, { cache: "no-store" })
      .then(response => response.ok ? response.json() : { files: [] })
      .then(payload => (Array.isArray(payload?.files) ? payload.files : [])
        .map(file => ({ url: safeMediaUrl(file?.signed_url || file?.url), type: String(file?.content_type || file?.mime_type || file?.file_name || file?.name || "").toLowerCase() }))
        .filter(file => file.url))
      .catch(() => []));
  }
  return recordFilesRequests.get(id);
}

function recordFileMediaType(file) {
  const hint = `${file.type} ${file.url.split("?")[0].toLowerCase()}`;
  if (/video|\.(mp4|webm|mov|m4v)\b/.test(hint)) return "video";
  if (/audio|\.(mp3|wav|ogg|m4a|aac)\b/.test(hint)) return "audio";
  return "image";
}

function missingMediaHtml(item) {
  return isCellularCallRecord(item)
    ? `<div><span class="material-symbols-rounded">graphic_eq</span><strong>${escapeHtml(activeLocaleText("ההקלטה אינה זמינה", "Recording unavailable"))}</strong></div><p>${escapeHtml(activeLocaleText("לא צורף שמע לרשומה זו.", "No audio attached to this record."))}</p>`
    : `<p class="object-viewer-media-missing">${escapeHtml(activeLocaleText("המדיה של רשומה זו אינה זמינה.", "Media for this record is unavailable."))}</p>`;
}

function showMissingMedia(element, item) {
  const player = element.closest(".call-player");
  if (player) {
    player.innerHTML = missingMediaHtml(item);
    return;
  }
  const container = element.closest(".object-viewer-media") || element;
  container.outerHTML = missingMediaHtml(item);
}

function initializeViewerMediaFallback(item, recordId) {
  const body = document.getElementById("objectViewerBody");
  if (!body) return;
  const stillOpen = () => document.getElementById("objectViewerId")?.textContent === String(recordId) && !document.getElementById("objectViewer")?.hidden;
  const elements = [...body.querySelectorAll("video[src], audio[src], img[src]")];
  elements.forEach((element, index) => {
    element.addEventListener("error", async () => {
      if (element.dataset.mediaFallback === "tried") {
        if (stillOpen()) showMissingMedia(element, item);
        return;
      }
      element.dataset.mediaFallback = "tried";
      const files = await recordFileUrls(recordId);
      if (!stillOpen() || !element.isConnected) return;
      const file = files[index] || files[0];
      if (file) element.src = file.url;
      else showMissingMedia(element, item);
    });
  });
  const hasI360Media = Boolean(item["i360.media.kind"] || item["i360.media.file_count"]);
  if (elements.length || !(isCellularCallRecord(item) || isVisualCollectionRecord(item) || hasI360Media)) return;
  void recordFileUrls(recordId).then(files => {
    if (!files.length || !stillOpen()) return;
    const file = files[0];
    const type = recordFileMediaType(file);
    const player = body.querySelector(".call-player");
    if (player && type === "audio") {
      player.innerHTML = `<div><span class="material-symbols-rounded">graphic_eq</span><strong>${escapeHtml(activeLocaleText("הקלטה", "Recording"))}</strong></div><audio controls preload="metadata" src="${escapeHtml(file.url)}"></audio>`;
      return;
    }
    if (player) return;
    const media = type === "video"
      ? `<video controls preload="metadata" src="${escapeHtml(file.url)}"></video>`
      : type === "audio" ? `<audio controls preload="metadata" src="${escapeHtml(file.url)}"></audio>` : `<img src="${escapeHtml(file.url)}" alt="">`;
    const expandLabel = escapeHtml(activeLocaleText("הרחב מדיה למסך מלא", "Expand media to full screen"));
    const fullscreenButton = type === "audio" ? "" : `<button type="button" class="visual-media-fullscreen" data-visual-media-fullscreen title="${expandLabel}" aria-label="${expandLabel}"><span class="material-symbols-rounded" aria-hidden="true">open_in_full</span></button>`;
    body.insertAdjacentHTML("afterbegin", `<div class="object-viewer-media">${media}${fullscreenButton}</div>`);
  });
}

let visualMediaOverlayTrigger = null;

function closeVisualCollectionMediaFullscreen({ restoreFocus = true } = {}) {
  const overlay = document.getElementById("visualMediaOverlay");
  const content = document.getElementById("visualMediaOverlayContent");
  if (!overlay || overlay.hidden) return;
  content?.querySelectorAll("video,audio").forEach(media => media.pause());
  if (content) content.replaceChildren();
  overlay.hidden = true;
  document.body.classList.remove("visual-media-overlay-open");
  const trigger = visualMediaOverlayTrigger;
  visualMediaOverlayTrigger = null;
  if (restoreFocus) trigger?.focus();
}

function toggleVisualCollectionMediaFullscreen(trigger) {
  const media = trigger.closest(".object-viewer-media");
  const source = media?.querySelector("img,video");
  const overlay = document.getElementById("visualMediaOverlay");
  const content = document.getElementById("visualMediaOverlayContent");
  const closeButton = document.getElementById("visualMediaOverlayClose");
  if (!source || !overlay || !content || !closeButton) return;
  const closeLabel = activeLocaleText("סגור מדיה מוגדלת", "Close expanded media");
  overlay.querySelector(".visual-media-overlay-dialog")?.setAttribute("aria-label", activeLocaleText("מדיית מקור מוגדלת", "Expanded source media"));
  closeButton.setAttribute("aria-label", closeLabel);
  closeButton.title = closeLabel;
  const expandedMedia = source.cloneNode(true);
  expandedMedia.removeAttribute("id");
  expandedMedia.removeAttribute("loading");
  if (expandedMedia.tagName === "VIDEO") expandedMedia.controls = true;
  content.replaceChildren(expandedMedia);
  visualMediaOverlayTrigger = trigger;
  overlay.hidden = false;
  document.body.classList.add("visual-media-overlay-open");
  closeButton.focus();
}

let objectViewerUavAnimation = 0;

function stopSimulatedUavStream() {
  if (objectViewerUavAnimation) cancelAnimationFrame(objectViewerUavAnimation);
  objectViewerUavAnimation = 0;
}

function startSimulatedUavStream(item) {
  stopSimulatedUavStream();
  const canvas = document.getElementById("objectViewerUavCanvas");
  if (!canvas) return;
  const context = canvas.getContext("2d");
  if (!context) return;
  const seedText = String(item.mission_id || "UAV-MISSION");
  const seed = [...seedText].reduce((value, character) => (value * 31 + character.charCodeAt(0)) >>> 0, 2166136261);
  const startedAt = performance.now();
  const draw = now => {
    const time = (now - startedAt) / 1000;
    const width = canvas.width;
    const height = canvas.height;
    context.fillStyle = "#65705c";
    context.fillRect(0, 0, width, height);
    for (let index = 0; index < 34; index += 1) {
      const x = (seed * (index + 3) % width + Math.sin(time * .08 + index) * 16 + width) % width;
      const y = (seed * (index + 11) % height + Math.cos(time * .06 + index) * 12 + height) % height;
      const radius = 18 + (seed + index * 19) % 56;
      context.fillStyle = index % 3 ? "rgba(43,54,39,.2)" : "rgba(174,164,126,.16)";
      context.beginPath(); context.arc(x, y, radius, 0, Math.PI * 2); context.fill();
    }
    context.strokeStyle = "rgba(201,193,154,.46)";
    context.lineWidth = 10;
    context.beginPath(); context.moveTo(-20, height * .72); context.bezierCurveTo(width * .24, height * .4, width * .62, height * .84, width + 20, height * .3); context.stroke();
    context.strokeStyle = "rgba(55,62,51,.72)";
    context.lineWidth = 2;
    context.stroke();
    for (let index = 0; index < 4; index += 1) {
      const progress = (time * (13 + index * 2) + index * 142 + seed % 97) % (width + 100) - 50;
      const y = height * .66 - Math.sin((progress / width) * Math.PI * 1.7) * height * .17 + index * 7;
      context.save(); context.translate(progress, y); context.rotate(-.18 + Math.sin(time * .2) * .08); context.fillStyle = "#20251f"; context.fillRect(-13, -6, 26, 12); context.strokeStyle = "rgba(235,238,216,.75)"; context.lineWidth = 1; context.strokeRect(-16, -9, 32, 18); context.restore();
    }
    context.strokeStyle = "rgba(230,236,218,.82)";
    context.lineWidth = 1;
    context.beginPath(); context.arc(width / 2, height / 2, 38, 0, Math.PI * 2); context.moveTo(width / 2 - 62, height / 2); context.lineTo(width / 2 - 14, height / 2); context.moveTo(width / 2 + 14, height / 2); context.lineTo(width / 2 + 62, height / 2); context.moveTo(width / 2, height / 2 - 62); context.lineTo(width / 2, height / 2 - 14); context.moveTo(width / 2, height / 2 + 14); context.lineTo(width / 2, height / 2 + 62); context.stroke();
    context.fillStyle = "rgba(235,240,220,.9)";
    context.font = "18px monospace";
    context.textAlign = "left";
    context.fillText(`ALT  ${Math.round(1780 + Math.sin(time * .3) * 12)} M`, 18, 29);
    context.fillText(`SPD  ${Math.round(84 + Math.cos(time * .25) * 3)} KT`, 18, 54);
    context.textAlign = "right";
    context.fillText(new Date(Date.now()).toISOString().slice(11, 19) + "Z", width - 18, 29);
    context.fillStyle = "rgba(8,12,8,.08)";
    for (let y = 0; y < height; y += 4) context.fillRect(0, y, width, 1);
    objectViewerUavAnimation = requestAnimationFrame(draw);
  };
  objectViewerUavAnimation = requestAnimationFrame(draw);
}

function isCellularGeolocationRecord(item) {
  return item?.source_type === "Cellular Geolocations" || item?.collection_family === "scenario_cellular_geolocation";
}

function isAdintRecord(item) {
  return String(item?.source_type || "").trim().toUpperCase() === "ADINT";
}

const IPDR_SOURCE_FIELDS = ["start_time", "end_time", "ip_source", "ip_target", "ip_public", "ip_private", "ip_out", "source_record_id", "source_port", "target_port", "public_port", "protocol", "bytes_sent", "bytes_received", "source_system", "imei", "mac", "SUBNETMASK"];

function ipdrTableFieldLabel(key) {
  if (key === "event_id") return activeLocaleText("מזהה פנימי", "Canonical record ID");
  if (key === "source_record_id") return activeLocaleText("מזהה מקור", "Source record ID");
  return viewerFieldLabel(key);
}

function isIpdrRecord(item) {
  return String(item?.source_type || "").trim().toUpperCase() === "IPDR";
}

function isPersonEntity(item) {
  return String(item?.entity_type || "").trim().toLowerCase() === "person";
}

function viewerFields(item, kind) {
  // Rows from a profile query with "all_fields" carry every i360 item field as "i360.<path>": show them all.
  const i360Keys = Object.keys(item || {}).filter(key => key.startsWith("i360.") && item[key] != null && item[key] !== "").sort((a, b) => a.localeCompare(b, "en"));
  if (kind === "record" && i360Keys.length) {
    return ["record_id", "source_type", ...i360Keys].filter(key => item[key] != null && item[key] !== "").map(key => [key, item[key]]);
  }
  if (kind === "ipdr_package") return ["package_id", "classification", "provider", "source_system", "filename", "sha256", "record_count", "validation_state", "session_validation_counts", "observed_coverage", "requested_scope", "acquired_at", "imported_at", "ingest_batch_id", "authority_case_reference", "chain_of_custody_note", "field_semantics", "transformations", "limitations"].map(key => [key, item[key] ?? activeLocaleText("לא ידוע", "Unknown")]);
  if (kind === "record" && isCellularGeolocationRecord(item)) return ["event_id", "timestamp_utc", "imei", "sim", "target_msisdn", "target_imsi", "operator_msisdn", "operator_imsi", "location_name"].map(key => [key, item[key] || (key === "location_name" ? item.location_id : "") || "—"]);
  const hidden = new Set(["event_summary", "canonical_name", "media", "image_series", "video_url", "audio_url", "image_url", "raw_data_references", "call_started_at_utc", "call_duration_seconds", "side_a_imei", "side_a_number", "side_a_location_id", "side_a_location_name", "side_b_imei", "side_b_number", "side_b_location_id", "side_b_location_name", "call_transcript", "call_transcript_en", "demo_media"]);
  if (kind === "record" && isIpdrRecord(item)) ["entity_name", "location_name", "location_accuracy_m"].forEach(key => hidden.add(key));
  if (kind === "record" && isAdintRecord(item) && item.device_id) {
    return ["event_id", "device_id", "timestamp_utc", "brand", "model", "os", "keyboard_language", "ip", "latitude", "longitude", "accuracy_m"].map(key => [key, item[key] == null || item[key] === "" ? "—" : item[key]]);
  }
  if (["record", "evidence"].includes(kind) && isIpdrRecord(item) && item.source_record_id) {
    const keys = item.package_id ? ["event_id", "record_type", "package_id", "ingest_batch_id", "source_reference", "validation", ...IPDR_SOURCE_FIELDS] : IPDR_SOURCE_FIELDS;
    return keys.map(key => [key, item[key] == null || item[key] === "" ? "—" : item[key]]);
  }
  const preferred = kind === "person"
    ? ["identity_status", "given_name", "family_name", "gender", "age_years", "date_of_birth", "place_of_birth", "nationality", "ethnicity", "occupation", "residence", "previous_residences", "role", "affiliations", "connections", "military_service", "languages", "associated_entity_ids", "identifiers", "aliases", "event_count", "top_locations", "top_sources", "biographical_notes"]
    : kind === "record"
    ? ["timestamp_utc", "timestamp_basis", "source_type", "collection_family", "source_reliability_label", "certainty_level", "entity_name", "location_name", "advertising_id", "ip_address", "imei", "session_start_utc", "session_end_utc", "source_port", "protocol", "bytes_up", "bytes_down", "location_accuracy_m", "call_id", "observation_id", "mission_id", "video_segment_id"]
    : kind === "evidence"
      ? ["evidence_status", "claim_type", "confidence", "object_class", "subject_entity_ids", "location_ids", "valid_from", "valid_to", "source_groups", "source_record_ids", "quantity", "movement", "created_by_processor"]
    : kind === "assessment"
      ? ["status", "confidence", "scope", "key_judgments", "alternatives", "contradictions", "intelligence_gaps", "indicators", "evidence_ids", "overlays", "revision", "updated_at"]
    : ["entity_type", "aliases", "event_count", "top_locations", "top_sources"];
  return preferred.filter(key => !hidden.has(key) && item[key] != null && item[key] !== "").map(key => [key, item[key]]);
}

function viewerFieldLabel(key) {
  const labels = {
    package_id: ["חבילת ראיות", "Evidence package"],
    evidence_type: ["סוג ראיה", "Evidence type"],
    record_type: ["סוג רשומה", "Record type"],
    ingest_batch_id: ["אצוות קליטה", "Ingest batch"],
    source_reference: ["הפניה למקור", "Source reference"],
    validation: ["בדיקת זמנים", "Session validation"],
    provider: ["ספק", "Provider"],
    filename: ["קובץ מקור", "Source file"],
    sha256: ["חתימת SHA-256", "SHA-256 checksum"],
    record_count: ["מספר רשומות", "Record count"],
    classification: ["סיווג", "Classification"],
    validation_state: ["מצב אימות", "Validation state"],
    session_validation_counts: ["בדיקות זמן", "Session validation counts"],
    observed_coverage: ["טווח נצפה", "Observed coverage"],
    requested_scope: ["היקף מבוקש", "Requested scope"],
    acquired_at: ["זמן קבלה", "Acquisition time"],
    imported_at: ["זמן קליטה", "Import time"],
    authority_case_reference: ["אסמכתת תיק", "Authority/case reference"],
    chain_of_custody_note: ["שרשרת משמורת", "Chain of custody"],
    field_semantics: ["משמעות שדות", "Field semantics"],
    transformations: ["עיבוד", "Transformations"],
    limitations: ["מגבלות", "Limitations"],
    start_time: ["תחילת חיבור", "Start time"],
    end_time: ["סיום חיבור", "End time"],
    ip_source: ["IP מקור", "Source IP"],
    ip_target: ["IP יעד", "Target IP"],
    ip_public: ["IP ציבורי", "Public IP"],
    ip_private: ["IP פרטי", "Private IP"],
    ip_out: ["IP יוצא", "Outbound IP"],
    source_record_id: ["מזהה רשומה", "Record ID"],
    target_port: ["פורט יעד", "Target port"],
    public_port: ["פורט ציבורי", "Public port"],
    bytes_sent: ["בתים שנשלחו", "Bytes sent"],
    bytes_received: ["בתים שהתקבלו", "Bytes received"],
    source_system: ["מערכת מקור", "Source system"],
    mac: ["MAC", "MAC"],
    SUBNETMASK: ["מסכת רשת", "Subnet mask"],
    device_id: ["מזהה מכשיר", "Device ID"],
    brand: ["יצרן", "Brand"],
    model: ["דגם", "Model"],
    os: ["מערכת הפעלה", "OS"],
    keyboard_language: ["שפת מקלדת", "Keyboard language"],
    ip: ["כתובת IP", "IP address"],
    latitude: ["קו רוחב", "Latitude"],
    longitude: ["קו אורך", "Longitude"],
    accuracy_m: ["דיוק במטרים", "Accuracy (m)"],
    advertising_id: ["מזהה פרסום", "Advertising ID"],
    ip_address: ["כתובת IP", "IP address"],
    imei: ["IMEI", "IMEI"],
    sim: ["SIM", "SIM"],
    target_msisdn: ["MSISDN יעד", "Target MSISDN"],
    target_imsi: ["IMSI יעד", "Target IMSI"],
    operator_msisdn: ["MSISDN מפעיל", "Operator MSISDN"],
    operator_imsi: ["IMSI מפעיל", "Operator IMSI"],
    session_start_utc: ["תחילת חיבור", "Session start (UTC)"],
    session_end_utc: ["סיום חיבור", "Session end (UTC)"],
    source_port: ["פורט מקור", "Source port"],
    protocol: ["פרוטוקול", "Protocol"],
    bytes_up: ["בתים שנשלחו", "Bytes uploaded"],
    bytes_down: ["בתים שהתקבלו", "Bytes downloaded"],
    location_accuracy_m: ["דיוק מיקום במטרים", "Location accuracy (m)"],
    timestamp_basis: ["בסיס הזמן", "Timestamp basis"],
    timestamp_utc: ["זמן", "Time"],
    source_type: ["סוג מקור", "Source type"],
    collection_family: ["משפחת איסוף", "Collection family"],
    source_reliability_label: ["אמינות מקור", "Source reliability"],
    certainty_level: ["רמת ודאות", "Confidence"],
    entity_name: ["גורם", "Entity"],
    location_name: ["מיקום", "Location"],
    event_id: ["מזהה רשומה", "Record ID"],
    observation_id: ["מזהה תצפית", "Observation ID"],
    mission_id: ["מזהה משימה", "Mission ID"],
    video_segment_id: ["מזהה מקטע", "Segment ID"],
    call_id: ["מזהה שיחה", "Call ID"],
    entity_type: ["סוג ישות", "Entity type"],
    identity_status: ["מצב זיהוי", "Identity status"],
    given_name: ["שם פרטי", "Given name"],
    family_name: ["שם משפחה", "Family name"],
    gender: ["מגדר", "Gender"],
    age_years: ["גיל", "Age"],
    date_of_birth: ["תאריך לידה", "Date of birth"],
    place_of_birth: ["מקום לידה", "Place of birth"],
    role: ["תפקיד", "Role"],
    occupation: ["עיסוק", "Occupation"],
    affiliations: ["שיוכים", "Affiliations"],
    nationality: ["לאום", "Nationality"],
    ethnicity: ["מוצא", "Ethnicity"],
    languages: ["שפות", "Languages"],
    residence: ["מקום מגורים", "Residence"],
    previous_residences: ["מקומות מגורים קודמים", "Previous residences"],
    connections: ["קשרים", "Connections"],
    military_service: ["שירות צבאי", "Military service"],
    associated_entity_ids: ["ישויות קשורות", "Associated entities"],
    identifiers: ["מזהים", "Identifiers"],
    biographical_notes: ["הערות ביוגרפיות", "Biographical notes"],
    aliases: ["שמות נוספים", "Aliases"],
    event_count: ["מספר רשומות", "Record count"],
    top_locations: ["מיקומים מובילים", "Top locations"],
    top_sources: ["מקורות מובילים", "Top sources"],
    evidence_status: ["מצב ראיה", "Evidence status"],
    claim_type: ["סוג טענה", "Claim type"],
    confidence: ["ביטחון", "Confidence"],
    object_class: ["סוג אובייקט", "Object class"],
    subject_entity_ids: ["ישויות", "Entities"],
    location_ids: ["מיקומים", "Locations"],
    valid_from: ["תקף מ", "Valid from"],
    valid_to: ["תקף עד", "Valid to"],
    source_groups: ["קבוצות מקור", "Source groups"],
    source_record_ids: ["רשומות מקור", "Source records"],
    quantity: ["כמות", "Quantity"],
    movement: ["תנועה", "Movement"],
    created_by_processor: ["מעבד", "Processor"]
    ,status: ["מצב", "Status"]
    ,scope: ["תחום", "Scope"]
    ,key_judgments: ["שיפוטים מרכזיים", "Key judgments"]
    ,alternatives: ["חלופות", "Alternatives"]
    ,contradictions: ["סתירות", "Contradictions"]
    ,intelligence_gaps: ["פערי מודיעין", "Intelligence gaps"]
    ,indicators: ["אינדיקטורים לשינוי", "Change indicators"]
    ,evidence_ids: ["ראיות תומכות", "Supporting evidence"]
    ,overlays: ["גרפיקה אנליטית", "Analytic overlays"]
    ,revision: ["גרסה", "Revision"]
    ,updated_at: ["עודכן", "Updated"]
  };
  if (!labels[key] && String(key).startsWith("i360.")) return String(key).slice("i360.".length).replaceAll("_", " ");
  return labels[key] ? activeLocaleText(...labels[key]) : key.replaceAll("_", " ");
}

function viewerValue(value) {
  if (Array.isArray(value)) return value.map(item => typeof item === "object" ? (item.location_name || item.source_type || item.name || item.entity_id || JSON.stringify(item)) : item).join(", ");
  if (value && typeof value === "object") return JSON.stringify(value);
  return String(value);
}

const ENTITY_REFERENCE_FIELDS = new Set(["associated_entity_ids", "related_entity_ids", "subject_entity_ids", "entity_ids", "side_a_entity_id", "side_b_entity_id"]);

function entityViewerTarget(entityId, preferredKind = "") {
  const id = String(entityId || "").trim();
  if (!id) return null;
  const objects = viewerObjects();
  const kinds = [preferredKind, "person", "organization"].filter((kind, index, values) => kind && values.indexOf(kind) === index);
  return kinds.find(kind => objects.has(`${kind}:${id}`)) || null;
}

function entityViewerLinkHtml(entityId, label = entityId, preferredKind = "") {
  const id = String(entityId || "").trim();
  const kind = entityViewerTarget(id, preferredKind);
  if (!kind) return `<code dir="ltr">${escapeHtml(label || id || "—")}</code>`;
  return `<button type="button" class="object-viewer-open" data-viewer-kind="${escapeHtml(kind)}" data-viewer-id="${escapeHtml(id)}">${escapeHtml(label || id)}</button>`;
}

function viewerFieldValueHtml(key, value) {
  if (!ENTITY_REFERENCE_FIELDS.has(key)) return escapeHtml(viewerValue(value));
  const ids = Array.isArray(value) ? value : [value];
  return ids.map(id => entityViewerLinkHtml(id)).join(" ");
}

function organizationEvidenceHtml(item) {
  const available = viewerObjects();
  const locations = (item.top_locations || []).filter(location => (location.evidence_record_ids || []).length);
  if (!locations.length) return "";
  const rows = locations.map(location => {
    const ids = (location.evidence_record_ids || []).slice(0, 8);
    const links = ids.map(id => available.has(`record:${id}`)
      ? `<button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(id)}">${escapeHtml(id)}</button>`
      : `<code dir="ltr">${escapeHtml(id)}</code>`).join(" ");
    return `<li><strong>${escapeHtml(location.location_name || location.location_id || "-")}</strong><span>${escapeHtml(milStdClaimLabel(location.assessment_status || "reported"))} · ${Number(location.presence_evidence_count || location.count || ids.length).toLocaleString(currentLocaleTag())} ${escapeHtml(activeLocaleText("רשומות", "records"))}</span><div class="object-viewer-evidence-links">${links}</div></li>`;
  }).join("");
  return `<section class="object-viewer-evidence"><h3>${escapeHtml(activeLocaleText("ראיות לפי נוכחות במיקום", "Evidence by location presence"))}</h3><ul>${rows}</ul></section>`;
}

function personProfileHtml(item) {
  const status = item.identity_status || activeLocaleText("לא צוין", "Not specified");
  const role = item.role || activeLocaleText("לא צוין", "Not specified");
  const summary = item.description || item.biographical_notes || activeLocaleText("לא סופק תקציר לפרופיל זה.", "No profile summary was supplied.");
  return `<section class="person-viewer-profile"><div><p class="person-viewer-status">${escapeHtml(status)}</p><h3>${escapeHtml(role)}</h3><p>${escapeHtml(summary)}</p></div></section>`;
}

function personTelecomDetailsHtml(item) {
  const telecom = item.telecom && typeof item.telecom === "object" ? item.telecom : {};
  const derivation = telecom.subscriber_identity_derivation && typeof telecom.subscriber_identity_derivation === "object"
    ? telecom.subscriber_identity_derivation
    : null;
  const extracted = derivation && derivation.claim && typeof derivation.claim.value === "object"
    ? { ...derivation.claim.value, supporting_record_ids: derivation.supporting_record_ids || [] }
    : null;
  const approved = telecom.approved_subscriber_identity && typeof telecom.approved_subscriber_identity === "object"
    ? telecom.approved_subscriber_identity
    : null;
  const resolvedMsisdn = approved?.msisdn || telecom.msisdn;
  const resolvedImsi = approved?.imsi || telecom.imsi;
  const identifier = (label, value, action = false) => `<div><dt>${escapeHtml(label)}</dt><dd dir="ltr">${value ? (action ? collectionImeiButton(value) : escapeHtml(value)) : "—"}</dd></div>`;
  const recordButtons = (telecom.reference_record_ids || []).map(id => `<button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(id)}">${escapeHtml(id)}</button>`).join("");
  const callButtons = (telecom.calls || []).map(call => `<button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(call.event_id || "")}">${escapeHtml(call.event_id || "")}${call.side ? ` · ${escapeHtml(activeLocaleText(`צד ${call.side.toUpperCase()}`, `Side ${call.side.toUpperCase()}`))}` : ""}</button>`).join("");
  const extractedIdentifiers = extracted && (extracted.msisdn || extracted.imsi);
  const reviewCard = extractedIdentifiers && !approved ? `<section class="person-telecom-review" aria-label="${escapeHtml(activeLocaleText("מזהי מנוי שחולצו וממתינים לאישור", "Extracted subscriber identifiers awaiting approval"))}">
    <div class="person-telecom-review-heading"><span class="material-symbols-rounded" aria-hidden="true">psychology</span><div><strong>${escapeHtml(activeLocaleText("זהות מנוי שחולצה", "Extracted subscriber identity"))}</strong><span>${escapeHtml(activeLocaleText("נדרש אישור אנליסט", "Analyst review required"))}</span></div></div>
    <dl class="person-telecom-identifier-grid">${identifier("MSISDN", extracted.msisdn)}${identifier("IMSI", extracted.imsi)}</dl>
    <p>${escapeHtml(activeLocaleText("התאמה עקבית ל-IMEI ברשומות מיקום סלולריות.", "Consistently matched to this IMEI across cellular-geolocation records."))}</p>
    <button type="button" class="person-telecom-approve" data-approve-telecom-entity="${escapeHtml(item.entity_id || "")}"><span class="material-symbols-rounded" aria-hidden="true">verified</span>${escapeHtml(activeLocaleText("אשר", "Approve"))}</button>
  </section>` : "";
  const approvalStatus = approved ? `<span class="person-telecom-approved"><span class="material-symbols-rounded" aria-hidden="true">verified</span>${escapeHtml(activeLocaleText("אושר", "Approved"))}</span>` : "";
  if (!telecom.imei && !resolvedMsisdn && !resolvedImsi && !reviewCard && !recordButtons && !callButtons) return "";
  return `<section class="person-telecom-details" aria-label="${escapeHtml(activeLocaleText("מזהי תקשורת וקישורים", "Telecom identifiers and links"))}">
    <h3><span class="material-symbols-rounded" aria-hidden="true">phonelink</span>${escapeHtml(activeLocaleText("מזהי תקשורת", "Telecom identifiers"))}${approvalStatus}</h3>
    <dl class="person-telecom-identifier-grid">${identifier("IMEI", telecom.imei, true)}${resolvedMsisdn || resolvedImsi ? `${identifier("MSISDN", resolvedMsisdn)}${identifier("IMSI", resolvedImsi)}` : ""}</dl>
    ${reviewCard}
    ${recordButtons ? `<div class="person-telecom-link-group"><h4>${escapeHtml(activeLocaleText("רשומות ייחוס", "Reference records"))}</h4><div>${recordButtons}</div></div>` : ""}
    ${callButtons ? `<div class="person-telecom-link-group"><h4>${escapeHtml(activeLocaleText("שיחות", "Calls"))}</h4><div>${callButtons}</div></div>` : ""}
  </section>`;
}

// The review endpoint returns the updated entity (in English); reload the entity rows in the
// current locale so the viewer shows the approved identifiers, falling back to the returned entity.
async function refreshEntityAfterReview(entityId, returnedEntity) {
  const replace = (list, entity) => {
    const index = list.findIndex(item => item?.entity_id === entityId);
    if (index >= 0) list[index] = { ...list[index], ...entity };
    else list.push(entity);
  };
  let entity = null;
  try {
    const response = await fetch(buildLocaleApiUrl(`/api/layers/${encodeURIComponent("entity-metadata:all")}/rows`), { cache: "no-store" });
    const payload = await response.json();
    if (response.ok && Array.isArray(payload.rows)) {
      state.entityDirectory = payload.rows;
      entity = payload.rows.find(item => item?.entity_id === entityId) || null;
    }
  } catch (error) {
    entity = null;
  }
  entity = entity || (returnedEntity && typeof returnedEntity === "object" ? { ...returnedEntity, entity_id: entityId } : null);
  if (!entity) return;
  replace(state.entityDirectory, entity);
  state.layers.filter(layer => ["entity_metadata", "person_entities"].includes(layer.kind)).forEach(layer => {
    const index = (layer.items || []).findIndex(item => item?.entity_id === entityId);
    if (index >= 0) layer.items[index] = { ...layer.items[index], ...entity };
  });
  renderEvidence();
}

async function approveExtractedTelecomIdentity(entityId, button) {
  if (!entityId || button.disabled) return;
  button.disabled = true;
  const original = button.innerHTML;
  button.innerHTML = `<span class="material-symbols-rounded" aria-hidden="true">progress_activity</span>${escapeHtml(activeLocaleText("מאשר...", "Approving..."))}`;
  try {
    const response = await fetch("/api/derivations/review", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify({ entity_id: entityId, action: "approve" })
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || activeLocaleText("אישור מזהי התקשורת נכשל", "Could not approve telecom identifiers"));
    await refreshEntityAfterReview(entityId, payload.entity);
    openObjectViewer("person", entityId, objectViewerReturnFocus || button);
  } catch (error) {
    button.disabled = false;
    button.innerHTML = original;
    button.title = error.message || activeLocaleText("אישור מזהי התקשורת נכשל", "Could not approve telecom identifiers");
  }
}

function entityRecordLocationPoints(item) {
  const entityId = String(item?.entity_id || "").trim();
  if (!entityId) return [];
  const valuesFor = value => Array.isArray(value) ? value.map(String) : String(value || "").split(/[,;|\s]+/).filter(Boolean);
  const related = state.events.filter(event => {
    if (String(event.entity_id || "") === entityId) return true;
    return [event.entity_ids, event.related_entity_ids, event.subject_entity_ids, event.side_a_entity_id, event.side_b_entity_id].some(value => valuesFor(value).includes(entityId));
  });
  const byLocation = new Map();
  related.forEach(event => {
    const locationId = String(event.location_id || "").trim();
    const location = LOCATIONS[locationId] || {};
    const lon = Number(location.lon ?? event.longitude ?? event.lon);
    const lat = Number(location.lat ?? event.latitude ?? event.lat);
    if (!locationId || !Number.isFinite(lon) || !Number.isFinite(lat)) return;
    const point = byLocation.get(locationId) || {
      locationId, name: location.name || event.location_name || locationId, lon, lat,
      records: [], latestTimestamp: ""
    };
    const recordId = event.record_id || event.event_id;
    if (recordId && !point.records.includes(recordId)) point.records.push(recordId);
    if (String(event.timestamp_utc || "") > point.latestTimestamp) point.latestTimestamp = String(event.timestamp_utc || "");
    byLocation.set(locationId, point);
  });
  return [...byLocation.values()].sort((a, b) => b.records.length - a.records.length || a.name.localeCompare(b.name));
}

function entityLocationMapHtml(item) {
  const points = entityRecordLocationPoints(item);
  if (!points.length) return "";
  const locations = points.length.toLocaleString(currentLocaleTag());
  return `<section class="entity-record-map-panel call-map-panel" aria-labelledby="entityLocationMapTitle">
    <div id="entityViewerMap" aria-label="${escapeHtml(activeLocaleText("מיקומים של רשומות המקושרות לישות", "Locations of records connected to this entity"))}"></div>
    <div class="call-map-caption"><span class="material-symbols-rounded">location_on</span><span id="entityLocationMapTitle">${escapeHtml(activeLocaleText(`מיקומי ישות · ${locations}`, `Entity locations · ${locations}`))}</span><button type="button" id="entityFitMap">${escapeHtml(activeLocaleText("התאם", "Fit locations"))}</button></div>
  </section>`;
}

function initializeEntityLocationMap(item) {
  entityViewerMap?.remove();
  entityViewerMap = null;
  const container = document.getElementById("entityViewerMap");
  const points = entityRecordLocationPoints(item);
  if (!container || !points.length || typeof maplibregl === "undefined") return;
  const map = new maplibregl.Map({
    container,
    style: { version: 8, sources: { imagery: { type: "raster", tiles: ["https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"], tileSize: 256, attribution: "Imagery © Esri, Vantor, Earthstar Geographics" } }, layers: [{ id: "imagery", type: "raster", source: "imagery" }] },
    center: [points[0].lon, points[0].lat], zoom: 9, interactive: true
  });
  entityViewerMap = map;
  map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-left");
  const bounds = new maplibregl.LngLatBounds();
  points.forEach(point => {
    bounds.extend([point.lon, point.lat]);
    const marker = document.createElement("button");
    marker.type = "button";
    marker.className = "cellular-call-map-endpoint entity-location-map-marker";
    marker.textContent = String(point.records.length);
    marker.setAttribute("aria-label", `${point.name}: ${point.records.length} records`);
    const recordList = point.records.slice(0, 6).map(escapeHtml).join(" · ");
    const popup = `<strong>${escapeHtml(point.name)}</strong><span>${escapeHtml(`${point.records.length} ${activeLocaleText("רשומות", "records")}`)}</span>${recordList ? `<small dir="ltr">${recordList}</small>` : ""}`;
    new maplibregl.Marker({ element: marker }).setLngLat([point.lon, point.lat]).setPopup(new maplibregl.Popup({ offset: 14 }).setHTML(`<div class="entity-location-map-popup">${popup}</div>`)).addTo(map);
  });
  const fit = () => map.fitBounds(bounds, { padding: 32, maxZoom: 13, duration: 0 });
  map.on("load", () => { map.resize(); fit(); });
  document.getElementById("entityFitMap")?.addEventListener("click", fit);
}

function personWorkspaceHtml(item) {
  const points = entityRecordLocationPoints(item);
  const records = [...new Set(points.flatMap(point => point.records))];
  const detail = (label, value, direction = "auto") => value ? `<div><dt>${escapeHtml(label)}</dt><dd dir="${direction}">${escapeHtml(viewerValue(value))}</dd></div>` : "";
  const mapPanel = points.length
    ? entityLocationMapHtml(item)
    : `<section class="call-map-panel person-map-empty"><span class="material-symbols-rounded">location_off</span><strong>${escapeHtml(activeLocaleText("אין מיקומי רשומות מקושרים", "No connected record locations"))}</strong><p>${escapeHtml(activeLocaleText("יוצגו כאן מיקומים לאחר שייווצרו רשומות המקושרות לאדם.", "Connected record locations will appear here when available."))}</p></section>`;
  const recordLinks = records.length
    ? records.map(id => `<button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(id)}">${escapeHtml(id)}</button>`).join("")
    : `<p class="call-empty">${escapeHtml(activeLocaleText("לא נמצאו רשומות מקושרות.", "No connected records."))}</p>`;
  return `<section class="person-workspace call-workspace" aria-label="${escapeHtml(activeLocaleText("פרופיל אדם", "Person profile"))}">
    <aside class="call-sidebar person-profile-sidebar">
      ${personProfileHtml(item)}
      <dl class="call-detail-list">
        ${detail(activeLocaleText("גיל", "Age"), item.age_years ? `${item.age_years} ${activeLocaleText("שנים", "years")}` : "")}
        ${detail(activeLocaleText("לאום", "Nationality"), item.nationality)}
        ${detail(activeLocaleText("מגורים", "Residence"), item.residence)}
        ${detail(activeLocaleText("תפקיד", "Role"), item.role)}
        ${detail(activeLocaleText("שפות", "Languages"), item.languages)}
        ${detail(activeLocaleText("שירות צבאי", "Military service"), item.military_service)}
      </dl>
    </aside>
    <div class="call-main person-workspace-main">
      ${personTelecomDetailsHtml(item)}
      ${mapPanel}
      <section class="call-conversation person-records-panel">
        <header class="call-conversation-heading"><span class="material-symbols-rounded">hub</span><h3>${escapeHtml(activeLocaleText("רשומות מקושרות", "Connected records"))}</h3><span>${escapeHtml(records.length.toLocaleString(currentLocaleTag()))}</span></header>
        <div class="person-record-list">${recordLinks}</div>
      </section>
    </div>
  </section>`;
}

function evidenceProvenanceHtml(item) {
  const available = viewerObjects();
  const ids = item.source_record_ids || [];
  if (!ids.length) return "";
  const links = ids.map(id => available.has(`record:${id}`)
    ? `<button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(id)}">${escapeHtml(id)}</button>`
    : `<code dir="ltr">${escapeHtml(id)}</code>`).join(" ");
  return `<section class="object-viewer-evidence"><h3>${escapeHtml(activeLocaleText("מקור וייחוס", "Provenance"))}</h3><div class="object-viewer-evidence-links">${links}</div></section>`;
}

function recordLinkedEntitiesHtml(item) {
  const links = Array.isArray(item.observed_entity_links) ? item.observed_entity_links : [];
  if (!links.length) return "";
  const ruleLabel = rule => ({
    event_entity_id_v1: activeLocaleText("מזהה ישות קנוני ברשומה", "Canonical entity ID in record"),
    adint_device_entity_v1: activeLocaleText("מזהה מכשיר", "Device identifier"),
    entity_imei_to_ipdr_imei_v1: "IMEI",
    entity_imei_to_cellular_target_imei_v1: "IMEI",
    entity_imei_to_call_party_v1: activeLocaleText("IMEI של צד א׳", "Side A IMEI"),
    entity_imei_to_call_speaker_imei_v1: activeLocaleText("IMEI דובר בתמליל", "Transcript speaker IMEI")
  }[rule] || activeLocaleText("התאמת שדה", "Field match"));
  const rows = links.map(link => {
    const entityId = String(link.entity_id || "");
    const kind = String(link.entity_type || "").toLowerCase() === "person" ? "person" : "organization";
    const name = link.entity_name || entityId;
    const fields = `${link.record_field || "record"} = ${link.entity_field || "entity"}`;
    return `<li>${entityViewerLinkHtml(entityId, name, kind)}<span>${escapeHtml(ruleLabel(link.rule_id))} · <code dir="ltr">${escapeHtml(fields)}</code> · <code dir="ltr">${escapeHtml(link.matched_value || "—")}</code></span></li>`;
  }).join("");
  return `<section class="object-viewer-evidence record-entity-links"><h3>${escapeHtml(activeLocaleText("ישויות מקושרות", "Linked entities"))}</h3><ul>${rows}</ul></section>`;
}

function recordLinkedRawRecordsHtml(item) {
  const links = Array.isArray(item.observed_record_links) ? item.observed_record_links : [];
  if (!links.length) return "";
  const rows = links.map(link => {
    const fields = `${link.record_field || "record"} = ${link.linked_record_field || "record"}`;
    const label = link.rule_id === "adint_ip_to_ipdr_public_ip_v1"
      ? activeLocaleText("כתובת IP תואמת", "Matching IP address")
      : activeLocaleText("התאמת שדה", "Field match");
    return `<li><button type="button" class="object-viewer-open" data-linked-record-open="true" data-viewer-kind="record" data-viewer-id="${escapeHtml(link.record_id || "")}">${escapeHtml(link.record_id || "—")}</button><span>${escapeHtml(label)} · <code dir="ltr">${escapeHtml(fields)}</code> · <code dir="ltr">${escapeHtml(link.matched_value || "—")}</code></span></li>`;
  }).join("");
  return `<section class="object-viewer-evidence record-raw-links"><h3>${escapeHtml(activeLocaleText("רשומות גולמיות מקושרות", "Linked raw records"))}</h3><ul>${rows}</ul></section>`;
}

function recordLinkIndicator(item) {
  const entityLinkCount = Array.isArray(item?.observed_entity_links) ? item.observed_entity_links.length : 0;
  const rawLinkCount = Array.isArray(item?.observed_record_links) ? item.observed_record_links.length : 0;
  if (!entityLinkCount && !rawLinkCount) return "";
  const label = rawLinkCount
    ? activeLocaleText("לרשומה יש קישורים מתועדים", "This record has documented links")
    : activeLocaleText("לרשומה יש קישורים לישויות", "This record has entity links");
  return `<span class="record-link-indicator" role="img" aria-label="${escapeHtml(label)}"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M10.5 13.5a4.25 4.25 0 0 0 6.01.01l2.12-2.12a4.25 4.25 0 0 0-6.01-6.01l-1.21 1.2"></path><path d="M13.5 10.5a4.25 4.25 0 0 0-6.01-.01L5.37 12.6a4.25 4.25 0 1 0 6.01 6.01l1.2-1.2"></path><path d="m8.8 15.2 6.4-6.4"></path></svg><span class="record-link-tooltip" role="tooltip">${escapeHtml(label)}</span></span>`;
}

function assessmentEvidenceHtml(item) {
  const available = viewerObjects();
  const ids = item.evidence_ids || [];
  if (!ids.length) return "";
  const links = ids.map(id => available.has(`evidence:${id}`)
    ? `<button type="button" class="object-viewer-open" data-viewer-kind="evidence" data-viewer-id="${escapeHtml(id)}">${escapeHtml(id)}</button>`
    : `<code dir="ltr">${escapeHtml(id)}</code>`).join(" ");
  return `<section class="object-viewer-evidence"><h3>${escapeHtml(activeLocaleText("ראיות תומכות", "Supporting evidence"))}</h3><div class="object-viewer-evidence-links">${links}</div></section>`;
}

function setViewerDocked(target = null) {
  const viewer = document.getElementById("objectViewer");
  const timeline = document.getElementById("timelineView");
  const table = document.getElementById("rawEventsOverlay");
  objectViewerDockTarget = target;
  viewer.classList.remove("is-maximized");
  const docked = Boolean(target);
  viewer.classList.toggle("is-docked", docked);
  [timeline, table].forEach(container => container?.classList.toggle("has-record-viewer", container === target));
  viewer.querySelector(".object-viewer").setAttribute("aria-modal", String(!docked));
  (target || document.body).appendChild(viewer);
}

function setViewerMaximized(maximized) {
  const viewer = document.getElementById("objectViewer");
  const maximizeButton = document.getElementById("objectViewerMaximize");
  const timeline = document.getElementById("timelineView");
  const table = document.getElementById("rawEventsOverlay");
  if (!viewer || viewer.hidden) return;
  if (!maximized) {
    setViewerDocked(objectViewerDockTarget);
  } else {
    viewer.classList.remove("is-docked");
    viewer.classList.add("is-maximized");
    [timeline, table].forEach(container => container?.classList.remove("has-record-viewer"));
    viewer.querySelector(".object-viewer").setAttribute("aria-modal", "true");
    document.body.appendChild(viewer);
  }
  const isMaximized = viewer.classList.contains("is-maximized");
  const label = activeLocaleText(isMaximized ? "שחזר גודל" : "הגדל למסך מלא", isMaximized ? "Restore size" : "Maximize viewer");
  if (maximizeButton) {
    maximizeButton.setAttribute("aria-pressed", String(isMaximized));
    maximizeButton.setAttribute("aria-label", label);
    maximizeButton.title = label;
    maximizeButton.querySelector(".material-symbols-rounded").textContent = isMaximized ? "close_fullscreen" : "open_in_full";
  }
}

function closeObjectViewer() {
  const viewer = document.getElementById("objectViewer");
  closeVisualCollectionMediaFullscreen({ restoreFocus: false });
  stopSimulatedUavStream();
  cellularViewerMap?.remove(); cellularViewerMap = null;
  entityViewerMap?.remove(); entityViewerMap = null;
  viewer.querySelectorAll("video,audio").forEach(media => { media.pause(); media.removeAttribute("src"); media.load(); });
  viewer.hidden = true;
  setViewerDocked();
  objectViewerDockTarget = null;
  renderEvidence();
  document.querySelectorAll(".call-timeline-entry").forEach(row => row.setAttribute("aria-pressed", "false"));
  objectViewerReturnFocus?.focus?.();
  objectViewerReturnFocus = null;
}

function objectMemoryPayload(kind, id) {
  const item = viewerObjects().get(`${kind}:${id}`);
  if (!item) return null;
  const label = kind === "record" ? (item.record_id || item.event_id || id) : (item.title || item.canonical_name || item.object_class || id);
  return { kind: "object", object_kind: kind, object_id: id, label, source_type: item.source_type || "", summary: item.event_summary || item.summary || "" };
}

async function saveObjectToInvestigationMemory(kind, id, trigger, comment = "", confirmed = false) {
  if (state.draftSessionActive) { openDraftCreateModal(() => saveObjectToInvestigationMemory(kind, id, trigger)); return; }
  const artifact = objectMemoryPayload(kind, id);
  if (!state.investigationId || !artifact) return;
  if (!confirmed) { openMemoryCommentDialog({ label: artifact.label, trigger, onSave: value => saveObjectToInvestigationMemory(kind, id, trigger, value, true) }); return; }
  const response = await fetch("/api/investigation-memory/artifact", { method: "POST", headers: { "Content-Type": "application/json; charset=utf-8" }, body: JSON.stringify({ investigation_id: state.investigationId, name: state.investigationName, artifact, comment: memoryCommentValue(comment) }) });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || activeLocaleText("שמירת האובייקט נכשלה", "Failed to save object"));
  await loadInvestigationMemory();
}

async function savePolygonToInvestigationMemory(polygon, comment = "", confirmed = false) {
  if (state.draftSessionActive) { openDraftCreateModal(() => savePolygonToInvestigationMemory(polygon)); return; }
  if (!state.investigationId || !polygon?.coordinates) return;
  const artifact = { kind: "polygon", label: activeLocaleText("אזור מסומן", "Marked area"), geometry: { type: "Polygon", coordinates: [polygon.coordinates] } };
  if (!confirmed) { openMemoryCommentDialog({ label: artifact.label, trigger: document.getElementById("polygonDrawButton"), onSave: value => savePolygonToInvestigationMemory(polygon, value, true) }); return; }
  const response = await fetch("/api/investigation-memory/artifact", { method: "POST", headers: { "Content-Type": "application/json; charset=utf-8" }, body: JSON.stringify({ investigation_id: state.investigationId, name: state.investigationName, artifact, comment: memoryCommentValue(comment) }) });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || activeLocaleText("שמירת האזור נכשלה", "Failed to save area"));
  await loadInvestigationMemory();
}

function openObjectViewer(kind, id, trigger = document.activeElement) {
  if (!['record', 'organization', 'person', 'evidence', 'assessment', 'ipdr_package'].includes(kind)) return false;
  const item = viewerObjects().get(`${kind}:${id}`);
  if (!item) return false;
  state.focusedViewerRecordId = kind === "record" ? String(id) : null;
  renderEvidence();
  if (kind === "record") {
    const reveal = () => revealViewerRecordInTable(id);
    if (typeof requestAnimationFrame === "function") requestAnimationFrame(reveal);
    else reveal();
  }
  objectViewerReturnFocus = trigger;
  const viewer = document.getElementById("objectViewer");
  viewer.classList.remove("is-maximized");
  const title = kind === "record"
    ? (isUavVideoRecord(item) ? activeLocaleText("תצפית וידאו מכטב״ם", "UAV video observation") : isCellularCallRecord(item) ? activeLocaleText("שיחה סלולרית", "Cellular call") : (item.source_type || activeLocaleText("רשומת מקור", "Source record")))
    : kind === "ipdr_package" ? activeLocaleText("חבילת ראיות IPDR", "IPDR evidence package")
    : kind === "evidence" ? (item.object_class || item.claim_type || id)
    : kind === "assessment" ? (item.title || id)
    : (item.canonical_name || id);
  document.getElementById("objectViewerKind").textContent = kind === "ipdr_package" ? activeLocaleText("חבילת ראיות", "Evidence package") : kind === "record" ? (isIpdrRecord(item) && item.evidence_type ? activeLocaleText("ראיית IPDR", "IPDR evidence") : activeLocaleText("רשומה גולמית", "Raw record")) : kind === "person" ? activeLocaleText("אדם", "Person") : kind === "evidence" ? activeLocaleText("אובייקט ראיה", "Evidence object") : kind === "assessment" ? activeLocaleText("הערכת אויב", "Enemy assessment") : activeLocaleText("ישות", "Entity");
  document.getElementById("objectViewerTitle").textContent = title;
  document.getElementById("objectViewerId").textContent = id;
  const objectMemoryAction = document.getElementById("objectMemoryAction");
  if (objectMemoryAction) {
    const memoryLabel = activeLocaleText("שמור לזיכרון", "Save to memory");
    objectMemoryAction.dataset.memoryObjectKind = kind;
    objectMemoryAction.dataset.memoryObjectId = id;
    objectMemoryAction.title = memoryLabel;
    objectMemoryAction.setAttribute("aria-label", memoryLabel);
    objectMemoryAction.querySelector(".object-memory-action-label").textContent = memoryLabel;
    objectMemoryAction.hidden = false;
  }
  viewer.querySelectorAll("video,audio").forEach(media => { media.pause(); media.removeAttribute("src"); media.load(); });
  cellularViewerMap?.remove(); cellularViewerMap = null;
  entityViewerMap?.remove(); entityViewerMap = null;
  const timeline = document.getElementById("timelineView");
  const table = document.getElementById("rawEventsOverlay");
  const dockTarget = kind === "record" && isCellularCallRecord(item) && timeline.classList.contains("active")
    ? timeline
    : ["person", "organization"].includes(kind) && document.getElementById("tableView").classList.contains("active")
      ? table
      : null;
  setViewerDocked(dockTarget);
  document.querySelectorAll(".call-timeline-entry").forEach(row => row.setAttribute("aria-pressed", String(row.dataset.viewerId === id)));
  const cellularCallViewer = kind === "record" && isCellularCallRecord(item);
  const visualCollectionViewer = kind === "record" && isVisualCollectionRecord(item);
  const personViewer = kind === "person";
  viewer.classList.toggle("is-cellular-viewer", cellularCallViewer);
  viewer.classList.toggle("is-visual-collection-viewer", visualCollectionViewer);
  viewer.classList.toggle("is-person-viewer", personViewer);
  const mediaHtml = viewerMediaHtml(item);
  const cellularHtml = kind === "record" ? cellularCallHtml(item) : "";
  const fields = viewerFields(item, kind).map(([key,value]) => `<div class="object-viewer-field"><dt>${escapeHtml(viewerFieldLabel(key))}</dt><dd>${viewerFieldValueHtml(key, value)}</dd></div>`).join("");
  const entityMapHtml = kind === "organization" ? entityLocationMapHtml(item) : "";
  document.getElementById("objectViewerBody").innerHTML = `${mediaHtml}${cellularHtml}${ipdrPackageLinkHtml(item, kind)}${personViewer ? personWorkspaceHtml(item) : ""}${entityMapHtml}${["record", "evidence", "assessment"].includes(kind) ? `<p class="object-viewer-summary">${escapeHtml(item.event_summary || item.summary || "-")}</p>` : ""}${personViewer ? "" : `<dl class="object-viewer-fields">${fields}</dl>`}${kind === "record" ? `${recordLinkedEntitiesHtml(item)}${recordLinkedRawRecordsHtml(item)}` : kind === "organization" ? organizationEvidenceHtml(item) : kind === "evidence" ? evidenceProvenanceHtml(item) : kind === "assessment" ? assessmentEvidenceHtml(item) : ""}`;
  viewer.hidden = false;
  setViewerMaximized(false);
  if (cellularCallViewer) initializeCellularViewer(item);
  if (cellularCallViewer) startCellularCallAudio();
  if (["person", "organization"].includes(kind)) initializeEntityLocationMap(item);
  if (kind === "record" && isUavVideoRecord(item)) startSimulatedUavStream(item);
  if (kind === "record") initializeViewerMediaFallback(item, id);
  else document.querySelectorAll("#objectViewerBody .object-viewer-media img, #objectViewerBody .object-viewer-media video").forEach(media => {
    media.addEventListener("error", () => media.closest(".object-viewer-media")?.remove());
  });
  document.getElementById("objectViewerClose").focus();
  return true;
}

function rawRecordCatalogLayerId(record) {
  const sourceType = String(record?.source_type || "").trim();
  if (!sourceType) return "";
  const directId = `events:${sourceType}`;
  return state.layerCatalog.find(layer => layer.id === directId)?.id
    || state.layerCatalog.find(layer => String(layer.source_type || "").trim() === sourceType)?.id
    || "";
}

async function openLinkedRawRecord(id, trigger) {
  const record = viewerObjects().get(`record:${id}`);
  const catalogLayerId = rawRecordCatalogLayerId(record);
  if (!record || !catalogLayerId) return false;
  const layer = await openCatalogLayer(catalogLayerId, { silent: true });
  if (!layer) return false;
  state.activeLayerId = layer.id;
  state.rawOverlayMinimized = false;
  activateView("table");
  renderAllViews();
  return openObjectViewer("record", id, trigger);
}

function isCallsLayer(layer) {
  return layer.kind === "events" && ((layer.items?.length > 0 && layer.items.every(isCellularCallRecord)) || /cellular calls/i.test(layer.source_type || layer.label || ""));
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

function renderAllViews() {
  renderMap();
  renderTimeline();
  renderEvidence();
}

function activateView(view) {
  const requestedView = view === "evidence" ? "table" : view;
  const safeView = viewLabels()[requestedView] ? requestedView : "map";
  const dockedViewer = document.getElementById("objectViewer");
  const expectedDockParent = safeView === "timeline"
    ? document.getElementById("timelineView")
    : safeView === "table"
      ? document.getElementById("rawEventsOverlay")
      : null;
  if (dockedViewer?.classList.contains("is-docked") && dockedViewer.parentElement !== expectedDockParent) closeObjectViewer();
  document.querySelector(".view-stack")?.classList.toggle("timeline-mode", safeView === "timeline");
  document.querySelectorAll(".view-tab").forEach(button => button.classList.toggle("active", button.dataset.view === safeView));
  document.querySelectorAll(".view-pane").forEach(pane => pane.classList.toggle("active", pane.id === `${safeView}View`));
  document.querySelector(".view-stack")?.classList.toggle("table-mode", safeView === "table");
  renderEvidence();
  if (safeView === "map" && state.map) {
    setTimeout(() => {
      state.map.resize();
      renderMap();
    }, 0);
  }
}

function clearMarkers() {
  (state.cellularCallMapArtifacts || []).slice().reverse().forEach(({ layerId, sourceId, onClick, onMouseEnter, onMouseLeave }) => {
    if (layerId && onClick) state.map.off("click", layerId, onClick);
    if (layerId && onMouseEnter) state.map.off("mouseenter", layerId, onMouseEnter);
    if (layerId && onMouseLeave) state.map.off("mouseleave", layerId, onMouseLeave);
    if (layerId && state.map.getLayer(layerId)) state.map.removeLayer(layerId);
    if (sourceId && state.map.getSource(sourceId)) state.map.removeSource(sourceId);
  });
  state.cellularCallMapArtifacts = [];
  (state.assessmentMapArtifacts || []).slice().reverse().forEach(({ layerId, sourceId }) => {
    if (layerId && state.map.getLayer(layerId)) state.map.removeLayer(layerId);
    if (sourceId && state.map.getSource(sourceId)) state.map.removeSource(sourceId);
  });
  state.assessmentMapArtifacts = [];
  state.markers.forEach(marker => marker.remove());
  state.markers = [];
  state.focusedEventMarker?.remove();
  state.focusedEventMarker = null;
  state.focusedEventPopup?.remove();
  state.focusedEventPopup = null;
}

function cellularCallMapLocation(event, side) {
  const prefix = side === "a" ? "side_a" : "side_b";
  const locationId = event[`${prefix}_location_id`];
  const canonical = LOCATIONS[locationId];
  if (!locationId || !canonical) return null;
  return {
    id: locationId,
    name: event[`${prefix}_location_name`] || canonical.name || locationId,
    lon: Number(canonical.lon),
    lat: Number(canonical.lat),
    number: event[`${prefix}_sim`] || event[`${prefix}_number`] || "-",
  };
}

function addCellularCallMapPresentation(event, layer, index, bounds) {
  const sideA = cellularCallMapLocation(event, "a");
  const sideB = cellularCallMapLocation(event, "b");
  if (!sideA || !sideB) return false;
  const recordId = String(event.record_id || event.event_id || event.call_id || "");
  if (!recordId) return false;
  const base = sanitizeLayerKey(`cellular-call-${recordId}-${index}`);
  const sourceId = `${base}-source`;
  const layerId = `${base}-layer`;
  state.map.addSource(sourceId, {
    type: "geojson",
    data: {
      type: "Feature",
      properties: { record_id: recordId },
      geometry: { type: "LineString", coordinates: [[sideA.lon, sideA.lat], [sideB.lon, sideB.lat]] },
    },
  });
  state.map.addLayer({
    id: layerId,
    type: "line",
    source: sourceId,
    paint: {
      "line-color": layer.color || "#64c8d0",
      "line-opacity": 0.76,
      "line-width": 3,
      "line-dasharray": [2, 1.25],
    },
  });
  const onClick = mapEvent => {
    if (state.polygonDraw?.active || mapEvent?.originalEvent?.defaultPrevented) return;
    mapEvent?.originalEvent?.preventDefault?.();
    openObjectViewer("record", recordId, state.map.getCanvas());
  };
  const onMouseEnter = () => { if (!state.polygonDraw?.active) state.map.getCanvas().style.cursor = "pointer"; };
  const onMouseLeave = () => { if (!state.polygonDraw?.active) state.map.getCanvas().style.cursor = ""; };
  state.map.on("click", layerId, onClick);
  state.map.on("mouseenter", layerId, onMouseEnter);
  state.map.on("mouseleave", layerId, onMouseLeave);
  state.cellularCallMapArtifacts.push({ layerId, sourceId, onClick, onMouseEnter, onMouseLeave });

  [["a", sideA], ["b", sideB]].forEach(([side, location]) => {
    const sideLabel = side === "a" ? activeLocaleText("צד א׳", "Side A") : activeLocaleText("צד ב׳", "Side B");
    const element = document.createElement("button");
    element.type = "button";
    element.className = `cellular-call-map-endpoint cellular-call-map-endpoint-${side}`;
    element.dataset.viewerKind = "record";
    element.dataset.viewerId = recordId;
    element.setAttribute("aria-haspopup", "dialog");
    element.setAttribute("aria-label", `${recordId}, ${sideLabel}, ${location.name}`);
    element.innerHTML = `<span aria-hidden="true">${side.toUpperCase()}</span>`;
    const other = side === "a" ? sideB : sideA;
    const popup = new maplibregl.Popup({ offset: 20, closeButton: true, closeOnClick: true }).setHTML(`
      <div class="map-popup cellular-call-map-popup" dir="${currentLocale() === "en" ? "ltr" : "rtl"}">
        <strong>${escapeHtml(sideLabel)} · ${escapeHtml(location.name)}</strong>
        <span dir="ltr">${escapeHtml(location.number)}</span>
        <em>${escapeHtml(activeLocaleText("שיחה אל", "Call to"))} ${escapeHtml(other.name)}</em>
        <code dir="ltr">${escapeHtml(recordId)}</code>
        <button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(recordId)}">${escapeHtml(activeLocaleText("פתח את השיחה", "Open call"))}</button>
      </div>`);
    state.markers.push(new maplibregl.Marker({ element, anchor: "center" }).setLngLat([location.lon, location.lat]).setPopup(popup).addTo(state.map));
    bounds.extend([location.lon, location.lat]);
  });
  return true;
}

function renderMap() {
  if (!state.mapReady) return;
  clearMarkers();
  const byLocation = new Map();
  const milStdDescriptors = [];
  const bounds = new maplibregl.LngLatBounds();
  const addLocationCount = (locationId, count, label, aggregateLocation = null, color = null, viewerRef = null) => {
    if (!locationId) return;
    const existing = byLocation.get(locationId) || { location_id: locationId, count: 0, labels: new Set(), colors: new Set(), viewerRefs: new Map(), viewerEligible: true, aggregateLocation };
    existing.count += Number(count || 0);
    existing.labels.add(label);
    if (color) existing.colors.add(color);
    if (aggregateLocation) existing.aggregateLocation = aggregateLocation;
    if (viewerRef?.id) existing.viewerRefs.set(`${viewerRef.kind}:${viewerRef.id}`, viewerRef);
    else existing.viewerEligible = false;
    byLocation.set(locationId, existing);
  };
  visibleLayers("map").forEach(layer => {
    const items = itemsForLayerPresentation(layer);
    if (layer.kind === "events") {
      const grouped = new Map();
      items.forEach((event, index) => {
        if (isCellularCallRecord(event) && addCellularCallMapPresentation(event, layer, index, bounds)) return;
        // A record with no location object is drawn at its own coordinates (e.g. raw GPS updates).
        const lat = Number(event.latitude);
        const lon = Number(event.longitude);
        const ownPoint = !event.location_id && event.latitude !== "" && event.longitude !== ""
          && Number.isFinite(lat) && Number.isFinite(lon);
        const key = event.location_id || (ownPoint ? `point:${lat.toFixed(5)},${lon.toFixed(5)}` : "");
        if (!key) return;
        const current = grouped.get(key) || { count: 0, first: null, point: null };
        current.count += 1;
        current.first ||= event;
        if (ownPoint) current.point ||= { location_name: `${lat.toFixed(5)}, ${lon.toFixed(5)}`, latitude: lat, longitude: lon };
        grouped.set(key, current);
      });
      grouped.forEach((group, locationId) => {
        addLocationCount(locationId, group.count, layer.label, group.point, layer.color, group.count === 1 ? { kind: "record", id: group.first.record_id || group.first.event_id } : null);
      });
    } else if (layer.kind === "locations") {
      items.forEach(item => addLocationCount(item.location_id, item.count || 1, layer.label, item, layer.color));
    } else if (layer.kind === "location_metadata") {
      items.forEach(item => addLocationCount(item.location_id, item.event_count || item.count || 1, item.location_name || layer.label, item, layer.color));
    } else if (layer.kind === "entity_metadata") {
      milStdDescriptors.push(...milStdOrganizationDescriptors(layer));
      items.filter(entity => !MIL_STD_ORGANIZATIONS[entity.entity_id]).forEach(entity => {
        (entity.top_locations || []).forEach(location => addLocationCount(
          location.location_id,
          location.count || 1,
          entity.canonical_name || entity.entity_id || layer.label,
          location,
          layer.color,
          { kind: "organization", id: entity.entity_id }
        ));
      });
    } else if (layer.kind === "evidence") {
      items.forEach(item => {
        const descriptor = milStdEvidenceDescriptor(item);
        if (descriptor) milStdDescriptors.push(descriptor);
      });
    } else if (layer.kind === "assessments") {
      items.forEach(assessment => (assessment.overlays || []).forEach((overlay, index) => {
        const geometry = overlay?.geometry;
        if (!geometry || !["Point", "LineString", "Polygon"].includes(geometry.type)) return;
        const type = String(overlay.type || "");
        const color = type === "route_axis" ? "#42a5f5" : type === "confidence_envelope" ? "#ab7df6" : "#ffb74d";
        const confidenceOpacity = overlay.confidence === "high" ? 1 : overlay.confidence === "low" ? 0.58 : 0.8;
        if (geometry.type === "Point") {
          const [lon, lat] = geometry.coordinates || [];
          if (!Number.isFinite(Number(lon)) || !Number.isFinite(Number(lat))) return;
          const element = document.createElement("div");
          element.className = "assessment-point-marker";
          element.style.setProperty("--assessment-color", color);
          element.setAttribute("aria-label", `${assessment.title || assessment.assessment_id}: ${overlay.meaning || overlay.type}`);
          const popup = new maplibregl.Popup({ offset: 18 }).setHTML(`<div class="map-popup"><strong>${escapeHtml(assessment.title || assessment.assessment_id)}</strong><span>${escapeHtml(overlay.meaning || overlay.type)}</span><em>${escapeHtml(confidenceLabel(overlay.confidence || assessment.confidence))}</em></div>`);
          state.markers.push(new maplibregl.Marker({ element }).setLngLat([Number(lon), Number(lat)]).setPopup(popup).addTo(state.map));
          bounds.extend([Number(lon), Number(lat)]);
          return;
        }
        const base = sanitizeLayerKey(`assessment-${assessment.assessment_id}-${index}`);
        const sourceId = `${base}-source`;
        const layerId = `${base}-layer`;
        if (state.map.getLayer(layerId)) state.map.removeLayer(layerId);
        if (state.map.getSource(sourceId)) state.map.removeSource(sourceId);
        state.map.addSource(sourceId, { type: "geojson", data: { type: "Feature", properties: {}, geometry } });
        if (geometry.type === "Polygon") {
          const outlineLayerId = `${base}-outline`;
          const isEnvelope = type === "confidence_envelope";
          state.map.addLayer({
            id: layerId,
            type: "fill",
            source: sourceId,
            paint: { "fill-color": color, "fill-opacity": (isEnvelope ? 0.045 : 0.075) * confidenceOpacity },
          });
          state.map.addLayer({
            id: outlineLayerId,
            type: "line",
            source: sourceId,
            paint: {
              "line-color": color,
              "line-opacity": confidenceOpacity,
              "line-width": isEnvelope ? 2 : 2.5,
              "line-dasharray": isEnvelope ? [1, 2] : [4, 2],
            },
          });
          state.assessmentMapArtifacts.push({ layerId, sourceId }, { layerId: outlineLayerId });
        } else {
          state.map.addLayer({
            id: layerId,
            type: "line",
            source: sourceId,
            paint: { "line-color": color, "line-opacity": confidenceOpacity, "line-width": 4 },
          });
          state.assessmentMapArtifacts.push({ layerId, sourceId });
          const route = geometry.coordinates || [];
          const end = route.at(-1);
          const previous = route.at(-2);
          if (Array.isArray(end) && Array.isArray(previous)) {
            const bearing = Math.atan2(Number(end[0]) - Number(previous[0]), Number(end[1]) - Number(previous[1])) * 180 / Math.PI;
            const arrow = document.createElement("div");
            arrow.className = "assessment-route-arrow";
            arrow.style.setProperty("--assessment-bearing", `${bearing}deg`);
            arrow.setAttribute("aria-label", `${assessment.title || assessment.assessment_id}: ${overlay.meaning || overlay.type}`);
            const popup = new maplibregl.Popup({ offset: 18 }).setHTML(`<div class="map-popup"><strong>${escapeHtml(assessment.title || assessment.assessment_id)}</strong><span>${escapeHtml(overlay.meaning || overlay.type)}</span><em>${escapeHtml(confidenceLabel(overlay.confidence || assessment.confidence))}</em></div>`);
            state.markers.push(new maplibregl.Marker({ element: arrow, anchor: "center" }).setLngLat([Number(end[0]), Number(end[1])]).setPopup(popup).addTo(state.map));
          }
        }
        const coordinates = geometry.type === "Polygon" ? geometry.coordinates.flat(2) : geometry.coordinates.flat(1);
        for (let i = 0; i < coordinates.length; i += 2) bounds.extend([Number(coordinates[i]), Number(coordinates[i + 1])]);
      }));
    }
  });
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
    const viewerRefs = [...item.viewerRefs.values()];
    if (viewerRefs.length === 1 && item.viewerEligible) {
      element.dataset.viewerKind = viewerRefs[0].kind;
      element.dataset.viewerId = viewerRefs[0].id;
      element.setAttribute("aria-haspopup", "dialog");
    }
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
  const milStdLocationIndexes = new Map();
  coalesceEvidenceDescriptors(milStdDescriptors).forEach(descriptor => {
    const location = LOCATIONS[descriptor.locationId] || (
      descriptor.latitude != null && descriptor.longitude != null
        ? { name: descriptor.locationId, lon: descriptor.longitude, lat: descriptor.latitude }
        : null
    );
    if (!location) return;
    const index = milStdLocationIndexes.get(descriptor.locationId) || 0;
    milStdLocationIndexes.set(descriptor.locationId, index + 1);
    const angle = index * 2.399963;
    const ring = Math.floor(index / 8) + 1;
    const radius = index ? 0.00115 * ring : 0;
    const lon = Number(location.lon) + Math.cos(angle) * radius;
    const lat = Number(location.lat) + Math.sin(angle) * radius;
    const element = milStdMarkerElement(descriptor);
    const popup = new maplibregl.Popup({ offset: 28, closeButton: true, closeOnClick: true }).setHTML(milStdPopupHtml(descriptor, location.name || descriptor.locationId));
    const marker = new maplibregl.Marker({ element, anchor: "center" }).setLngLat([lon, lat]).setPopup(popup).addTo(state.map);
    state.markers.push(marker);
    bounds.extend([lon, lat]);
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
  const locationId = event.location_id || (event.location_ids || [])[0] || event.key;
  const requestedName = String(event.location_name || event.name || event.label || "").trim().toLowerCase();
  const canonical = LOCATIONS[locationId] || Object.values(LOCATIONS).find(location => (
    requestedName && String(location.name || "").trim().toLowerCase() === requestedName
  )) || null;
  const lon = canonical?.lon ?? event.longitude ?? event.lon;
  const lat = canonical?.lat ?? event.latitude ?? event.lat;
  if (lon == null || lat == null || String(lon).trim() === "" || String(lat).trim() === "" || !Number.isFinite(Number(lon)) || !Number.isFinite(Number(lat)) || Math.abs(Number(lon)) > 180 || Math.abs(Number(lat)) > 90) return null;
  return { lon: Number(lon), lat: Number(lat) };
}

function mapSelectionKey(layerId, kind, itemId) {
  return `${String(layerId)}:${String(kind)}:${String(itemId)}`;
}

function isMapItemSelected(layerId, kind, itemId) {
  return state.focusedMapSelection === mapSelectionKey(layerId, kind, itemId);
}

function isViewerRecordSelected(itemId) {
  return String(state.focusedViewerRecordId || "") === String(itemId || "");
}

function revealViewerRecordInTable(recordId) {
  const tableView = document.getElementById("tableView");
  const body = document.getElementById("evidenceRows");
  if (!tableView?.classList.contains("active") || !body) return;
  const recordButton = [...body.querySelectorAll('[data-viewer-kind="record"][data-viewer-id]')]
    .find(button => String(button.dataset.viewerId) === String(recordId));
  recordButton?.closest("tr")?.scrollIntoView({ block: "center", inline: "nearest" });
}

function mapItemId(item = {}, kind = "event") {
  if (kind === "target") return String(item.target_id || item.id || "");
  if (kind === "evidence") return String(item.evidence_id || item.id || "");
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
  if (kind === "evidence") return `<div class="map-popup milstd-popup" dir="${currentLocale() === "en" ? "ltr" : "rtl"}"><strong>${escapeHtml(String(item.object_class || item.claim_type || item.evidence_id))}</strong><span>${escapeHtml(String(item.evidence_status || "-"))} · ${escapeHtml(String(confidenceLabel(item.confidence)))}</span><em dir="ltr">${escapeHtml(String(item.evidence_id || "-"))}</em><p>${escapeHtml(String(item.summary || ""))}</p><button type="button" class="object-viewer-open" data-viewer-kind="evidence" data-viewer-id="${escapeHtml(item.evidence_id || "")}">${escapeHtml(activeLocaleText("פתח פרטים", "Open details"))}</button></div>`;
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
    state.focusedEventMarker?.remove();
    state.focusedEventMarker = null;
    state.focusedEventPopup?.remove();
    state.focusedEventPopup = null;
    renderEvidence();
    return;
  }
  state.focusedEventMarker?.remove();
  state.focusedEventMarker = null;
  state.focusedEventPopup?.remove();
  state.focusedEventPopup = null;
  state.focusedMapSelection = selectionKey;
  renderEvidence();

  activateView("map");
  setTimeout(() => {
    if (!state.mapReady || !state.map) return;
    if (isCellularCallRecord(selectedEvent)) {
      const sideA = cellularCallMapLocation(selectedEvent, "a");
      const sideB = cellularCallMapLocation(selectedEvent, "b");
      if (sideA && sideB) {
        const callBounds = new maplibregl.LngLatBounds();
        callBounds.extend([sideA.lon, sideA.lat]);
        callBounds.extend([sideB.lon, sideB.lat]);
        state.map.fitBounds(callBounds, { padding: 120, maxZoom: 10.5, duration: 450 });
        return;
      }
    }
    state.map.easeTo({
      center: [coordinates.lon, coordinates.lat],
      zoom: Math.max(Number(state.map.getZoom?.() || 0), kind === "location" ? 12 : 13),
      duration: 450
    });
    const descriptor = kind === "evidence" ? milStdEvidenceDescriptor(selectedEvent) : null;
    const markerElement = descriptor ? milStdMarkerElement(descriptor) : document.createElement("div");
    if (!descriptor) {
      markerElement.className = "map-marker focused-map-marker";
      markerElement.style.setProperty("--layer-color", layer?.color || "#8ab4f8");
      markerElement.innerHTML = '<span class="map-marker-dot"></span>';
    }
    markerElement.classList.add("focused-map-selection-marker");
    state.focusedEventMarker = new maplibregl.Marker({ element: markerElement, anchor: "center" })
      .setLngLat([coordinates.lon, coordinates.lat])
      .addTo(state.map);
    state.focusedEventPopup = new maplibregl.Popup({ offset: 32, closeButton: true, closeOnClick: false })
      .setLngLat([coordinates.lon, coordinates.lat])
      .setHTML(mapItemPopupHtml(selectedEvent, kind))
      .addTo(state.map);
  }, 0);
}

function callTimelineEntry(event) {
  const id = event.event_id || event.record_id;
  const time = String(event.call_started_at_utc || event.timestamp_utc || "").replace("T", " ").replace("Z", " UTC");
  const duration = Number(event.call_duration_seconds);
  const party = (side, fallback) => {
    const prefix = `side_${side}`;
    const name = event[`${prefix}_entity_name`] || activeLocaleText(`צד ${side === "a" ? "א׳" : "ב׳"}`, `Side ${side.toUpperCase()}`);
    const number = event[`${prefix}_sim`] || event[`${prefix}_number`] || "—";
    const imei = event[`${prefix}_imei`] || "—";
    return `<span class="call-list-party"><strong>${escapeHtml(name || fallback)}</strong><small dir="ltr">SIM ${escapeHtml(number)}</small><small dir="ltr">IMEI ${escapeHtml(imei)}</small></span>`;
  };
  const callLocation = cellularCallMapLocation(event, "a");
  const location = String(callLocation?.name || event.side_a_location_name || event.location_name || event.side_a_location_id || event.location_id || "—").split(" — ")[0];
  const coordinates = callLocation ? `${callLocation.lat.toFixed(6)}, ${callLocation.lon.toFixed(6)}` : "";
  return `<button type="button" class="call-timeline-entry" data-viewer-kind="record" data-viewer-id="${escapeHtml(id)}" aria-pressed="false">
    <span class="call-list-play"><span class="material-symbols-rounded" aria-hidden="true">play_arrow</span></span>
    <span class="call-list-time"><strong>${escapeHtml(time)}</strong><small>${escapeHtml(id)}${duration > 0 ? ` · ${duration.toFixed(1)}s` : ""}</small></span>
    ${party("a", "A")}${party("b", "B")}
    <span class="call-list-location"><strong>${escapeHtml(location)}</strong><small dir="ltr">${escapeHtml(coordinates)}</small></span>
  </button>`;
}

function ipdrPackageLinkHtml(item, kind) {
  if (kind === "ipdr_package") {
    return `<section class="object-viewer-summary"><button type="button" class="object-viewer-open" data-viewer-kind="ipdr_package" data-viewer-id="${escapeHtml(item.package_id)}">${escapeHtml(item.package_id)}</button><p>${escapeHtml(activeLocaleText("נתוני הדגמה סינתטיים", "Synthetic demonstration data"))} · ${escapeHtml(item.record_count)} ${escapeHtml(activeLocaleText("רשומות", "records"))}</p><button type="button" data-ipdr-package-open="events:IPDR">${escapeHtml(activeLocaleText("פתח רשומות חבילה", "Open package records"))}</button></section>`;
  }
  if (!isIpdrRecord(item) || !item.package_id) return "";
  return `<section class="object-viewer-summary"><button type="button" class="object-viewer-open" data-viewer-kind="ipdr_package" data-viewer-id="${escapeHtml(item.package_id)}">${escapeHtml(activeLocaleText("חבילת ראיות", "Evidence package"))}: ${escapeHtml(item.package_id)}</button></section>`;
}

function ipdrTimelineEntry(event) {
  const id = event.event_id || event.record_id;
  const times = `${event.start_time || activeLocaleText("לא ידוע", "Unknown")} → ${event.end_time || activeLocaleText("לא ידוע", "Unknown")}`;
  const state = event.validation?.state || "unknown";
  const validation = state === "valid" ? activeLocaleText("מרווח תקין", "Valid interval") : state === "invalid" ? activeLocaleText("מרווח לא תקין", "Invalid interval") : activeLocaleText("מרווח לא ידוע", "Unknown interval");
  return `<button type="button" class="call-timeline-entry" data-viewer-kind="record" data-viewer-id="${escapeHtml(id)}"><span dir="ltr">${escapeHtml(times)}</span><strong dir="ltr">${escapeHtml(event.ip_source || "—")} → ${escapeHtml(event.ip_target || "—")}${recordLinkIndicator(event)}</strong><span>${escapeHtml(validation)}</span><span dir="ltr">${escapeHtml(id)}</span></button>`;
}

function renderTimeline() {
  const timeline = document.getElementById("timeline");
  const timelineLayers = focusedTimelineLayers();
  const eventTimelineItems = timelineLayers
    .filter(layer => layer.kind === "events")
    .flatMap(layer => itemsForLayerPresentation(layer).map(event => ({ type: "event", layer, event, sort: event.date })));
  const evidenceTimelineItems = timelineLayers
    .filter(layer => layer.kind === "evidence")
    .flatMap(layer => itemsForLayerPresentation(layer).filter(event => event.evidence_type !== "ipdr_package").map(event => ({ type: "event", layer, event: {
      ...event,
      timestamp_utc: event.valid_from,
      event_summary: event.summary,
      record_id: event.evidence_id,
      location_id: (event.location_ids || [])[0],
      entity_id: (event.subject_entity_ids || [])[0],
    }, sort: event.date })));
  const aggregateTimelineItems = timelineLayers
    .filter(layer => layer.kind === "time_aggregation")
    .flatMap(layer => itemsForLayerPresentation(layer).map(item => ({ type: "aggregation", layer, item, sort: item.sortKey })));
  eventTimelineItems.push(...evidenceTimelineItems);
  if (!eventTimelineItems.length && !aggregateTimelineItems.length) { timeline.className = "timeline empty-state"; timeline.textContent = activeLocaleText("לא נבחרו שכבות עם ציר זמן להצגה.", "No timeline layers were selected for display."); return; }
  timeline.className = "timeline";
  const aggregationHtml = aggregateTimelineItems.map(({ layer, item }) => `
    <article class="timeline-item" style="${layerColorStyle(layer)}">
      <span class="timeline-dot"></span>
      <div class="timeline-time">${escapeHtml(item.timeLabel)}</div>
      <div class="timeline-title">${escapeHtml(layer.label)} · ${escapeHtml(activeLocaleText(`${item.count.toLocaleString("he-IL")} אירועים`, `${item.count.toLocaleString("en-US")} events`))}</div>
      <div class="timeline-summary">${escapeHtml(item.summary)}</div>
    </article>`).join("");
  const callOnly = eventTimelineItems.length > 0 && !aggregateTimelineItems.length && eventTimelineItems.every(({ event }) => isCellularCallRecord(event));
  const eventHtml = eventTimelineItems.sort((a, b) => a.sort - b.sort).map(({ layer, event }) => isIpdrRecord(event) ? ipdrTimelineEntry(event) : isCellularCallRecord(event) ? callTimelineEntry(event) : `
    <article class="timeline-item" style="${layerColorStyle(layer)}">
      <span class="timeline-dot"></span>
      <div class="timeline-time">${escapeHtml(String(event.timestamp_utc || "").replace("T", " ").replace("Z", ""))}</div>
      <div class="timeline-title">${escapeHtml(layer.label)} · ${escapeHtml(event.location_name)}${recordLinkIndicator(event)}</div>
      <div class="timeline-summary">${escapeHtml(event.event_summary)}</div>
    </article>`).join("");
  timeline.classList.toggle("call-list-timeline", callOnly);
  timeline.innerHTML = callOnly ? `<div class="call-list-header"><span></span><span>Date &amp; time</span><span>Side A</span><span>Side B</span><span>Location</span></div><div class="call-list-rows">${eventHtml}</div>` : aggregationHtml + eventHtml;
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
        <span class="result-column-title">${escapeHtml(label)}</span>
        <span class="result-column-actions">
          <button type="button" class="result-column-sort" data-result-sort="${column}" data-result-layer="${escapeHtml(String(layer.id))}" title="${escapeHtml(activeLocaleText(`מיין לפי ${label}. ${directionLabel}`, `Sort by ${label}. ${directionLabel}`))}" aria-label="${escapeHtml(activeLocaleText(`מיין לפי ${label}. ${directionLabel}`, `Sort by ${label}. ${directionLabel}`))}">
            <span class="material-symbols-rounded" aria-hidden="true">${activeSort ? (control.sortDirection === "asc" ? "arrow_upward" : "arrow_downward") : "unfold_more"}</span>
          </button>
          <button type="button" class="result-column-filter-toggle ${filterValue ? "active" : ""}" data-result-filter-toggle="${column}" data-result-layer="${escapeHtml(String(layer.id))}" title="${escapeHtml(activeLocaleText(`סנן לפי ${label}`, `Filter by ${label}`))}" aria-label="${escapeHtml(activeLocaleText(`סנן לפי ${label}`, `Filter by ${label}`))}" aria-expanded="${filterOpen ? "true" : "false"}">
            <span class="material-symbols-rounded" aria-hidden="true">filter_alt</span>
          </button>
        </span>
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
  document.getElementById("evidenceRows")?.querySelectorAll(".object-viewer-open[data-viewer-kind][data-viewer-id]").forEach(open => {
    if (open.nextElementSibling?.classList.contains("table-object-memory")) return;
    const save = document.createElement("button");
    save.type = "button";
    save.className = "table-object-memory";
    save.dataset.memoryObjectKind = open.dataset.viewerKind;
    save.dataset.memoryObjectId = open.dataset.viewerId;
    save.title = activeLocaleText("שמור לזיכרון", "Save to memory");
    save.setAttribute("aria-label", save.title);
    save.innerHTML = '<span class="memory-bookmark-icon" aria-hidden="true"></span>';
    open.insertAdjacentElement("afterend", save);
  });
  const imeiColumns = [...head.querySelectorAll("th")]
    .map((cell, index) => /\bimei\b/i.test(normalizedTableCellText(cell.textContent)) ? index : -1)
    .filter(index => index >= 0);
  if (imeiColumns.length) document.getElementById("evidenceRows")?.querySelectorAll("tr").forEach(row => {
    imeiColumns.forEach(index => {
      const cell = row.children[index];
      const imei = normalizedTableCellText(cell?.textContent);
      if (cell && imei && !cell.querySelector(".collection-imei")) cell.innerHTML = collectionImeiButton(imei);
    });
  });
}

function renderEvidence() {
  const overlay = document.getElementById("rawEventsOverlay");
  const viewStack = overlay?.closest(".view-stack");
  const tabs = document.getElementById("rawEventsTabs");
  const timelineTabs = document.getElementById("timelineLayersTabs");
  const head = document.getElementById("evidenceHead");
  const body = document.getElementById("evidenceRows");
  const filterPanel = document.getElementById("layerFilterPanel");
  if (!overlay || !tabs || !head || !body) return;

  const tableLayers = roleWorkspaceLayers().filter(layer => layer.capabilities.table);
  tableLayers.forEach(layer => ensureLayerFilterState(layer));
  if (!tableLayers.length) {
    overlay.hidden = true;
    tabs.innerHTML = "";
    if (timelineTabs) timelineTabs.innerHTML = "";
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
  overlay.classList.toggle("minimized", state.rawOverlayMinimized && !viewStack?.classList.contains("table-mode"));
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
  const layerTabsMarkup = tableLayers.map(layer => {
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
  tabs.innerHTML = layerTabsMarkup;
  if (timelineTabs) timelineTabs.innerHTML = layerTabsMarkup;

  if (!activeLayer) return;
  ensureLayerFilterState(activeLayer);
  renderLayerFilterPanel(activeLayer);
  const activeItems = activeLayer.visible ? itemsForLayerPresentation(activeLayer) : [];
  if (activeLayer.kind === "assessments") {
    head.innerHTML = `<tr><th>${escapeHtml(activeLocaleText("הערכה", "Assessment"))}</th><th>${escapeHtml(activeLocaleText("מצב", "Status"))}</th><th>${escapeHtml(activeLocaleText("ביטחון", "Confidence"))}</th><th>${escapeHtml(activeLocaleText("שיפוטים מרכזיים", "Key judgments"))}</th><th>${escapeHtml(activeLocaleText("ראיות", "Evidence"))}</th><th>${escapeHtml(activeLocaleText("גרפיקה", "Overlays"))}</th><th>${escapeHtml(activeLocaleText("גרסה", "Revision"))}</th></tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(item => `<tr><td><button type="button" class="object-viewer-open" data-viewer-kind="assessment" data-viewer-id="${escapeHtml(item.assessment_id || "")}">${escapeHtml(item.title || item.assessment_id || "-")}</button><small dir="ltr">${escapeHtml(item.assessment_id || "-")}</small></td><td>${escapeHtml(item.status || "-")}</td><td>${escapeHtml(confidenceLabel(item.confidence))}</td><td>${escapeHtml((item.key_judgments || []).map(entry => entry.judgment || entry).slice(0, 3).join(" · ") || item.summary || "-")}</td><td>${Number((item.evidence_ids || []).length).toLocaleString(currentLocaleTag())}</td><td>${Number((item.overlays || []).length).toLocaleString(currentLocaleTag())}</td><td>${Number(item.revision || 1).toLocaleString(currentLocaleTag())}</td></tr>`).join("") : `<tr><td colspan="7" class="empty-cell">${escapeHtml(activeLocaleText("לא נמצאו הערכות להצגה.", "No assessments found."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "evidence" && activeLayer.items?.length && activeLayer.items.every(item => item.evidence_type === "ipdr_package")) {
    const keys = ["package_id", "filename", "source_system", "record_count", "classification", "validation_state"];
    head.innerHTML = `<tr>${keys.map(key => `<th>${escapeHtml(viewerFieldLabel(key))}</th>`).join("")}</tr>`;
    body.innerHTML = activeItems.map(item => `<tr>${keys.map(key => `<td>${key === "package_id" ? `<button type="button" class="object-viewer-open" data-viewer-kind="ipdr_package" data-viewer-id="${escapeHtml(item.package_id)}">${escapeHtml(item.package_id)}</button>` : escapeHtml(item[key] ?? "—")}</td>`).join("")}</tr>`).join("") || `<tr><td colspan="6" class="empty-cell">${escapeHtml(activeLocaleText("אין חבילות להצגה", "No packages to display"))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  if (activeLayer.kind === "evidence") {
    head.innerHTML = `<tr><th class="result-map-action-column"></th><th>${escapeHtml(activeLocaleText("ראיה", "Evidence"))}</th><th>${escapeHtml(activeLocaleText("מצב", "Status"))}</th><th>${escapeHtml(activeLocaleText("טענה", "Claim"))}</th><th>${escapeHtml(activeLocaleText("ישות", "Entity"))}</th><th>${escapeHtml(activeLocaleText("מיקום", "Location"))}</th><th>${escapeHtml(activeLocaleText("ביטחון", "Confidence"))}</th><th>${escapeHtml(activeLocaleText("רשומות מקור", "Source records"))}</th></tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(item => {
      const itemId = item.evidence_id;
      const selected = isMapItemSelected(activeLayer.id, "evidence", itemId);
      return `<tr class="${selected ? "map-selected-row" : ""}"><td class="result-map-action-cell">${mapActionButton(activeLayer.id, "evidence", itemId, item)}</td><td><button type="button" class="object-viewer-open" data-viewer-kind="evidence" data-viewer-id="${escapeHtml(itemId)}">${escapeHtml(itemId)}</button></td><td>${escapeHtml(item.evidence_status || "-")}</td><td>${escapeHtml(item.object_class || item.claim_type || "-")}</td><td>${escapeHtml((item.subject_entity_ids || []).join(", ") || "-")}</td><td>${escapeHtml((item.location_ids || []).join(", ") || "-")}</td><td>${escapeHtml(confidenceLabel(item.confidence))}</td><td>${Number((item.source_record_ids || []).length).toLocaleString(currentLocaleTag())}</td></tr>`;
    }).join("") : `<tr><td colspan="8" class="empty-cell">${escapeHtml(activeLocaleText("לא נמצאו ראיות להצגה.", "No evidence found."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
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
  if (activeLayer.kind === "person_entities") {
    head.innerHTML = `<tr><th>${escapeHtml(activeLocaleText("אדם", "Person"))}</th><th>${escapeHtml(activeLocaleText("גיל", "Age"))}</th><th>${escapeHtml(activeLocaleText("לאום", "Nationality"))}</th><th>${escapeHtml(activeLocaleText("מגורים", "Residence"))}</th><th>${escapeHtml(activeLocaleText("שפות", "Languages"))}</th><th>${escapeHtml(activeLocaleText("קשרים", "Connections"))}</th><th>${escapeHtml(activeLocaleText("רשומות", "Records"))}</th></tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(item => {
      const name = item.canonical_name || item.entity_id || "-";
      const initials = String(name).split(/\s+/).map(part => part[0]).join("").slice(0, 2).toUpperCase();
      const imageUrl = safeMediaUrl(item.image_url);
      const portrait = imageUrl
        ? `<img src="${escapeHtml(imageUrl)}" alt="" loading="lazy">`
        : `<span aria-hidden="true">${escapeHtml(initials)}</span>`;
      return `<tr class="person-entity-table-row">
        <td><div class="person-table-identity"><div class="person-table-portrait">${portrait}</div><div><button type="button" class="object-viewer-open" data-viewer-kind="person" data-viewer-id="${escapeHtml(item.entity_id || "")}">${escapeHtml(name)}</button><small dir="ltr">${escapeHtml(item.entity_id || "-")}</small></div></div></td>
        <td>${escapeHtml(item.age_years || "-")}</td>
        <td>${escapeHtml(item.nationality || "-")}</td>
        <td>${escapeHtml(item.residence || "-")}</td>
        <td>${escapeHtml(viewerValue(item.languages || "-"))}</td>
        <td>${escapeHtml(viewerValue(item.connections || "-"))}</td>
        <td>${Number(item.event_count || item.count || 0).toLocaleString(currentLocaleTag())}</td>
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
        <td><button type="button" class="object-viewer-open" data-viewer-kind="${isPersonEntity(item) ? "person" : "organization"}" data-viewer-id="${escapeHtml(item.entity_id || "")}">${escapeHtml(item.canonical_name || item.entity_id || "-")}</button></td>
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
  const i360KeysOf = item => Object.keys(item || {}).filter(key => key.startsWith("i360.") && item[key] != null && item[key] !== "");
  if (activeLayer.kind === "events" && activeLayer.items?.length && activeLayer.items.every(item => i360KeysOf(item).length)) {
    // Every i360 field the layer's items carry, except the image/media ones (the viewer shows those).
    const keys = [...new Set(activeLayer.items.flatMap(i360KeysOf))].sort((a, b) => a.localeCompare(b, "en"))
      .filter(key => !/^i360\.(media|thumbnail|image|files?)(\.|$)/.test(key));
    const first = ["i360.item_id", "i360.event_time", "i360.item_type", "i360.sub_type", "i360.source_application"].filter(key => keys.includes(key));
    const columns = [...first, ...keys.filter(key => !first.includes(key))];
    head.innerHTML = `<tr><th class="result-map-action-column" data-result-action-column="true"></th>${columns.map(key => `<th>${escapeHtml(viewerFieldLabel(key))}</th>`).join("")}</tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(event => {
      const eventId = String(event.record_id || event.event_id || "");
      const selected = isMapItemSelected(activeLayer.id, "event", eventId);
      return `<tr class="${[selected ? "map-selected-row" : "", isViewerRecordSelected(eventId) ? "viewer-selected-row" : ""].filter(Boolean).join(" ")}"><td class="result-map-action-cell">${mapActionButton(activeLayer.id, "event", eventId, event)}</td>${columns.map(key => {
        const value = escapeHtml(event[key] == null || event[key] === "" ? "—" : event[key]);
        return key === "i360.item_id"
          ? `<td dir="ltr"><button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(eventId)}">${value}</button>${recordLinkIndicator(event)}</td>`
          : `<td>${value}</td>`;
      }).join("")}</tr>`;
    }).join("") : `<tr><td colspan="${columns.length + 1}" class="empty-cell">${escapeHtml(activeLocaleText("השכבה מוסתרת או ריקה.", "Layer is hidden or empty."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  const cellularGeolocationTable = activeLayer.items?.length
    ? activeLayer.items.every(isCellularGeolocationRecord)
    : activeLayer.catalogLayerId === "events:Cellular Geolocations";
  if (cellularGeolocationTable) {
    const columns = ["event_id", "timestamp_utc", "imei", "sim", "target_msisdn", "target_imsi", "operator_msisdn", "operator_imsi", "location_name"];
    head.innerHTML = `<tr><th class="result-map-action-column" data-result-action-column="true"></th>${columns.map(key => `<th>${escapeHtml(viewerFieldLabel(key))}</th>`).join("")}</tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(event => {
      const id = String(event.record_id || event.event_id || "");
      return `<tr class="${isViewerRecordSelected(id) ? "viewer-selected-row" : ""}"><td>${mapActionButton(activeLayer.id, "event", id, event)}</td>${columns.map(key => {
        const value = escapeHtml(event[key] || (key === "location_name" ? event.location_id : "") || "—");
        return key === "event_id" ? `<td><button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(id)}">${value}</button>${recordLinkIndicator(event)}</td>` : `<td dir="ltr">${key === "imei" ? collectionImeiButton(event[key]) : value}</td>`;
      }).join("")}</tr>`;
    }).join("") : `<tr><td colspan="6" class="empty-cell">${escapeHtml(activeLocaleText("השכבה ריקה.", "Layer is empty."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  const adintTable = activeLayer.items?.length
    ? activeLayer.items.every(isAdintRecord)
    : activeLayer.catalogLayerId === "events:ADINT";
  if (adintTable) {
    const columns = ["event_id", "device_id", "timestamp_utc", "brand", "model", "os", "keyboard_language", "ip", "latitude", "longitude", "accuracy_m"];
    head.innerHTML = `<tr><th class="result-map-action-column" data-result-action-column="true"></th>${columns.map(key => `<th>${escapeHtml(viewerFieldLabel(key))}</th>`).join("")}</tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(event => {
      const eventId = String(event.record_id || event.event_id || "");
      const selected = isMapItemSelected(activeLayer.id, "event", eventId);
      return `<tr class="${[selected ? "map-selected-row" : "", isViewerRecordSelected(eventId) ? "viewer-selected-row" : ""].filter(Boolean).join(" ")}"><td class="result-map-action-cell">${mapActionButton(activeLayer.id, "event", eventId, event)}</td>${columns.map(key => {
        const value = escapeHtml(event[key] == null || event[key] === "" ? "—" : event[key]);
        return key === "event_id"
          ? `<td dir="ltr"><button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(eventId)}">${value}</button>${recordLinkIndicator(event)}</td>`
          : `<td dir="ltr">${value}</td>`;
      }).join("")}</tr>`;
    }).join("") : `<tr><td colspan="12" class="empty-cell">${escapeHtml(activeLocaleText("השכבה מוסתרת או ריקה.", "Layer is hidden or empty."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  const ipdrTable = activeLayer.items?.length
    ? activeLayer.items.every(isIpdrRecord)
    : activeLayer.catalogLayerId === "events:IPDR";
  if (ipdrTable && (activeLayer.items || []).some(event => event.source_record_id)) {
    const fields = ["event_id", ...IPDR_SOURCE_FIELDS];
    head.innerHTML = `<tr>${fields.map(key => `<th>${escapeHtml(ipdrTableFieldLabel(key))}</th>`).join("")}</tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(event => `<tr class="${isViewerRecordSelected(event.event_id || event.record_id || "") ? "viewer-selected-row" : ""}">${fields.map(key => {
      const value = escapeHtml(event[key] == null || event[key] === "" ? "—" : event[key]);
      return key === "event_id"
        ? `<td dir="ltr"><button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(event.event_id || event.record_id || "")}">${value}</button>${recordLinkIndicator(event)}</td>`
        : `<td dir="ltr">${key === "imei" ? collectionImeiButton(event[key]) : value}</td>`;
    }).join("")}</tr>`).join("") : `<tr><td colspan="19" class="empty-cell">${escapeHtml(activeLocaleText("השכבה מוסתרת או ריקה.", "Layer is hidden or empty."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  if (ipdrTable) {
    head.innerHTML = `<tr><th>${escapeHtml(activeLocaleText("מזהה רשומה", "Record ID"))}</th><th>${escapeHtml(activeLocaleText("זמן", "Time"))}</th><th>${escapeHtml(activeLocaleText("אמינות", "Reliability"))}</th><th>${escapeHtml(activeLocaleText("ודאות", "Certainty"))}</th><th>${escapeHtml(activeLocaleText("כתובת IP", "IP address"))}</th><th>IMEI</th><th>${escapeHtml(activeLocaleText("תקציר", "Summary"))}</th></tr>`;
    body.innerHTML = activeItems.length ? activeItems.map(event => `
      <tr><td dir="ltr"><button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(event.record_id || event.event_id || "")}">${escapeHtml(event.record_id || event.event_id || "-")}</button>${recordLinkIndicator(event)}</td>
      <td dir="ltr">${escapeHtml(event.timestamp_utc || "-")}</td>
      <td>${escapeHtml(event.source_reliability_label || event.source_reliability || "-")}</td>
      <td>${escapeHtml(event.certainty_level || "-")}</td>
      <td dir="ltr">${escapeHtml(event.ip_address || "-")}</td>
      <td dir="ltr">${collectionImeiButton(event.imei)}</td>
      <td>${escapeHtml(event.event_summary || "-")}</td></tr>`).join("")
      : `<tr><td colspan="7" class="empty-cell">${escapeHtml(activeLocaleText("השכבה מוסתרת או ריקה.", "Layer is hidden or empty."))}</td></tr>`;
    enhanceResultsTable(activeLayer);
    return;
  }
  const cellularCallTable = (activeLayer.items || []).some(isCellularCallRecord) || ["events:Cellular Calls", "events:שיחות סלולר"].includes(activeLayer.catalogLayerId);
  const endpointHeaders = cellularCallTable
    ? `<th>${escapeHtml(activeLocaleText("מיקום צד א׳", "Side A location"))}</th><th>${escapeHtml(activeLocaleText("מיקום צד ב׳", "Side B location"))}</th><th>Side A SIM</th><th>Side B SIM</th><th>Side A IMEI</th><th>Side B IMEI</th>`
    : "";
  head.innerHTML = `<tr><th class="result-map-action-column" data-result-action-column="true" aria-label="${escapeHtml(activeLocaleText("פעולות", "Actions"))}"></th><th>${escapeHtml(activeLocaleText("מזהה רשומה", "Record ID"))}</th><th>${escapeHtml(activeLocaleText("זמן", "Time"))}</th><th>${escapeHtml(activeLocaleText("אמינות", "Reliability"))}</th><th>${escapeHtml(activeLocaleText("ודאות", "Certainty"))}</th><th>${escapeHtml(activeLocaleText("גורם", "Actor"))}</th><th>${escapeHtml(activeLocaleText("מיקום", "Location"))}</th>${endpointHeaders}<th>${escapeHtml(activeLocaleText("תקציר", "Summary"))}</th></tr>`;
  body.innerHTML = activeItems.length ? activeItems.map(event => {
    const eventId = String(event.record_id || event.event_id || "");
    const selected = isMapItemSelected(activeLayer.id, "event", eventId);
    return `
      <tr class="${[selected ? "map-selected-row" : "", isViewerRecordSelected(eventId) ? "viewer-selected-row" : ""].filter(Boolean).join(" ")}">
      <td class="result-map-action-cell">${mapActionButton(activeLayer.id, "event", eventId, event)}</td>
      <td dir="ltr"><button type="button" class="object-viewer-open" data-viewer-kind="record" data-viewer-id="${escapeHtml(eventId)}">${escapeHtml(event.record_id || event.event_id || "-")}</button>${recordLinkIndicator(event)}</td>
      <td dir="ltr">${escapeHtml(event.timestamp_utc)}</td>
      <td>${escapeHtml(event.source_reliability_label || event.source_reliability || "-")}</td>
      <td>${escapeHtml(event.certainty_level || "-")}</td>
      <td>${escapeHtml(event.entity_name || event.entity_id || "-")}</td>
      <td>${escapeHtml(event.location_name || "-")}</td>
      ${cellularCallTable ? `<td dir="ltr">${escapeHtml(event.side_a_location_id || "-")}</td><td dir="ltr">${escapeHtml(event.side_b_location_id || "-")}</td><td dir="ltr">${escapeHtml(event.side_a_sim || "—")}</td><td dir="ltr">${escapeHtml(event.side_b_sim || "—")}</td><td dir="ltr">${collectionImeiButton(event.side_a_imei)}</td><td dir="ltr">${collectionImeiButton(event.side_b_imei)}</td>` : ""}
      <td>${escapeHtml(event.event_summary || "-")}</td>
    </tr>`;
  }).join("") : `<tr><td colspan="${cellularCallTable ? 12 : 8}" class="empty-cell">${escapeHtml(activeLocaleText("השכבה מוסתרת או ריקה.", "Layer is hidden or empty."))}</td></tr>`;
  enhanceResultsTable(activeLayer);
}

function resetInvestigation() {
  closeObjectViewer();
  state.layers = [];
  state.activeLayerId = null;
  state.rawOverlayMinimized = false;
  state.rawOverlayHeight = 28;
  state.resultTableControls.clear();
  state.focusedMapSelection = null;
  state.investigationMemory = null;
  state.investigationMemoryError = "";
  state.investigationMemoryLoading = false;
  state.layerSearchQuery = "";
  state.layerSearchOpen = false;
  state.activeTeamMemberId = null;
  state.activeRoleWorkspace = null;
  activateView("map");
  renderAllViews();
  renderLayerSelector();
  renderInvestigationSelector();
  renderMichlolTeam();
  if (state.map) setTimeout(() => state.map.resize(), 0);
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[char]);
}

document.addEventListener("input", event => {
  const filter = event.target.closest(".result-column-filter[data-result-filter]");
  if (!filter) return;
  const control = resultTableControl(filter.dataset.resultLayer);
  control.filters[Number(filter.dataset.resultFilter)] = filter.value;
  applyResultTableControls(filter.dataset.resultLayer);
});

document.addEventListener("click", event => {
  if (polygonActionMenu && !polygonActionMenu.hidden && !event.target.closest("#polygonActionMenu")) {
    closePolygonActionMenu();
  }
  const resultTableControlEntries = state.resultTableControls instanceof Map
    ? [...state.resultTableControls.entries()]
    : Object.entries(state.resultTableControls || {});
  const openResultFilter = resultTableControlEntries.find(([, control]) => Number.isInteger(control.openFilterColumn));
  if (openResultFilter && !event.target.closest(".result-column-filter-popover, .result-column-filter-toggle")) {
    openResultFilter[1].openFilterColumn = null;
    renderEvidence();
  }
  const memoryDelete = event.target.closest("[data-memory-delete-group][data-memory-delete-id]");
  if (memoryDelete) {
    event.preventDefault();
    void deleteMemoryEntry(memoryDelete.dataset.memoryDeleteGroup, memoryDelete.dataset.memoryDeleteId).catch(error => { memoryCommentError.textContent = error.message; memoryCommentError.hidden = false; });
    return;
  }
  const memoryOpen = event.target.closest("[data-memory-open-group][data-memory-open-id]");
  if (memoryOpen) {
    event.preventDefault();
    void openMemoryEntry(memoryOpen.dataset.memoryOpenGroup, memoryOpen.dataset.memoryOpenId, memoryOpen);
    return;
  }
  const memoryObject = event.target.closest("[data-memory-object-kind][data-memory-object-id]");
  if (memoryObject) {
    event.preventDefault();
    void saveObjectToInvestigationMemory(memoryObject.dataset.memoryObjectKind, memoryObject.dataset.memoryObjectId, memoryObject);
    return;
  }
  const imeiCollection = event.target.closest("[data-collection-imei]");
  if (imeiCollection) {
    event.preventDefault();
    openCollectionRequestDialog({ type: "imei", imei: imeiCollection.dataset.collectionImei }, imeiCollection);
    return;
  }
  const telecomApproval = event.target.closest("[data-approve-telecom-entity]");
  if (telecomApproval) {
    event.preventDefault();
    void approveExtractedTelecomIdentity(telecomApproval.dataset.approveTelecomEntity, telecomApproval);
    return;
  }
  const visualMediaFullscreen = event.target.closest("[data-visual-media-fullscreen]");
  if (visualMediaFullscreen) {
    event.preventDefault();
    void toggleVisualCollectionMediaFullscreen(visualMediaFullscreen);
    return;
  }
  if (event.target.closest("#visualMediaOverlayClose") || event.target.id === "visualMediaOverlay") {
    closeVisualCollectionMediaFullscreen();
    return;
  }
  const linkedRecordTrigger = event.target.closest("[data-linked-record-open][data-viewer-id]");
  if (linkedRecordTrigger) {
    event.preventDefault();
    void openLinkedRawRecord(linkedRecordTrigger.dataset.viewerId, linkedRecordTrigger);
    return;
  }
  const viewerTrigger = event.target.closest("[data-viewer-kind][data-viewer-id]");
  if (viewerTrigger) {
    event.preventDefault();
    openObjectViewer(viewerTrigger.dataset.viewerKind, viewerTrigger.dataset.viewerId, viewerTrigger);
    return;
  }
  const packageOpen = event.target.closest("[data-ipdr-package-open]");
  if (packageOpen) {
    closeObjectViewer();
    void openCatalogLayer(packageOpen.dataset.ipdrPackageOpen);
    return;
  }
  if (event.target.closest("#objectViewerMaximize")) {
    setViewerMaximized(!document.getElementById("objectViewer").classList.contains("is-maximized"));
    return;
  }
  if (event.target.closest("#objectViewerClose") || event.target.id === "objectViewer") {
    closeObjectViewer();
    return;
  }
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
    selectTeamMember(michlolMember.dataset.memberId);
    return;
  }
  if (!event.target.closest(".investigation-switcher") && state.investigationSelectorOpen) {
    setInvestigationSelectorOpen(false);
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
    state.layers = state.layers.filter(item => item.id !== layerIdToClose);
    if (state.activeLayerId === layerIdToClose) {
      state.activeLayerId = state.layers.find(layer => layer.capabilities.table && layer.visible)?.id
        || state.layers.find(layer => layer.capabilities.table)?.id
        || null;
    }
    renderAllViews();
    renderLayerSelector();
    return;
  }
  const rawLayerTab = event.target.closest("[data-layer-id]");
  if (rawLayerTab) {
    state.activeLayerId = rawLayerTab.dataset.layerId;
    renderEvidence();
    renderTimeline();
  }
  if (event.target.closest("#rawEventsMinimize")) {
    state.rawOverlayMinimized = !state.rawOverlayMinimized;
    renderEvidence();
  }
  if (event.target.closest("#rawEventsClose")) {
    state.layers = [];
    state.activeLayerId = null;
    renderAllViews();
    renderLayerSelector();
  }
  if (!event.target.closest(".layer-selector") && state.layerSearchOpen) {
    state.layerSearchOpen = false;
    renderLayerSelector();
  }
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
  if (event.key === "Escape" && !document.getElementById("visualMediaOverlay")?.hidden) {
    event.preventDefault();
    closeVisualCollectionMediaFullscreen();
    return;
  }
  const columnFilter = event.target.closest(".result-column-filter[data-result-filter]");
  if (columnFilter && (event.key === "Enter" || event.key === "Escape")) {
    event.preventDefault();
    const control = resultTableControl(columnFilter.dataset.resultLayer);
    control.openFilterColumn = null;
    renderEvidence();
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

welcomeDraftButton?.addEventListener("click", () => startDraftInvestigation());

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
    const existing = findInvestigationByName(name);
    if (existing) selectInvestigation(existing);
    else void addOrSelectInvestigation();
  }
  if (event.key === "Escape") setInvestigationSelectorOpen(false);
});
investigationAddButton?.addEventListener("click", () => void addOrSelectInvestigation());
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
});
memoryButton?.addEventListener("click", () => openMemoryScreen(memoryButton));
document.getElementById("memoryModalClose")?.addEventListener("click", closeMemoryScreen);
memoryModal?.addEventListener("click", event => { if (event.target === memoryModal) closeMemoryScreen(); });
document.getElementById("polygonSaveMemory")?.addEventListener("click", () => {
  const polygon = pendingPolygonAction;
  closePolygonActionMenu();
  if (polygon) void savePolygonToInvestigationMemory(polygon);
});
document.getElementById("polygonRequestCollection")?.addEventListener("click", () => {
  const polygon = pendingPolygonAction;
  closePolygonActionMenu();
  if (polygon) openCollectionRequestDialog({ type: "polygon", coordinates: polygon.coordinates }, document.getElementById("polygonDrawButton"));
});
document.getElementById("collectionRequestClose")?.addEventListener("click", closeCollectionRequestDialog);
document.getElementById("collectionRequestCancel")?.addEventListener("click", closeCollectionRequestDialog);
collectionRequestModal?.addEventListener("click", event => { if (event.target === collectionRequestModal) closeCollectionRequestDialog(); });
collectionRequestTypes?.addEventListener("change", updateCollectionSourceSelectionAction);
collectionRequestForm?.addEventListener("submit", async event => {
  event.preventDefault();
  const submit = document.getElementById("collectionRequestSubmit");
  submit.disabled = true;
  collectionRequestError.hidden = true;
  try { await submitCollectionRequest(); }
  catch (error) { collectionRequestError.textContent = error.message || activeLocaleText("שליחת בקשת האיסוף נכשלה", "Could not submit collection request"); collectionRequestError.hidden = false; }
  finally { submit.disabled = false; }
});
document.querySelectorAll("[data-close-task-modal]").forEach(button => button.addEventListener("click", () => {
  closeCollectionTaskDialog(document.getElementById(button.dataset.closeTaskModal));
}));
[adintTaskModal, sigintTaskModal, cellularCallsTaskModal, cctvTaskModal].forEach(modal => {
  modal?.addEventListener("click", event => { if (event.target === modal) closeCollectionTaskDialog(modal); });
});
document.querySelectorAll("[data-exclusive-chips], [data-task-segment]").forEach(group => group.addEventListener("click", event => {
  const button = event.target.closest("button");
  if (!button) return;
  group.querySelectorAll("button").forEach(item => item.classList.toggle("selected", item === button));
}));
document.querySelectorAll("[data-multi-chips]").forEach(group => group.addEventListener("click", event => {
  const button = event.target.closest("button");
  if (button) button.classList.toggle("selected");
}));
function validateAdintTaskForm() {
  const from = document.getElementById("adintDateFrom");
  const to = document.getElementById("adintDateTo");
  if (!from || !to) return true;
  to.min = from.value;
  to.setCustomValidity(from.value && to.value && from.value > to.value ? "The end date must be on or after the start date." : "");
  return to.checkValidity();
}
function validateSigintIdentifiers() {
  const imei = document.getElementById("sigintImei");
  const msisdn = document.getElementById("sigintMsisdn");
  const imsi = document.getElementById("sigintImsi");
  const stateLabel = document.getElementById("sigintImeiState");
  const values = [imei, msisdn, imsi].map(input => String(input?.value || "").trim());
  const imeiValid = !values[0] || /^\d{15}$/.test(values[0]);
  if (imei) imei.setCustomValidity(imeiValid ? "" : "IMEI must contain 15 digits.");
  [msisdn, imsi].forEach(input => input?.setCustomValidity(values.some(Boolean) ? "" : "Enter at least one identifier."));
  if (stateLabel) { stateLabel.textContent = imeiValid && values[0] ? "✓ valid" : "Enter a 15-digit IMEI"; stateLabel.classList.toggle("invalid", !imeiValid); }
  return imeiValid && values.some(Boolean);
}
document.getElementById("adintDateFrom")?.addEventListener("change", validateAdintTaskForm);
document.getElementById("adintDateTo")?.addEventListener("change", validateAdintTaskForm);
["sigintImei", "sigintMsisdn", "sigintImsi"].forEach(id => document.getElementById(id)?.addEventListener("input", validateSigintIdentifiers));
document.getElementById("sigintCircles")?.addEventListener("change", () => {
  ["sigintMainCircle", "sigintSubCircle"].forEach(id => { const field = document.getElementById(id); if (field) field.disabled = false; });
  const caseField = document.getElementById("sigintCaseSelect"); if (caseField) caseField.disabled = true;
});
document.getElementById("sigintCase")?.addEventListener("change", () => {
  ["sigintMainCircle", "sigintSubCircle"].forEach(id => { const field = document.getElementById(id); if (field) field.disabled = true; });
  const caseField = document.getElementById("sigintCaseSelect"); if (caseField) caseField.disabled = false;
});
document.getElementById("adintEditMap")?.addEventListener("click", () => {
  closeCollectionTaskDialog(adintTaskModal);
  document.getElementById("polygonDrawButton")?.click();
});
document.getElementById("cctvEditMap")?.addEventListener("click", () => {
  closeCollectionTaskDialog(cctvTaskModal);
  document.getElementById("polygonDrawButton")?.click();
});
document.getElementById("adintTaskForm")?.addEventListener("submit", async event => {
  if (!validateAdintTaskForm() || !event.currentTarget.checkValidity()) { event.preventDefault(); event.currentTarget.reportValidity(); return; }
  event.preventDefault(); await completeDemoCollectionTask(adintTaskModal, "adint");
});
document.getElementById("sigintTaskForm")?.addEventListener("submit", async event => {
  if (!validateSigintIdentifiers() || !event.currentTarget.checkValidity()) { event.preventDefault(); event.currentTarget.reportValidity(); return; }
  event.preventDefault(); await completeDemoCollectionTask(sigintTaskModal, "cellular_geolocations");
});
document.getElementById("cellularCallsTaskForm")?.addEventListener("submit", async event => {
  if (!event.currentTarget.checkValidity()) { event.preventDefault(); event.currentTarget.reportValidity(); return; }
  event.preventDefault(); await completeDemoCollectionTask(cellularCallsTaskModal, "cellular_calls");
});
document.getElementById("cctvTaskForm")?.addEventListener("submit", async event => {
  if (!event.currentTarget.checkValidity()) { event.preventDefault(); event.currentTarget.reportValidity(); return; }
  event.preventDefault(); await completeDemoCollectionTask(cctvTaskModal, "cctv");
});
document.getElementById("memoryCommentClose")?.addEventListener("click", closeMemoryCommentDialog);
document.getElementById("memoryCommentCancel")?.addEventListener("click", closeMemoryCommentDialog);
memoryCommentModal?.addEventListener("click", event => { if (event.target === memoryCommentModal) closeMemoryCommentDialog(); });
memoryCommentForm?.addEventListener("submit", async event => {
  event.preventDefault();
  const action = pendingMemoryCommentAction;
  if (!action) return;
  const submit = document.getElementById("memoryCommentSubmit");
  submit.disabled = true;
  memoryCommentError.hidden = true;
  try { await action.onSave(memoryCommentValue(memoryCommentInput.value)); closeMemoryCommentDialog(); }
  catch (error) { memoryCommentError.textContent = error.message || activeLocaleText("השמירה נכשלה", "Save failed"); memoryCommentError.hidden = false; }
  finally { submit.disabled = false; }
});
appHomeButton?.addEventListener("click", () => setPageView("welcome"));
welcomePage?.addEventListener("click", event => {
  const action = event.target.closest("[data-welcome-action]");
  if (action) {
    if (action.dataset.welcomeAction === "join" && action.dataset.invitedInvestigation === "true") {
      joinInvitedInvestigation(invitedInvestigationById(action.dataset.invitationId));
      return;
    }
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
  if (event.key === "Escape" && memoryCommentModal && !memoryCommentModal.hidden) {
    event.preventDefault();
    closeMemoryCommentDialog();
    return;
  }
  if (event.key === "Escape" && memoryModal && !memoryModal.hidden) {
    event.preventDefault();
    closeMemoryScreen();
    return;
  }
  if (event.key === "Escape" && collectionRequestModal && !collectionRequestModal.hidden) {
    event.preventDefault();
    closeCollectionRequestDialog();
    return;
  }
  if (event.key === "Escape" && adintTaskModal && !adintTaskModal.hidden) {
    event.preventDefault();
    closeCollectionTaskDialog(adintTaskModal);
    return;
  }
  if (event.key === "Escape" && sigintTaskModal && !sigintTaskModal.hidden) {
    event.preventDefault();
    closeCollectionTaskDialog(sigintTaskModal);
    return;
  }
  if (event.key === "Escape" && cellularCallsTaskModal && !cellularCallsTaskModal.hidden) {
    event.preventDefault();
    closeCollectionTaskDialog(cellularCallsTaskModal);
    return;
  }
  if (event.key === "Escape" && cctvTaskModal && !cctvTaskModal.hidden) {
    event.preventDefault();
    closeCollectionTaskDialog(cctvTaskModal);
    return;
  }
  if (event.key === "Escape" && polygonActionMenu && !polygonActionMenu.hidden) {
    event.preventDefault();
    closePolygonActionMenu();
    return;
  }
  if (event.key === "Escape" && !document.getElementById("objectViewer").hidden) {
    event.preventDefault();
    closeObjectViewer();
    return;
  }
  if (event.key === "Escape" && welcomeActionModal && !welcomeActionModal.hidden) {
    closeWelcomeAction();
  }
  if (event.key === "Escape" && draftCreateModal && !draftCreateModal.hidden) {
    closeDraftCreateModal();
  }
});
applyLocaleUi();
setPageView("welcome", { focus: false });

async function boot() {
  if (demoRuntime?.scenario_id !== "kosovo" && demoRuntime?.scenario_id) {
    Object.keys(LOCATIONS).forEach(key => delete LOCATIONS[key]);
  }
  initMap();
  await loadInvestigations();
  await loadLayerCatalog();
  await loadInvestigationMemory({ restoreLayers: true });
  let runtimeStatus = null;
  try {
    runtimeStatus = await fetch(buildLocaleApiUrl("/api/status"), { cache: "no-store" }).then(response => response.json());
    Object.keys(LOCATIONS).forEach(key => delete LOCATIONS[key]);
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
      renderAllViews();
    }
    const datasetUrl = runtimeStatus.dataset_url || buildLocaleApiUrl("/api/dataset/events");
    const response = await fetch(datasetUrl, { cache: "no-store" });
    if (!response.ok) throw new Error("dataset unavailable");
    state.events = parseCsv(await response.text()).map(enrich);
    try {
      const entityResponse = await fetch(buildLocaleApiUrl(`/api/layers/${encodeURIComponent("entity-metadata:all")}/rows`), { cache: "no-store" });
      const entityPayload = await entityResponse.json();
      if (!entityResponse.ok) throw new Error(entityPayload.error || "entity directory unavailable");
      state.entityDirectory = Array.isArray(entityPayload.rows) ? entityPayload.rows : [];
    } catch (error) {
      state.entityDirectory = [];
    }
    const versionLabel = runtimeStatus.dataset_version ? ` · ${runtimeStatus.dataset_version.toUpperCase()}` : "";
    updateSystemStatus("dataset",
      `${state.events.length.toLocaleString("he-IL")} אירועים זמינים במאגר${versionLabel}`,
      `${state.events.length.toLocaleString("en-US")} events available in the dataset${versionLabel}`,
      "ready"
    );
  } catch (error) {
    updateSystemStatus("dataset", "טעינת הנתונים נכשלה", "Failed to load data", "error");
  }
}

boot();
