import csv, hashlib, unittest
from pathlib import Path
from demo_runtime import load_profile
ROOT=Path(__file__).resolve().parent
class CallMedia(unittest.TestCase):
 def test_media_and_preserved_records(self):
  p=load_profile(ROOT,'syria',verify=True)
  def rows(path):
   with path.open(encoding='utf-8',newline='') as f:return {r['event_id']:r for r in csv.DictReader(f)}
  current=rows(ROOT/p['files']['events'])
  self.assertEqual({key for key in current if key.startswith('REC-SYR-CALL-')},{'REC-SYR-CALL-001','REC-SYR-CALL-002'})
  c=current['REC-SYR-CALL-001']
  self.assertEqual(c['side_a_sim'],'8996301746283951072')
  self.assertEqual(c['side_b_sim'],'8996301839572614087')
  self.assertEqual(c['call_transcript_speaker_imei'],'353294702931926')
  self.assertEqual(c['side_a_imei'],'353294702931926')
  self.assertEqual(c['side_b_imei'],'352099001122338')
  self.assertEqual(c['call_transcript_original'].replace('\r\n','\n'),(ROOT/c['call_transcript_url'].lstrip('/')).read_text(encoding='utf-8'))
  self.assertEqual(c['call_transcript_en'].replace('\r\n','\n'),(ROOT/c['call_translation_url'].lstrip('/')).read_text(encoding='utf-8'))
  self.assertTrue((ROOT/c['audio_url'].lstrip('/')).is_file())
  self.assertTrue((ROOT/c['audio_url'].lstrip('/')).with_suffix('.wav').is_file())
  c2=current['REC-SYR-CALL-002']
  self.assertEqual(c2['side_a_imei'],'353294702931926')
  self.assertEqual(c2['side_b_imei'],'352099001122338')
  self.assertEqual(c2['call_transcript_original'].replace('\r\n','\n'),(ROOT/c2['call_transcript_url'].lstrip('/')).read_text(encoding='utf-8').strip())
  self.assertEqual(c2['call_transcript_en'].replace('\r\n','\n'),(ROOT/c2['call_translation_url'].lstrip('/')).read_text(encoding='utf-8').strip())
  self.assertTrue((ROOT/c2['audio_url'].lstrip('/')).is_file())
if __name__=='__main__':unittest.main()
