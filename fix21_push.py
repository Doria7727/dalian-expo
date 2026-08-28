#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix21_push.py: 推送交通页改版（用 mem git plumbing，BASE=4247252）"""
import subprocess, sys, os

REPO = r"C:\Users\ASUS\Desktop\2027大连工博会网站"

def sh(cmd, cwd=None, check=True, env=None):
    r = subprocess.run(cmd, cwd=cwd or REPO, shell=True, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    if check and r.returncode != 0:
        print(f"!! FAIL: {cmd}\nSTDOUT:{r.stdout}\nSTDERR:{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return r

BASE = sh("git rev-parse HEAD").stdout.strip()
print(f"BASE = {BASE}")

# 1. hash-object for each modified file
to_commit = ["assets/js/data.json", "assets/js/main.js", "assets/css/style.css", "assets/img/travel/travel-overview.jpg"]
file_shas = {}
for relpath in to_commit:
    with open(os.path.join(REPO, relpath), "rb") as f:
        content = f.read()
    p = subprocess.Popen(['git', 'hash-object', '-w', '--stdin'],
                         cwd=REPO, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(content)
    sha = out.decode().strip()
    print(f"  sha({relpath}) = {sha}")
    file_shas[relpath] = sha

env = os.environ.copy()
env["GIT_AUTHOR_NAME"] = "WorkBuddy"
env["GIT_AUTHOR_EMAIL"] = "wb@workbuddy.local"
env["GIT_COMMITTER_NAME"] = "WorkBuddy"
env["GIT_COMMITTER_EMAIL"] = "wb@workbuddy.local"

# 2. read-tree BASE
sh("git read-tree " + BASE, cwd=REPO)

# 3. update-index
for relpath, sha in file_shas.items():
    relpath_unix = relpath.replace("\\", "/")
    sh(f"git update-index --add --cacheinfo 100644,{sha},{relpath_unix}", cwd=REPO)

# 4. write-tree
tree = sh("git write-tree").stdout.strip()
print(f"tree = {tree}")

# 5. commit-tree
commit = sh(f"git commit-tree {tree} -p {BASE} -m \"travel: 改用 venue 总览图 + 5 条路线编号 + 距离数据\"").stdout.strip()
print(f"commit = {commit}")

# 6. update-ref
sh(f"git update-ref refs/heads/main {commit}", cwd=REPO)

# 7. push
ssh_env = {**env, "GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"}
r = sh("git push github main --force", cwd=REPO, env=ssh_env, check=False)
print("push stdout:", r.stdout)
print("push stderr:", r.stderr)
print("push exit:", r.returncode)
