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
  self.assertEqual(len(rows),444);self.assertEqual(len(byid),444)
  for row in old:self.assertEqual(row,{k:byid[row['event_id']][k] for k in row})
  geo=[r for r in rows if r['source_type']=='Cellular Geolocations'];self.assertEqual(len(geo),18)
  calls=[r for r in rows if r.get('call_id')];self.assertEqual(len(calls),2)
  for call in calls:
   for side in ['a','b']:
    matches=[g for g in geo if g['imei']==call[f'side_{side}_imei'] and g['location_id']==call[f'side_{side}_location_id'] and g['timestamp_utc'][:13]==call['timestamp_utc'][:13]]
    self.assertTrue(matches)
    self.assertNotEqual(call['side_a_location_id'],call['side_b_location_id'])
  self.assertTrue(all(r['synthetic_media']=='true' for r in geo+calls))
  self.assertNotIn('Cellular Geolocations',load_profile(ROOT,'kosovo')['sources']['en'])
 def test_route_order_and_preserved_history(self):
  p=load_profile(ROOT,'syria',verify=True)
  rows=list(csv.DictReader((ROOT/p['files']['events']).read_text().splitlines()))
  route=sorted([r for r in rows if r['event_id'].startswith('REC-SYR-CELL-ROUTE-')],key=lambda r:r['timestamp_utc'])
  self.assertEqual(len(route),12)
  self.assertEqual(route[0]['location_id'],'LOC-SYR-CELL-START-001')
  self.assertEqual(route[-1]['location_id'],'LOC-SYR-COAST-011')
  self.assertEqual(len({r['imei'] for r in route}),1)
  self.assertEqual(len({r['timestamp_utc'] for r in route}),12)
  loc=json.loads((ROOT/p['files']['locations']).read_text())
  self.assertAlmostEqual((loc['LOC-SYR-CELL-START-001']['latitude']-loc['LOC-SYR-SAT-001']['latitude'])*3.141592653589793/180*6371000,60,places=5)
  self.assertEqual(loc['LOC-SYR-CELL-START-001']['longitude'],loc['LOC-SYR-SAT-001']['longitude'])
  self.assertTrue(all(loc[a['location_id']]['longitude']>loc[b['location_id']]['longitude'] for a,b in zip(route,route[1:])))
  north=loc['LOC-SYR-CALL-NORTH-001']
  self.assertTrue(all(north['latitude']-loc[r['location_id']]['latitude']>1.4 for r in route))
  calls=[r for r in rows if r.get('call_id')]
  self.assertEqual({r['location_id'] for r in calls},{'LOC-SYR-COAST-005'})
  for c in calls:
   self.assertEqual(c['location_id'],c['side_a_location_id'])
   self.assertEqual(c['side_b_location_id'],'LOC-SYR-CALL-NORTH-001')
   self.assertLess(route[5]['timestamp_utc'],c['timestamp_utc']);self.assertLess(c['timestamp_utc'],route[6]['timestamp_utc'])
  old=list(csv.DictReader((ROOT/'data/syria_cellular_v1/events.csv').read_text().splitlines()))
  byid={r['event_id']:r for r in rows}
  for row in old:
   if not row.get('call_id'):self.assertEqual(row,{k:byid[row['event_id']][k] for k in row})
  for id,value in json.loads((ROOT/'data/syria_cellular_v1/locations.json').read_text()).items():self.assertEqual(loc[id],value)
 def test_catalog_public_fields_and_identifier_search(self):
  with tempfile.TemporaryDirectory() as state:
   code="""import server as ui
import mcp_server.server as s
layer,rows=ui.get_ui_layer_rows('events:Cellular Geolocations','en')
assert layer['count']==18 and len(rows)==18 and layer['capabilities']['map']
for key,value in [('sim','DEMO-SIM-SYR-001'),('imei','990000000000001')]:
 r=s.search_events({'source_types':['Cellular Geolocations'],'keywords':[value]})
 assert r['total']==14 and all(e[key]==value for e in r['events'])
r=s.search_events({'source_types':['Cellular Calls'],'keywords':['990000000000002']})
assert r['total']==2 and all(e['side_b_imei']=='990000000000002' for e in r['events'])
"""
   result=subprocess.run([sys.executable,'-c',code],cwd=ROOT,env={**os.environ,'INTELLIGENCE_POC_SCENARIO':'syria','INTELLIGENCE_POC_STATE_ROOT':state},capture_output=True,text=True,timeout=60)
   self.assertEqual(result.returncode,0,result.stderr)
