import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class CanonicalSourceContractTests(unittest.TestCase):
    def test_canonical_files_match_the_current_source_manifest(self):
        manifest = ROOT / "deployment" / "SHA256SUMS-v164.txt"
        for line in manifest.read_text(encoding="utf-8").splitlines():
            expected, name = line.split(None, 1)
            actual = hashlib.sha256((ROOT / name.strip()).read_bytes()).hexdigest()
            self.assertEqual(expected, actual, name)

    def test_no_duplicate_editable_production_tree_remains(self):
        self.assertFalse((ROOT / "deployment" / "vm-production-v162").exists())

    def test_v164_bilingual_welcome_ui_contract_is_canonical(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn('app.js?v=164', index)
        self.assertIn('styles.css?v=137', index)
        self.assertIn('id="languageToggle"', index)
        self.assertIn('id="welcomePage"', index)
        self.assertIn('id="welcomePromptForm"', index)
        self.assertIn('id="myInvestigationsList"', index)
        self.assertIn('id="playbackNextButton"', index)
        self.assertIn('id="playbackResetButton"', index)
        self.assertIn('id="workstreamRail"', index)
        self.assertIn('data-workstream-results=', app)
        self.assertIn('activeLocaleText("הצג תוצאות", "Show results")', app)
        self.assertIn('fetch(buildLocaleApiUrl("/api/investigations")', app)
        self.assertIn('async function showWorkstreamResultVisibility', app)
        self.assertIn('async function resetInvestigationPlayback', app)
        self.assertIn('function renderWelcomePage()', app)
        self.assertIn('function setPageView(view, options = {})', app)


if __name__ == "__main__":
    unittest.main()
