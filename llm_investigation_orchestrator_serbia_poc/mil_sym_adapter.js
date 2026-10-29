/* MIL-STD-2525E Change 1 point mappings. See vendor/mil-sym-ts/README.md. */
(function (root) {
  "use strict";
  const registry = Object.freeze({
    "unit": { basic: "10000000" },
    "brigade": { basic: "10000000", echelon: "18" },
    "infantry": { basic: "10121100" },
    "mechanized-infantry": { basic: "10121102" },
    "engineer": { basic: "10140700" },
    "headquarters": { basic: "10000000", headquarters: "2" },
    "aviation": { basic: "10000000" },
    "armored-vehicle": { basic: "15120100" },
    "logistics-truck": { basic: "15140100" },
    // A point observation supplies no two-point geometry for the convoy control measure.
    "vehicle-convoy": { basic: "15120000" },
    "helicopter": { basic: "01110200" }
  });
  const affiliations = Object.freeze({ unknown: "1", friendly: "3", neutral: "4", hostile: "6" });
  const cache = new Map();
  function sidc(key, affiliation = "unknown") {
    const entry = registry[key];
    if (!entry) return null;
    return "150" + (affiliations[affiliation] || "1") + entry.basic.slice(0, 2) + "0" +
      (entry.headquarters || "0") + (entry.echelon || "00") + entry.basic.slice(2) +
      (entry.modifier1 || "00") + "00";
  }
  function render(key, affiliation) {
    const id = sidc(key, affiliation);
    if (!id || !root.C5Ren) return null;
    if (cache.has(id)) return cache.get(id);
    try {
      const lib = root.C5Ren;
      const info = lib.MSLookup.getInstance().getMSLInfo(id);
      if (!info || info.getBasicSymbolID() !== registry[key].basic || info.getMinPointCount() !== 1) return null;
      const attributes = new Map([[lib.MilStdAttributes.PixelSize, "40"]]);
      const result = lib.MilStdIconRenderer.getInstance().RenderSVG(id, new Map(), attributes);
      const svg = result?.getSVG();
      if (!svg || !svg.includes("<svg") || !/<(?:path|rect|circle|ellipse|polygon|polyline|line)\b/.test(svg)) return null;
      const rendered = Object.freeze({ sidc: id, name: info.getName(), uri: "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg) });
      if (cache.size >= 128) cache.delete(cache.keys().next().value);
      cache.set(id, rendered);
      return rendered;
    } catch (error) {
      console.warn("Military symbol unavailable; using a plain marker", key, error);
      return null;
    }
  }
  root.MilitarySymbols = Object.freeze({ registry, sidc, render });
})(typeof window === "undefined" ? globalThis : window);
