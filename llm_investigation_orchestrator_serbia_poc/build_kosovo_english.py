"""Build a complete English projection without changing identifiers or evidence facts."""
import csv, json, re
from pathlib import Path
from generate_english_projection import EXACT_TEXT_MAP, PHRASE_REPLACEMENTS, LOCATION_PATTERNS
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data/serbian_intelligence_v2_1"
OUTPUT = ROOT / "data/kosovo_english_v1"
HEBREW = re.compile(r"[\u0590-\u05ff]")
def normalize(value):
    return value.replace("״", '\"').replace("׳", "'").replace("־", "-")
TERMS = {normalize(k): v for k,v in [*PHRASE_REPLACEMENTS, *EXACT_TEXT_MAP.items(), *json.loads((ROOT / "kosovo_english_terms.json").read_text(encoding="utf-8")).items()] if HEBREW.search(k)}
# Include complete location names before translating smaller constituent phrases.
for item in json.loads((SOURCE / "serbia_kosovo_locations_v2_1.json").read_text(encoding="utf-8")).values():
    for field,value in item.items():
        if isinstance(value,str):
            for pattern, replacement in LOCATION_PATTERNS:
                match=pattern.fullmatch(value)
                if match: TERMS[normalize(value)] = replacement(match)
PATTERN = re.compile("|".join(re.escape(k) for k in sorted(TERMS,key=len,reverse=True)))
def translate(value):
    if isinstance(value,dict): return {k:translate(v) for k,v in value.items()}
    if isinstance(value,list): return [translate(v) for v in value]
    if not isinstance(value,str) or not HEBREW.search(value): return value
    result = PATTERN.sub(lambda m:TERMS[m[0]],normalize(value))
    result = re.sub(r"associated with confidence (Low|Medium|High) ל([^.]+?) in the area ", r"associated with \2 with \1 confidence in the area ", result)
    return result
def build(strict=True):
    OUTPUT.mkdir(exist_ok=True)
    with (SOURCE / "serbia_kosovo_events_projection_v2_1.csv").open(encoding="utf-8-sig",newline="") as stream:
        reader=csv.DictReader(stream);fields=reader.fieldnames; rows=list(reader)
    projected=[translate(row) for row in rows]
    for row in projected:
        if row.get("call_transcript_en"): row["call_transcript"]=row["call_transcript_en"]
    objects={"locations":translate(json.loads((SOURCE / "serbia_kosovo_locations_v2_1.json").read_text(encoding="utf-8"))),"entities":translate(json.loads((SOURCE / "serbia_kosovo_entities_v2_1.json").read_text(encoding="utf-8")))}
    residual=sorted(set(re.findall(r"[\u0590-\u05ff][\u0590-\u05ff \"'–-]*",json.dumps([projected,objects],ensure_ascii=False))))
    if residual and strict: raise ValueError("Untranslated Hebrew: " + repr(residual))
    with (OUTPUT / "events.csv").open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=fields,lineterminator="\n");writer.writeheader();writer.writerows(projected)
    for name,data in objects.items(): (OUTPUT / (name+".json")).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    return residual
if __name__=="__main__":
    build(); print("English projection complete")
