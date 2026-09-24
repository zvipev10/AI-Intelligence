import csv,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from demo_runtime import load_profile
ROOT=Path(__file__).resolve().parent
class CellularGeolocations(unittest.TestCase):
 def test_data_preservation_and_sample_links(self):
  profile=load_profile(ROOT,'syria',verify=True)
  rows=list(csv.DictReader((ROOT/profile['files']['events']).read_text().splitlines()))
  old=list(csv.DictReader((ROOT/'data/syria_adint_v3/events.csv').read_text().splitlines()))
  byid={r['event_id']:r for r in rows}
  self.assertEqual(len(rows),430);self.assertEqual(len(byid),430)
  for row in old:self.assertEqual(row,{k:byid[row['event_id']][k] for k in row})
  geo=[r for r in rows if r['source_type']=='Cellular Geolocations'];self.assertEqual(len(geo),4)
  calls=[r for r in rows if r.get('call_id')];self.assertEqual(len(calls),2)
  for call in calls:
   for side in ['a','b']:
    matches=[g for g in geo if g['imei']==call[f'side_{side}_imei'] and g['location_id']==call[f'side_{side}_location_id'] and g['timestamp_utc'][:13]==call['timestamp_utc'][:13]]
    self.assertEqual(len(matches),1)
  self.assertTrue(all(r['synthetic_media']=='true' for r in geo+calls))
  self.assertNotIn('Cellular Geolocations',load_profile(ROOT,'kosovo')['sources']['en'])
 def test_catalog_public_fields_and_identifier_search(self):
  with tempfile.TemporaryDirectory() as state:
   code="""import server as ui
import mcp_server.server as s
layer,rows=ui.get_ui_layer_rows('events:Cellular Geolocations','en')
assert layer['count']==4 and len(rows)==4 and layer['capabilities']['map']
for key,value in [('sim','DEMO-SIM-SYR-001'),('imei','990000000000001')]:
 r=s.search_events({'source_types':['Cellular Geolocations'],'keywords':[value]})
 assert r['total']==2 and all(e[key]==value for e in r['events'])
r=s.search_events({'source_types':['Cellular Calls'],'keywords':['990000000000002']})
assert r['total']==2 and all(e['side_b_imei']=='990000000000002' for e in r['events'])
"""
   result=subprocess.run([sys.executable,'-c',code],cwd=ROOT,env={**os.environ,'INTELLIGENCE_POC_SCENARIO':'syria','INTELLIGENCE_POC_STATE_ROOT':state},capture_output=True,text=True,timeout=60)
   self.assertEqual(result.returncode,0,result.stderr)
