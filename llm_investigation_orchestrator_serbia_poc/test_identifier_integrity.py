import csv,json,unittest
from pathlib import Path
from demo_runtime import load_profile
ROOT=Path(__file__).resolve().parent
class IdentifierIntegrity(unittest.TestCase):
 def test_replacement_preserves_non_target_records_and_identifier_validity(self):
  profile=load_profile(ROOT,'syria',verify=True)
  directory=ROOT/Path(profile['files']['events']).parent
  mapping=json.loads((directory/'identifier-mapping.json').read_text())['mapping']
  self.assertEqual(len(set(mapping.values())),len(mapping))
  for locale in ['events.csv','events.en.csv']:
   def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
   before=read(ROOT/'data/syria_cellular_records_v1'/locale);after=read(directory/locale)
   self.assertEqual(len(before),726);self.assertEqual(len(after),726)
   after_by_id={row['event_id']:row for row in after}
   for old in before:
    if old['source_type'] not in {'ADINT','IPDR'}:
     self.assertEqual(old,after_by_id[old['event_id']])
   calls=[r for r in after if r.get('call_id')]
   for call in calls:
    for side in ['a','b']:
     if not call[f'side_{side}_imei']:continue
     linked=[r for r in after if r.get('imei')==call[f'side_{side}_imei']]
     self.assertTrue(linked)
   for row in after:
    for key in ['imei','side_a_imei','side_b_imei','call_transcript_speaker_imei','sim','side_a_sim','side_b_sim']:
     value=row.get(key)
     if not value:continue
     self.assertTrue(value.isdigit())
     self.assertEqual(len(value),19 if 'sim' in key else 15)
     digits=[int(x) for x in value[::-1]]
     total=sum((d*2//10+d*2%10) if i%2 else d for i,d in enumerate(digits))
     self.assertEqual(total%10,0,value)
   source_imei=calls[0]['call_transcript_speaker_imei']
   self.assertEqual(source_imei,'353294702931926')
   self.assertEqual(sum(r.get('imei')==source_imei and r.get('source_type')=='IPDR' for r in after),4)
if __name__=='__main__':unittest.main()
