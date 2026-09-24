import csv,json,unittest
from pathlib import Path
from demo_runtime import load_profile
ROOT=Path(__file__).resolve().parent
class IdentifierIntegrity(unittest.TestCase):
 def test_all_records_preserve_links_and_only_identifiers_change(self):
  profile=load_profile(ROOT,'syria',verify=True)
  directory=ROOT/Path(profile['files']['events']).parent
  mapping=json.loads((directory/'identifier-mapping.json').read_text())['mapping']
  self.assertEqual(len(set(mapping.values())),len(mapping))
  for locale in ['events.csv','events.en.csv']:
   def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
   before=read(ROOT/'data/syria_call_media_v4'/locale);after=read(directory/locale)
   self.assertEqual(len(before),443);self.assertEqual(len(after),443)
   for old,new in zip(before,after):
    expected={}
    for k,v in old.items():
     for a,b in mapping.items():v=v.replace(a,b)
     expected[k]=v
    self.assertEqual(new,expected)
   calls=[r for r in after if r.get('call_id')]
   for call in calls:
    for side in ['a','b']:
     linked=[r for r in after if r.get('imei')==call[f'side_{side}_imei']]
     self.assertTrue(linked)
     self.assertEqual({r['sim'] for r in linked},{call[f'side_{side}_sim']})
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
   self.assertEqual(sum(r.get('imei')==source_imei for r in after),2)
if __name__=='__main__':unittest.main()
