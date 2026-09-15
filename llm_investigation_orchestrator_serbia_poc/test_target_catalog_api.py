import unittest
from unittest.mock import patch

import server


class TargetCatalogApiTests(unittest.TestCase):
    def test_catalog_advertises_precomputed_evidence(self):
        with patch.object(server, "evidence_catalog_count", return_value=1):
            layers = {layer["id"]: layer for layer in server.list_ui_layers()}
        evidence_layer = layers[server.EVIDENCE_CATALOG_LAYER_ID]
        self.assertEqual(evidence_layer["kind"], "evidence")
        self.assertEqual(evidence_layer["family"], "evidence")
        self.assertEqual(evidence_layer["count"], 1)
        self.assertTrue(evidence_layer["capabilities"]["timeline"])

    def test_catalog_evidence_rows_use_precomputed_artifact(self):
        evidence = {"evidence_id": "EVD-REC-1", "source_record_ids": ["REC-1"]}
        with patch.object(server, "load_evidence_catalog", return_value=[evidence]):
            layer, rows = server.get_ui_layer_rows(server.EVIDENCE_CATALOG_LAYER_ID)
        self.assertEqual(layer["kind"], "evidence")
        self.assertEqual(rows, [evidence])

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
