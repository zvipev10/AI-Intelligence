"""One-time English Kosovo migration using the maintained release/activation contract.
Run after build_demo_index for both scenarios and evidence_catalog for English Kosovo.
Preserves the original Kosovo state; never copies it over a pre-existing new namespace.
"""
import argparse, hashlib, json, shlex, time
from pathlib import Path
from remote_deploy_ui import connect, run, sftp_mkdirs
from remote_release import build_manifest, get_json, local_commit, upload, verify_hashes, LOCAL_ROOT


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--key",type=Path,required=True)
    parser.add_argument("--build-root",type=Path,required=True)
    args=parser.parse_args()
    commit=local_commit()
    derived={}
    for scenario,folder in [("kosovo","kosovo-en-index"),("syria","syria-index-v12")]:
        base=args.build_root/folder
        metadata=json.loads((base/"semantic_event_index_hybrid_embedding.json").read_text())
        cache=base/"semantic_event_index_hybrid_embedding.pkl"
        if hashlib.sha256(cache.read_bytes()).hexdigest()!=metadata["sha256"]:raise ValueError("Invalid build cache")
        if metadata["manifest"]["version"]!="semantic-event-index-v12-english-object-parity":raise ValueError("Stale build cache")
        for file in [cache,cache.with_suffix(".json")]:derived[f"{scenario}/{file.name}"]=file
    for name in ["he.json","en.json","manifest.json"]:derived[f"evidence/{name}"]=args.build_root/"kosovo-en-evidence"/name
    client=connect(args.key.resolve())
    try:
        pointer=get_json(client,"cat /opt/demo-runtime/control/deployed-release.json")
        baseline=get_json(client,"cat "+shlex.quote(pointer["release_manifest"]))
        status=get_json(client,"curl -fsS http://127.0.0.1:8769/api/status")
        if status["scenario_id"]!="kosovo" or status["dataset_version"]!="v2.1":raise ValueError("Expected original Kosovo runtime; inspect state before migration")
        manifest=build_manifest(baseline,commit)
        staging=upload(client,manifest,commit)
        sftp=client.open_sftp()
        hashes={}
        try:
            for name,file in derived.items():
                destination=staging+"/derived/"+name
                sftp_mkdirs(sftp,str(Path(destination).parent).replace("\\","/"))
                sftp.put(str(file),destination)
                hashes[name]=hashlib.sha256(file.read_bytes()).hexdigest()
        finally:sftp.close()
        payload={"staging":staging,"manifest":manifest,"baseline":baseline,"pointer":pointer,"commit":commit,"hashes":hashes}
        script=REMOTE_SCRIPT.replace("PAYLOAD",repr(json.dumps(payload)))
        code,out,err=run(client,"cd /opt/serbia-poc-ui && /home/ubuntu/.hermes/hermes-agent/venv/bin/python - <<'PY'\n"+script+"\nPY",timeout=900,check=False)
        print(out,flush=True)
        if code:raise RuntimeError(err or "Migration failed; inspect preserved transition")
        verify_hashes(client,manifest,commit,f"/opt/demo-runtime/releases/{commit}/release-manifest.json")
        live=get_json(client,"curl -fsS http://127.0.0.1:8769/api/status")
        if live["scenario_id"]!="kosovo" or live["dataset_version"]!="v2.1-en1" or live["maintenance"]:raise RuntimeError("Post-release identity failed")
        print(json.dumps({"commit":commit,"scenario":live["scenario_id"],"dataset":live["dataset_version"],"rows":live["dataset_rows"],"maintenance":live["maintenance"]}))
    finally:client.close()

REMOTE_SCRIPT = r'''
import fcntl, hashlib, json, os, shutil, tarfile, time, uuid
from pathlib import Path
from activate_demo import Activator, atomic_json
from demo_runtime import load_profile
p=json.loads(PAYLOAD)
root=Path('/opt/demo-runtime'); control=root/'control'; staging=Path(p['staging']); ui=Path('/opt/serbia-poc-ui'); mcp=Path('/opt/serbia-poc')
operator=Activator()
new_state=root/'state/kosovo/v2.1-en1'
previous=json.loads(operator.current.read_text())
if previous['scenario_id']!='kosovo' or previous['dataset_version']!='v2.1':raise RuntimeError('Unexpected prior identity')
if new_state.exists():raise RuntimeError('New namespace already exists; refuse overwrite')
state_size=sum(f.stat().st_size for f in (root/'state/kosovo/v2.1').rglob('*') if f.is_file())
if shutil.disk_usage(root).free < state_size * 2 + 512 * 1024 * 1024:raise RuntimeError('Insufficient disk space for migration and recovery')
for name,expected in p['hashes'].items():
    if hashlib.sha256((staging/'derived'/name).read_bytes()).hexdigest()!=expected:raise RuntimeError('Derived hash mismatch')
for section,folder in [('files','ui'),('mcp_files','mcp')]:
    for name,expected in p['manifest'][section].items():
        if hashlib.sha256((staging/folder/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()!=expected:raise RuntimeError('Source staging mismatch: '+name)
backup=Path('/home/ubuntu/deploy-backups')/('kosovo-english-'+time.strftime('%Y%m%dT%H%M%SZ')+'.tar.gz')
backup.parent.mkdir(parents=True,exist_ok=True)
with (control/'activation.lock').open('a') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    operator.verify_release(Path(p['pointer']['release_manifest']))
    target={'scenario_id':'kosovo','dataset_version':'v2.1-en1','activation_generation':uuid.uuid4().hex}
    atomic_json(operator.journal,{'phase':'draining','previous':previous,'target':target})
    atomic_json(control/'maintenance.json',{'target':'kosovo','release':p['commit']})
    try:operator.drain(120)
    except Exception:
        operator.journal.unlink(missing_ok=True);(control/'maintenance.json').unlink(missing_ok=True);raise
    operator.services('stop')
    source_state=root/'state/kosovo/v2.1'
    syria_index=root/'state/syria/cellular-records-v13/semantic_index'
    try:
        with tarfile.open(backup,'w:gz') as archive:
            for section,folder,location in [('files','ui',ui),('mcp_files','mcp',mcp)]:
                for name in p['manifest'][section]:
                    if (location/name).is_file():
                        archive.add(location/name,arcname=folder+'/'+name,recursive=False)
            archive.add(ui/'release-manifest.json',arcname='ui/release-manifest.json',recursive=False)
            archive.add(syria_index,arcname='syria-index')
        os.chmod(backup,0o600)
        shutil.copytree(source_state,new_state)
        atomic_json(new_state/'state.json',{'schema_version':1,'scenario_id':'kosovo','dataset_version':'v2.1-en1'})
        # Carry immutable IDs and saved text forward; update only dataset identity metadata.
        def rebind(value):
            if isinstance(value,list):return [rebind(x) for x in value]
            if isinstance(value,dict):return {k:('v2.1-en1' if k in {'dataset','dataset_version'} and v=='v2.1' else rebind(v)) for k,v in value.items()}
            return value
        for file in new_state.rglob('*.json'):
            if 'semantic_index' in file.parts or 'evidence_catalog' in file.parts:continue
            try:data=json.loads(file.read_text(encoding='utf-8')); updated=rebind(data)
            except (ValueError,UnicodeError):continue
            if updated!=data:atomic_json(file,updated)
        for section,folder,location in [('files','ui',ui),('mcp_files','mcp',mcp)]:
            for name in p['manifest'][section]:
                destination=location/name;destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(staging/folder/name,destination);os.chmod(destination,0o644)
        for scenario,index in [('kosovo',new_state/'semantic_index'),('syria',syria_index)]:
            index.mkdir(parents=True,exist_ok=True)
            for file in (staging/'derived'/scenario).iterdir():shutil.copyfile(file,index/file.name)
        evidence=new_state/'evidence_catalog';evidence.mkdir(parents=True,exist_ok=True)
        for file in (staging/'derived/evidence').iterdir():shutil.copyfile(file,evidence/file.name)
        release=root/'releases'/p['commit'];release.mkdir(exist_ok=False)
        atomic_json(release/'release-manifest.json',p['manifest']);atomic_json(ui/'release-manifest.json',p['manifest'])
        for scenario in ['kosovo','syria']:
            profile=load_profile(ui,scenario,verify=True);load_profile(mcp,scenario,verify=True);operator.verify_search_cache(profile)
        operator.verify_release(release/'release-manifest.json')
        # Use the installed readiness policy, including bounded slow-VM request timeouts.
        import importlib, activate_demo
        operator=importlib.reload(activate_demo).Activator()
        operator.select(target);operator.services('start');operator.health(target,timeout=240)
        atomic_json(operator.current,target)
        atomic_json(control/'deployed-release.json',{'app_commit':p['commit'],'release_manifest':str(release/'release-manifest.json')})
        operator.journal.unlink(missing_ok=True);(control/'maintenance.json').unlink(missing_ok=True)
        print(json.dumps({'backup':str(backup),'previous':previous,'target':target}),flush=True)
    except Exception:
        operator.services('stop')
        if backup.exists():
            with tarfile.open(backup,'r:gz') as archive:
                for member in archive.getmembers():
                    if not member.isfile():continue
                    prefix,relative=member.name.split('/',1)
                    location={'ui':ui,'mcp':mcp,'syria-index':syria_index}[prefix]
                    destination=(location/relative).resolve()
                    if not destination.is_relative_to(location.resolve()):raise RuntimeError('Unsafe recovery path')
                    destination.parent.mkdir(parents=True,exist_ok=True)
                    destination.write_bytes(archive.extractfile(member).read())
        previous['activation_generation']=uuid.uuid4().hex
        operator.select(previous);operator.services('start');operator.health(previous,timeout=240)
        atomic_json(operator.current,previous);atomic_json(control/'deployed-release.json',p['pointer'])
        operator.journal.unlink(missing_ok=True);(control/'maintenance.json').unlink(missing_ok=True)
        raise
'''

if __name__=="__main__": main()
