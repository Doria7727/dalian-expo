import os, subprocess
os.chdir(r"C:\Users\ASUS\Desktop\2027大连工博会网站")

# 1. index.html
p = "index.html"
with open(p, "r", encoding="utf-8") as f: s = f.read()
s = s.replace("<title>中国国际工业装备博览会 - 官网首页</title>", "<title>2027大连国际工业博览会</title>")
s = s.replace("中国国际工业装备博览会（CIIE）官方展会信息平台", "2027（第29届）大连国际工业博览会官方信息平台")
with open(p, "w", encoding="utf-8") as f: f.write(s)
print("index.html OK")

# 2. main.js
p = "assets/js/main.js"
with open(p, "r", encoding="utf-8") as f: s = f.read()
old = '<span class="txt"><b>${esc(SITE.name)}</b><span>${esc(SITE.enName)}</span></span>'
new = '<span class="txt"><b>${esc(SITE.shortName)}</b><span>${esc(SITE.enName)}</span></span>\n          <img class="brand-logo" src="assets/img/logo-ief-ufi.png" alt="IEF 中国·大连 · UFI 国际认证" />'
s = s.replace(old, new)
old2 = """      <section class="hero">
        <div class="container hero-inner">
          <div class="hero-top">
            <span class="brand-mark"><span class="num">${esc(SITE.edition)}</span><span class="ed">${esc(SITE.theme || '数智引领工业')}</span></span>
            <img class="hero-logo" src="assets/img/logo-ief-ufi.png" alt="IEF 中国·大连 · UFI 国际认证" />
          </div>
          <h1>${esc(SITE.name)}</h1>"""
new2 = """      <section class="hero">
        <div class="container hero-inner">
          <span class="tag">${esc(SITE.edition)} · ${esc(SITE.year)}</span>
          <h1>${esc(SITE.name)}</h1>"""
s = s.replace(old2, new2)
with open(p, "w", encoding="utf-8") as f: f.write(s)
print("main.js OK")

# 3. style.css
p = "assets/css/style.css"
with open(p, "r", encoding="utf-8") as f: s = f.read()
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
s = s.replace(old_b, new_b)
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
s = s.replace(old_h, new_h)
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
s = s.replace(old_m, new_m)
with open(p, "w", encoding="utf-8") as f: f.write(s)
print("style.css OK")

# 4. git 操作（一体化：rm + add 全部保留文件 + commit + push github）
print("=== git rm hero-bg-real.jpg ===")
r = subprocess.run(["git", "rm", "-q", "assets/img/hero-bg-real.jpg"], capture_output=True, text=True)
print("rc=", r.returncode, r.stdout, r.stderr)

print("=== 检查磁盘文件实际状态 ===")
all_files = [
    "index.html",
    "assets/js/main.js",
    "assets/css/style.css",
    "assets/js/data.json",
    "assets/img/hero-bg.svg",
    "assets/img/logo-ief-ufi.png",
    "assets/vendor/decap-cms.js",
]
for f in all_files:
    print(f"  {f}: exists={os.path.exists(f)}")

print("=== git add（精确指定存在的文件）===")
existing = [f for f in all_files if os.path.exists(f)]
print(f"Adding {len(existing)} files: {existing}")
r = subprocess.run(["git", "add"] + existing, capture_output=True, text=True)
print("rc=", r.returncode, r.stdout, r.stderr)

print("=== git status ===")
r = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
print(r.stdout)

print("=== git commit ===")
r = subprocess.run(["git", "commit", "-q", "-m", "导航栏品牌区精简并加 IEF/UFI 认证 logo；hero 改回 SVG 背景；浏览器 title 改为'2027大连国际工业博览会'"], capture_output=True, text=True)
print("rc=", r.returncode, r.stdout, r.stderr)

print("=== git push github ===")
env = os.environ.copy()
env["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
r = subprocess.run(["git", "push", "github", "main"], capture_output=True, text=True, env=env)
print("STDOUT:", r.stdout)
print("STDERR:", r.stderr)
print("rc=", r.returncode)

print("=== git log ===")
r = subprocess.run(["git", "log", "--oneline", "-3"], capture_output=True, text=True)
print(r.stdout)
