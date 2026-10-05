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
  self.assertEqual(c['side_b_sim'],'')
  self.assertEqual(c['call_transcript_speaker_imei'],'353294702931926')
  self.assertEqual(c['side_a_imei'],'353294702931926')
  self.assertEqual(c['side_b_imei'],'')
  self.assertEqual(c['call_transcript_original'].replace('\r\n','\n'),(ROOT/c['call_transcript_url'].lstrip('/')).read_text(encoding='utf-8'))
  self.assertEqual(c['call_transcript_en'].replace('\r\n','\n'),(ROOT/c['call_translation_url'].lstrip('/')).read_text(encoding='utf-8'))
  self.assertTrue((ROOT/c['audio_url'].lstrip('/')).is_file())
  self.assertTrue((ROOT/c['audio_url'].lstrip('/')).with_suffix('.wav').is_file())
  c2=current['REC-SYR-CALL-002']
  self.assertEqual(c2['side_a_imei'],'353294702931926')
  self.assertEqual(c2['side_b_imei'],'')
  self.assertEqual(c2['side_b_sim'],'')
  self.assertEqual(c2['call_transcript_original'].replace('\r\n','\n'),(ROOT/c2['call_transcript_url'].lstrip('/')).read_text(encoding='utf-8').strip())
  self.assertEqual(c2['call_transcript_en'].replace('\r\n','\n'),(ROOT/c2['call_translation_url'].lstrip('/')).read_text(encoding='utf-8').strip())
  self.assertTrue((ROOT/c2['audio_url'].lstrip('/')).is_file())
  locations=__import__('json').loads((ROOT/p['files']['locations']).read_text(encoding='utf-8'))
  self.assertEqual((c['location_id'],c['side_a_location_id']),('LOC-SYR-CALL-001','LOC-SYR-CALL-001'))
  self.assertEqual((locations[c['location_id']]['latitude'],locations[c['location_id']]['longitude']),(35.05008341925823,36.27154430013932))
  self.assertEqual((c2['location_id'],c2['side_a_location_id']),('LOC-SYR-CALL-002','LOC-SYR-CALL-002'))
  self.assertEqual((locations[c2['location_id']]['latitude'],locations[c2['location_id']]['longitude']),(34.9837599416126,35.889327777437586))

 def test_call_timeline_and_viewer_follow_reference_layout(self):
  app=(ROOT/'app.js').read_text(encoding='utf-8')
  styles=(ROOT/'styles.css').read_text(encoding='utf-8')
  self.assertIn('class="call-list-header"',app)
  self.assertIn('Date &amp; time',app)
  self.assertIn('class="call-list-party"',app)
  self.assertIn('class="call-list-location"',app)
  self.assertIn('function startCellularCallAudio()',app)
  self.assertIn('<audio controls autoplay preload="auto"',app)
  self.assertIn('if (cellularCallViewer) startCellularCallAudio();',app)
  self.assertIn('.timeline.call-list-timeline',styles)
  self.assertIn('grid-template-columns:minmax(520px,47%) minmax(480px,1fr)',styles)
  self.assertIn('.is-cellular-viewer .call-workspace { grid-template-columns:minmax(0,1fr); }',styles)
if __name__=='__main__':unittest.main()
