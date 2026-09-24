import csv,json,math,unittest
from pathlib import Path
from demo_runtime import load_profile
ROOT=Path(__file__).resolve().parent
class SatelliteUpdate(unittest.TestCase):
 def test_single_image_new_locations_and_preserved_other_sources(self):
  p=load_profile(ROOT,'syria',verify=True)
  rows=list(csv.DictReader((ROOT/p['files']['events']).read_text().splitlines()))
  old={r['event_id']:r for r in csv.DictReader((ROOT/'data/syria_ipdr_v1/events.csv').read_text().splitlines())}
  loc=json.loads((ROOT/p['files']['locations']).read_text());self.assertEqual(len(loc),88)
  sats=[r for r in rows if r['source_type']=='Satellite'];self.assertEqual(len(sats),2)
  for r in rows:
   if r['source_type']!='Satellite':self.assertEqual(old[r['event_id']],{k:r[k] for k in old[r['event_id']]})
  for r in sats:
   self.assertNotIn('ADINT',r['event_summary']);self.assertNotIn('repeatedly',r['event_summary'])
   self.assertTrue(r['location_id'].startswith('LOC-SYR-SAT-'))
   series=json.loads(r['image_series']);self.assertEqual(len(series),1)
   self.assertEqual(series[0]['location_id'],r['location_id']);self.assertNotIn('paired_record_id',series[0]);self.assertNotIn('pair_id',series[0])
   self.assertTrue((ROOT/series[0]['image_url'].lstrip('/')).is_file())
   a=loc[old[r['event_id']]['location_id']];b=loc[r['location_id']]
   d=6371000*math.cos(math.radians(a['latitude']))*math.radians(b['longitude']-a['longitude'])
   self.assertAlmostEqual(d,30,places=2);self.assertEqual(a['latitude'],b['latitude'])
   self.assertEqual(r['synthetic_media'],'true');self.assertIn('capture date not supplied',r['timestamp_basis'])
if __name__=='__main__':unittest.main()
