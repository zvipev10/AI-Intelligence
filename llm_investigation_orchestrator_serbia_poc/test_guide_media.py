"""Keep published guide media in both source and the deployment package."""
import ast
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class ResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.resources = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"src", "poster"} and value and value.startswith("./"):
                self.resources.add(value[2:])


class GuideMediaTests(unittest.TestCase):
    def test_all_local_guide_resources_exist_and_ship(self):
        parser = ResourceParser()
        parser.feed((ROOT / "system-capabilities-guide.html").read_text(encoding="utf-8"))
        tree = ast.parse((ROOT / "mcp_server/remote_deploy_ui.py").read_text(encoding="utf-8"))
        lists = {target.id: ast.literal_eval(node.value)
                 for node in tree.body if isinstance(node, ast.Assign)
                 for target in node.targets if isinstance(target, ast.Name) and target.id in {"FILES", "DIRS"}}
        self.assertTrue(parser.resources)
        for resource in parser.resources:
            with self.subTest(resource=resource):
                self.assertTrue((ROOT / resource).is_file(), "Missing guide resource")
                self.assertTrue(resource in lists["FILES"] or any(resource.startswith(d + "/") for d in lists["DIRS"]),
                                "Guide resource omitted from deployment")


if __name__ == "__main__":
    unittest.main()
