import csv,json,unittest
from pathlib import Path
from demo_runtime import load_profile
ROOT=Path(__file__).resolve().parent
class MediaRelocation(unittest.TestCase):
 def test_only_media_locations_changed(self):
  profile=load_profile(ROOT,'syria',verify=True)
  current=list(csv.DictReader((ROOT/profile['files']['events']).read_text().splitlines()))
  previous={r['event_id']:r for r in csv.DictReader((ROOT/'data/syria_adint_v1/events.csv').read_text().splitlines())}
  mapping={'LOC-SYR-001':'LOC-SYR-ADINT-002','LOC-SYR-002':'LOC-SYR-ADINT-001'}
  self.assertEqual(len(current),324)
  for row in current:
   old=previous[row['event_id']]
   if row['source_type'] not in ['CCTV','Satellite']:
    self.assertEqual(row,old);continue
   self.assertEqual(row['location_id'],mapping[old['location_id']])
   for key in row:
    if key not in ['location_id','event_summary','image_series']:self.assertEqual(row[key],old[key])
   if row['image_series']:
    images=json.loads(row['image_series']);self.assertEqual(len(images),3)
    for image,before in zip(images,json.loads(old['image_series'])):
     self.assertEqual(image,{**before,'location_id':mapping[before['location_id']],'paired_location_id':mapping[before['paired_location_id']]})
  for filename in ['ADINT.json','locations.json','locations.en.json','entities.json','entities.en.json']:
   self.assertEqual((ROOT/'data/syria_adint_v1'/filename).read_bytes(),(ROOT/'data/syria_adint_v2'/filename).read_bytes())
if __name__=='__main__':unittest.main()
