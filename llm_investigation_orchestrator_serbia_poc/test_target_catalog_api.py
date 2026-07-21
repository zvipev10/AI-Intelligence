import unittest
from unittest.mock import patch

import server


class TargetCatalogApiTests(unittest.TestCase):
    def test_uav_video_catalog_layer_uses_short_display_label(self):
        self.assertEqual(
            server.SOURCE_TYPE_DISPLAY_LABELS["חיל האוויר הסרבי - ניצול וידאו מכטב״ם"],
            'וידאו מכטב"מ',
        )

    def test_catalog_advertises_persisted_attack_targets(self):
        with patch.object(server, "load_persisted_attack_targets", return_value=[{"target_id": "TGT-1"}]):
            layers = {layer["id"]: layer for layer in server.list_ui_layers()}
        target_layer = layers[server.ATTACK_TARGET_CATALOG_LAYER_ID]
        self.assertEqual(target_layer["kind"], "attack_targets")
        self.assertEqual(target_layer["family"], "targets")
        self.assertEqual(target_layer["count"], 1)
        self.assertTrue(target_layer["capabilities"]["map"])

    def test_catalog_rows_use_the_constrained_reader(self):
        target = {"target_id": "TGT-1", "location_id": "LOC-1"}
        with patch.object(server, "load_persisted_attack_targets", return_value=[target]):
            layer, rows = server.get_ui_layer_rows(server.ATTACK_TARGET_CATALOG_LAYER_ID)
        self.assertEqual(layer["kind"], "attack_targets")
        self.assertEqual(rows, [target])


if __name__ == "__main__":
    unittest.main()
