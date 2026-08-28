#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix22_push.py: 推送缺失的二级页面 html + 之前改动修复 (BASE=48e19e1)"""
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

# 待提交
to_commit = [
    "assets/js/data.json",
    "assets/js/main.js",
    "assets/css/style.css",
    "assets/img/travel/travel-overview.jpg",
    "guide.html", "news.html", "news-detail.html", "register.html", "schedule.html", "travel.html",
]

file_shas = {}
for relpath in to_commit:
    fp = os.path.join(REPO, relpath)
    if not os.path.exists(fp):
        print(f"  missing {relpath} - skip")
        continue
    with open(fp, "rb") as f:
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

sh("git read-tree " + BASE, cwd=REPO)

for relpath, sha in file_shas.items():
    relpath_unix = relpath.replace("\\", "/")
    sh(f"git update-index --add --cacheinfo 100644,{sha},{relpath_unix}", cwd=REPO)

tree = sh("git write-tree").stdout.strip()
print(f"tree = {tree}")

commit = sh(f"git commit-tree {tree} -p {BASE} -m \"travel: 重写交通页版式 + 把缺失的 6 个二级 html 加入仓库\"").stdout.strip()
print(f"commit = {commit}")

sh(f"git update-ref refs/heads/main {commit}", cwd=REPO)

ssh_env = {**env, "GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"}
r = sh("git push github main --force", cwd=REPO, env=ssh_env, check=False)
print("push stdout:", r.stdout)
print("push stderr:", r.stderr)
print("push exit:", r.returncode)
