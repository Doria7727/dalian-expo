import os, subprocess, glob

BASE = "a7f0627b265db0cde2bf24f65518ddf8fef610b0"
MODIFIED = {"assets/css/style.css", "assets/js/data.json", "assets/js/main.js"}
NEW_FILES = sorted(glob.glob("assets/img/past/past*.jpg"))

def git_show(path):
    return subprocess.run(["git", "show", f"{BASE}:{path}"], capture_output=True).stdout

def write_blob(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    r = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=data, capture_output=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.decode().strip()

def idx_add(path, sha):
    subprocess.run(["git", "update-index", "--add", "--cacheinfo", f"100644,{sha},{path}"], check=True)

# list tracked files at BASE
out = subprocess.run(["git", "ls-tree", "-r", "--name-only", BASE], capture_output=True, text=True).stdout.strip().split("\n")
out = [p.replace("\\", "/") for p in out if p]
junk = [p for p in out if '"' in p]
NEW_FILES = [p.replace("\\", "/") for p in NEW_FILES]

# reset index to BASE
subprocess.run(["git", "read-tree", BASE], check=True)
for j in junk:
    subprocess.run(["git", "update-index", "--force-remove", j], check=True)

# edited files from disk
for path in MODIFIED:
    disk = open(path, "r", encoding="utf-8").read()
    idx_add(path, write_blob(disk))

# new photos from disk (normalize to POSIX slashes for git)
for path in NEW_FILES:
    path = path.replace("\\", "/")
    blob = open(path, "rb").read()
    idx_add(path, write_blob(blob))
    print("added photo", path)

# re-add every other tracked file from BASE unchanged
for path in out:
    if path in MODIFIED or path in junk:
        continue
    idx_add(path, write_blob(git_show(path)))

tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
print("TREE", tree)

# validation
base_files = (set(out) - set(junk)) | set(NEW_FILES)  # expected set (junk excluded, intentionally dropped)
new_files = set(subprocess.run(["git", "ls-tree", "-r", "--name-only", tree], capture_output=True, text=True).stdout.strip().split("\n"))
new_files = set(p for p in new_files if p and '"' not in p)
removed = base_files - new_files
added = new_files - base_files
print("REMOVED", removed)
print("ADDED", added)
assert removed == set(), f"Unexpected removed: {removed}"
assert added == set(), f"Unexpected added (should be empty, new photos already counted): {added}"

# confirm PAST_PHOTOS wired
assert "PAST_PHOTOS = D.PAST_PHOTOS" in open("assets/js/main.js", encoding="utf-8").read()
assert "assets/img/past/past10.jpg" in open("assets/js/data.json", encoding="utf-8").read()

msg = "往届回顾：替换为 10 张真实展会照片（数据驱动 PAST_PHOTOS）"
r = subprocess.run(["git", "commit-tree", tree, "-p", BASE, "-m", msg], capture_output=True, text=True)
commit = r.stdout.strip()
print("COMMIT", commit)
subprocess.run(["git", "update-ref", "refs/heads/main", commit], check=True)
env = os.environ.copy()
env["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
r = subprocess.run(["git", "push", "github", "main", "--force"], capture_output=True, text=True, env=env)
print("PUSH rc", r.returncode, r.stdout, r.stderr)
assert r.returncode == 0
print("DONE", commit)
