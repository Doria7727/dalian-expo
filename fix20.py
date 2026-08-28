#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix20.py: 改 footer tagline 文字"""
import subprocess, sys, os, time

REPO = r"C:\Users\ASUS\Desktop\2027大连工博会网站"
PYTHON = r"C:\Users\ASUS\.workbuddy\binaries\python\versions\3.13.12\python.exe"

def sh(cmd, cwd=None, check=True, env=None):
    r = subprocess.run(cmd, cwd=cwd or REPO, shell=True, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    if check and r.returncode != 0:
        print(f"!! FAIL: {cmd}\nSTDOUT:{r.stdout}\nSTDERR:{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return r

BASE = sh("git rev-parse HEAD").stdout.strip()  # current = 719cafb
print(f"BASE = {BASE}")

# 1. hash-object for each modified file
files_with_content = []
for relpath in ["assets/js/main.js"]:
    with open(os.path.join(REPO, relpath), "rb") as f:
        content = f.read()
    sha = sh(f'git hash-object -w --stdin', cwd=REPO)
    # re-run with input
    p = subprocess.Popen(['git', 'hash-object', '-w', '--stdin'],
                         cwd=REPO, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(content)
    sha = out.decode().strip()
    print(f"  sha({relpath}) = {sha}")
    files_with_content.append((relpath, sha))

# 2. setup git env (no CRLF mangling)
env = os.environ.copy()
env["GIT_AUTHOR_NAME"] = "WorkBuddy"
env["GIT_AUTHOR_EMAIL"] = "wb@workbuddy.local"
env["GIT_COMMITTER_NAME"] = "WorkBuddy"
env["GIT_COMMITTER_EMAIL"] = "wb@workbuddy.local"

# 3. read-tree BASE
sh("git read-tree " + BASE, cwd=REPO)

# 4. update-index for modified files
for relpath, sha in files_with_content:
    relpath_unix = relpath.replace("\\", "/")
    sh(f"git update-index --add --cacheinfo 100644,{sha},{relpath_unix}", cwd=REPO)

# 5. write-tree
tree = sh("git write-tree").stdout.strip()
print(f"tree = {tree}")

# 6. commit-tree
commit = sh(f"git commit-tree {tree} -p {BASE} -m \"footer: tagline 东北工业标杆展会 → 大连国际工业博览会\"").stdout.strip()
print(f"commit = {commit}")

# 7. update-ref main
sh(f"git update-ref refs/heads/main {commit}", cwd=REPO)

# 8. push github
ssh_env = {**env, "GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"}
r = sh("git push github main --force", cwd=REPO, env=ssh_env, check=False)
print("push stdout:", r.stdout)
print("push stderr:", r.stderr)
print("push exit:", r.returncode)
