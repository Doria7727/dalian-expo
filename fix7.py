#!/usr/bin/env python3
# fix7.py - 修复 renderHome 缺 const c + 修正 enName 为 INDUSTRY FAIR
import os, sys, subprocess

BASE = "0f266d0237b81111752c5cf6b023c1160dc41e72"
REPO = "C:/Users/ASUS/Desktop/2027大连工博会网站"
os.chdir(REPO)

r = subprocess.run(["git","read-tree",BASE], capture_output=True, text=True)
if r.returncode != 0: print("FAIL read-tree:",r.stderr); sys.exit(1)
print("OK read-tree BASE")

def write_blob(d):
    r = subprocess.run(["git","hash-object","-w","--stdin"], input=d, capture_output=True)
    if r.returncode != 0: raise RuntimeError(r.stderr.decode())
    return r.stdout.decode().strip()

def idx_add(p,b):
    r = subprocess.run(["git","update-index","--add","--cacheinfo",f"100644,{b},{p}"], capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(r.stderr)

for f in ["assets/js/main.js","assets/js/data.json"]:
    if not os.path.exists(f): print(f"FAIL missing {f}"); sys.exit(1)
    with open(f,"rb") as fp: blob = write_blob(fp.read())
    idx_add(f, blob)
    print(f"OK staged {f} {blob[:10]}")

tree = subprocess.run(["git","write-tree"], capture_output=True, text=True).stdout.strip()
print(f"OK tree {tree}")

def list_tree(c):
    r = subprocess.run(["git","ls-tree","-r",c], capture_output=True, text=True)
    return {l.split("\t",1)[1]:l.split(" ",2)[2].split("\t",1)[0] for l in r.stdout.strip().split("\n") if l}

b = list_tree(BASE); n = list_tree(tree)
assert set(b)==set(n), f"set diff -{set(b)-set(n)} +{set(n)-set(b)}"
chg = sorted(f for f in b if b[f]!=n[f])
assert chg == ["assets/js/data.json","assets/js/main.js"], f"unexpected: {chg}"
print("OK only main.js + data.json changed")

parent = subprocess.run(["git","rev-parse",BASE], capture_output=True, text=True).stdout.strip()
r = subprocess.run(["git","commit-tree",tree,"-p",parent,"-m","fix: add const c in renderHome, set enName to 'Dalian International Industry Fair'"], capture_output=True, text=True)
nc = r.stdout.strip()
print(f"OK commit {nc}")
subprocess.run(["git","update-ref","refs/heads/main",nc], check=True)

env = os.environ.copy(); env["GIT_SSH_COMMAND"]="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
r = subprocess.run(["git","push","github","main","--force"], capture_output=True, text=True, env=env)
print("push:", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip())
print("DONE", nc)
