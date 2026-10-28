import re
import unittest
from pathlib import Path

import server

ROOT = Path(__file__).resolve().parent.parent


class DockerfileTests(unittest.TestCase):
    def test_every_static_page_is_copied_into_the_image(self):
        # The runtime stage copies files by name; a page the server serves but the image lacks answers not_found
        # (the launcher, home.html, was missing on LAMBDA on 27 Oct 2026).
        text = re.sub(r"\\\s*\n", " ", (ROOT / "Dockerfile").read_text(encoding="utf-8"))  # join continued lines
        runtime = text.split("COPY --from=test", 1)[1]
        copied = {name for line in runtime.splitlines() if line.startswith("COPY ")
                  for name in line.split()[1:-1] if not name.startswith("--")}
        missing = sorted({name for name in server.STATIC_FILES.values() if name not in copied})
        self.assertEqual([], missing)


if __name__ == "__main__":
    unittest.main()
