"""展会介绍二级页面：把 nav "展会介绍" 指向 about.html，并完整重写 renderAbout，
内容板块与 aiforce 参考页一致（Hero+4统计 / WHY 6项 / SCOPE 10项 / PRICING 2类 / 往届照片墙 / 参展咨询）。

BASE = 616743c（当前 HEAD）。改了 3 个文件：
  - assets/js/data.json  （NAV[0].href=about.html; 新增 WHY_EXHIBIT / SCOPE_DETAIL / BOOTH_PRICING）
  - assets/js/main.js    （变量声明+解构加 3 个；renderAbout 完整重写）
  - assets/css/style.css （新增 about 二级页样式）
"""
import os, subprocess, sys
from pathlib import Path

REPO = Path(r"C:\Users\ASUS\Desktop\2027大连工博会网站")
BASE = "616743c"
COMMIT_MSG = "展会介绍改成独立二级页面 about.html：内容板块对齐 aiforce 参考页（Hero+4统计/为什么选/展品范围/展位费用/往届回顾/参展咨询）"


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

    print("[2] 覆盖 3 个文件")
    add_file("assets/js/data.json")
    add_file("assets/js/main.js")
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
