#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix18.py: footer logo 简化 + about Hero 文字可读性修复
- main.js: footer 的 logoBlock() 改用纯图片
- style.css: .footer-brand .footer-logo-img (56px)
- style.css: .page-hero 内 .about-meta/.stats-strip-inner 配色修正（深蓝底文字）

git plumbing:
  read-tree BASE → hash-object -w → update-index → write-tree → commit-tree → update-ref → push
"""
import subprocess, sys, os, tempfile

REPO = r"C:\Users\ASUS\Desktop\2027大连工博会网站"
BASE = "d77ef91"
REMOTE = "github"
BRANCH = "main"

os.chdir(REPO)

def run(cmd, cwd=None, stdin=None, env=None, check=True):
    r = subprocess.run(cmd, cwd=cwd or REPO, shell=True, input=stdin,
                       capture_output=True, text=False, env=env)
    if check and r.returncode != 0:
        print(f"!! CMD FAIL: {cmd}\nSTDOUT:{r.stdout!r}\nSTDERR:{r.stderr!r}", file=sys.stderr)
        sys.exit(1)
    return r

def add_to_index(path):
    """用临时文件传 stdin 给 hash-object,以避免被 sh() 截字节"""
    blob = open(path, "rb").read()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".bin")
    try:
        tmp.write(blob); tmp.close()
        sha = run(f'git hash-object -w "{path}"').stdout.strip().decode()
    finally:
        os.unlink(tmp.name)
    run(f'git update-index --add --cacheinfo 100644,{sha},{path}')
    return sha

# 继承 BASE 树
run(f'git read-tree {BASE}')

# 把两个改过的文件加入索引
files = ["assets/js/main.js", "assets/css/style.css"]
for f in files:
    add_to_index(f)
    print(f"  added: {f}")

# 写树 + 提交
tree = run('git write-tree').stdout.strip().decode()
parent = run(f'git rev-parse {BASE}').stdout.strip().decode()
msg = "footer logo 简化 + about Hero 文字可读性修复"
commit = run(f'git commit-tree {tree} -p {parent} -m "{msg}"').stdout.strip().decode()
run(f'git update-ref refs/heads/{BRANCH} {commit}')
print(f"local commit: {commit}")

# 推送
ssh_env = {**os.environ, "GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"}
run(f'git push {REMOTE} {BRANCH} --force', env=ssh_env)
print(f"pushed: {commit}")
