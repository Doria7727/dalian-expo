import os, sys, subprocess
os.chdir(r"C:\Users\ASUS\Desktop\2027大连工博会网站")

def run(cmd, input=None, check=True):
    r = subprocess.run(cmd, input=input, capture_output=True, text=False if input else True)
    if check and r.returncode != 0:
        sys.stderr.write(f"FAILED: {cmd}\n{r.stderr}\n")
        raise SystemExit(1)
    return r.stdout

def git_show(path, ref="HEAD"):
    r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git show {ref}:{path} failed: {r.stderr.decode('utf-8', 'ignore')}")
    return r.stdout

def write_blob(data: bytes) -> str:
    r = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=data, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"hash-object failed: {r.stderr.decode('utf-8', 'ignore')}")
    return r.stdout.strip().decode()

def idx_add(path, blob, mode="100644"):
    r = subprocess.run(["git", "update-index", "--add", "--cacheinfo", f"{mode},{blob},{path}"], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"update-index add {path}: {r.stderr}")

def idx_rm(path):
    r = subprocess.run(["git", "update-index", "--force-remove", path], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"update-index rm {path}: {r.stderr}")

BASE = "ed0466a"  # 固定基线，避免受当前 HEAD 状态影响

# 0. 先把 index 重置成 BASE 的树，保证基线干净（不依赖工作区磁盘）
subprocess.run(["git", "read-tree", BASE], check=True)

# 1. 修改 index.html
c = git_show("index.html", BASE).decode("utf-8")
c = c.replace("<title>中国国际工业装备博览会 - 官网首页</title>", "<title>2027大连国际工业博览会</title>")
c = c.replace("中国国际工业装备博览会（CIIE）官方展会信息平台", "2027（第29届）大连国际工业博览会官方信息平台")
idx_add("index.html", write_blob(c.encode("utf-8")))
print("OK index.html")

# 2. 修改 main.js
c = git_show("assets/js/main.js", BASE).decode("utf-8")
c = c.replace(
    '<span class="txt"><b>${esc(SITE.name)}</b><span>${esc(SITE.enName)}</span></span>',
    '<span class="txt"><b>${esc(SITE.shortName)}</b><span>${esc(SITE.enName)}</span></span>\n          <img class="brand-logo" src="assets/img/logo-ief-ufi.png" alt="IEF 中国·大连 · UFI 国际认证" />'
)
old_hero = """      <section class="hero">
        <div class="container hero-inner">
          <div class="hero-top">
            <span class="brand-mark"><span class="num">${esc(SITE.edition)}</span><span class="ed">${esc(SITE.theme || '数智引领工业')}</span></span>
            <img class="hero-logo" src="assets/img/logo-ief-ufi.png" alt="IEF 中国·大连 · UFI 国际认证" />
          </div>
          <h1>${esc(SITE.name)}</h1>"""
new_hero = """      <section class="hero">
        <div class="container hero-inner">
          <span class="tag">${esc(SITE.edition)} · ${esc(SITE.year)}</span>
          <h1>${esc(SITE.name)}</h1>"""
assert old_hero in c, "main.js hero block not found"
c = c.replace(old_hero, new_hero)
idx_add("assets/js/main.js", write_blob(c.encode("utf-8")))
print("OK main.js")

# 3. 修改 style.css
c = git_show("assets/css/style.css", BASE).decode("utf-8")
old_b = """.header-inner { display: flex; align-items: center; justify-content: space-between; height: var(--header-h); }
.brand { display: flex; align-items: center; gap: 12px; color: #fff; }
.brand .logo {
  width: 42px; height: 42px; border-radius: 8px; flex: none;
  background: linear-gradient(135deg, var(--c-accent), #ff8a4c);
  display: grid; place-items: center; font-weight: 800; color: #fff; font-size: 1.1rem;
}
.brand .txt { line-height: 1.15; }
.brand .txt b { font-size: 1.05rem; display: block; }
.brand .txt span { font-size: .72rem; letter-spacing: .12em; color: #9fb6cf; text-transform: uppercase; }"""
new_b = """.header-inner { display: flex; align-items: center; justify-content: space-between; gap: 18px; height: var(--header-h); }
.brand { display: flex; align-items: center; gap: 12px; color: #fff; flex: none; min-width: 0; }
.brand .logo {
  width: 42px; height: 42px; border-radius: 8px; flex: none;
  background: linear-gradient(135deg, var(--c-accent), #ff8a4c);
  display: grid; place-items: center; font-weight: 800; color: #fff; font-size: 1.1rem;
}
.brand .txt { line-height: 1.15; }
.brand .txt b { font-size: 1.05rem; display: block; }
.brand .txt span { font-size: .72rem; letter-spacing: .12em; color: #9fb6cf; text-transform: uppercase; }
.brand-logo {
  height: 36px; width: auto; max-width: 180px; margin-left: 4px;
  filter: drop-shadow(0 1px 3px rgba(0,0,0,.35));
  object-fit: contain;
}"""
assert old_b in c, "css brand not found"
c = c.replace(old_b, new_b)

old_h = """/* ---------- Hero ---------- */
.hero {
  position: relative; color: #fff; overflow: hidden;
  background:
    linear-gradient(135deg, rgba(13,43,78,.88) 0%, rgba(20,58,99,.72) 100%),
    url("../img/hero-bg-real.jpg") center/cover no-repeat;
  background-blend-mode: normal;
}
.hero::before {
  content: ""; position: absolute; inset: 0;
  background: radial-gradient(ellipse at center, rgba(0,0,0,0) 30%, rgba(0,0,0,.35) 100%);
  pointer-events: none;
}
.hero-inner { padding: 90px 0 80px; position: relative; z-index: 2; }
.hero-top {
  display: flex; align-items: flex-start; justify-content: space-between; gap: 24px;
  margin-bottom: 28px; flex-wrap: wrap;
}
.hero-top .brand-mark {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 8px 16px; border: 1px solid rgba(255,255,255,.35);
  border-radius: 999px; font-size: .9rem; letter-spacing: .08em;
  background: rgba(255,255,255,.08); backdrop-filter: blur(4px);
}
.hero-top .brand-mark .num {
  font-weight: 800; color: #ffb37a; font-size: 1.1rem;
}
.hero-top .brand-mark .ed { color: #e8f0f8; }
.hero-logo {
  height: 56px; width: auto; max-width: 280px;
  filter: drop-shadow(0 2px 8px rgba(0,0,0,.45));
  object-fit: contain;
}
.hero .tag {
  display: inline-block; padding: 6px 16px; border: 1px solid rgba(255,255,255,.4);
  border-radius: 999px; font-size: .82rem; letter-spacing: .08em; margin-bottom: 18px;
  background: rgba(255,255,255,.10);
  text-shadow: 0 1px 3px rgba(0,0,0,.5);
}
.hero h1 {
  font-size: 3rem; margin-bottom: 14px; color:#fff;
  text-shadow: 0 2px 12px rgba(0,0,0,.65), 0 1px 3px rgba(0,0,0,.5);
}
.hero .sub {
  font-size: 1.25rem; max-width: 640px; color: #f0f6fc; margin-bottom: 26px;
  text-shadow: 0 1px 6px rgba(0,0,0,.6);
}
.hero-meta { display: flex; flex-wrap: wrap; gap: 26px; margin: 26px 0 32px; }
.hero-meta .mi { display: flex; align-items: center; gap: 10px; text-shadow: 0 1px 4px rgba(0,0,0,.55); }
.hero-meta .mi .ic { font-size: 1.5rem; }
.hero-meta .mi b { display: block; font-size: 1.05rem; }
.hero-meta .mi span { font-size: .85rem; color: #d6e4f0; }
.hero-actions { display: flex; gap: 14px; flex-wrap: wrap; }

@media (max-width: 720px) {
  .hero-logo { height: 44px; }
  .hero h1 { font-size: 2rem; }
}"""
new_h = """/* ---------- Hero ---------- */
.hero {
  position: relative; color: #fff; overflow: hidden;
  background:
    linear-gradient(120deg, rgba(13,43,78,.92), rgba(20,58,99,.78)),
    url("../img/hero-bg.svg") center/cover no-repeat;
}
.hero-inner { padding: 90px 0 80px; }
.hero .tag {
  display: inline-block; padding: 6px 16px; border: 1px solid rgba(255,255,255,.4);
  border-radius: 999px; font-size: .82rem; letter-spacing: .08em; margin-bottom: 18px;
  background: rgba(255,255,255,.06);
}
.hero h1 { font-size: 3rem; margin-bottom: 14px; color:#fff; }
.hero .sub { font-size: 1.25rem; max-width: 640px; color: #e8f0f8; margin-bottom: 26px; }
.hero-meta { display: flex; flex-wrap: wrap; gap: 26px; margin: 26px 0 32px; }
.hero-meta .mi { display: flex; align-items: center; gap: 10px; }
.hero-meta .mi .ic { font-size: 1.5rem; }
.hero-meta .mi b { display: block; font-size: 1.05rem; }
.hero-meta .mi span { font-size: .85rem; color: #b9cde0; }
.hero-actions { display: flex; gap: 14px; flex-wrap: wrap; }"""
assert old_h in c, "css hero not found"
c = c.replace(old_h, new_h)

old_m = """  .hero h1 { font-size: 2rem; }
  .hero .sub { font-size: 1.05rem; }
  .hero-inner { padding: 60px 0 56px; }
  .stats { grid-template-columns: repeat(2, 1fr); }
  .grid-2, .grid-3, .grid-4, .news-grid { grid-template-columns: 1fr; }
  .form-grid { grid-template-columns: 1fr; }
  .section { padding: 50px 0; }
  h1 { font-size: 1.8rem; } h2 { font-size: 1.5rem; }
  .footer-grid { grid-template-columns: 1fr; }
  .article { padding: 26px 20px; }
}"""
new_m = """  .hero h1 { font-size: 2rem; }
  .hero .sub { font-size: 1.05rem; }
  .hero-inner { padding: 60px 0 56px; }
  .stats { grid-template-columns: repeat(2, 1fr); }
  .grid-2, .grid-3, .grid-4, .news-grid { grid-template-columns: 1fr; }
  .form-grid { grid-template-columns: 1fr; }
  .section { padding: 50px 0; }
  h1 { font-size: 1.8rem; } h2 { font-size: 1.5rem; }
  .footer-grid { grid-template-columns: 1fr; }
  .article { padding: 26px 20px; }
  .brand-logo { height: 28px; max-width: 140px; }
  .brand .txt b { font-size: .95rem; }
  .brand .txt span { display: none; }
}"""
assert old_m in c, "css media not found"
c = c.replace(old_m, new_m)
idx_add("assets/css/style.css", write_blob(c.encode("utf-8")))
print("OK style.css")

# 4. 添加其他 tracked 文件（从 BASE 直接读 blob）
for path in ["assets/js/data.json", "assets/img/hero-bg.svg", "assets/img/logo-ief-ufi.png", "assets/vendor/decap-cms.js"]:
    idx_add(path, write_blob(git_show(path, BASE)))
    print(f"OK {path}")

# 5. 从索引移除 hero-bg-real.jpg
idx_rm("assets/img/hero-bg-real.jpg")
print("OK removed hero-bg-real.jpg")

# 6. 写 tree + commit
tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
parent = BASE
msg = "导航栏品牌区精简并加 IEF/UFI 认证 logo；hero 改回 SVG 背景；浏览器 title 改为'2027大连国际工业博览会'"
commit = subprocess.run(["git", "commit-tree", tree, "-p", parent, "-m", msg], capture_output=True, text=True).stdout.strip()
print("tree:", tree, "commit:", commit)

# 7. 更新 main ref
subprocess.run(["git", "update-ref", "refs/heads/main", commit], check=True)
print("ref updated")

# 8. 验证 commit 内容
r = subprocess.run(["git", "ls-tree", "-r", commit], capture_output=True, text=True)
print("COMMIT FILES:")
for line in r.stdout.strip().split("\n"):
    if line:
        print(" ", line)

# 8.5 验证：与 HEAD 对比，只允许预期差异（避免误删）
head_files = subprocess.run(["git", "ls-tree", "-r", BASE], capture_output=True, text=True).stdout.strip().split("\n")
head_set = {l.split("\t")[-1] for l in head_files if l}
new_set = {l.split("\t")[-1] for l in r.stdout.strip().split("\n") if l}
removed = head_set - new_set
added = new_set - head_set
print("REMOVED:", removed)
print("ADDED:", added)
assert removed == {"assets/img/hero-bg-real.jpg"}, f"非预期删除: {removed}"
assert added == set(), f"非预期新增: {added}"

# 9. push
env = os.environ.copy()
env["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
r = subprocess.run(["git", "push", "github", "main", "--force"], capture_output=True, text=True, env=env)
print("PUSH STDOUT:", r.stdout)
print("PUSH STDERR:", r.stderr)
print("rc=", r.returncode)
