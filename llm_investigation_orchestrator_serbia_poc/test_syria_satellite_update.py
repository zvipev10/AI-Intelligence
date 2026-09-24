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
   if r['event_id'] in old and r['source_type'] not in ['Satellite','ADINT']:self.assertEqual(old[r['event_id']],{k:r[k] for k in old[r['event_id']]})
  for r in sats:
   self.assertNotIn('ADINT',r['event_summary']);self.assertNotIn('repeatedly',r['event_summary'])
   self.assertTrue(r['location_id'].startswith('LOC-SYR-SAT-'))
   series=json.loads(r['image_series']);self.assertEqual(len(series),1)
   self.assertEqual(series[0]['location_id'],r['location_id']);self.assertNotIn('paired_record_id',series[0]);self.assertNotIn('pair_id',series[0])
   self.assertTrue((ROOT/series[0]['image_url'].lstrip('/')).is_file())
   expected={'LOC-SYR-SAT-001':(35.065212338738036,36.28815755309795),'LOC-SYR-SAT-002':(35.06503531383431,36.289563371508734)}
   self.assertEqual((loc[r['location_id']]['latitude'],loc[r['location_id']]['longitude']),expected[r['location_id']])
   self.assertEqual(r['synthetic_media'],'true');self.assertIn('capture date not supplied',r['timestamp_basis'])
if __name__=='__main__':unittest.main()
