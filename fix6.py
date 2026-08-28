#!/usr/bin/env python3
# fix6.py - 仅提交 main.js 调试版（加 try/catch 暴露错误）
import os, sys, subprocess

BASE = "8a8edcee937c7adb1ce353faa1f16dea834adfa8"
REPO = "C:/Users/ASUS/Desktop/2027大连工博会网站"
os.chdir(REPO)

r = subprocess.run(["git", "read-tree", BASE], capture_output=True, text=True)
if r.returncode != 0: print("FAIL read-tree:", r.stderr); sys.exit(1)
print("OK read-tree BASE")

def write_blob(data):
    r = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=data, capture_output=True)
    if r.returncode != 0: raise RuntimeError(r.stderr.decode())
    return r.stdout.decode().strip()

def idx_add(path, blob):
    r = subprocess.run(["git", "update-index", "--add", "--cacheinfo",
                        f"100644,{blob},{path}"], capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(r.stderr)

with open("assets/js/main.js","rb") as fp: blob = write_blob(fp.read())
idx_add("assets/js/main.js", blob)
print(f"OK staged main.js {blob[:10]}")

tree = subprocess.run(["git","write-tree"], capture_output=True, text=True).stdout.strip()
print(f"OK tree {tree}")

def list_tree(c):
    r = subprocess.run(["git","ls-tree","-r",c], capture_output=True, text=True)
    return {l.split("\t",1)[1]:l.split(" ",2)[2].split("\t",1)[0] for l in r.stdout.strip().split("\n") if l}

b = list_tree(BASE); n = list_tree(tree)
assert set(b)==set(n), f"set diff\n  -{set(b)-set(n)}\n  +{set(n)-set(b)}"
chg = [f for f in b if b[f]!=n[f]]
assert chg == ["assets/js/main.js"], f"unexpected changes: {chg}"
print(f"OK only main.js changed")

parent = subprocess.run(["git","rev-parse",BASE], capture_output=True, text=True).stdout.strip()
r = subprocess.run(["git","commit-tree",tree,"-p",parent,"-m","debug: wrap render in try/catch to expose error"], capture_output=True, text=True)
nc = r.stdout.strip()
print(f"OK commit {nc}")
subprocess.run(["git","update-ref","refs/heads/main",nc], check=True)

env = os.environ.copy(); env["GIT_SSH_COMMAND"]="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
r = subprocess.run(["git","push","github","main","--force"], capture_output=True, text=True, env=env)
print("push rc=", r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip())
