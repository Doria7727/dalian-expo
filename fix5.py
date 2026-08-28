#!/usr/bin/env python3
# fix5.py - 完整重构方案：基于内存 git 对象构建提交
# 改动：assets/js/main.js（重写）, assets/css/style.css（重写）, assets/js/data.json（NAV 改 6 锚点）
# BASE = 3c3cae0（当前 GitHub HEAD），保留所有其他文件
import os, sys, subprocess

BASE = "3c3cae03047aba8d7261b20c500cdb853c0fe30b"
REPO = "C:/Users/ASUS/Desktop/2027大连工博会网站"
os.chdir(REPO)

# 1. 把 index 重置成 BASE 的树（保证基线干净，不依赖工作区）
r = subprocess.run(["git", "read-tree", BASE], capture_output=True, text=True)
if r.returncode != 0:
    print("FAIL read-tree:", r.stderr); sys.exit(1)
print("OK read-tree BASE")

# 2. 从 git 对象读 BASE 中的文件作为参考
def git_show(path, commit=BASE):
    r = subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"show {commit}:{path}: {r.stderr.decode('utf-8','ignore')}")
    return r.stdout

def write_blob(data):
    r = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=data, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"hash-object: {r.stderr.decode('utf-8','ignore')}")
    return r.stdout.decode("utf-8").strip()

def idx_add(path, blob):
    r = subprocess.run(["git", "update-index", "--add", "--cacheinfo",
                        f"100644,{blob},{path}"], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"add {path}: {r.stderr}")

def idx_rm(path):
    r = subprocess.run(["git", "update-index", "--force-remove", path], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"rm {path}: {r.stderr}")

# 3. 读取本地新文件
NEW_FILES = ["assets/js/main.js", "assets/css/style.css", "assets/js/data.json"]
for f in NEW_FILES:
    if not os.path.exists(f):
        print(f"FAIL 磁盘上找不到 {f}"); sys.exit(1)
    size = os.path.getsize(f)
    print(f"OK disk {f} ({size} bytes)")

# 4. 为每个新文件创建 blob 并加入 index
for f in NEW_FILES:
    with open(f, "rb") as fp:
        blob = write_blob(fp.read())
    idx_add(f, blob)
    print(f"OK staged {f} -> {blob[:10]}")

# 5. 写树
tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
print(f"OK tree {tree}")
if not tree:
    print("FAIL empty tree"); sys.exit(1)

# 6. 前置校验：对比 BASE 树和新树，期望只有那 3 个文件变化
def list_tree(commit):
    r = subprocess.run(["git", "ls-tree", "-r", commit], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ls-tree {commit}: {r.stderr}")
    return {line.split("\t",1)[1]: line.split(" ",2)[2].split("\t",1)[0] for line in r.stdout.strip().split("\n") if line}

base_files = list_tree(BASE)
new_files = list_tree(tree)
assert set(base_files.keys()) == set(new_files.keys()), \
    f"file set mismatch!\n  only in base: {set(base_files)-set(new_files)}\n  only in new:  {set(new_files)-set(base_files)}"
print(f"OK file set unchanged ({len(new_files)} files)")

# 改动列表
changed = [f for f in base_files if base_files[f] != new_files[f]]
print(f"OK changed files: {sorted(changed)}")
expected = set(NEW_FILES)
actual = set(changed)
if actual != expected:
    print(f"FAIL unexpected changes! actual={actual} expected={expected}"); sys.exit(1)
print("OK only the 3 intended files changed")

# 7. 创建 commit
parent = subprocess.run(["git", "rev-parse", BASE], capture_output=True, text=True).stdout.strip()
msg = "Redesign site per aiforce reference: single-page with anchor nav, split hero, 10 scope cards, 2-card contact, new D+IEF+leaf logo"
r = subprocess.run(["git", "commit-tree", tree, "-p", parent, "-m", msg], capture_output=True, text=True)
if r.returncode != 0:
    print("FAIL commit-tree:", r.stderr); sys.exit(1)
new_commit = r.stdout.strip()
print(f"OK new commit {new_commit}")

# 8. 更新 main 分支
r = subprocess.run(["git", "update-ref", "refs/heads/main", new_commit], capture_output=True, text=True)
if r.returncode != 0:
    print("FAIL update-ref:", r.stderr); sys.exit(1)
print(f"OK local main -> {new_commit}")

# 9. 推送到 GitHub
env = os.environ.copy()
env["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
r = subprocess.run(["git", "push", "github", "main", "--force"], capture_output=True, text=True, env=env)
if r.returncode != 0:
    print("FAIL push:", r.stderr); sys.exit(1)
print("OK push:", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "")
print(f"DONE -> {new_commit}")
