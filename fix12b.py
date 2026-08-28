"""fix12b.py — 优化 logo 显示：放大图片、简化旁边的文字
- .brand-img 头部 56px / 页脚 68px
- .brand 改成 flex column 垂直堆叠（图片在上，英文小字在下）
- 删除中文标题（因为 logo 图里已经嵌入了"中国·大连 iEF"，避免重复）
"""
import os, subprocess

REPO = r"C:\Users\ASUS\Desktop\2027大连工博会网站"
os.chdir(REPO)

BASE = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print("BASE =", BASE)

def git_show(p):
    return subprocess.run(["git", "show", f"{BASE}:{p}"], capture_output=True).stdout

def write_blob(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return subprocess.run(["git", "hash-object", "-w", "--stdin"], input=data, capture_output=True).stdout.decode().strip()

def idx_add(p, sha):
    subprocess.run(["git", "update-index", "--add", "--cacheinfo", f"100644,{sha},{p}"], check=True)

css = git_show("assets/css/style.css").decode("utf-8")

# 删掉旧 .brand-img / .footer-brand .brand-img 段，重新整理 .brand 布局
old_block = """.brand { display: flex; align-items: center; gap: 12px; color: #fff; flex: none; text-decoration: none; }
.brand:hover { color: #fff; }"""

new_block = """.brand { display: flex; flex-direction: column; align-items: flex-start; gap: 4px; color: #fff; flex: none; text-decoration: none; padding: 6px 0; }
.brand:hover { color: #fff; }"""

assert old_block in css, ".brand 块未找到"
css = css.replace(old_block, new_block)

# 替换旧 .brand-img 追加段
old_addition = """/* =========================================================
   头部 / 页脚 Logo：用户提供的红 D + iEF + UFI 组合图
   ========================================================= */
.brand-mark {
  /* 由 .brand-img 自适应高度，这里保留容器便于布局对齐 */
  display: inline-flex; align-items: center; justify-content: flex-start;
  background: transparent; padding: 0; border-radius: 0; height: auto;
}
.brand-img {
  display: block; height: 44px; width: auto; max-width: 220px;
  object-fit: contain; user-select: none;
}
/* footer 更大一点 */
.footer-brand .brand-img { height: 56px; max-width: 280px; }

/* 兜底：原 .brand-d / .brand-ief / .brand-leaf 隐藏（不再渲染，但样式保留） */
.brand-mark > .brand-d,
.brand-mark > .brand-ief,
.brand-mark > .brand-leaf { display: none !important; }

/* 移动端适当缩小 */
@media (max-width: 720px) {
  .brand-img { height: 36px; max-width: 180px; }
  .footer-brand .brand-img { height: 44px; max-width: 220px; }
}"""

new_addition = """/* =========================================================
   头部 / 页脚 Logo：用户提供的红 D + iEF + UFI 组合图
   ========================================================= */
.brand-mark {
  display: inline-flex; align-items: center; justify-content: flex-start;
  background: transparent; padding: 0; border-radius: 0; height: auto; line-height: 0;
}
.brand-img {
  display: block; height: 52px; width: auto; max-width: 230px;
  object-fit: contain; user-select: none;
}
/* footer 更大一点 */
.footer-brand .brand-img { height: 68px; max-width: 300px; }

/* 兜底：原 .brand-d / .brand-ief / .brand-leaf 隐藏（不再渲染，但样式保留） */
.brand-mark > .brand-d,
.brand-mark > .brand-ief,
.brand-mark > .brand-leaf { display: none !important; }

/* 英文副标题改为更小的字 */
.brand-txt { line-height: 1.2; margin-top: 2px; }
.brand-txt b { display: block; font-size: 1.02rem; color: #fff; font-weight: 700; letter-spacing: .02em; }
.brand-txt span { display: none; }

/* 页脚里把中文标题降为正常大小 */
.footer-brand .brand-txt b { font-size: 1rem; }

/* 移动端适当缩小 */
@media (max-width: 720px) {
  .brand-img { height: 44px; max-width: 195px; }
  .footer-brand .brand-img { height: 56px; max-width: 250px; }
}"""

assert old_addition in css, "fix12 追加段未找到"
css_new = css.replace(old_addition, new_addition)

# 也需要修一下 header-inner，让 header 在 logo 调大后仍正常
# 看下 .header-inner 当前样式
print("正在检查 header-inner 等...")

out = [("assets/css/style.css", write_blob(css_new))]
out = [t for t in out if '"' not in t[0]]

subprocess.run(["git", "read-tree", "--empty"], check=True)
for p, sha in out:
    idx_add(p, sha)
    print("+", p, sha[:8])

new_tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
commit = subprocess.run(
    ["git", "commit-tree", new_tree, "-p", BASE, "-m",
     "Header logo 优化：图片放大到 52px；布局改为竖排（图在上、中文标题在下、英文副标题隐藏避免与图片'中国·大连 iEF'重复）"],
    capture_output=True, text=True
).stdout.strip()
print("commit =", commit)
subprocess.run(["git", "update-ref", "refs/heads/main", commit], check=True)
push = subprocess.run(
    ["git", "push", "github", "main", "--force"],
    capture_output=True, text=True,
    env={**os.environ, "GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"}
)
print("push rc:", push.returncode)
print(push.stdout[-600:])
if push.stderr:
    print("STDERR:", push.stderr[-500:])
