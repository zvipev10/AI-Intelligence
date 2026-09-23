"""Verify lossless documentation migration against the pinned Git baseline."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[4]
TASK = Path(__file__).resolve().parent
manifest = json.loads((TASK / "migration-manifest.json").read_text(encoding="utf-8"))
headings = 0
for entry in manifest["files"]:
    original = subprocess.check_output(["git", "show", f"{manifest['base_commit']}:{entry['original']}"], cwd=ROOT)
    archived = (ROOT / entry["snapshot"]).read_bytes()
    assert original == archived, entry["original"]
    assert hashlib.sha256(archived).hexdigest() == entry["sha256"]
    assert len(archived) == entry["bytes"]
    expected = [(n, line) for n, line in enumerate(original.decode("utf-8").splitlines(), 1) if re.match(r"^#{1,6} ", line)]
    assert expected == [(h["line"], h["heading"]) for h in entry["headings"]]
    for h in entry["headings"]:
        destination = TASK / h["destination"] if h["destination"].startswith("archive/") else ROOT / h["destination"]
        assert destination.exists(), destination
    headings += len(expected)
changed = subprocess.check_output(["git", "diff", "--name-only", manifest["base_commit"]], cwd=ROOT, text=True).splitlines()
untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True).splitlines()
paths = sorted(set(changed + untracked))
errors = []
links = 0
for name in paths:
    assert name.endswith((".md", ".md.txt", ".json", ".py", ".gitattributes")), f"Unexpected non-document change: {name}"
    path = ROOT / name
    if path.suffix != ".md":
        continue
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text):
        target = target.strip("<>").split("#", 1)[0]
        if not target or re.match(r"[a-zA-Z]+:", target):
            continue
        links += 1
        if not (path.parent / unquote(target)).exists():
            errors.append(f"{name}: {target}")
assert not errors, "Broken local links: " + repr(errors)
print(f"PASS: {len(manifest['files'])} exact-byte snapshots; {headings} headings; {links} local links; documentation-only scope.")
