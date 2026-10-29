import csv, json, re, unittest
from pathlib import Path
from build_kosovo_english import ROOT, SOURCE, OUTPUT, translate
from evidence_catalog import build_catalog
from mcp_server.evidence_semantics import normalize_evidence_event, ENGLISH_OBJECT_CLASSES

class EnglishDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (SOURCE/"serbia_kosovo_events_projection_v2_1.csv").open(encoding="utf-8-sig") as stream: cls.original=list(csv.DictReader(stream))
        with (OUTPUT/"events.csv").open(encoding="utf-8-sig") as stream: cls.english=list(csv.DictReader(stream))
    def test_complete_translation_and_identical_record_identity(self):
        self.assertEqual(len(self.english),14833)
        for old,new in zip(self.original,self.english):
            self.assertFalse(re.search(r"[\u0590-\u05ff]",json.dumps(new,ensure_ascii=False)),new["event_id"])
            for key in old:
                if not re.search(r"[\u0590-\u05ff]",old[key] or ""):
                    self.assertEqual(old[key],new[key],(old["event_id"],key))
            self.assertEqual(re.findall(r"\d+",old["event_summary"].replace("החטיבה השנייה", "2nd Brigade").replace("החטיבה השלישית", "3rd Brigade")), re.findall(r"\d+",new["event_summary"]),old["event_id"])
    def test_locations_entities_keep_identity_and_coordinates(self):
        for name,filename in [("locations","serbia_kosovo_locations_v2_1.json"),("entities","serbia_kosovo_entities_v2_1.json")]:
            old=json.loads((SOURCE/filename).read_text(encoding="utf-8"));new=json.loads((OUTPUT/(name+".json")).read_text(encoding="utf-8"))
            self.assertEqual(translate(old),new)
            self.assertFalse(re.search(r"[\u0590-\u05ff]",json.dumps(new,ensure_ascii=False)))
    def test_english_profile_does_not_retranslate_records(self):
        import subprocess, sys, tempfile, os
        with tempfile.TemporaryDirectory() as state:
            code = "import server; from unittest.mock import patch; " + "p=patch.object(server, 'translate_plain', side_effect=AssertionError('English package must not be retranslated')); p.start(); " + "assert len(server.load_ui_events('en')) == 14833; assert server.dataset_row_count('en') == 14833"
            result=subprocess.run([sys.executable,'-c',code],cwd=ROOT,env={**os.environ,'INTELLIGENCE_POC_SCENARIO':'kosovo','INTELLIGENCE_POC_STATE_ROOT':state},capture_output=True,text=True,timeout=30)
            self.assertEqual(result.returncode,0,result.stderr)
    def test_semantic_classification_parity(self):
        for old,new in zip(self.original,self.english):
            a,b=normalize_evidence_event(old),normalize_evidence_event(new)
            self.assertEqual(translate(a.get("object_class","")),b.get("object_class",""),old["event_id"])
            self.assertEqual(a["object_class_resolution"]["method"],b["object_class_resolution"]["method"])
    def test_evidence_catalog_preserves_memberships(self):
        a=build_catalog(self.original,dataset_version="v2.1");b=build_catalog(self.english,dataset_version="v2.1-en1",locale="en")
        self.assertEqual(a["counts"],b["counts"])
        self.assertEqual({r["evidence_id"] for r in a["rows"]},{r["evidence_id"] for r in b["rows"]})
        self.assertFalse(re.search(r"[\u0590-\u05ff]",json.dumps(b,ensure_ascii=False)))
if __name__=="__main__": unittest.main()
