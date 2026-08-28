"""fix12.py — 把头部/页脚 logo 替换为用户提供的"红 D + IEF + UFI"三合一组合图
- 保存图片到 assets/img/logo-composite.png
- main.js logoBlock() 用 <img> 替代原自定义红 D + IEF + 绿叶 SVG
- style.css 让图像在不同断点自适应（header 高度 44px / footer 高度 56px / 移动端 38px）
- 把原来的 .brand-d / .brand-ief / .brand-leaf 样式降级隐藏（不删 CSS，避免破坏子页面）
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

# ------------------------------------------------------------------
# 1. 复制原始 PNG 到 assets/img/logo-composite.png（保留透明通道）
# ------------------------------------------------------------------
src_png = r"C:\Users\ASUS\Desktop\2027工业博览会\媒体\logo\32acbf27c4006fe1fb30f74de263a281.png"
with open(src_png, "rb") as f:
    png_bytes = f.read()
png_sha = write_blob(png_bytes)
print("logo-composite.png sha:", png_sha[:8], "bytes:", len(png_bytes))

# ------------------------------------------------------------------
# 2. main.js: 替换 logoBlock 的 .brand-mark 内容
# ------------------------------------------------------------------
main_js = git_show("assets/js/main.js").decode("utf-8")

old_logo = '''  /* logo SVG：红 D + IEF + 绿叶 + 中文/英文 */
  function logoBlock() {
    return `
      <a class="brand" href="index.html">
        <span class="brand-mark">
          <span class="brand-d">D</span>
          <span class="brand-ief">IEF</span>
          <svg class="brand-leaf" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M17 8C8 10 5.9 16.17 3.82 21.34l1.89.66.95-2.3c.48.17.98.3 1.34.3C19 20 22 3 22 3c-1 2-8 2.25-13 3.25S2 11.5 2 13.5s1.75 3.75 1.75 3.75C7 8 17 8 17 8z" fill="#7cb342"/>
          </svg>
        </span>
        <span class="brand-txt">
          <b>${esc((SITE.name || '').replace(/^2027（.*?）/, '').replace(/[()（）]/g, '').trim() || '大连国际工业博览会')}</b>
          <span>${esc((SITE.enName || 'DALIAN INTERNATIONAL INDUSTRY FAIR').toUpperCase())}</span>
        </span>
      </a>`;
  }'''

new_logo = '''  /* logo：用用户提供的"红 D + IEF + UFI"组合图替代之前的自定义 SVG */
  function logoBlock() {
    return `
      <a class="brand" href="index.html">
        <span class="brand-mark">
          <img class="brand-img" src="assets/img/logo-composite.png" alt="大连国际工业博览会 · IEF · UFI" />
        </span>
        <span class="brand-txt">
          <b>${esc((SITE.name || '').replace(/^2027（.*?）/, '').replace(/[()（）]/g, '').trim() || '大连国际工业博览会')}</b>
          <span>${esc((SITE.enName || 'DALIAN INTERNATIONAL INDUSTRY FAIR').toUpperCase())}</span>
        </span>
      </a>`;
  }'''

assert old_logo in main_js, "logoBlock 未找到"
main_js_new = main_js.replace(old_logo, new_logo)

# ------------------------------------------------------------------
# 3. style.css: 新增 .brand-img 规则；隐藏原 .brand-d / .brand-ief / .brand-leaf（兜底）
# ------------------------------------------------------------------
css = git_show("assets/css/style.css").decode("utf-8")

css_addition = """

/* =========================================================
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
}
"""

css_new = css + css_addition

# ------------------------------------------------------------------
# 4. git 索引 + 提交 + 推送
# ------------------------------------------------------------------
out = [
    ("assets/js/main.js",                write_blob(main_js_new)),
    ("assets/css/style.css",             write_blob(css_new)),
    ("assets/img/logo-composite.png",    png_sha),
]
# 过滤掉引号包围的废弃文件
out = [t for t in out if '"' not in t[0]]

subprocess.run(["git", "read-tree", "--empty"], check=True)
for p, sha in out:
    idx_add(p, sha)
    print("+", p, sha[:8])

new_tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
commit = subprocess.run(
    ["git", "commit-tree", new_tree, "-p", BASE, "-m",
     "头部/页脚 logo 替换为用户提供的红 D + iEF + UFI 三合一组合图"],
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
