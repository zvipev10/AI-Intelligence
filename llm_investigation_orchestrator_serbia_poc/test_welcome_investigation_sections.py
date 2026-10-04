import unittest
from pathlib import Path


class WelcomeInvestigationSectionsTests(unittest.TestCase):
    def test_welcome_page_has_invited_and_system_proposed_sections(self):
        root = Path(__file__).resolve().parent
        index = (root / "index.html").read_text(encoding="utf-8")
        app = (root / "app.js").read_text(encoding="utf-8")
        self.assertIn("Investigations that I was invited to join", index)
        self.assertIn("Relevant investigations proposed by the system", index)
        self.assertIn('id="invitedInvestigationsList"', index)
        self.assertIn("const SYRIA_INVITED_INVESTIGATIONS", app)
        self.assertIn("const SYRIA_PROPOSED_INVESTIGATIONS", app)
        self.assertIn("invitedInvestigationsList.innerHTML = INVITED_INVESTIGATIONS.map", app)


if __name__ == "__main__":
    unittest.main()
