import unittest
from pathlib import Path


class WelcomeInvestigationSectionsTests(unittest.TestCase):
    def test_welcome_page_has_invited_and_system_proposed_sections(self):
        root = Path(__file__).resolve().parent
        index = (root / "index.html").read_text(encoding="utf-8")
        app = (root / "app.js").read_text(encoding="utf-8")
        self.assertIn("Invitations to join", index)
        self.assertIn("Similar investigations to join", index)
        self.assertIn('id="invitedInvestigationsList"', index)
        self.assertIn('id="invitedInvestigationsCount"', index)
        self.assertIn('id="similarInvestigationsCount"', index)
        self.assertIn("const SYRIA_INVITED_INVESTIGATIONS", app)
        self.assertIn("const SYRIA_PROPOSED_INVESTIGATIONS", app)
        self.assertIn("Suspicious military convoy", app)
        self.assertIn("invitedInvestigationsList.innerHTML = invitedInvestigations.map", app)
        self.assertIn("if (!welcomeSectionsFromI360()) return INVITED_INVESTIGATIONS;", app)
        self.assertIn("function joinInvitedInvestigation(invitation)", app)
        self.assertIn("const ownedInvestigations = investigations.filter", app)
        self.assertIn("invitedInvestigationsCount.textContent = invitedInvestigations.length", app)
        self.assertIn("similarInvestigationsCount.textContent = similarInvestigations.length", app)
        self.assertIn("if (!welcomeSectionsFromI360()) return SIMILAR_INVESTIGATIONS;", app)
        self.assertIn('data-invited-investigation="${investigation.invited ? "true" : "false"}"', app)


if __name__ == "__main__":
    unittest.main()
