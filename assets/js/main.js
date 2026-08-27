/* =========================================================
   通用脚本：头部/底部注入、锚点导航、各页面数据渲染
   数据：assets/js/data.json（异步加载）
   2027-08-26 全面重构：参考 aiforce 参考站重构为深蓝+橙单页设计
   ========================================================= */
(function () {
  "use strict";

  let SITE, NAV, ABOUT, EXHIBIT_SCOPE, EXHIBITORS, NEWS, SCHEDULE, TRANSPORT, HOTELS, APPLY_INFO, PAST_PHOTOS, WHY_EXHIBIT, SCOPE_DETAIL, BOOTH_PRICING;

  const $ = (s, ctx = document) => ctx.querySelector(s);
  const $$ = (s, ctx = document) => Array.from(ctx.querySelectorAll(s));
  const esc = (str) => String(str == null ? "" : str)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
  const fmtDate = (d) => {
    const dt = new Date(d);
    if (isNaN(dt)) return d;
    return `${dt.getFullYear()}-${String(dt.getMonth() + 1).padStart(2, "0")}-${String(dt.getDate()).padStart(2, "0")}`;
  };

  /* 当前是否在首页（用于锚点导航的智能前缀） */
  const isHome = () => {
    const p = location.pathname;
    return p.endsWith("/") || p.endsWith("/index.html") || /\/index\.html?$/i.test(p) || p === "" || p === "/";
  };

  /* href 处理：首页用纯锚点，子页面加 index.html 前缀 */
  const navHref = (href) => {
    if (href && href.startsWith("#")) {
      return isHome() ? href : "index.html" + href;
    }
    return href;
  };

  /* logo SVG：红 D + IEF + 绿叶 + 中文/英文 */
  function logoBlock() {
    return `
      <a class="brand" href="index.html">
        <img class="brand-img" src="assets/img/logo-composite.png" alt="大连国际工业博览会 · 中国大连 iEF · UFI 认证" />
        <span class="brand-txt">
          <b>${esc((SITE.name || '').replace(/^2027（.*?）/, '').replace(/[()（）]/g, '').trim() || '大连国际工业博览会')}</b>
          <span>${esc((SITE.enName || 'DALIAN INTERNATIONAL INDUSTRY FAIR').toUpperCase())}</span>
        </span>
      </a>`;
  }

  /* ---------- 注入头部 ---------- */
  function buildHeader() {
    const cur = document.body.getAttribute("data-page") || "";
    const navLinks = NAV.map(n => {
      const href = navHref(n.href);
      const isActive = isHome() && n.href === "#about" ? "" :
                       (n.page === cur ? "active" : "");
      return `<a href="${esc(href)}" class="${isActive}">${esc(n.label)}</a>`;
    }).join("");
    const html = `
      <div class="header-inner container">
        ${logoBlock()}
        <button class="nav-toggle" aria-label="菜单" id="navToggle">☰</button>
        <nav class="nav" id="nav">
          ${navLinks}
        </nav>
        <a class="nav-cta" href="${navHref('#contact')}">参展咨询</a>
      </div>`;
    const headerEl = $("#site-header");
    if (headerEl) headerEl.innerHTML = html;

    const t = $("#navToggle");
    if (t) t.addEventListener("click", () => $("#nav").classList.toggle("open"));
    $$("#nav a").forEach(a => a.addEventListener("click", () => {
      const nav = $("#nav"); if (nav) nav.classList.remove("open");
    }));
  }

  /* ---------- 注入底部 ---------- */
  function buildFooter() {
    const c = SITE.contact;
    const quick = NAV.map(n => `<a href="${esc(navHref(n.href))}">${esc(n.label)}</a>`).join("");
    $("#site-footer").innerHTML = `
      <div class="container">
        <div class="footer-cols">
          <div class="footer-brand">
            <img class="brand-img footer-logo-img" src="assets/img/logo-composite.png" alt="大连国际工业博览会 · 中国大连 iEF · UFI 认证" />
            <p class="footer-tagline">数智引领工业 · 大连国际工业博览会</p>
            <p class="footer-meta">${esc(SITE.edition)} · ${esc(SITE.year)}<br>${esc(SITE.dateText)}<br>${esc(SITE.venue)}</p>
          </div>
          <div class="footer-col">
            <h4>快速导航</h4>
            ${quick}
            <a href="apply.html">参展报名</a>
          </div>
          <div class="footer-col">
            <h4>参展服务</h4>
            <a href="brands.html">参展品牌</a>
            <a href="schedule.html">日程安排</a>
            <a href="travel.html">交通与酒店</a>
            <a href="news.html">新闻动态</a>
          </div>
          <div class="footer-col">
            <h4>联系我们</h4>
            <p>联系人：${esc(c.person || '')}${c.personTitle ? `（${esc(c.personTitle)}）` : ''}</p>
            <p>电话：${esc(c.phone)}</p>
            <p>邮箱：${esc(c.email)}</p>
            <p>微信：${esc(c.wechat)}</p>
            <p>${esc(c.address)}</p>
          </div>
        </div>
        <div class="footer-bottom">
          © ${SITE.year} ${esc(SITE.name)} 版权所有 · 主办：${esc(SITE.organizer)}
        </div>
      </div>`;
  }

  /* =========================================================
     首页（单页，锚点 section 渲染）
     ========================================================= */
  function renderHome() {
    const c = SITE.contact;
    const stats = SITE.stats.map(s => `<div class="stat-tile"><b>${esc(s.num)}</b><span>${esc(s.label)}</span></div>`).join("");

    // 展会亮点 6 项（数据来自 ABOUT.highlights 4 项 + 2 项补充，保证 6 项）
    const baseHl = ABOUT.highlights || [];
    const hl6 = [
      baseHl[0],
      baseHl[1],
      baseHl[2],
      baseHl[3],
      { ic: "📣", title: "全域立体化宣传矩阵", desc: "抖音、微信、央视、人民网等全媒体持续投放，参展企业免费享官方公众号推文与现场专访。" },
      { ic: "🤝", title: "20+ 场同期论坛与供需对接", desc: "高端论坛、技术峰会、轴承专区供需对接专场，搭建产学研商交流桥梁，精准匹配上下游资源。" }
    ].filter(Boolean);

    // 展品范围 10 项（带编号）
    const scopeCards = EXHIBIT_SCOPE.map((g, i) => {
      const n = String(i + 1).padStart(2, "0");
      const items = (g.items || []).slice(0, 5).map(it => `<span class="scope-tag">${esc(it.text)}</span>`).join("");
      const more = (g.items || []).length > 5 ? `<span class="scope-more">+${(g.items||[]).length - 5}</span>` : "";
      return `
        <div class="scope-card">
          <div class="scope-num">${n}</div>
          <h3>${esc(g.group)}</h3>
          <div class="scope-tags">${items}${more}</div>
        </div>`;
    }).join("");

    // 往届回顾照片墙（用 data.json 的 PAST_PHOTOS 真实照片，标签已移除）
    const pastPhotos = (PAST_PHOTOS || []).map(p => `
      <div class="past-tile">
        <img src="${esc(p.img)}" alt="${esc(p.alt || '往届大连工博会现场')}" loading="lazy" />
      </div>`).join("");

    // 首页 Hero 右侧：往届照片轮播（与 #past 区块共享 PAST_PHOTOS 数据源，全部 16 张循环播放）
    const heroSlides = (PAST_PHOTOS || []).map((p, i) => `
      <div class="hero-slide${i === 0 ? ' active' : ''}">
        <img src="${esc(p.img)}" alt="${esc(p.alt || '往届大连工博会现场')}" loading="${i === 0 ? 'eager' : 'lazy'}" />
      </div>`).join("");
    const heroDots = (PAST_PHOTOS || []).map((p, i) => `
      <button class="hero-slide-dot${i === 0 ? ' active' : ''}" data-idx="${i}" aria-label="第 ${i+1} 张"></button>`).join("");

    $("#page-content").innerHTML = `
      <!-- HERO（左右分屏） -->
      <section class="hero-split" id="home">
        <div class="container hero-split-inner">
          <div class="hero-text">
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
              <a class="btn btn-outline" href="about.html">了解更多</a>
            </div>
          </div>
          <div class="hero-visual">
            <div class="hero-slideshow" id="heroSlideshow">
              <div class="hero-slides">${heroSlides}</div>
              <div class="hero-slide-nav">
                <button class="hero-slide-arrow" data-dir="-1" aria-label="上一张">‹</button>
                <div class="hero-slide-dots">${heroDots}</div>
                <button class="hero-slide-arrow" data-dir="1" aria-label="下一张">›</button>
              </div>
              <div class="hero-slide-counter"><span id="heroSlideCur">1</span> / ${(PAST_PHOTOS || []).length}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 数字条 -->
      <section class="stats-strip">
        <div class="container stats-strip-inner">
          ${SITE.stats.slice(0,4).map(s => `<div class="stat-tile"><b>${esc(s.num)}</b><span>${esc(s.label)}</span></div>`).join("")}
        </div>
      </section>

      <!-- 关于展会 -->
      <section class="block" id="about">
        <div class="container">
          <div class="section-head">
            <span class="eyebrow">ABOUT DIIE</span>
            <h2>关于大连工博会</h2>
            <p>${esc(ABOUT.intro.slice(0, 80))}…</p>
          </div>
          <div class="grid grid-3 hl-grid">
            ${hl6.map(h => `<div class="card"><div class="ic">${esc(h.ic)}</div><h3>${esc(h.title)}</h3><p>${esc(h.desc)}</p></div>`).join("")}
          </div>
          <div class="center" style="margin-top:36px;">
            <a class="btn btn-ghost" href="about.html">查看完整展会介绍 →</a>
          </div>
        </div>
      </section>

      <!-- 展品范围 -->
      <section class="block" id="scope">
        <div class="container">
          <div class="section-head">
            <span class="eyebrow">EXHIBITION SCOPE</span>
            <h2>十大主题展区</h2>
            <p>覆盖工业制造全产业链，打造东北亚工业前沿技术交流与商贸对接核心载体</p>
          </div>
          <div class="scope-grid">${scopeCards}</div>
        </div>
      </section>

      <!-- 展位费用 -->
      <section class="block block-alt" id="pricing">
        <div class="container">
          <div class="section-head">
            <span class="eyebrow">BOOTH PRICING</span>
            <h2>展位费用</h2>
            <p>灵活的展位方案，满足不同规模企业的参展需求</p>
          </div>
          <div class="pricing-grid">
            <div class="price-card price-card-light">
              <span class="price-tag">STANDARD BOOTH</span>
              <h3>标准展位</h3>
              <div class="price-line"><b>国内企业（3m×3m）</b><span class="price-num">8,000 <i>元/个</i></span></div>
              <div class="price-line"><b>国外企业（3m×3m）</b><span class="price-num">3,000 <i>美元/个</i></span></div>
              <p class="price-note">配备：展板、加高楣板、80 方柱型材、一张洽谈桌、两把折叠椅、地毯、两只射灯及一个 5A 电源插座（仅限于 300W 以内小功率视听设备使用）。主通道两侧展位加收 20%。</p>
            </div>
            <div class="price-card price-card-dark">
              <span class="price-tag">RAW SPACE</span>
              <h3>室内光地</h3>
              <div class="price-line"><b>国内企业</b><span class="price-num">800 <i>元/㎡</i></span></div>
              <div class="price-line"><b>国外企业</b><span class="price-num">300 <i>美元/㎡</i></span></div>
              <p class="price-note">室内光地不少于 36 平方米，主通道两侧展位加价 20%。展台特别装修，特装管理费由参展商自理，适合品牌特装展示，自由设计搭建。</p>
              <a class="btn btn-primary" href="apply.html">立即申请展位 →</a>
            </div>
          </div>
        </div>
      </section>

      <!-- 往届回顾 -->
      <section class="block" id="past">
        <div class="container">
          <div class="section-head">
            <span class="eyebrow">PAST EDITIONS</span>
            <h2>往届回顾</h2>
            <p>历届展会盛况，记录每一届的精彩瞬间与商贸成果</p>
          </div>
          <div class="past-grid">${pastPhotos}</div>
        </div>
      </section>

      <!-- 联系组委会 -->
      <section class="block block-alt" id="contact">
        <div class="container">
          <div class="section-head">
            <span class="eyebrow">CONTACT US</span>
            <h2>联系组委会</h2>
            <p>展位详情、参展政策、专区合作方案均可联系组委会咨询，抢抓东北市场先机</p>
          </div>
          <div class="contact-grid">
            <!-- 左：联系方式 -->
            <div class="contact-info">
              <h3>组委会联系方式</h3>
              <div class="ci-list">
                <div class="ci-row">
                  <div class="ci-ic">📞</div>
                  <div class="ci-body">
                    <span>联系人 / 电话（微信同号）</span>
                    <b>${esc(c.person || '李玥')} | ${esc(c.phone)}</b>
                  </div>
                </div>
                <div class="ci-row">
                  <div class="ci-ic">✉️</div>
                  <div class="ci-body">
                    <span>电子邮箱</span>
                    <b>${esc(c.email)}</b>
                  </div>
                </div>
                <div class="ci-row">
                  <div class="ci-ic">🏢</div>
                  <div class="ci-body">
                    <span>办公地址</span>
                    <b>${esc(c.address)}</b>
                  </div>
                </div>
                <div class="ci-row">
                  <div class="ci-ic">📅</div>
                  <div class="ci-body">
                    <span>展会时间 / 地点</span>
                    <b>${esc(SITE.dateText)} · ${esc(SITE.venue)}</b>
                  </div>
                </div>
              </div>
              <div class="qr-block">
                <img class="qr-img" src="assets/img/wechat-qr.jpg" alt="大连工博会官方微信二维码" />
                <div class="qr-text">
                  <p>扫码加微信<br>展会咨询 / 商务对接</p>
                  <span class="qr-tip">大连展会 · 辽宁大连</span>
                </div>
              </div>
            </div>
            <!-- 右：参展咨询表单 -->
            <div class="contact-form-card">
              <h3>参展咨询</h3>
              <p class="form-lead">填写以下信息，组委会将在 24 小时内与您联系</p>
              <form id="homeContactForm" novalidate>
                <div class="cf-row">
                  <div class="cf-field"><label>公司名称 <span class="req">*</span></label><input name="company" required placeholder="请输入公司名称"></div>
                  <div class="cf-field"><label>联系人 <span class="req">*</span></label><input name="contact" required placeholder="您的姓名"></div>
                </div>
                <div class="cf-row">
                  <div class="cf-field"><label>联系电话 <span class="req">*</span></label><input name="phone" required placeholder="11 位手机号"></div>
                  <div class="cf-field"><label>邮箱</label><input name="email" type="email" placeholder="可选"></div>
                </div>
                <div class="cf-field"><label>意向展区</label>
                  <select name="zone">
                    <option value="">请选择（可选）</option>
                    ${EXHIBIT_SCOPE.map(g => `<option value="${esc(g.group)}">${esc(g.group)}</option>`).join("")}
                  </select>
                </div>
                <div class="cf-field"><label>咨询内容</label>
                  <textarea name="message" rows="3" placeholder="展位类型 / 面积 / 特殊需求 等"></textarea>
                </div>
                <button type="submit" class="btn btn-primary cf-submit">提交咨询</button>
                <div class="form-success hidden" id="homeContactOk"></div>
              </form>
            </div>
          </div>
        </div>
      </section>
    `;

    // 首页联系表单提交：通过 FormSubmit.co 把数据同步到 1060200619@qq.com
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
            "公司名称：" + (data.company || "") + "\n" +
            "联系人：" + (data.contact || "") + "\n" +
            "联系电话：" + (data.phone || "") + "\n" +
            "邮箱：" + (data.email || "") + "\n" +
            "意向展区：" + (data.zone || "") + "\n" +
            "咨询内容：" + (data.message || "") + "\n" +
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
    })();
  }

  /* =========================================================
     子页面渲染（保留原逻辑，子页面继续用旧 CSS 类）
     ========================================================= */
  function newsCard(n) {
    return `
      <article class="card news-card">
        <div class="news-thumb" style="background:${esc(n.cover)};">
          <span class="cat">${esc(n.category)}</span>
        </div>
        <div class="news-body">
          <div class="date">${fmtDate(n.date)}</div>
          <h3>${esc(n.title)}</h3>
          <p>${esc(n.summary)}</p>
          <a class="more" href="news-detail.html?id=${esc(n.id)}">阅读全文 →</a>
        </div>
      </article>`;
  }

  function renderAbout() {
    const aboutStats = [
      { num: "6万+", label: "专业采购观众" },
      { num: "1000+", label: "国内外参展企业" },
      { num: "6万㎡", label: "展览总面积" },
      { num: "29届", label: "连续举办传承" }
    ];
    const statsHtml = aboutStats.map(s => `<div class="stat-tile"><b>${s.num}</b><span>${s.label}</span></div>`).join("");

    const whyHtml = (WHY_EXHIBIT || []).map(w => `
      <div class="reason-item">
        <div class="reason-num">${esc(w.num)}</div>
        <h3>${esc(w.title)}</h3>
        <p>${esc(w.desc)}</p>
      </div>`).join("");

    const scopeHtml = (SCOPE_DETAIL || []).map(s => `
      <div class="scope-item">
        <span class="scope-num">${esc(s.num)}</span>
        <h3>${esc(s.title)}</h3>
        <p>${esc(s.desc)}</p>
      </div>`).join("");

    const bp = BOOTH_PRICING || {};
    const std = bp.standard || {}, raw = bp.raw || {};
    const pricingHtml = `
      <div class="pricing-grid">
        <div class="pricing-card">
          <h3>${esc(std.name || "标准展位")}</h3>
          <div class="price-line"><b>${esc(std.cn)}</b></div>
          <div class="price-line"><b>${esc(std.usd)}</b></div>
          <p class="price-desc">${esc(std.include)}</p>
        </div>
        <div class="pricing-card">
          <h3>${esc(raw.name || "室内光地")}</h3>
          <div class="price-line"><b>${esc(raw.cn)}</b></div>
          <div class="price-line"><b>${esc(raw.usd)}</b></div>
          <p class="price-desc">${esc(raw.min)} ${esc(raw.note)}</p>
        </div>
      </div>`;

    const pastHtml = (PAST_PHOTOS || []).map(p => `
      <div class="past-tile">
        <img src="${esc(p.img)}" alt="${esc(p.alt || '往届大连工博会现场')}" loading="lazy" />
      </div>`).join("");

    const c = (SITE && SITE.contact) || {};
    const contactHtml = `
      <section class="section alt" id="contact">
        <div class="container">
          <div class="section-head"><span class="eyebrow">CONTACT</span><h2>参展咨询</h2><p>展位详情、参展政策、专区合作方案均可联系组委会咨询，抢抓东北市场先机</p></div>
          <div class="contact-grid">
            <div class="contact-info">
              <h3>组委会联系方式</h3>
              <div class="ci-list">
                <div class="ci-row"><div class="ci-ic">📞</div><div class="ci-body"><span>联系人 / 电话（微信同号）</span><b>${esc(c.person || '李玥')} | ${esc(c.phone)}</b></div></div>
                <div class="ci-row"><div class="ci-ic">✉️</div><div class="ci-body"><span>电子邮箱</span><b>${esc(c.email)}</b></div></div>
                <div class="ci-row"><div class="ci-ic">🏢</div><div class="ci-body"><span>办公地址</span><b>${esc(c.address)}</b></div></div>
                <div class="ci-row"><div class="ci-ic">📅</div><div class="ci-body"><span>展会时间 / 地点</span><b>${esc(SITE.dateText)} · ${esc(SITE.venue)}</b></div></div>
              </div>
              <div class="qr-block">
                <img class="qr-img" src="assets/img/wechat-qr.jpg" alt="大连工博会官方微信二维码" />
                <div class="qr-text"><p>扫码加微信<br>展会咨询 / 商务对接</p><span class="qr-tip">大连展会 · 辽宁大连</span></div>
              </div>
            </div>
            <div class="contact-form-card">
              <h3>参展咨询</h3>
              <p class="form-lead">填写以下信息，组委会将在 24 小时内与您联系</p>
              <a class="btn btn-primary" href="index.html#contact" style="display:block; text-align:center;">前往填写参展咨询表单 →</a>
            </div>
          </div>
        </div>
      </section>`;

    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 展会介绍</div>
          <h1>2027（第29届）大连国际工业博览会</h1>
          <p class="page-hero-sub">展会主题：数智引领工业</p>
          <div class="about-meta">
            <div><span>展览时间</span><b>${esc(SITE.dateText)}</b></div>
            <div><span>展览地点</span><b>${esc(SITE.venue)}</b></div>
            <div><span>展览规模</span><b>${esc(SITE.heroScale || '60,000 平方米')}</b></div>
          </div>
          <div class="stats-strip-inner" style="margin-top:28px;">${statsHtml}</div>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <div class="section-head"><span class="eyebrow">WHY EXHIBIT</span><h2>为什么选择大连工博会</h2><p>深耕工业领域近三十载，东北地区标杆级专业工业盛会，多重权威认证加持，为企业布局东北工业市场提供可靠平台</p></div>
          <div class="grid grid-2 why-grid">${whyHtml}</div>
        </div>
      </section>

      <section class="section alt">
        <div class="container">
          <div class="section-head"><span class="eyebrow">EXHIBITION SCOPE</span><h2>展品范围</h2><p>十大主题展区，覆盖工业制造全产业链，打造东北亚工业前沿技术交流与商贸对接核心载体</p></div>
          <div class="grid grid-2 scope-grid">${scopeHtml}</div>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <div class="section-head"><span class="eyebrow">BOOTH PRICING</span><h2>展位费用</h2><p>灵活的展位方案，满足不同规模企业的参展需求</p></div>
          ${pricingHtml}
        </div>
      </section>

      <section class="section alt">
        <div class="container">
          <div class="section-head"><span class="eyebrow">PAST EDITIONS</span><h2>往届回顾</h2><p>历届大连工博会现场实况</p></div>
          <div class="past-grid">${pastHtml}</div>
        </div>
      </section>

      ${contactHtml}
    `;
  }

  function renderExhibits() {
    const groups = EXHIBIT_SCOPE.map(g => {
      const chips = g.items.map(i => `<span class="chip">${esc(i.text)}</span>`).join("");
      return `<div class="scope-group"><h3><span class="dot"></span>${esc(g.group)}</h3><div class="chips">${chips}</div></div>`;
    }).join("");
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 展品范围</div>
          <h1>展品范围</h1>
          <p>十大主题展区，覆盖工业全产业链</p>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <div class="grid grid-2">${groups}</div>
          <div class="center" style="margin-top:36px;">
            <a class="btn btn-ghost" href="exhibitors.html">浏览参展企业 →</a>
          </div>
        </div>
      </section>`;
  }

  function renderExhibitors() {
    const cats = ["全部", ...EXHIBIT_SCOPE.map(g => g.group)];
    const filterBtns = cats.map((c, i) =>
      `<button class="filter-btn ${i === 0 ? "active" : ""}" data-cat="${esc(c)}">${esc(c)}</button>`).join("");
    const cards = EXHIBITORS.map(e => `
      <div class="card exh-card" data-cat="${esc(e.category)}">
        <div class="exh-logo">${esc(e.logo)}</div>
        <div>
          <h3>${esc(e.name)}</h3>
          <div class="cat">${esc(e.category)}</div>
          <div class="booth">展位号：${esc(e.booth)}</div>
          <p class="desc">${esc(e.desc)}</p>
        </div>
      </div>`).join("");
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 展商名录</div>
          <h1>展商名录</h1>
          <p>以下为往届部分参展头部品牌（共 ${EXHIBITORS.length} 家），2027 参展名录持续更新中</p>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <div class="filters">${filterBtns}</div>
          <div class="grid grid-2" id="exhGrid">${cards}</div>
        </div>
      </section>`;
    $$(".filter-btn").forEach(btn => btn.addEventListener("click", () => {
      $$(".filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const cat = btn.getAttribute("data-cat");
      $$("#exhGrid .exh-card").forEach(card => {
        card.style.display = (cat === "全部" || card.getAttribute("data-cat") === cat) ? "" : "none";
      });
    }));
  }

  function renderNews() {
    const items = NEWS.map(n => {
      const dt = new Date(n.date);
      const day = String(dt.getDate()).padStart(2, "0");
      const mon = `${dt.getFullYear()}.${String(dt.getMonth() + 1).padStart(2, "0")}`;
      return `
        <div class="news-list-item">
          <div class="date"><b>${day}</b><span>${mon}</span></div>
          <div>
            <span class="chip" style="background:var(--c-accent); color:#fff; border:none;">${esc(n.category)}</span>
            <h3><a href="news-detail.html?id=${esc(n.id)}">${esc(n.title)}</a></h3>
            <p>${esc(n.summary)}</p>
          </div>
        </div>`;
    }).join("");
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 新闻动态</div>
          <h1>新闻动态</h1>
          <p>展会公告、展品前瞻、活动预告与参观服务资讯</p>
        </div>
      </section>
      <section class="section">
        <div class="container" style="max-width:920px;">${items}</div>
      </section>`;
  }

  function renderNewsDetail() {
    const id = new URLSearchParams(location.search).get("id");
    const n = NEWS.find(x => x.id === id) || NEWS[0];
    if (!n) { $("#page-content").innerHTML = `<section class="section container"><p>未找到该新闻。</p></section>`; return; }
    const body = n.body.map(p => `<p>${esc(p.text)}</p>`).join("");
    const related = NEWS.filter(x => x.id !== n.id).slice(0, 3).map(newsCard).join("");
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / <a href="news.html">新闻动态</a> / 详情</div>
          <h1 style="font-size:1.8rem;">${esc(n.title)}</h1>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <article class="article">
            <div class="meta">${fmtDate(n.date)} · 分类：${esc(n.category)} · 来源：${esc(SITE.name)}</div>
            ${body}
            <div style="margin-top:26px;"><a class="btn btn-ghost" href="news.html">← 返回新闻列表</a></div>
          </article>
          <h3 style="text-align:center; margin:50px 0 20px;">更多新闻</h3>
          <div class="news-grid">${related}</div>
        </div>
      </section>`;
  }

  function renderSchedule() {
    const days = SCHEDULE.map(d => {
      const items = d.sessions.map(s => `
        <div class="tl-item">
          <div class="time">${esc(s.time)}</div>
          <div class="title">${esc(s.title)}</div>
          <div class="meta">${esc(s.meta)}</div>
        </div>`).join("");
      return `<div class="schedule-day"><h3>${esc(d.day)}</h3><div class="timeline">${items}</div></div>`;
    }).join("");
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 同期活动</div>
          <h1>同期活动安排</h1>
          <p>${esc(SITE.dateText)} · 展期精彩活动不停歇</p>
        </div>
      </section>
      <section class="section"><div class="container" style="max-width:880px;">${days}</div></section>`;
  }

  function renderTravel() {
    const routesHtml = TRANSPORT.routes.map(r => `
      <li class="route-item">
        <span class="route-num">${r.num}</span>
        <div class="route-body">
          <h4>${esc(r.title)}</h4>
          <p>${esc(r.desc)}</p>
        </div>
      </li>`).join("");
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 交通与酒店</div>
          <h1>交通与酒店指南</h1>
          <p>展馆位于大连保税区，多种出行方案，助您轻松规划行程</p>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <div class="grid grid-2" style="align-items:stretch; gap:32px;">
            <div class="venue-figure">
              <img src="assets/img/travel/travel-overview.jpg" alt="大连自贸区国际会展中心实景" />
            </div>
            <div>
              <h2 style="font-size:1.3rem; margin:0 0 14px;">展馆地址</h2>
              <div style="background:var(--c-navy); color:#fff; border-radius:var(--radius); padding:18px 22px;">
                <p style="font-size:1.15rem; font-weight:700; margin:0 0 6px;">${esc(SITE.venue)}</p>
                <p style="color:#cfe0f0; margin:0; font-size:.95rem;">${esc(TRANSPORT.addr)}</p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section class="section alt">
        <div class="container">
          <div class="section-head"><span class="eyebrow">Route</span><h2>出行路线</h2><p>5 种主要出行方式，从机场 / 火车站 / 高铁 / 高速直达展馆</p></div>
          <ul class="route-list">${routesHtml}</ul>
        </div>
      </section>
`;
  }
  function renderRegister() {
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 参观预登记</div>
          <h1>参观预登记</h1>
          <p>免费获取电子参观证，享快捷入场与商务配对服务</p>
        </div>
      </section>
      <section class="section">
        <div class="container" style="max-width:920px;">
          <div class="grid grid-2" style="align-items:start; gap:30px;">
            <div class="form-wrap">
              <h2 style="margin-top:0; font-size:1.4rem;">填写登记信息</h2>
              <form id="regForm" novalidate>
                <div class="form-grid">
                  <div class="field"><label>姓名 <span class="req">*</span></label><input name="name" required><div class="err" data-for="name"></div></div>
                  <div class="field"><label>手机号 <span class="req">*</span></label><input name="phone" required pattern="1[0-9]{10}"><div class="err" data-for="phone"></div></div>
                  <div class="field"><label>公司名称 <span class="req">*</span></label><input name="company" required><div class="err" data-for="company"></div></div>
                  <div class="field"><label>职务</label><input name="title"></div>
                  <div class="field"><label>所属行业 <span class="req">*</span></label>
                    <select name="industry" required>
                      <option value="">请选择</option>
                      <option>机械制造</option><option>汽车</option><option>电子电气</option>
                      <option>能源</option><option>航空航天</option><option>医疗器械</option>
                      <option>其他</option>
                    </select><div class="err" data-for="industry"></div></div>
                  <div class="field"><label>邮箱</label><input name="email" type="email"><div class="err" data-for="email"></div></div>
                  <div class="field full"><label>感兴趣的主题展区</label>
                    <div style="display:flex; flex-wrap:wrap; gap:10px;">
                      ${EXHIBIT_SCOPE.map(g => `<label style="font-weight:400; display:flex; align-items:center; gap:6px;"><input type="checkbox" name="interest" value="${esc(g.group)}"> ${esc(g.group)}</label>`).join("")}
                    </div>
                  </div>
                  <div class="field full"><label>备注</label><textarea name="remark" rows="3" placeholder="可填写同行人数、特殊需求等"></textarea></div>
                </div>
                <button type="submit" class="btn btn-primary" style="margin-top:18px; width:100%; justify-content:center;">提交预登记</button>
                <p class="form-note">提交即表示同意主办方使用您的信息用于展会服务。本示例表单在前端校验后本地保存，正式上线可对接表单/CRM 系统。</p>
                <div class="form-success hidden" id="regOk"></div>
              </form>
            </div>
            <div>
              <h3>预登记权益</h3>
              <ul>
                <li>专属快捷通道，二维码快速入场</li>
                <li>免费下载电子会刊与展商名录</li>
                <li>同期论坛优先预约席位</li>
                <li>智能商务配对服务</li>
                <li>团体参观（10 人以上）专属接驳</li>
              </ul>
              <div class="guide-block" style="margin-top:20px;">
                <h3 style="margin-top:0;">温馨提示</h3>
                <p style="margin:0;">预登记审核通过后，电子参观证将发送至您填写的手机/邮箱。现场凭码入场，无需排队购票。</p>
              </div>
            </div>
          </div>
        </div>
      </section>`;
    const form = $("#regForm");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      let ok = true;
      const setErr = (name, msg) => {
        const box = form.querySelector(`.err[data-for="${name}"]`);
        if (box) box.textContent = msg || "";
        if (msg) ok = false;
      };
      ["name", "phone", "company", "industry"].forEach(n => setErr(n, ""));
      const data = Object.fromEntries(new FormData(form).entries());
      if (!data.name) setErr("name", "请填写姓名");
      if (!/^1[0-9]{10}$/.test(data.phone || "")) setErr("phone", "请填写正确的 11 位手机号");
      if (!data.company) setErr("company", "请填写公司名称");
      if (!data.industry) setErr("industry", "请选择所属行业");
      if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) setErr("email", "邮箱格式不正确");
      if (!ok) return;
      try { localStorage.setItem("diie_reg_" + Date.now(), JSON.stringify(data)); } catch (_) {}
      const okBox = $("#regOk");
      okBox.textContent = `✅ 登记成功！${esc(data.name)}，感谢您的预登记，电子参观证将发送至 ${esc(data.phone)}。`;
      okBox.classList.remove("hidden");
      form.reset();
      okBox.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  }

  function renderContact() {
    const c = SITE.contact;
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 联系我们</div>
          <h1>联系我们</h1>
          <p>展位咨询、观众服务、媒体合作，欢迎随时联系主办方</p>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <div class="grid grid-2" style="align-items:start; gap:30px;">
            <div class="form-wrap">
              <h2 style="margin-top:0; font-size:1.4rem;">展位 / 合作咨询</h2>
              <div class="info-row"><div class="ic">👤</div><div><h4>联系人</h4><p>${esc(c.person || '')}${c.personTitle ? `（${esc(c.personTitle)}）` : ''}</p></div></div>
              <div class="info-row"><div class="ic">📞</div><div><h4>咨询电话</h4><p>${esc(c.phone)}（工作日 9:00-18:00）</p></div></div>
              <div class="info-row"><div class="ic">✉️</div><div><h4>电子邮箱</h4><p>${esc(c.email)}</p></div></div>
              <div class="info-row"><div class="ic">💬</div><div><h4>微信公众号</h4><p>${esc(c.wechat)}</p></div></div>
              <div class="info-row"><div class="ic">🏢</div><div><h4>办公地址</h4><p>${esc(c.address)}</p></div></div>
            </div>
            <div>
              <h3>参展报名</h3>
              <p>如需申请展位或了解赞助方案，请发送邮件至 <b>${esc(c.email)}</b>，注明"参展咨询+公司名称"，我们将安排专属顾问与您对接。</p>
              <h3 style="margin-top:24px;">媒体合作</h3>
              <p>欢迎媒体朋友申请采访证与新闻素材，联系邮箱同上，注明"媒体合作"。</p>
              <div class="guide-block" style="margin-top:20px;">
                <h3 style="margin-top:0;">观众服务</h3>
                <p style="margin:0;">个人参观请前往「参观预登记」页面在线登记，免费获取电子参观证。</p>
              </div>
            </div>
          </div>
        </div>
      </section>`;
  }

  function renderGuide() {
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 内容更新指南</div>
          <h1>内容更新指南</h1>
          <p>主办方可不依赖开发人员，自行维护网站资讯</p>
        </div>
      </section>
      <section class="section">
        <div class="container" style="max-width:920px;">
          <div class="guide-block">
            <h3>一、网站结构说明</h3>
            <p>全站采用「数据与页面分离」设计：所有文字内容集中在 <code>assets/js/data.json</code>，页面负责展示。主办方修改该文件后刷新即可看到更新。</p>
            <p><b>最省事的方式（推荐）</b>：直接用网站自带的 <b>内容管理后台</b> 编辑。访问 <code>你的网址/admin/</code>，用账号密码登录，在「网站内容」表单里改文字、保存即自动重新发布，<b>完全不用碰代码</b>。后台的配置与启用方法见本站根目录的《后台使用说明.md》。</p>
          </div>
          <div class="guide-block">
            <h3>二、如何更新各栏目</h3>
            <p>用文本编辑器（如记事本、VS Code）打开 <code>data.json</code>，找到对应板块的 JSON 键修改：</p>
            <ul>
              <li><b>展会基础信息</b>：修改 <code>SITE</code>。</li>
              <li><b>展会介绍</b>：修改 <code>ABOUT</code>。</li>
              <li><b>展品范围</b>：修改 <code>EXHIBIT_SCOPE</code>。</li>
              <li><b>展商名录</b>：修改 <code>EXHIBITORS</code>。</li>
              <li><b>新闻动态</b>：修改 <code>NEWS</code>。</li>
              <li><b>导航栏目</b>：修改 <code>NAV</code>。</li>
            </ul>
          </div>
          <div class="guide-block">
            <h3>三、新增一条新闻示例</h3>
            <pre>{
  "id": "n07",
  "title": "新闻标题",
  "date": "2026-05-10",
  "category": "展会公告",
  "summary": "一句话摘要。",
  "cover": "linear-gradient(135deg,#0d2b4e,#1f5f8b)",
  "body": [
    { "text": "第一段正文。" }
  ]
}</pre>
          </div>
          <div class="guide-block">
            <h3>四、域名与免费托管</h3>
            <p>本网站是纯静态页面，可直接部署到 Cloudflare Pages / Netlify / Vercel 等免费平台，绑定自定义域名（约 60-100 元/年）即可上线。</p>
          </div>
        </div>
      </section>`;
  }

  function renderBrands() {
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 参展品牌</div>
          <h1>参展品牌</h1>
          <p>汇聚全球工业领军企业，往届部分参展品牌一览（仅供参考，排名不分先后）</p>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <div class="brands-page-board">
            <img src="assets/img/brands/brands-overview.png" alt="往届参展品牌：GROB / Mazak / EMAG / Panasonic / Hexagon / ZEISS / SANYO / FLUKE / KUKA / FANUC / YASKAWA / 三菱 / SMC / 一汽-大众 / OTC / SIEMENS / Mahr / rexroth / Schneider Electric / RENISHAW / KEYENCE 基恩士 / 迪能机床 / 亚德客 / 大族激光 / Unitree 宇树 / 新松 / 海康机器人 / 钛虎机器人 / TSUGAMI / 凯特精机 / Linde / 德永 / Mitutoyo / KYOCERA 等" loading="lazy" />
            <p class="brands-page-cap">仅选取部分品牌（logo），排名不分先后</p>
          </div>
        </div>
      </section>`;
  }

  function renderApply() {
    const fee = APPLY_INFO.fee.map(f => `
      <div class="info-row"><div class="ic">💰</div><div>
        <h4>${esc(f.type)}</h4>
        <p><b>${esc(f.price)}</b></p>
        <p class="muted">${esc(f.note)}</p>
      </div></div>`).join("");
    const steps = APPLY_INFO.steps.map(s => `
      <div class="tl-item"><div class="time">${esc(s.t)}</div><div class="title">${esc(s.p)}</div></div>`).join("");
    const faq = APPLY_INFO.faq.map(f => `
      <div class="guide-block" style="margin-bottom:14px;">
        <h3 style="margin-top:0; font-size:1rem;">Q：${esc(f.q)}</h3>
        <p style="margin:0;">${esc(f.a)}</p>
      </div>`).join("");
    const zones = EXHIBIT_SCOPE.map(g => `<option value="${esc(g.group)}">${esc(g.group)}</option>`).join("");
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 参展报名</div>
          <h1>参展报名</h1>
          <p>在线申请展位，抢占 2027 大连工博会黄金展期，享官方免费宣传支持</p>
        </div>
      </section>
      <section class="section">
        <div class="container" style="max-width:1080px;">
          <div class="grid grid-2" style="align-items:start; gap:30px;">
            <div class="form-wrap">
              <h2 style="margin-top:0; font-size:1.4rem;">填写参展报名表</h2>
              <form id="applyForm" novalidate>
                <div class="form-grid">
                  <div class="field full"><label>企业名称 <span class="req">*</span></label><input name="company" required placeholder="请填写营业执照全称"><div class="err" data-for="company"></div></div>
                  <div class="field"><label>联系人 <span class="req">*</span></label><input name="contact" required><div class="err" data-for="contact"></div></div>
                  <div class="field"><label>手机号 <span class="req">*</span></label><input name="phone" required pattern="1[0-9]{10}"><div class="err" data-for="phone"></div></div>
                  <div class="field"><label>职务</label><input name="title" placeholder="如 市场总监"></div>
                  <div class="field"><label>邮箱</label><input name="email" type="email"><div class="err" data-for="email"></div></div>
                  <div class="field full"><label>意向参展展区 <span class="req">*</span></label>
                    <select name="zone" required>
                      <option value="">请选择展区</option>
                      ${zones}
                    </select><div class="err" data-for="zone"></div></div>
                  <div class="field"><label>展位类型 <span class="req">*</span></label>
                    <select name="boothType" required>
                      <option value="">请选择</option>
                      <option value="标准展位">标准展位（3m×3m）</option>
                      <option value="室内光地">室内光地（≥36㎡）</option>
                    </select><div class="err" data-for="boothType"></div></div>
                  <div class="field" id="stdWrap">
                    <label>标准展位数量（个） <span class="req">*</span></label>
                    <input name="boothStd" type="number" min="1" placeholder="如 2"><div class="err" data-for="boothStd"></div>
                  </div>
                  <div class="field hidden" id="rawWrap">
                    <label>光地面积（㎡） <span class="req">*</span></label>
                    <input name="boothRaw" type="number" min="36" placeholder="不少于 36"><div class="err" data-for="boothRaw"></div>
                  </div>
                  <div class="field full"><label>主营产品 / 展品类别 <span class="req">*</span></label>
                    <input name="products" required placeholder="如 数控机床、工业机器人"><div class="err" data-for="products"></div></div>
                  <div class="field full"><label>备注 / 特殊需求</label><textarea name="remark" rows="3" placeholder="可填写期望展位位置、搭建需求等"></textarea></div>
                </div>
                <button type="submit" class="btn btn-primary" style="margin-top:18px; width:100%; justify-content:center;">提交参展报名</button>
                <p class="form-note">提交后，报名信息将发送到组委会邮箱 1060200619@qq.com，主办方 1 个工作日内与您联系。提交即表示同意主办方与您联系对接参展事宜。</p>
                <div class="form-success hidden" id="applyOk"></div>
              </form>
            </div>
            <div>
              <h3 style="margin-top:0;">展位费用</h3>
              <div style="background:#fff; border:1px solid var(--c-line); border-radius:var(--radius); padding:18px;">${fee}</div>
              <h3 style="margin-top:26px;">参展流程</h3>
              <div class="timeline">${steps}</div>
              <h3 style="margin-top:26px;">常见问题</h3>
              ${faq}
            </div>
          </div>
        </div>
      </section>`;
    const form = $("#applyForm");
    const typeSel = form.querySelector('[name="boothType"]');
    const stdWrap = $("#stdWrap"), rawWrap = $("#rawWrap");
    const syncBooth = () => {
      const isStd = typeSel.value === "标准展位";
      stdWrap.classList.toggle("hidden", !isStd);
      rawWrap.classList.toggle("hidden", isStd);
    };
    typeSel.addEventListener("change", syncBooth);
    syncBooth();
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      let ok = true;
      const setErr = (name, msg) => {
        const box = form.querySelector(`.err[data-for="${name}"]`);
        if (box) box.textContent = msg || "";
        if (msg) ok = false;
      };
      ["company", "contact", "phone", "zone", "boothType", "boothStd", "boothRaw", "products", "email"]
        .forEach(n => setErr(n, ""));
      const data = Object.fromEntries(new FormData(form).entries());
      if (!data.company) setErr("company", "请填写企业名称");
      if (!data.contact) setErr("contact", "请填写联系人");
      if (!/^1[0-9]{10}$/.test(data.phone || "")) setErr("phone", "请填写正确的 11 位手机号");
      if (!data.zone) setErr("zone", "请选择参展展区");
      if (!data.boothType) setErr("boothType", "请选择展位类型");
      if (data.boothType === "标准展位" && !(Number(data.boothStd) > 0)) setErr("boothStd", "请填写标准展位数量");
      if (data.boothType === "室内光地" && !(Number(data.boothRaw) >= 36)) setErr("boothRaw", "光地面积不少于 36 ㎡");
      if (!data.products) setErr("products", "请填写主营产品/展品类别");
      if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) setErr("email", "邮箱格式不正确");
      if (!ok) return;

      // 本地缓存一份（防止网络异常丢数据，本机也可回看）
      try { localStorage.setItem("diie_apply_" + Date.now(), JSON.stringify(data)); } catch (_) {}

      const submitBtn = form.querySelector('button[type="submit"]');
      const okBox = $("#applyOk");
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "正在提交..."; }

      // ---- 主通道：FormSubmit.co AJAX，发到 1060200619@qq.com ----
      // 首次提交需主轮机人在收件箱点 "Activate Form" 邮件完成激活。
      let delivered = false;
      try {
        const payload = {
          _subject: "【大连工博会·参展报名】" + (data.company || "") + " · " + (data.contact || ""),
          _template: "table",
          _captcha: "false",
          "企业名称": data.company || "",
          "联系人": data.contact || "",
          "手机号": data.phone || "",
          "职务": data.title || "",
          "邮箱": data.email || "",
          "意向参展展区": data.zone || "",
          "展位类型": data.boothType || "",
          "标准展位数量（个）": data.boothStd || "",
          "光地面积（㎡）": data.boothRaw || "",
          "主营产品/展品类别": data.products || "",
          "备注/特殊需求": data.remark || "",
          "提交时间": new Date().toLocaleString("zh-CN")
        };
        const r = await fetch("https://formsubmit.co/ajax/1060200619@qq.com", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(payload)
        });
        delivered = r.ok;
      } catch (_) { delivered = false; }

      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "提交参展报名"; }

      if (delivered) {
        okBox.innerHTML = `✅ 已收到！报名表已发送到组委会邮箱 <b>1060200619@qq.com</b>，<b>${esc(data.company)}</b>（${esc(data.contact)}）将在 <b>1 个工作日内</b>与您联系对接展位事宜。`;
      } else {
        // 兑底：调起邮件客户端（关键信息精简），同时提示直打电话
        const subject = encodeURIComponent("【大连工博会·参展报名】" + (data.company || "") + " · " + (data.contact || ""));
        const body = encodeURIComponent(
          "企业名称：" + (data.company || "") + "\n" +
          "联系人：" + (data.contact || "") + "\n" +
          "手机号：" + (data.phone || "") + "\n" +
          "意向展区：" + (data.zone || "") + "\n" +
          "展位类型：" + (data.boothType || "") + "\n" +
          (data.boothType === "标准展位" ? "标准展位数量：" + (data.boothStd || "") + "\n" : "") +
          (data.boothType === "室内光地" ? "光地面积：" + (data.boothRaw || "") + "㎡\n" : "") +
          "主营产品：" + (data.products || "") + "\n" +
          "备注：" + (data.remark || "") + "\n"
        );
        okBox.innerHTML = `⚠️ 提交未发送出去。请拨打组委会电话 <a href="tel:18624268832"><b>18624268832</b></a>（李玥），或点此处直接发邮件：<a href="mailto:1060200619@qq.com?subject=${subject}&body=${body}">1060200619@qq.com</a>。`;
      }
      okBox.classList.remove("hidden");
      form.reset();
      syncBooth();
      okBox.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  }

  /* ---------- 回到顶部 ---------- */
  function setupToTop() {
    const btn = document.createElement("button");
    btn.className = "to-top"; btn.innerHTML = "↑"; btn.setAttribute("aria-label", "回到顶部");
    document.body.appendChild(btn);
    window.addEventListener("scroll", () => {
      btn.classList.toggle("show", window.scrollY > 400);
    });
    btn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  }

  /* ---------- 启动 ---------- */
  async function boot() {
    try {
      const res = await fetch("assets/js/data.json", { cache: "no-store" });
      if (!res.ok) throw new Error("HTTP " + res.status);
      const D = await res.json();
      SITE = D.SITE; NAV = D.NAV; ABOUT = D.ABOUT;
      EXHIBIT_SCOPE = D.EXHIBIT_SCOPE; EXHIBITORS = D.EXHIBITORS;
      NEWS = D.NEWS; SCHEDULE = D.SCHEDULE; TRANSPORT = D.TRANSPORT;
      HOTELS = D.HOTELS; APPLY_INFO = D.APPLY_INFO; PAST_PHOTOS = D.PAST_PHOTOS; WHY_EXHIBIT = D.WHY_EXHIBIT; SCOPE_DETAIL = D.SCOPE_DETAIL; BOOTH_PRICING = D.BOOTH_PRICING;
    } catch (e) {
      const box = document.getElementById("page-content");
      const msg = esc(String((e && e.message) || e));
      if (box) box.innerHTML = '<section class="section container"><p style="color:#c0392b;">内容加载失败：' + msg + '。请通过本地服务器或部署后的网址访问。</p></section>';
      return;
    }
    buildHeader();
    buildFooter();
    setupToTop();
    const page = document.body.getAttribute("data-page");
    const map = {
      home: renderHome, about: renderAbout, exhibits: renderExhibits,
      exhibitors: renderExhibitors, brands: renderBrands, news: renderNews, newsDetail: renderNewsDetail,
      schedule: renderSchedule, travel: renderTravel, register: renderRegister,
      apply: renderApply, contact: renderContact, guide: renderGuide
    };
    try {
      (map[page] || renderHome)();
    } catch (e) {
      console.error("Render error:", e);
      const box = document.getElementById("page-content");
      if (box) box.innerHTML = '<section class="section container"><pre style="color:#c0392b;white-space:pre-wrap;background:#fff;padding:20px;border-radius:8px;">Render error: ' + String((e&&e.message)||e) + '\n' + String((e&&e.stack)||'') + '</pre></section>';
    }
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
