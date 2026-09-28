import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class TimelineLayerTabsTests(unittest.TestCase):
    def test_timeline_has_the_same_open_layer_tabs_as_the_table(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn('id="timelineLayersTabs"', index)
        self.assertIn('const timelineTabs = document.getElementById("timelineLayersTabs");', app)
        self.assertIn('timelineTabs.innerHTML = layerTabsMarkup;', app)
        self.assertIn('.timeline-layer-tabs', styles)


if __name__ == "__main__":
    unittest.main()
