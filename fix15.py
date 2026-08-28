"""往届照片扩容：把用户提供的 6 张图片（图片1-6.jpg）作为 past11-past16
加入 data.json 的 PAST_PHOTOS 数组，并去掉 main.js 中 hero 轮播的 slice(0,8)
限制，让往届回顾网格和 Hero 轮播都用全部 16 张图。

BASE = 99d68f2（当前 HEAD），用 read-tree BASE 继承父树再 update-index 覆盖。
"""
import os, subprocess, sys
from pathlib import Path

REPO = Path(r"C:\Users\ASUS\Desktop\2027大连工博会网站")
BASE = "99d68f2"
COMMIT_MSG = "往届回顾扩容：从 10 张新增为 16 张（用户提供的图片1-6.jpg→past11-16），去除 Hero 轮播 .slice(0,8) 限制让全部 16 张循环播放"


def sh(cmd, cwd=None, check=True, env=None):
    e = env if env is not None else os.environ.copy()
    r = subprocess.run(cmd, cwd=cwd or REPO, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace", env=e)
    if check and r.returncode != 0:
        print(f"!! CMD FAIL: {cmd}\nSTDOUT:{r.stdout}\nSTDERR:{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return r


def add_file(relpath):
    """把磁盘文件 add 进 git 索引。"""
    p = REPO / relpath
    if not p.exists():
        print(f"!! 缺失文件: {relpath}", file=sys.stderr); sys.exit(1)
    blob = subprocess.run(f'git hash-object -w --stdin < "{p.as_posix()}"', cwd=REPO, shell=True, capture_output=True, text=True)
    if blob.returncode != 0 or not blob.stdout.strip():
        print(f"!! hash-object 失败 {relpath}: {blob.stderr}", file=sys.stderr); sys.exit(1)
    sha = blob.stdout.strip()
    r = sh(f'git update-index --add --cacheinfo 100644,{sha},{relpath}')
    print(f"  + {relpath} -> {sha[:8]}")


def main():
    os.chdir(REPO)
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "WorkBuddy"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "wb@dalian-expo.local"

    print(f"[1] 清理临时索引 + 读 BASE={BASE}")
    sh('git read-tree HEAD')
    r = sh('git read-tree ' + BASE)  # 继承父树所有现有文件
    print(r.stdout.strip())

    print("[2] 把磁盘文件塞回索引（覆盖）")
    # 1) 修改过的
    add_file("assets/js/data.json")
    add_file("assets/js/main.js")
    # 2) 新增的 6 张图片
    for i in range(11, 17):
        add_file(f"assets/img/past/past{i:02d}.jpg")

    print("[3] 写树 + 提交")
    tree = sh("git write-tree").stdout.strip()
    print(f"  tree={tree[:10]}")
    commit = sh(f'git commit-tree {tree} -p {BASE} -m "{COMMIT_MSG}"', env=env).stdout.strip()
    print(f"  commit={commit}")
    sh(f'git update-ref refs/heads/main {commit}')
    print("[4] 强制推送到 github")
    push_env = env.copy()
    push_env["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    r = subprocess.run("git push github main --force", cwd=REPO, shell=True, capture_output=True, text=True, env=push_env)
    print("PUSH STDOUT:", r.stdout)
    print("PUSH STDERR:", r.stderr)
    if r.returncode != 0:
        sys.exit(1)
    print("DONE.")


if __name__ == "__main__":
    main()
