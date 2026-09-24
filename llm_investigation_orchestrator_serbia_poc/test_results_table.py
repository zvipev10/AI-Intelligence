import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class ResultsTableTests(unittest.TestCase):
    def test_syria_geometry_free_presentation_end_to_end(self):
        code = '''
from unittest.mock import patch
import server as ui
import mcp_server.server as mcp
from agent_result_pipeline import presentation_view_from_audit
catalog = ui.list_ui_layers('en')
ipdr = next(layer for layer in catalog if layer['id'] == 'events:IPDR')
assert ipdr['count'] == 300 and ipdr['capabilities']['map'] is False
assert next(layer for layer in catalog if layer['id'] == 'events:ADINT')['capabilities']['map']
layer, rows = ui.get_ui_layer_rows('events:IPDR', 'en')
assert len(rows) == 300 and all(not row.get('location_id') for row in rows)
for view in ('table', 'evidence'):
 result = mcp.present_requested_results({'layers':[{'kind':'events','ids':[rows[0]['event_id']],'label':'IP match','view':view}], 'evidence_layers':[{'kind':'events','ids':[rows[0]['event_id']],'label':'Supporting IPDR','view':view}]})
 selected = result['requested_result_layers'][0]
 assert selected['recommended_view'] == 'table'
 assert selected['capabilities']['map'] is False
 assert selected['rows'][0]['imei'] == rows[0]['imei']
 assert result['evidence_reference_layers'][0]['recommended_view'] == 'table'
 assert presentation_view_from_audit([{'tool':'present_requested_results','result':result}]) == 'table'
with patch.object(mcp, 'load_ui_catalog', return_value=catalog):
 assert mcp.open_catalog_layers({'catalog_layer_ids':['events:Cellular Calls'],'locale':'en'})['catalog_layer_actions'][0]['view']=='timeline'
 assert mcp.open_catalog_layers({'catalog_layer_ids':['events:Cellular Calls'],'locale':'en','view':'map'})['catalog_layer_actions'][0]['view']=='map'
 for view in ('map','table','evidence'):
  result = mcp.open_catalog_layers({'catalog_layer_ids':['events:IPDR'],'view':view,'locale':'en'})
  assert result['catalog_layer_actions'][0]['view'] == 'table'
for name in ('present_requested_results','open_catalog_layers'):
 tool = next(t for t in mcp.TOOLS if t['name'] == name)
 assert 'table' in str(tool['inputSchema'])
'''
        with tempfile.TemporaryDirectory() as state:
            result = subprocess.run([sys.executable, '-c', code], cwd=ROOT,
                env={**os.environ, 'INTELLIGENCE_POC_SCENARIO':'syria','INTELLIGENCE_POC_STATE_ROOT':state},
                capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr.decode())

if __name__ == '__main__':
    unittest.main()
