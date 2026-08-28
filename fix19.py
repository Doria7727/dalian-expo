#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix19.py: about 页面 WHY/SCOPE 从卡片网格改为参考页风格的大编号纯文本列表
- main.js: WHY/SCOPE 去掉 .card，改用 .reason-item/.scope-item；WHY 容器改 grid-2
- style.css: .reason-item/.scope-item 纯文本列表（去背景边框、加分隔线、编号醒目、段落清晰 --c-ink）
git plumbing: read-tree BASE -> hash-object -w -> update-index -> write-tree -> commit-tree -> update-ref -> push
"""
import subprocess, os, tempfile

REPO = r"C:\Users\ASUS\Desktop\2027大连工博会网站"
BASE = "719cafb"
REMOTE = "github"
BRANCH = "main"

os.chdir(REPO)

def run(cmd, stdin=None, env=None, check=True):
    r = subprocess.run(cmd, cwd=REPO, shell=True, input=stdin,
                       capture_output=True, text=False, env=env)
    if check and r.returncode != 0:
        print(f"!! FAIL: {cmd}\n{r.stderr!r}", file=__import__('sys').stderr)
        raise SystemExit(1)
    return r

def add_to_index(path):
    blob = open(path, "rb").read()
    sha = run(f'git hash-object -w "{path}"').stdout.strip().decode()
    run(f'git update-index --add --cacheinfo 100644,{sha},{path}')
    print(f"  added: {path}")

run(f'git read-tree {BASE}')
for f in ["assets/js/main.js", "assets/css/style.css"]:
    add_to_index(f)

tree = run('git write-tree').stdout.strip().decode()
parent = run(f'git rev-parse {BASE}').stdout.strip().decode()
msg = "about 页面 WHY/SCOPE 改为参考页风格的大编号纯文本列表（去卡片背景、段落清晰）"
commit = run(f'git commit-tree {tree} -p {parent} -m "{msg}"').stdout.strip().decode()
run(f'git update-ref refs/heads/{BRANCH} {commit}')
print(f"local commit: {commit}")
ssh_env = {**os.environ, "GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"}
run(f'git push {REMOTE} {BRANCH} --force', env=ssh_env)
print(f"pushed: {commit}")
