import csv,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from demo_runtime import load_profile
ROOT=Path(__file__).resolve().parent
class IpdrImport(unittest.TestCase):
 def test_source_parity_and_other_layers(self):
  p=load_profile(ROOT,'syria',verify=True)
  rows=list(csv.DictReader((ROOT/p['files']['events']).read_text().splitlines()))
  source=list(csv.DictReader((ROOT/'data/syria_ipdr_v1/IPDR-expanded.csv').read_text().splitlines()))
  current={r['source_record_id']:r for r in rows if r['source_type']=='IPDR'}
  self.assertEqual(len(rows),424);self.assertEqual(len(current),300)
  for raw in source:
   row=current[raw['record_id']]
   for k,v in raw.items():self.assertEqual(row['source_record_id' if k=='record_id' else k.strip()],v)
   self.assertFalse(row['entity_id']);self.assertFalse(row['location_id'])
  previous=list(csv.DictReader((ROOT/'data/syria_adint_v2/events.csv').read_text().splitlines()))
  byid={r['event_id']:r for r in rows}
  for old in previous:
   if old['source_type']=='IPDR':self.assertNotIn(old['event_id'],byid)
   else:self.assertEqual(old,{k:byid[old['event_id']][k] for k in old})
 def test_public_fields_and_identifiers(self):
  with tempfile.TemporaryDirectory() as state:
   code="""import mcp_server.server as s
rows=[s.public_event(r) for r in s.EVENTS if r['source_type']=='IPDR']
assert len(rows)==300 and sum(bool(r['imei']) for r in rows)==2
assert all(not r['location_id'] and not r['entity_id'] for r in rows)
for key in ['source_record_id','ip_source','ip_target','ip_public','source_system']:
 assert s.search_events({'source_types':['IPDR'],'keywords':[rows[0][key]]})['total']>0
assert all(len(r['source_record_id'])>=15 for r in rows)
"""
   r=subprocess.run([sys.executable,'-c',code],cwd=ROOT,env={**os.environ,'INTELLIGENCE_POC_SCENARIO':'syria','INTELLIGENCE_POC_STATE_ROOT':state},capture_output=True,text=True,timeout=60)
   self.assertEqual(r.returncode,0,r.stderr)
if __name__=='__main__':unittest.main()
