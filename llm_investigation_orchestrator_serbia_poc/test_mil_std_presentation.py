import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
APP = (ROOT / "app.js").read_text(encoding="utf-8")
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "styles.css").read_text(encoding="utf-8")
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")


class MilStdPresentationContractTests(unittest.TestCase):
    def test_versioned_legend_is_present(self):
        self.assertIn('id="milStdLegend"', HTML)
        self.assertIn("MIL-STD-2525E Change 1", HTML)
        self.assertIn('data-i18n-text-en="MIL-STD-2525 legend"', HTML)

    def test_registry_contains_twelve_organizations(self):
        registry = APP.split("const MIL_STD_ORGANIZATIONS", 1)[1].split("});", 1)[0]
        entity_ids = set(re.findall(r'"(ENT-[A-Z0-9-]+)"\s*:', registry))
        self.assertEqual(12, len(entity_ids))
        self.assertEqual(7, len([item for item in entity_ids if item.startswith("ENT-SAF-")]))

    def test_four_uav_classes_have_bilingual_mappings(self):
        registry = APP.split("const MIL_STD_UAV_OBJECTS", 1)[1].split("});", 1)[0]
        for code in ("armored-vehicle", "logistics-truck", "vehicle-convoy", "helicopter"):
            self.assertIn(f'code: "{code}"', registry)
        self.assertIn('event.collection_family !== "airborne_isr_video_exploitation"', APP)
        self.assertIn('affiliation: "unknown"', APP)

    def test_claim_state_and_confidence_do_not_change_affiliation(self):
        self.assertIn("function milStdConfidence", APP)
        self.assertIn("status-reported", CSS)
        self.assertIn("confidence-low", CSS)
        self.assertNotIn("status-reported .milstd-frame { border-style: dashed", CSS)
        self.assertIn("reported", APP)
        self.assertIn("assessed", APP)

    def test_entity_layer_exposes_location_evidence(self):
        self.assertIn('"assessment_status"', SERVER)
        self.assertIn('"presence_claim"', SERVER)
        self.assertIn("event_supports_presence", SERVER)
        self.assertIn('"latest_timestamp_utc"', SERVER)
        self.assertIn('"evidence_record_ids"', SERVER)
        self.assertIn("organizationEvidenceHtml", APP)
        self.assertIn("Evidence by location presence", APP)

    def test_symbols_open_only_supported_single_objects(self):
        self.assertIn('element.dataset.viewerKind = descriptor.kind', APP)
        self.assertIn('element.dataset.viewerId = descriptor.id', APP)
        self.assertIn('data-viewer-kind="${descriptor.kind}"', APP)
        self.assertIn("viewerRefs.length === 1 && item.viewerEligible", APP)


if __name__ == "__main__":
    unittest.main()
