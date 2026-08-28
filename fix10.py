import os, subprocess, re

BASE = "86347a7f03f7d22ffdfca0352ade698d58b78417"
MOD = "assets/css/style.css"

def git_show(p):
    return subprocess.run(["git", "show", f"{BASE}:{p}"], capture_output=True).stdout
def write_blob(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    r = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=data, capture_output=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.decode().strip()
def idx_add(p, sha):
    subprocess.run(["git", "update-index", "--add", "--cacheinfo", f"100644,{sha},{p}"], check=True)

out = subprocess.run(["git", "ls-tree", "-r", "--name-only", BASE], capture_output=True, text=True).stdout.strip().split("\n")
out = [p for p in out if p]
junk = [p for p in out if '"' in p]

subprocess.run(["git", "read-tree", BASE], check=True)
for j in junk:
    subprocess.run(["git", "update-index", "--force-remove", j], check=True)

disk = open(MOD, "r", encoding="utf-8").read()
m_tile = re.search(r"\.past-tile\s*\{([^}]*)\}", disk)
m_img  = re.search(r"\.past-tile img\s*\{([^}]*)\}", disk)
assert m_tile and m_img, "past-tile rules missing"
assert "place-items" not in m_tile.group(1), "old place-items still in .past-tile"
assert "position: absolute; inset: 0" in m_img.group(1), "new inset:0 rule missing"
assert "object-fit: cover" in m_img.group(1), "object-fit missing"
idx_add(MOD, write_blob(disk))

for p in out:
    if p == MOD or p in junk: continue
    idx_add(p, write_blob(git_show(p)))

tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
print("TREE", tree)

r = subprocess.run(["git", "commit-tree", tree, "-p", BASE, "-m", "往届照片：修正图片填充（去除 display:grid 引起的 letterbox）"], capture_output=True, text=True)
commit = r.stdout.strip()
print("COMMIT", commit)
subprocess.run(["git", "update-ref", "refs/heads/main", commit], check=True)

env = os.environ.copy()
env["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
r = subprocess.run(["git", "push", "github", "main", "--force"], capture_output=True, text=True, env=env)
print("PUSH rc", r.returncode)
print(r.stdout)
print(r.stderr)
assert r.returncode == 0
print("DONE", commit)
