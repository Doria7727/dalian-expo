"""fix13.py - 首页 Hero 文字+布局改版（按用户截图样张）

改动内容：
1. 大标题改为「2027大连国际 / 工业博览会」两行，橙色重音
2. 副标题改为「展会主题：数智引领工业」
3. 添加三列信息条：展览时间 / 展览地点 / 展览规模
4. 顶部 eyebrow 加橙色圆点装饰
5. CTA 按钮改为「申请参展 ->」「了解更多」
6. 配色仍然保持深海军蓝 + 工业橙
"""
import os
import subprocess

REPO = r"C:\Users\ASUS\Desktop\2027大连工博会网站"
os.chdir(REPO)

BASE = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
# f869e60 误删了 main.js / logo-composite.png，回退到上一个有完整文件的提交 3837289
LAST_GOOD = "3837289"
print("HEAD =", BASE, "BASE_USED =", LAST_GOOD)
BASE = LAST_GOOD

def git_show(p):
    return subprocess.run(["git", "show", f"{BASE}:{p}"], capture_output=True).stdout

def write_blob(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    r = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=data, capture_output=True)
    return r.stdout.decode().strip()

def idx_add(p, sha):
    subprocess.run(["git", "update-index", "--add", "--cacheinfo", f"100644,{sha},{p}"], check=True)

# 1. 读取 base 文件
main_js_raw = git_show("assets/js/main.js").decode("utf-8")
css_raw     = git_show("assets/css/style.css").decode("utf-8")

# 2. 改造 main.js：替换 hero-text 块
old_hero_text = """          <div class="hero-text">
            <span class="eyebrow eyebrow-light">${esc(SITE.edition)} · ${esc(SITE.year)}</span>
            <h1>${esc(SITE.theme)}<br><span class="hero-title">${esc(SITE.name)}</span></h1>
            <p class="hero-sub">深耕工业领域近三十载，东北地区标杆级专业工业盛会。2027 年 5 月，相约大连自贸区国际会展中心，共启数智工业新未来。</p>
            <div class="hero-actions">
              <a class="btn btn-primary" href="${navHref('#contact')}">立即参展咨询 →</a>
              <a class="btn btn-light" href="${navHref('#about')}">了解展会</a>
            </div>
          </div>"""

new_hero_text = """          <div class="hero-text">
            <span class="eyebrow eyebrow-light hero-eyebrow"><i class="hero-dot"></i>${esc(SITE.edition)} · 火热招商中</span>
            <h1 class="hero-h1">
              <span class="hero-title-main">2027大连国际</span>
              <span class="hero-title-accent">工业博览会</span>
            </h1>
            <p class="hero-theme">展会主题：${esc(SITE.theme)}</p>
            <div class="hero-info">
              <div class="hero-info-item">
                <span class="hero-info-label">展览时间</span>
                <span class="hero-info-value">${esc(SITE.dateText || '2027年5月12日—15日')}</span>
              </div>
              <div class="hero-info-item">
                <span class="hero-info-label">展览地点</span>
                <span class="hero-info-value">${esc(SITE.venue || '大连自贸区国际会展中心')}</span>
              </div>
              <div class="hero-info-item">
                <span class="hero-info-label">展览规模</span>
                <span class="hero-info-value">${esc(SITE.heroScale || '60,000 平方米')}</span>
              </div>
            </div>
            <div class="hero-actions">
              <a class="btn btn-primary" href="${navHref('#contact')}">申请参展 →</a>
              <a class="btn btn-outline" href="${navHref('#about')}">了解更多</a>
            </div>
          </div>"""

assert old_hero_text in main_js_raw, "hero-text 块未找到"
M = main_js_raw.replace(old_hero_text, new_hero_text)

# 3. CSS 新增
css_additions = """

/* =========================================================
   首页 Hero 新版排版（按 2026-08-27 截图样张）
   ========================================================= */
.hero-text .hero-eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  border-color: rgba(232,84,30,.45);
  background: rgba(232,84,30,.10);
  color: #ffb38a;
}
.hero-text .hero-eyebrow .hero-dot {
  display: inline-block; width: 8px; height: 8px; border-radius: 50%;
  background: var(--c-accent);
  box-shadow: 0 0 0 4px rgba(232,84,30,.18);
  animation: heroDotPulse 1.6s ease-in-out infinite;
}
@keyframes heroDotPulse {
  0%, 100% { box-shadow: 0 0 0 4px rgba(232,84,30,.18); }
  50%      { box-shadow: 0 0 0 7px rgba(232,84,30,.05); }
}
.hero-text .hero-h1 {
  margin: 0 0 12px; font-weight: 800; line-height: 1.05;
}
.hero-text .hero-title-main {
  display: block; font-size: 2.7rem; color: #ffffff; letter-spacing: .01em;
  text-shadow: 0 2px 12px rgba(10,31,61,.35);
}
.hero-text .hero-title-accent {
  display: block; font-size: 3.5rem;
  color: var(--c-accent);
  margin-top: 6px; font-weight: 900; letter-spacing: .04em;
  text-shadow: 0 2px 16px rgba(232,84,30,.32);
  background: linear-gradient(90deg, var(--c-accent) 0%, var(--c-accent-2) 100%);
  -webkit-background-clip: text; background-clip: text;
}
.hero-text .hero-theme {
  font-size: 1.05rem; color: #d5e3f3; margin: 18px 0 26px;
  font-weight: 500; letter-spacing: .02em;
}
.hero-info {
  display: grid; grid-template-columns: repeat(3, auto);
  gap: 38px; margin: 0 0 32px; align-items: start;
}
.hero-info-item { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.hero-info-label {
  font-size: .82rem; color: #8ea7c0; letter-spacing: .04em; font-weight: 500;
}
.hero-info-value {
  font-size: 1.05rem; color: #ffffff; font-weight: 700;
  letter-spacing: .01em; white-space: nowrap;
}

@media (max-width: 900px) {
  .hero-text .hero-title-main { font-size: 2.1rem; }
  .hero-text .hero-title-accent { font-size: 2.8rem; }
  .hero-info { grid-template-columns: repeat(3, 1fr); gap: 14px; }
  .hero-info-value { font-size: .92rem; white-space: normal; }
}
@media (max-width: 600px) {
  .hero-info { grid-template-columns: 1fr; gap: 14px; }
  .hero-text .hero-title-main { font-size: 1.8rem; }
  .hero-text .hero-title-accent { font-size: 2.4rem; }
}
"""

# 锚点：在 .hero-text .hero-sub 之前插入新样式
anchor = ".hero-text .hero-sub {\n  font-size: 1.05rem; color: #cfe0f0; margin: 14px 0 24px; max-width: 520px; line-height: 1.7;\n}"
assert anchor in css_raw, ".hero-text .hero-sub anchor 未找到"
css_new = css_raw.replace(anchor, css_additions + "\n" + anchor)

# 4. git plumbing：commit & push
out = [
    ("assets/js/main.js",    write_blob(M)),
    ("assets/css/style.css", write_blob(css_new)),
]

# 过滤引号包围的残留文件名（旧 bug）
junk = [p for p in out if '"' in p[0]]
if junk:
    print("跳过垃圾:", junk)
out = [t for t in out if t[0] not in junk]

subprocess.run(["git", "read-tree", "--empty"], check=True, cwd=REPO)
for p, sha in out:
    idx_add(p, sha)
    print("+", p, sha[:8])

new_tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
commit = subprocess.run(
    ["git", "commit-tree", new_tree, "-p", BASE, "-m",
     "首页 Hero 改版：标题改双行（2027大连国际 / 工业博览会 橙色重音）+ 展会主题副标题 + 三列信息条（时间/地点/规模）+ 申请参展/了解更多按钮"],
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
print("STDOUT:", push.stdout[-500:])
if push.stderr:
    print("STDERR:", push.stderr[-500:])
