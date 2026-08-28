"""往届回顾网格改 5 列 → 4 列，让 16 张图排成整齐的 4×4 方阵。

BASE = 4b2cd6a（当前 HEAD）。只改了 assets/css/style.css 一行：
  .past-grid { ... repeat(5, 1fr) ... }  →  repeat(4, 1fr)

用 read-tree BASE 继承父树再 update-index 覆盖，避免破树。
"""
import os, subprocess, sys
from pathlib import Path

REPO = Path(r"C:\Users\ASUS\Desktop\2027大连工博会网站")
BASE = "4b2cd6a"
COMMIT_MSG = "往届回顾网格改 5 列→4 列，16 张图排成整齐的 4×4 方阵"


def sh(cmd, cwd=None, check=True, env=None):
    e = env if env is not None else os.environ.copy()
    r = subprocess.run(cmd, cwd=cwd or REPO, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace", env=e)
    if check and r.returncode != 0:
        print(f"!! CMD FAIL: {cmd}\nSTDOUT:{r.stdout}\nSTDERR:{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return r


def add_file(relpath):
    p = REPO / relpath
    if not p.exists():
        print(f"!! 缺失文件: {relpath}", file=sys.stderr); sys.exit(1)
    blob = subprocess.run(f'git hash-object -w --stdin < "{p.as_posix()}"', cwd=REPO, shell=True, capture_output=True, text=True)
    if blob.returncode != 0 or not blob.stdout.strip():
        print(f"!! hash-object 失败 {relpath}: {blob.stderr}", file=sys.stderr); sys.exit(1)
    sha = blob.stdout.strip()
    sh(f'git update-index --add --cacheinfo 100644,{sha},{relpath}')
    print(f"  + {relpath} -> {sha[:8]}")


def main():
    os.chdir(REPO)
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "WorkBuddy"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "wb@dalian-expo.local"

    print(f"[1] read-tree BASE={BASE}")
    sh("git read-tree HEAD")
    sh("git read-tree " + BASE)

    print("[2] 覆盖 style.css")
    add_file("assets/css/style.css")

    print("[3] write-tree + commit-tree")
    tree = sh("git write-tree").stdout.strip()
    print(f"  tree={tree[:10]}")
    commit = sh(f'git commit-tree {tree} -p {BASE} -m "{COMMIT_MSG}"', env=env).stdout.strip()
    print(f"  commit={commit}")
    sh(f"git update-ref refs/heads/main {commit}")

    print("[4] push github --force")
    pe = env.copy()
    pe["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    r = subprocess.run("git push github main --force", cwd=REPO, shell=True, capture_output=True, text=True, env=pe)
    print("PUSH STDOUT:", r.stdout)
    print("PUSH STDERR:", r.stderr)
    if r.returncode != 0:
        sys.exit(1)
    print("DONE.")


if __name__ == "__main__":
    main()
