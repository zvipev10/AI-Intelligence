import csv, hashlib, unittest
from pathlib import Path
from demo_runtime import load_profile
ROOT=Path(__file__).resolve().parent
class CallMedia(unittest.TestCase):
 def test_media_and_preserved_records(self):
  p=load_profile(ROOT,'syria',verify=True)
  def rows(path):
   with path.open(encoding='utf-8',newline='') as f:return {r['event_id']:r for r in csv.DictReader(f)}
  current=rows(ROOT/p['files']['events']); previous=rows(ROOT/'data/syria_call_media_v1/events.csv')
  self.assertEqual(set(current),set(previous)-{'REC-SYR-CALL-002'})
  for key,row in previous.items():
   if key!='REC-SYR-CALL-002':self.assertEqual(row,{k:current[key][k] for k in row})
  c=current['REC-SYR-CALL-001']
  self.assertEqual(c['side_a_sim'],'DEMO-SIM-SYR-001')
  self.assertEqual(c['side_b_sim'],'DEMO-SIM-SYR-002')
  self.assertEqual(c['call_transcript_speaker_imei'],'353294702931926')
  self.assertEqual(c['side_a_imei'],previous[c['event_id']]['side_a_imei'])
  self.assertEqual(c['call_transcript_original'],(ROOT/c['call_transcript_url'].lstrip('/')).read_text(encoding='utf-8'))
  self.assertEqual(c['call_transcript_en'],(ROOT/c['call_translation_url'].lstrip('/')).read_text(encoding='utf-8'))
  self.assertTrue((ROOT/c['audio_url'].lstrip('/')).is_file())
  self.assertTrue((ROOT/c['audio_url'].lstrip('/')).with_suffix('.wav').is_file())
if __name__=='__main__':unittest.main()
