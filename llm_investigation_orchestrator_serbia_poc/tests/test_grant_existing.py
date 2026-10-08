"""tools/provision_types.py --grant-existing: dry run sends nothing; --apply grants the named profile."""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest import mock

from devtools.fake_hlapi import FakeEstate, make_server
from tests.test_api import start
from tools import provision_types


class GrantExistingTests(unittest.TestCase):
    def setUp(self):
        self.estate = FakeEstate({"manager": "pw"})
        self.estate.provision([{"type": "INTELLIGENCE_INVESTIGATION"}])
        self.fake = start(make_server("127.0.0.1", 0, self.estate))
        self.env = mock.patch.dict(os.environ, {"HL_API_URL": f"http://127.0.0.1:{self.fake.server_address[1]}",
                                                "I360_PASS": "pw"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.fake.shutdown()
        self.fake.server_close()

    def run_tool(self, *extra):
        argv = ["provision_types.py", "--username", "manager", "--grant-profile", "Analysts",
                "--grant-existing", "INTELLIGENCE_INVESTIGATION", *extra]
        out = io.StringIO()
        with mock.patch.object(sys, "argv", argv), redirect_stdout(out):
            code = provision_types.main()
        return code, out.getvalue()

    def test_dry_run_sends_nothing(self):
        code, out = self.run_tool()
        self.assertEqual(0, code, out)
        self.assertIn('POST /api/v1/entity-types/INTELLIGENCE_INVESTIGATION/grants {"profile": "Analysts", "permissions": ["VIEW"]}', out)
        self.assertNotIn("grants", self.estate.types["INTELLIGENCE_INVESTIGATION"])

    def test_apply_grants_view_and_create(self):
        code, out = self.run_tool("--permission", "VIEW", "--permission", "CREATE", "--apply", "--yes")
        self.assertEqual(0, code, out)
        self.assertEqual([{"profile": "Analysts", "permissions": ["VIEW", "CREATE"]}],
                         self.estate.types["INTELLIGENCE_INVESTIGATION"]["grants"])

    def test_missing_type_is_skipped(self):
        del self.estate.types["INTELLIGENCE_INVESTIGATION"]
        code, out = self.run_tool("--apply", "--yes")
        self.assertEqual(1, code)
        self.assertIn("not on this estate", out)


if __name__ == "__main__":
    unittest.main()
