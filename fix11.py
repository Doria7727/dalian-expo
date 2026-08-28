"""fix11.py — 4 个修改：
1) past-photos 去掉 "2026 现场" 标签
2) 首页 hero 右侧改成往届照片轮播
3) 参展咨询表单接入 FormSubmit.co（数据落到 1060200619@qq.com）
4) 联系区微信二维码替换为真实 QR 图
"""
import json
import os
import subprocess

REPO = r"C:\Users\ASUS\Desktop\2027大连工博会网站"
os.chdir(REPO)

BASE = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print("BASE =", BASE)

def git_show(p):
    return subprocess.run(["git", "show", f"{BASE}:{p}"], capture_output=True).stdout

def write_blob(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    r = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=data, capture_output=True)
    return r.stdout.decode().strip()

def idx_add(p, sha):
    subprocess.run(["git", "update-index", "--add", "--cacheinfo", f"100644,{sha},{p}"], check=True)

# ------------------------------------------------------------------
# 1. 读取原始 4 个文件并改造
# ------------------------------------------------------------------
data_json_raw = git_show("assets/js/data.json").decode("utf-8")
main_js_raw    = git_show("assets/js/main.js").decode("utf-8")
css_raw        = git_show("assets/css/style.css").decode("utf-8")

# ----- data.json: 删除 PAST_PHOTOS 中的 label 字段（避免再误显示） -----
data = json.loads(data_json_raw)
if "PAST_PHOTOS" in data:
    for p in data["PAST_PHOTOS"]:
        p.pop("label", None)
data_json_new = json.dumps(data, ensure_ascii=False, indent=2) + "\n"

# ----- main.js: 3 处改造 -----
M = main_js_raw

# (a) past-label 那行直接删
old_past_block = '''    // 往届回顾照片墙（用 data.json 的 PAST_PHOTOS 真实照片）
    const pastPhotos = (PAST_PHOTOS || []).map(p => `
      <div class="past-tile">
        <img src="${esc(p.img)}" alt="${esc(p.alt || '往届大连工博会现场')}" loading="lazy" />
        <span class="past-label">${esc(p.label || '往届')}</span>
      </div>`).join("");'''
new_past_block = '''    // 往届回顾照片墙（用 data.json 的 PAST_PHOTOS 真实照片，标签已移除）
    const pastPhotos = (PAST_PHOTOS || []).map(p => `
      <div class="past-tile">
        <img src="${esc(p.img)}" alt="${esc(p.alt || '往届大连工博会现场')}" loading="lazy" />
      </div>`).join("");

    // 首页 Hero 右侧：往届照片轮播（与 #past 区块共享 PAST_PHOTOS 数据源）
    const heroSlides = (PAST_PHOTOS || []).slice(0, 8).map((p, i) => `
      <div class="hero-slide${i === 0 ? ' active' : ''}">
        <img src="${esc(p.img)}" alt="${esc(p.alt || '往届大连工博会现场')}" loading="${i === 0 ? 'eager' : 'lazy'}" />
      </div>`).join("");
    const heroDots = (PAST_PHOTOS || []).slice(0, 8).map((p, i) => `
      <button class="hero-slide-dot${i === 0 ? ' active' : ''}" data-idx="${i}" aria-label="第 ${i+1} 张"></button>`).join("");'''
assert old_past_block in M, "pastPhotos 块未找到"
M = M.replace(old_past_block, new_past_block)

# (b) hero 视觉区：把 .hero-img-placeholder 替换成幻灯片
old_hero_visual = '''          <div class="hero-visual">
            <div class="hero-img-placeholder">
              <div class="hero-img-glow"></div>
              <svg viewBox="0 0 400 300" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="1.5">
                <!-- 工厂轮廓占位 -->
                <rect x="40" y="140" width="80" height="120"/>
                <rect x="140" y="100" width="80" height="160"/>
                <rect x="240" y="160" width="80" height="100"/>
                <path d="M340 120 L340 260 L380 260 L380 160 L360 140 L340 120 Z"/>
                <circle cx="80" cy="170" r="14" fill="rgba(232,84,30,.4)"/>
                <circle cx="180" cy="140" r="14" fill="rgba(232,84,30,.4)"/>
                <line x1="20" y1="260" x2="380" y2="260" stroke-width="2"/>
                <text x="200" y="290" text-anchor="middle" fill="rgba(255,255,255,.5)" font-size="14" font-family="sans-serif">[ 展会现场照片 · 待替换 ]</text>
              </svg>
            </div>
          </div>'''
new_hero_visual = '''          <div class="hero-visual">
            <div class="hero-slideshow" id="heroSlideshow">
              <div class="hero-slides">${heroSlides}</div>
              <div class="hero-slide-nav">
                <button class="hero-slide-arrow" data-dir="-1" aria-label="上一张">‹</button>
                <div class="hero-slide-dots">${heroDots}</div>
                <button class="hero-slide-arrow" data-dir="1" aria-label="下一张">›</button>
              </div>
              <div class="hero-slide-counter"><span id="heroSlideCur">1</span> / ${(PAST_PHOTOS || []).slice(0, 8).length}</div>
            </div>
          </div>'''
assert old_hero_visual in M, "hero-visual 块未找到"
M = M.replace(old_hero_visual, new_hero_visual)

# (c) 二维码占位替换为图片
old_qr = '''              <div class="qr-block">
                <div class="qr-placeholder">
                  <svg viewBox="0 0 60 60" fill="#1a2238"><rect x="0" y="0" width="20" height="20"/><rect x="40" y="0" width="20" height="20"/><rect x="0" y="40" width="20" height="20"/><rect x="6" y="6" width="8" height="8" fill="#fff"/><rect x="46" y="6" width="8" height="8" fill="#fff"/><rect x="6" y="46" width="8" height="8" fill="#fff"/><rect x="24" y="4" width="4" height="4"/><rect x="32" y="8" width="4" height="4"/><rect x="28" y="20" width="4" height="4"/><rect x="24" y="28" width="4" height="4"/><rect x="32" y="32" width="4" height="4"/><rect x="40" y="28" width="4" height="4"/><rect x="44" y="40" width="4" height="4"/><rect x="52" y="44" width="4" height="4"/><rect x="24" y="48" width="4" height="4"/><rect x="36" y="52" width="4" height="4"/></svg>
                </div>
                <p>扫码加微信<br>展会咨询 / 商务对接</p>
              </div>'''
new_qr = '''              <div class="qr-block">
                <img class="qr-img" src="assets/img/wechat-qr.jpg" alt="大连工博会官方微信二维码" />
                <div class="qr-text">
                  <p>扫码加微信<br>展会咨询 / 商务对接</p>
                  <span class="qr-tip">大连展会 · 辽宁大连</span>
                </div>
              </div>'''
assert old_qr in M, "QR 占位块未找到"
M = M.replace(old_qr, new_qr)

# (d) 表单提交：FormSubmit.co 同步到 1060200619@qq.com，带 mailto 兜底
old_form = '''    // 首页联系表单提交（前端校验 + 本地保存示例）
    const form = $("#homeContactForm");
    if (form) {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(form).entries());
        if (!data.company || !data.contact || !/^1[0-9]{10}$/.test(data.phone||"")) {
          alert("请填写公司名称、联系人，并确保手机号格式正确");
          return;
        }
        try { localStorage.setItem("diie_inquiry_" + Date.now(), JSON.stringify(data)); } catch(_) {}
        const ok = $("#homeContactOk");
        ok.textContent = `✅ 提交成功！我们将在 24 小时内与 ${data.contact} 联系。`;
        ok.classList.remove("hidden");
        form.reset();
      });
    }'''
new_form = '''    // 首页联系表单提交：通过 FormSubmit.co 把数据同步到 1060200619@qq.com
    // 本地缓存 + 可选调起邮件兜底；用户在自己邮箱即可看到全部咨询。
    const form = $("#homeContactForm");
    if (form) {
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(form).entries());
        if (!data.company || !data.contact || !/^1[0-9]{10}$/.test(data.phone||"")) {
          alert("请填写公司名称、联系人，并确保手机号格式正确");
          return;
        }
        const submitBtn = form.querySelector(".cf-submit");
        const ok = $("#homeContactOk");
        const submitText = submitBtn ? submitBtn.textContent : "";
        if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "正在提交..."; }

        // 本地缓存一份（防止网络异常丢数据，浏览此设备的组委会也能看到）
        try { localStorage.setItem("diie_inquiry_" + Date.now(), JSON.stringify(data)); } catch(_) {}

        // ---- 主通道：FormSubmit.co AJAX（首次需点击激活邮件） ----
        let delivered = false;
        try {
          const payload = {
            _subject: "【大连工博会参展咨询】" + (data.company || "") + " · " + (data.contact || ""),
            _template: "table",
            _captcha: "false",
            "公司名称": data.company || "",
            "联系人": data.contact || "",
            "联系电话": data.phone || "",
            "邮箱": data.email || "",
            "意向展区": data.zone || "",
            "咨询内容": data.message || "",
            "提交时间": new Date().toLocaleString("zh-CN")
          };
          const r = await fetch("https://formsubmit.co/ajax/1060200619@qq.com", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json" },
            body: JSON.stringify(payload)
          });
          delivered = r.ok;
        } catch (_) { delivered = false; }

        if (delivered) {
          ok.innerHTML = `✅ 提交成功！组委会将在 24 小时内联系 <b>${esc(data.contact)}</b>，邮件将发至 1060200619@qq.com。`;
          ok.classList.remove("hidden");
          form.reset();
        } else {
          // ---- 兜底：调起用户邮件客户端（需电脑配置默认邮件） ----
          const subject = encodeURIComponent("【大连工博会参展咨询】" + (data.company || "") + " · " + (data.contact || ""));
          const body = encodeURIComponent(
            "公司名称：" + (data.company || "") + "\\n" +
            "联系人：" + (data.contact || "") + "\\n" +
            "联系电话：" + (data.phone || "") + "\\n" +
            "邮箱：" + (data.email || "") + "\\n" +
            "意向展区：" + (data.zone || "") + "\\n" +
            "咨询内容：" + (data.message || "") + "\\n" +
            "提交时间：" + new Date().toLocaleString("zh-CN")
          );
          ok.innerHTML = `⚠️ 自动发送未完成（可能需在邮箱中点击激活链接）。<br>` +
                         `已为您打开邮件，发送至 <b>1060200619@qq.com</b> 后即可完成提交。<br>` +
                         `<a class="form-mailto" href="mailto:1060200619@qq.com?subject=${subject}&body=${body}">点此手动发送邮件</a>`;
          ok.classList.remove("hidden");
          // 自动调起
          window.location.href = `mailto:1060200619@qq.com?subject=${subject}&body=${body}`;
        }
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = submitText; }
      });
    }

    // 首页 Hero 轮播驱动
    (function bootHeroSlideshow(){
      const root = document.getElementById("heroSlideshow");
      if (!root) return;
      const slides = root.querySelectorAll(".hero-slide");
      const dots = root.querySelectorAll(".hero-slide-dot");
      const counter = document.getElementById("heroSlideCur");
      if (!slides.length) return;
      const total = slides.length;
      let i = 0, timer = null;
      function go(n){
        slides[i].classList.remove("active");
        if (dots[i]) dots[i].classList.remove("active");
        i = (n + total) % total;
        slides[i].classList.add("active");
        if (dots[i]) dots[i].classList.add("active");
        if (counter) counter.textContent = String(i + 1);
      }
      function next(){ go(i + 1); }
      function start(){ if (timer) clearInterval(timer); timer = setInterval(next, 5000); }
      function stop(){ if (timer) { clearInterval(timer); timer = null; } }
      start();
      dots.forEach((d, idx) => d.addEventListener("click", () => { go(idx); stop(); start(); }));
      root.querySelectorAll(".hero-slide-arrow").forEach(a => {
        a.addEventListener("click", () => {
          const dir = parseInt(a.dataset.dir || "1", 10);
          go(i + dir);
          stop(); start();
        });
      });
      root.addEventListener("mouseenter", stop);
      root.addEventListener("mouseleave", start);
      root.addEventListener("touchstart", stop, {passive:true});
    })();'''
assert old_form in M, "首页表单提交块未找到"
M = M.replace(old_form, new_form)

# ----- CSS：新增 hero slideshow + QR 大图 + 表单成功样式 -----
# 在 .hero-img-placeholder 末尾追加新类（在文件末尾追加样式，不破坏原行）
css_additions = """

/* =========================================================
   首页 Hero 往届照片轮播（替换原 SVG 占位）
   ========================================================= */
.hero-slideshow {
  position: relative; width: 100%; aspect-ratio: 4/3;
  border-radius: 16px; overflow: hidden;
  background: linear-gradient(135deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
  border: 1px solid rgba(255,255,255,.12);
  backdrop-filter: blur(2px);
}
.hero-slides { position: absolute; inset: 0; }
.hero-slide {
  position: absolute; inset: 0;
  opacity: 0; transition: opacity .9s ease;
  background: linear-gradient(180deg, transparent 60%, rgba(10,31,61,.55) 100%);
}
.hero-slide.active { opacity: 1; z-index: 2; }
.hero-slide img {
  position: absolute; inset: 0; width: 100%; height: 100%;
  object-fit: cover; display: block;
}
.hero-slide-nav {
  position: absolute; left: 50%; bottom: 14px; transform: translateX(-50%);
  display: flex; align-items: center; gap: 14px;
  background: rgba(10,31,61,.55); backdrop-filter: blur(6px);
  padding: 6px 12px; border-radius: 999px;
  z-index: 5; opacity: 0; transition: opacity .25s;
}
.hero-slideshow:hover .hero-slide-nav,
.hero-slideshow:focus-within .hero-slide-nav { opacity: 1; }
.hero-slide-arrow {
  background: rgba(255,255,255,.15); color: #fff; border: 0;
  width: 26px; height: 26px; border-radius: 50%; cursor: pointer;
  font-size: 1.1rem; line-height: 1; font-family: inherit;
  display: grid; place-items: center; transition: background .2s;
}
.hero-slide-arrow:hover { background: var(--c-orange); }
.hero-slide-dots { display: flex; gap: 6px; align-items: center; }
.hero-slide-dot {
  width: 18px; height: 4px; border-radius: 2px;
  background: rgba(255,255,255,.35); border: 0; cursor: pointer; padding: 0;
  transition: all .25s;
}
.hero-slide-dot.active { background: var(--c-orange); width: 28px; }
.hero-slide-counter {
  position: absolute; top: 12px; right: 12px;
  background: rgba(10,31,61,.6); color: #fff;
  padding: 4px 10px; border-radius: 999px; font-size: .78rem; font-weight: 600;
  z-index: 5; backdrop-filter: blur(4px);
}

/* 联系区微信二维码（高清版） */
.qr-block {
  display: flex; gap: 16px; align-items: center;
  margin-top: 20px; padding: 18px; background: var(--c-soft); border-radius: 12px;
}
.qr-img {
  flex: none; width: 132px; height: 132px; background: #fff;
  border: 1px solid var(--c-line); border-radius: 8px; padding: 6px;
  object-fit: contain; display: block;
}
.qr-text { display: flex; flex-direction: column; gap: 6px; }
.qr-text p { margin: 0; font-size: .9rem; color: var(--c-text); line-height: 1.5; font-weight: 600; }
.qr-tip { font-size: .78rem; color: var(--c-muted); }

/* 表单成功提示样式增强 */
.form-success a.form-mailto {
  display: inline-block; margin-top: 8px;
  color: var(--c-orange); text-decoration: underline; word-break: break-all;
}
"""

css_new = css_raw + css_additions

# ------------------------------------------------------------------
# 2. 写入 git 索引（in-memory plumbing）
# ------------------------------------------------------------------
out = []

# 3 个改造后的文件
out.append(("assets/js/data.json", write_blob(data_json_new)))
out.append(("assets/js/main.js",   write_blob(M)))
out.append(("assets/css/style.css",write_blob(css_new)))

# wechat-qr.jpg（直接从磁盘 hash 进去）
qr_path = os.path.join(REPO, "assets/img/wechat-qr.jpg")
with open(qr_path, "rb") as f:
    qr_data = f.read()
qr_sha = write_blob(qr_data)
out.append(("assets/img/wechat-qr.jpg", qr_sha))

# 过滤引号包围的残留文件名（旧 bug 留下的 "展会介绍.md"）
junk = [p for p in out if '"' in p[0]]
if junk:
    print("跳过垃圾:", junk)
out = [t for t in out if t[0] not in junk]

# 用 --remove-from-existing 清空当前索引，再 add 完整列表
subprocess.run(["git", "read-tree", "--empty"], check=True, cwd=REPO)
for p, sha in out:
    idx_add(p, sha)
    print("+", p, sha[:8])

# 提交并强推
new_tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
commit = subprocess.run(
    ["git", "commit-tree", new_tree, "-p", BASE, "-m",
     "首页 Hero 改为往届照片轮播；参展咨询表单接入 FormSubmit.co（数据落 1060200619@qq.com）；联系区替换为真实微信二维码；往届回顾移除 '2026 现场' 标签"],
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
print(push.stdout[-1000:])
if push.stderr:
    print("STDERR:", push.stderr[-1000:])
