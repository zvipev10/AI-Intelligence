#!/usr/bin/env python3
"""Install a hash-pinned source release without replacing runtime state."""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
import sys
import time
from pathlib import Path, PurePosixPath

from remote_deploy_ui import USER, connect, run, sftp_mkdirs

LOCAL_ROOT = Path(__file__).resolve().parent.parent
UI_ROOT = "/opt/serbia-poc-ui"
MCP_ROOT = "/opt/serbia-poc"
CONTROL = "/opt/demo-runtime/control"
RELEASES = "/opt/demo-runtime/releases"


def safe_path(name: str) -> Path:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"unsafe release path: {name!r}")
    return Path(*path.parts)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def local_commit() -> str:
    return subprocess.check_output(["git", "-C", str(LOCAL_ROOT.parent), "rev-parse", "HEAD"], text=True).strip()


def local_profiles() -> dict[str, dict[str, str]]:
    sys.path.insert(0, str(LOCAL_ROOT))
    from demo_runtime import load_profile
    result = {}
    for scenario in ("kosovo", "syria"):
        profile = load_profile(LOCAL_ROOT, scenario, verify=True)
        result[scenario] = {"dataset_version": profile["dataset_version"], "profile_version": str(profile["profile_version"])}
    return result


def build_manifest(baseline: dict, commit: str) -> dict:
    result = {"app_commit": commit, "files": {}, "mcp_files": {}, "profiles": local_profiles(),
              "schema_version": baseline.get("schema_version", 1), "state_schema_version": baseline.get("state_schema_version", 1)}
    for section in ("files", "mcp_files"):
        for name in baseline.get(section, {}):
            path = LOCAL_ROOT / safe_path(name)
            if not path.is_file():
                raise FileNotFoundError(f"missing release file: {name}")
            result[section][name] = sha256(path)
        if not result[section]:
            raise ValueError(f"baseline lacks {section}")
    return result


def get_json(client, command: str) -> dict:
    return json.loads(run(client, command, timeout=30)[1])


def upload(client, manifest: dict, commit: str) -> str:
    staging = f"/tmp/ai-intelligence-release-{commit[:12]}-{int(time.time())}"
    run(client, f"install -d -m 0700 {shlex.quote(staging)}/ui {shlex.quote(staging)}/mcp")
    sftp = client.open_sftp()
    try:
        for section, folder in (("files", "ui"), ("mcp_files", "mcp")):
            for name in manifest[section]:
                destination = str(PurePosixPath(staging) / folder / PurePosixPath(name))
                sftp_mkdirs(sftp, str(PurePosixPath(destination).parent))
                sftp.put(str(LOCAL_ROOT / safe_path(name)), destination)
        with sftp.open(f"{staging}/release-manifest.json", "w") as stream:
            stream.write(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    finally:
        sftp.close()
    return staging


def install(client, staging: str, manifest: dict, commit: str) -> tuple[str, str]:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    backup = f"/home/{USER}/deploy-backups/release-before-{commit[:12]}-{stamp}.tar.gz"
    release_dir = f"{RELEASES}/{commit}"
    payload = json.dumps({"staging": staging, "backup": backup, "ui": UI_ROOT, "mcp": MCP_ROOT,
                          "release": release_dir, "files": list(manifest["files"]), "mcp_files": list(manifest["mcp_files"])})
    script = """
import json, os, shutil, tarfile
from pathlib import Path
p = json.loads(PAYLOAD)
with tarfile.open(p['backup'], 'w:gz') as archive:
    for label, root, names in [('ui', Path(p['ui']), p['files']), ('mcp', Path(p['mcp']), p['mcp_files'])]:
        for name in names:
            source = root / name
            if source.is_file(): archive.add(source, arcname=label + '/' + name, recursive=False)
for source_root, destination_root in [(Path(p['staging']) / 'ui', Path(p['ui']),), (Path(p['staging']) / 'mcp', Path(p['mcp']),)]:
    for source in source_root.rglob('*'):
        if source.is_file():
            destination = destination_root / source.relative_to(source_root)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            os.chmod(destination, 0o644)
release = Path(p['release'])
release.mkdir(parents=True, exist_ok=False)
for destination in [release / 'release-manifest.json', Path(p['ui']) / 'release-manifest.json']:
    shutil.copyfile(Path(p['staging']) / 'release-manifest.json', destination)
    os.chmod(destination, 0o644)
""".replace("PAYLOAD", repr(payload))
    command = f"mkdir -p /home/{USER}/deploy-backups && python3 - <<'PY'\n{script}\nPY"
    run(client, command, timeout=180)
    return backup, f"{release_dir}/release-manifest.json"


def verify_hashes(client, manifest: dict, commit: str, manifest_path: str) -> None:
    payload = json.dumps({"manifest": manifest, "ui": UI_ROOT, "mcp": MCP_ROOT, "commit": commit, "path": manifest_path})
    script = """
import hashlib, json
from pathlib import Path
p=json.loads(PAYLOAD)
for section, root in [('files', Path(p['ui'])), ('mcp_files', Path(p['mcp']))]:
    for name, expected in p['manifest'][section].items():
        actual=hashlib.sha256((root/name).read_bytes().replace(b'\\r\\n', b'\\n')).hexdigest()
        if actual != expected: raise SystemExit('hash mismatch: ' + section + '/' + name)
if json.loads(Path(p['path']).read_text()) != p['manifest']: raise SystemExit('manifest mismatch')
print('verified')
""".replace("PAYLOAD", repr(payload))
    run(client, "python3 - <<'PY'\n" + script + "\nPY", timeout=90)


def update_pointer(client, commit: str, manifest_path: str) -> None:
    pointer = json.dumps({"app_commit": commit, "release_manifest": manifest_path}, indent=2) + "\n"
    script = "from pathlib import Path\nimport os\nt=Path('/opt/demo-runtime/control/deployed-release.json')\np=t.with_suffix('.next')\np.write_text(" + repr(pointer) + ", encoding='utf-8')\nos.replace(p,t)"
    run(client, "python3 - <<'PY'\n" + script + "\nPY", timeout=30)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", required=True, type=Path)
    parser.add_argument("--scenario", choices=("syria", "kosovo"), default="syria")
    args = parser.parse_args()
    commit = local_commit()
    client = connect(args.key.resolve())
    try:
        pointer = get_json(client, f"cat {CONTROL}/deployed-release.json")
        baseline = get_json(client, f"cat {shlex.quote(pointer['release_manifest'])}")
        manifest = build_manifest(baseline, commit)
        manifest_path = f"{RELEASES}/{commit}/release-manifest.json"
        code, existing, _ = run(client, f"cat {shlex.quote(manifest_path)}", timeout=30, check=False)
        if code == 0:
            if json.loads(existing) != manifest:
                raise RuntimeError("Existing release manifest differs from the checked-out source")
            backup = None
        else:
            staging = upload(client, manifest, commit)
            backup, manifest_path = install(client, staging, manifest, commit)
        verify_hashes(client, manifest, commit, manifest_path)
        _, activation, _ = run(client, f"/home/ubuntu/.hermes/hermes-agent/venv/bin/python {UI_ROOT}/activate_demo.py {args.scenario} --release {shlex.quote(manifest_path)}", timeout=240)
        status = json.loads(activation)
        if status.get('scenario_id') != args.scenario or status.get('maintenance'):
            raise RuntimeError(f"activation did not leave {args.scenario} active")
        update_pointer(client, commit, manifest_path)
        service = run(client, "sudo -n systemctl is-active serbia-poc-ui.service", timeout=30)[1].strip()
        if service != 'active': raise RuntimeError(f"UI service is {service!r}")
        print(json.dumps({"release": commit, "backup": backup, "release_manifest": manifest_path, "status": status, "service": service}, ensure_ascii=False, indent=2))
    finally:
        client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
