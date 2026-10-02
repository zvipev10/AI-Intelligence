import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class ObjectViewerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8")
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.styles = (ROOT / "styles.css").read_text(encoding="utf-8")

    def test_accessible_shared_dialog_exists(self):
        self.assertIn('id="objectViewer"', self.index)
        self.assertIn('role="dialog"', self.index)
        self.assertIn('aria-modal="true"', self.index)
        self.assertIn('aria-labelledby="objectViewerTitle"', self.index)

    def test_memory_action_is_in_the_viewer_header_next_to_the_record_title(self):
        header = self.index.split('<header class="object-viewer-header">', 1)[1].split("</header>", 1)[0]
        self.assertIn('id="objectMemoryAction"', header)
        self.assertIn('class="object-viewer-title-actions"', header)
        self.assertNotIn('class="object-memory-action" data-memory-object-kind=', self.app)
        self.assertIn('objectMemoryAction.dataset.memoryObjectKind = kind;', self.app)
        self.assertIn('objectMemoryAction.dataset.memoryObjectId = id;', self.app)
        self.assertIn('.object-memory-header-action {', self.styles)

    def test_records_organizations_and_evidence_are_supported(self):
        self.assertIn("if (!['record', 'organization', 'person', 'evidence', 'assessment'].includes(kind)) return false;", self.app)
        self.assertIn('data-viewer-kind="evidence"', self.app)
        self.assertNotIn('data-viewer-kind="target"', self.app)

    def test_grid_and_assistant_open_controls_exist(self):
        self.assertIn('data-viewer-kind="record"', self.app)
        self.assertIn('data-viewer-kind="organization"', self.app)
        self.assertIn("appendAssistantObjectLinks(article)", self.app)

    def test_map_opens_only_a_single_item(self):
        self.assertIn("viewerRefs.length === 1 && item.viewerEligible", self.app)
        self.assertIn("else existing.viewerEligible = false", self.app)

    def test_media_is_not_autoplayed_and_has_fallback(self):
        self.assertIn('<video controls preload="metadata"', self.app)
        self.assertIn('<audio controls preload="metadata"', self.app)
        self.assertNotIn('<video autoplay', self.app)
        self.assertIn('>ISR</span>', self.app)
        self.assertIn("function safeMediaUrl", self.app)

    def test_uav_media_is_presented_as_shared_source_material(self):
        self.assertIn('UAV video stream', self.app)
        self.assertIn('Collection-mission visualization.', self.app)
        self.assertIn('item.mission_id', self.app)
        self.assertIn('item.video_segment_id', self.app)
        self.assertIn('function viewerFieldLabel', self.app)

    def test_simulated_uav_stream_starts_and_stops_with_viewer(self):
        self.assertIn('function startSimulatedUavStream(item)', self.app)
        self.assertIn('requestAnimationFrame(draw)', self.app)
        self.assertIn('stopSimulatedUavStream();', self.app)
        self.assertIn('if (kind === "record" && isUavVideoRecord(item)) startSimulatedUavStream(item);', self.app)

    def test_record_header_does_not_repeat_the_event_summary(self):
        self.assertNotIn('const title = kind === "record" ? (item.event_summary || id)', self.app)
        self.assertIn('activeLocaleText("תצפית וידאו מכטב״ם", "UAV video observation")', self.app)

    def test_dialog_is_a_locale_aware_edge_drawer(self):
        self.assertIn(".object-viewer-backdrop", self.styles)
        self.assertIn(".object-viewer-fields", self.styles)
        self.assertIn("margin-inline-start: auto", self.styles)
        self.assertIn('[dir="rtl"] .object-viewer', self.styles)
        self.assertIn("height: 100dvh", self.styles)

    def test_cellular_calls_have_a_dedicated_non_duplicating_viewer(self):
        self.assertIn("function isCellularCallRecord(item)", self.app)
        self.assertIn("function cellularCallPartyHtml(item, side)", self.app)
        self.assertIn("function cellularCallHtml(item)", self.app)
        self.assertIn('activeLocaleText("שיחה סלולרית", "Cellular call")', self.app)
        self.assertIn('Call details', self.app)
        self.assertIn('Conversation', self.app)
        self.assertIn('"side_a_imei"', self.app)
        self.assertIn('"side_b_imei"', self.app)
        self.assertIn(".cellular-call-parties", self.styles)
        self.assertIn("grid-template-columns: minmax(0,1fr) minmax(0,1fr)", self.styles)

    def test_entity_viewer_includes_connected_record_location_map(self):
        self.assertIn("function entityRecordLocationPoints(item)", self.app)
        self.assertIn("function entityLocationMapHtml(item)", self.app)
        self.assertIn("function initializeEntityLocationMap(item)", self.app)
        self.assertIn('id="entityViewerMap"', self.app)
        self.assertIn('entityViewerMap?.remove()', self.app)
        self.assertIn('initializeEntityLocationMap(item)', self.app)
        self.assertIn('.entity-record-map-panel {', self.styles)
        self.assertIn('class="entity-record-map-panel call-map-panel"', self.app)
        self.assertIn('id="entityFitMap"', self.app)

    def test_people_use_a_dedicated_table_and_workspace_viewer(self):
        self.assertIn('function buildEntityMetadataLayers(items)', self.app)
        self.assertIn('kind: "person_entities"', self.app)
        self.assertIn('if (activeLayer.kind === "person_entities")', self.app)
        self.assertIn('function personWorkspaceHtml(item)', self.app)
        self.assertIn('viewer.classList.toggle("is-person-viewer", personViewer)', self.app)
        self.assertIn('.person-workspace {', self.styles)
        self.assertIn('.person-table-identity {', self.styles)

    def test_person_workspace_exposes_actionable_telecom_identifiers(self):
        self.assertIn('function personTelecomDetailsHtml(item)', self.app)
        self.assertIn('const telecom = item.telecom', self.app)
        self.assertIn('collectionImeiButton(value)', self.app)
        self.assertIn('Telecom identifiers', self.app)
        self.assertLess(
            self.app.index('<div class="call-main person-workspace-main">'),
            self.app.index('${personTelecomDetailsHtml(item)}')
        )
        self.assertIn('.person-telecom-identifier-grid {', self.styles)
        self.assertIn('Reference records', self.app)
        self.assertIn('Calls', self.app)

    def test_satellite_and_cctv_viewers_use_a_half_screen_drawer(self):
        self.assertIn('function isVisualCollectionRecord(item)', self.app)
        self.assertIn('viewer.classList.toggle("is-visual-collection-viewer", visualCollectionViewer);', self.app)
        self.assertIn('.is-visual-collection-viewer .object-viewer { width: min(50vw, calc(100vw - 28px)); }', self.styles)

    def test_satellite_and_cctv_media_can_expand_without_maximizing_the_viewer(self):
        self.assertIn('data-visual-media-fullscreen', self.app)
        self.assertIn('function toggleVisualCollectionMediaFullscreen(trigger)', self.app)
        self.assertIn('id="visualMediaOverlay"', self.index)
        self.assertIn('id="visualMediaOverlayClose"', self.index)
        self.assertIn('function closeVisualCollectionMediaFullscreen', self.app)
        self.assertIn('content.replaceChildren(expandedMedia)', self.app)
        self.assertIn('.visual-media-overlay {', self.styles)
        self.assertNotIn('media.requestFullscreen()', self.app)

    def test_entity_viewers_dock_beside_the_table(self):
        self.assertIn('function setViewerDocked(target = null)', self.app)
        self.assertIn('document.getElementById("rawEventsOverlay")', self.app)
        self.assertIn('["person", "organization"].includes(kind)', self.app)
        self.assertIn('.raw-events-overlay.has-record-viewer', self.styles)
        self.assertIn('> .object-viewer-backdrop.is-docked', self.styles)

    def test_every_item_viewer_can_be_maximized_over_the_active_presentation(self):
        self.assertIn('id="objectViewerMaximize"', self.index)
        self.assertIn('function setViewerMaximized(maximized)', self.app)
        self.assertIn('viewer.classList.add("is-maximized")', self.app)
        self.assertIn('document.body.appendChild(viewer)', self.app)
        self.assertIn('.object-viewer-backdrop.is-maximized .object-viewer', self.styles)

    def test_maximized_viewer_keeps_a_scrollable_body_for_specialized_viewers(self):
        fullscreen_body = self.styles.split('.object-viewer-backdrop.is-maximized .object-viewer-body {', 1)[1].split('}', 1)[0]
        self.assertIn('overflow-y: auto', fullscreen_body)
        self.assertIn('scrollbar-gutter: stable', fullscreen_body)


if __name__ == "__main__":
    unittest.main()
