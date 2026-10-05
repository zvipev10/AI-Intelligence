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

    def test_timeline_renders_only_the_focused_layer(self):
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        start = app.index("function renderTimeline()")
        end = app.index("function resultTableControl", start)
        render_timeline = app[start:end]
        self.assertIn("const timelineLayers = focusedTimelineLayers();", render_timeline)
        self.assertNotIn('visibleLayers("timeline")', render_timeline)
        self.assertIn("function focusedTimelineLayers()", app)
        self.assertIn("return layer?.visible && layer.capabilities.timeline ? [layer] : [];", app)
        tab_start = app.index('const rawLayerTab = event.target.closest("[data-layer-id]");')
        tab_end = app.index('if (event.target.closest("#rawEventsMinimize"))', tab_start)
        self.assertIn("renderTimeline();", app[tab_start:tab_end])


if __name__ == "__main__":
    unittest.main()
