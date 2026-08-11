import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class RawRecordMapJumpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8-sig")
        cls.styles = (ROOT / "styles.css").read_text(encoding="utf-8-sig")
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_raw_event_rows_expose_map_action(self):
        self.assertIn('data-result-map-item="${escapeHtml(itemId)}"', self.app)
        self.assertIn('data-result-map-kind="${escapeHtml(kind)}"', self.app)
        self.assertIn('data-result-map-layer="${escapeHtml(String(layerId))}"', self.app)
        self.assertIn('class="result-map-action ${selected ? "active" : ""}"', self.app)

    def test_jump_centers_map_and_opens_exact_event_popup(self):
        presenter = self.app.split("function toggleMapItem", 1)[1].split("function renderTimeline", 1)[0]
        self.assertIn('activateView("map")', presenter)
        self.assertIn("state.map.easeTo", presenter)
        self.assertIn("mapItemPopupHtml(selectedEvent, kind)", presenter)
        self.assertIn("state.focusedEventPopup", presenter)
        self.assertIn(".setLngLat([coordinates.lon, coordinates.lat])", presenter)

    def test_action_column_is_not_sortable_or_filterable(self):
        self.assertIn('cell.dataset.resultActionColumn === "true"', self.app)

    def test_missing_coordinates_disable_action(self):
        self.assertIn('const available = Boolean(eventMapCoordinates(item))', self.app)
        self.assertIn('${available ? "" : "disabled"}', self.app)

    def test_targets_locations_and_selection_feedback_use_shared_action(self):
        self.assertIn('mapActionButton(activeLayer.id, "target"', self.app)
        self.assertIn('mapActionButton(activeLayer.id, "location"', self.app)
        self.assertIn('aria-pressed="${selected ? "true" : "false"}"', self.app)
        self.assertIn("map-selected-row", self.styles)

    def test_assets_and_styles_are_present(self):
        self.assertIn(".result-map-action", self.styles)
        self.assertIn(".event-map-popup", self.styles)
        self.assertIn('styles.css?v=135', self.index)
        self.assertIn('app.js?v=154', self.index)


if __name__ == "__main__":
    unittest.main()
