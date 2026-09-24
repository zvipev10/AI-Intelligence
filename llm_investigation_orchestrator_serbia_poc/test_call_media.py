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
   if key!='REC-SYR-CALL-002':self.assertEqual({k:({'DEMO-SIM-SYR-001':'8996301746283951072','DEMO-SIM-SYR-002':'8996301839572614087'}.get(v,v) if k=='sim' else {'990000000000001':'353294708462710','990000000000002':'358240116593823'}.get(v,v)) for k,v in row.items()},{k:current[key][k] for k in row})
  c=current['REC-SYR-CALL-001']
  self.assertEqual(c['side_a_sim'],'8996301746283951072')
  self.assertEqual(c['side_b_sim'],'8996301839572614087')
  self.assertEqual(c['call_transcript_speaker_imei'],'353294702931926')
  self.assertEqual(c['side_a_imei'],'353294708462710')
  self.assertEqual(c['call_transcript_original'],(ROOT/c['call_transcript_url'].lstrip('/')).read_text(encoding='utf-8'))
  self.assertEqual(c['call_transcript_en'],(ROOT/c['call_translation_url'].lstrip('/')).read_text(encoding='utf-8'))
  self.assertTrue((ROOT/c['audio_url'].lstrip('/')).is_file())
  self.assertTrue((ROOT/c['audio_url'].lstrip('/')).with_suffix('.wav').is_file())
if __name__=='__main__':unittest.main()
