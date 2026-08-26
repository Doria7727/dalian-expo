/* =========================================================
   通用脚本：统一注入头部/底部、移动端菜单、各页面数据渲染
   数据：由 assets/js/data.json 在 boot() 中异步 fetch 加载（无需其他 script 引入）
   ========================================================= */
(function () {
  "use strict";

  /* ---------- 数据（由 assets/js/data.json 异步加载） ---------- */
  let SITE, NAV, ABOUT, EXHIBIT_SCOPE, EXHIBITORS, NEWS, SCHEDULE, TRANSPORT, HOTELS, APPLY_INFO;

  /* ---------- 工具 ---------- */
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

  /* ---------- 注入头部 ---------- */
  function buildHeader() {
    const cur = document.body.getAttribute("data-page") || "";
    const navLinks = NAV.map(n =>
      `<a href="${n.href}" class="${n.page === cur ? "active" : ""}">${esc(n.label)}</a>`
    ).join("");
    const html = `
      <div class="header-inner container">
        <a class="brand" href="index.html">
          <span class="logo">${esc(SITE.shortName.slice(0, 2))}</span>
          <span class="txt"><b>${esc(SITE.shortName)}</b><span>${esc(SITE.enName)}</span></span>
          <img class="brand-logo" src="assets/img/logo-ief-ufi.png" alt="IEF 中国·大连 · UFI 国际认证" />
        </a>
        <button class="nav-toggle" aria-label="菜单" id="navToggle">☰</button>
        <nav class="nav" id="nav">
          ${navLinks}
          <a class="btn btn-outline nav-cta" href="apply.html">参展报名</a>
          <a class="btn btn-primary nav-cta" href="register.html">参观预登记</a>
        </nav>
      </div>`;
    $("#site-header").innerHTML = html;

    $("#navToggle").addEventListener("click", () => {
      $("#nav").classList.toggle("open");
    });
    // 点击导航项后（移动端）收起菜单
    $$("#nav a").forEach(a => a.addEventListener("click", () => $("#nav").classList.remove("open")));
  }

  /* ---------- 注入底部 ---------- */
  function buildFooter() {
    const c = SITE.contact;
    const quick = NAV.map(n => `<a href="${n.href}">${esc(n.label)}</a>`).join("");
    $("#site-footer").innerHTML = `
      <div class="container">
        <div class="footer-grid">
          <div>
            <h4>${esc(SITE.name)}</h4>
            <p>${esc(SITE.edition)} · ${esc(SITE.year)}</p>
            <p>${esc(SITE.dateText)}</p>
            <p>${esc(SITE.venue)}</p>
            <p style="margin-top:14px;">主办：${esc(SITE.organizer)}</p>
          </div>
          <div>
            <h4>快速导航</h4>
            ${quick}
          </div>
          <div>
            <h4>参观服务</h4>
            <a href="register.html">参观预登记</a>
            <a href="exhibitors.html">展商名录</a>
            <a href="schedule.html">日程安排</a>
            <a href="travel.html">交通与酒店</a>
          </div>
          <div>
            <h4>联系我们</h4>
            <p>电话：${esc(c.phone)}</p>
            <p>邮箱：${esc(c.email)}</p>
            <p>微信：${esc(c.wechat)}</p>
            <p>${esc(c.address)}</p>
          </div>
        </div>
        <div class="footer-bottom">
          © ${SITE.year} ${esc(SITE.name)} 版权所有 · 本网站为展会信息发布平台示例
        </div>
      </div>`;
  }

  /* ---------- 各页面渲染 ---------- */
  function renderHome() {
    const stats = SITE.stats.map(s => `<div class="stat"><b>${esc(s.num)}</b><span>${esc(s.label)}</span></div>`).join("");
    const hl = ABOUT.highlights.map(h => `
      <div class="card">
        <div class="ic">${h.ic}</div>
        <h3>${esc(h.title)}</h3>
        <p>${esc(h.desc)}</p>
      </div>`).join("");
    const news = NEWS.slice(0, 3).map(n => newsCard(n)).join("");
    const scopeCats = EXHIBIT_SCOPE.slice(0, 6).map(s =>
      `<span class="chip">${esc(s.group)}</span>`).join("");

    $("#page-content").innerHTML = `
      <section class="hero">
        <div class="container hero-inner">
          <span class="tag">${esc(SITE.edition)} · ${esc(SITE.year)}</span>
          <h1>${esc(SITE.name)}</h1>
          <p class="sub">${esc(ABOUT.intro.slice(0, 60))}……数智引领工业，诚邀您共赴东北智造盛会。</p>
          <div class="hero-meta">
            <div class="mi"><span class="ic">📅</span><div><b>${esc(SITE.dateText)}</b><span>举办时间</span></div></div>
            <div class="mi"><span class="ic">📍</span><div><b>${esc(SITE.venue)}</b><span>${esc(SITE.venueAddr)}</span></div></div>
            <div class="mi"><span class="ic">🎫</span><div><b>免费预登记</b><span>专业观众开放</span></div></div>
          </div>
          <div class="hero-actions">
            <a class="btn btn-primary" href="register.html">立即预登记 →</a>
            <a class="btn btn-outline" href="about.html">了解展会</a>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <div class="section-head">
            <span class="eyebrow">By the Numbers</span>
            <h2>一届展会的分量</h2>
            <p>用数据看见工业博览会的规模与影响力</p>
          </div>
          <div class="stats">${stats}</div>
        </div>
      </section>

      <section class="section alt">
        <div class="container">
          <div class="section-head">
            <span class="eyebrow">Why CIIE</span>
            <h2>为什么选择我们</h2>
            <p>四大核心价值，连接产业上下游</p>
          </div>
          <div class="grid grid-4">${hl}</div>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <div class="section-head">
            <span class="eyebrow">Exhibit Scope</span>
            <h2>六大主题展区</h2>
            <p>覆盖工业全产业链的展示范围</p>
          </div>
          <div style="text-align:center; margin-bottom:30px;">${scopeCats}</div>
          <div style="text-align:center;">
            <a class="btn btn-ghost" href="exhibits.html">查看完整展品范围</a>
          </div>
        </div>
      </section>

      <section class="section alt">
        <div class="container">
          <div class="section-head">
            <span class="eyebrow">Latest News</span>
            <h2>新闻动态</h2>
            <p>及时了解展会最新公告与前瞻资讯</p>
          </div>
          <div class="news-grid">${news}</div>
          <div class="center" style="margin-top:30px;">
            <a class="btn btn-ghost" href="news.html">查看更多新闻</a>
          </div>
        </div>
      </section>

      <section class="section" style="background:var(--c-navy); color:#fff;">
        <div class="container center">
          <h2 style="color:#fff;">准备好开启您的工业之旅了吗？</h2>
          <p style="color:#cfe0f0; max-width:620px; margin:0 auto 22px;">完成预登记，即可免费获取电子参观证，享快捷入场与商务配对服务。</p>
          <a class="btn btn-primary" href="register.html">免费参观预登记 →</a>
        </div>
      </section>`;
  }

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
    const hl = ABOUT.highlights.map(h => `
      <div class="card"><div class="ic">${h.ic}</div><h3>${esc(h.title)}</h3><p>${esc(h.desc)}</p></div>`).join("");
    const secs = ABOUT.sections.map(s => `
      <div class="guide-block"><h3>${esc(s.h)}</h3><p>${esc(s.p)}</p></div>`).join("");
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 展会介绍</div>
          <h1>展会介绍</h1>
          <p>${esc(SITE.edition)} · ${esc(SITE.name)}</p>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <div class="grid grid-2" style="align-items:center; gap:40px;">
            <div>
              <h2>关于展会</h2>
              <p>${esc(ABOUT.intro)}</p>
              <p style="font-style:italic; color:var(--c-steel); border-left:3px solid var(--c-accent); padding-left:14px;">${esc(ABOUT.vision)}</p>
            </div>
            <div style="background:var(--c-soft); border-radius:var(--radius); padding:30px;">
              <h3 style="margin-top:0;">展会概况</h3>
              <ul style="margin:0;">
                <li><b>届次：</b>${esc(SITE.edition)}</li>
                <li><b>时间：</b>${esc(SITE.dateText)}</li>
                <li><b>地点：</b>${esc(SITE.venue)}</li>
                <li><b>规模：</b>${SITE.stats[0].num} 展示面积</li>
                <li><b>主办：</b>${esc(SITE.organizer)}</li>
                <li><b>承办：</b>${esc(SITE.coOrganizer)}</li>
              </ul>
            </div>
          </div>
        </div>
      </section>
      <section class="section alt">
        <div class="container">
          <div class="section-head"><span class="eyebrow">Highlights</span><h2>展会四大价值</h2></div>
          <div class="grid grid-4">${hl}</div>
        </div>
      </section>
      <section class="section">
        <div class="container" style="max-width:880px;">
          <h2 style="text-align:center; margin-bottom:24px;">深入了解</h2>
          ${secs}
        </div>
      </section>`;
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
          <p>六大主题展区，覆盖工业全产业链</p>
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
    const tp = TRANSPORT.map(t => `
      <div class="info-row"><div class="ic">${t.ic}</div><div><h4>${esc(t.h)}</h4><p>${esc(t.p)}</p></div></div>`).join("");
    const ht = HOTELS.map(h => `
      <div class="card hotel-card">
        <h3 style="margin-top:0;">${esc(h.name)}</h3>
        <p class="muted">📍 ${esc(h.dist)}</p>
        <p>${esc(h.note)}</p>
        <p class="price">${esc(h.price)}</p>
      </div>`).join("");
    $("#page-content").innerHTML = `
      <section class="page-hero">
        <div class="container">
          <div class="breadcrumb"><a href="index.html">首页</a> / 交通与酒店</div>
          <h1>交通与酒店指南</h1>
          <p>多种出行方案与周边协议酒店，助您轻松规划行程</p>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <div class="grid grid-2">
            <div>
              <h2 style="font-size:1.4rem;">如何抵达</h2>
              <div style="background:#fff; border:1px solid var(--c-line); border-radius:var(--radius); padding:20px;">${tp}</div>
            </div>
            <div>
              <h2 style="font-size:1.4rem;">展馆地址</h2>
              <div style="background:var(--c-navy); color:#fff; border-radius:var(--radius); padding:26px;">
                <p style="font-size:1.2rem; margin:0 0 8px;">${esc(SITE.venue)}</p>
                <p style="color:#cfe0f0; margin:0;">${esc(SITE.venueAddr)}</p>
                <p style="color:#cfe0f0; margin:14px 0 0;">建议导航至「国家会展中心 P 停车场」，展期提供免费接驳摆渡车。</p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section class="section alt">
        <div class="container">
          <div class="section-head"><span class="eyebrow">Hotels</span><h2>周边协议酒店</h2><p>预登记观众可凭确认短信享受协议价（示例数据）</p></div>
          <div class="grid grid-4">${ht}</div>
        </div>
      </section>`;
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
    form.addEventListener("submit", (e) => {
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
      try { localStorage.setItem("ciie_reg_" + Date.now(), JSON.stringify(data)); } catch (_) {}
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
            <p>用文本编辑器（如记事本、VS Code）打开 <code>data.json</code>，找到对应板块的 JSON 键修改（键名与下方一致）：</p>
            <ul>
              <li><b>展会基础信息</b>：修改 <code>SITE</code>（名称、时间、地点、数据指标、联系方式）。</li>
              <li><b>展会介绍</b>：修改 <code>ABOUT</code>（简介、价值点、深入段落）。</li>
              <li><b>展品范围</b>：修改 <code>EXHIBIT_SCOPE</code> 的展区与条目。</li>
              <li><b>展商名录</b>：在 <code>EXHIBITORS</code> 数组里增删企业（<code>category</code> 需与展区名称一致才能被筛选）。</li>
              <li><b>新闻动态</b>：在 <code>NEWS</code> 数组顶部插入新条目，<code>id</code> 保持唯一；<code>body</code> 为段落数组。</li>
              <li><b>日程安排</b>：修改 <code>SCHEDULE</code>。</li>
              <li><b>交通与酒店</b>：修改 <code>TRANSPORT</code> 与 <code>HOTELS</code>。</li>
              <li><b>导航栏目</b>：修改 <code>NAV</code> 可增删顶部菜单项。</li>
            </ul>
          </div>
          <div class="guide-block">
            <h3>三、新增一条新闻示例</h3>
            <pre>{
  "id": "n07",
  "title": "这里填新闻标题",
  "date": "2026-05-10",
  "category": "展会公告",
  "summary": "一句话摘要。",
  "cover": "linear-gradient(135deg,#0d2b4e,#1f5f8b)",
  "body": [
    { "text": "第一段正文。" },
    { "text": "第二段正文。" }
  ]
}</pre>
            <p>把以上对象粘贴到 <code>NEWS</code> 数组的最前面（<code>[</code> 之后），保存即可。注意正文每段是 <code>{ "text": "..." }</code> 的形式。</p>
          </div>
          <div class="guide-block">
            <h3>四、预登记表单对接（上线建议）</h3>
            <p>当前「参观预登记」与「参展报名」两个表单均在前端校验并本地保存（演示用）。正式上线时，可在 <code>main.js</code> 的 <code>renderRegister</code> / <code>renderApply</code> 提交逻辑中，将 <code>data</code> 通过 <code>fetch</code> 发送到贵司的表单系统、CRM 或邮件接口，即可收集真实的观众与展商报名数据。</p>
          </div>
          <div class="guide-block">
            <h3>五、域名与免费托管方案</h3>
            <p><b>是否需要买域名？</b>不需要。本网站是纯静态页面（无数据库、无后端），可直接部署到免费托管平台，平台会自动分配一个免费子域名（如 <code>xxx.netlify.app</code>、<code>username.github.io</code>），立即对外访问，零成本。</p>
            <p><b>什么时候才需要买域名？</b>当您希望用专属品牌域名（如 <code>dalian-expo.com</code>）提升专业度、统一企业邮箱、便于记忆与搜索时，再花约 60–100 元/年 购买即可；上述免费平台都支持一键绑定自定义域名。</p>
            <p><b>推荐免费托管（任选其一）：</b></p>
            <ul>
              <li><b>Netlify / Vercel</b>：把整个网站文件夹拖拽上传即可，秒级生成 <code>*.netlify.app</code> 子域名，自动 HTTPS、支持自定义域名，最适合不懂技术的运营人员。</li>
              <li><b>Cloudflare Pages</b>：免费 <code>*.pages.dev</code> 子域名，国内访问相对更稳定。</li>
              <li><b>GitHub Pages</b>：免费 <code>*.github.io</code> 子域名，适合有 Git 基础；国内访问偶尔偏慢。</li>
              <li><b>国内方案（面向中国大陆观众）</b>：腾讯云 COS / 阿里云 OSS 静态网站托管、Gitee Pages、Coding Pages。若绑定国内域名并用于境内服务器，需办理 ICP 备案（约 1–2 周，平台有指引）。</li>
            </ul>
            <p><b>两种部署方式：</b></p>
            <ul>
              <li><b>方式 A（带后台，推荐）</b>：把本文件夹推送到 GitHub 仓库，在 Netlify 用「Import from Git」导入，并启用 Identity + Git Gateway（详见《后台使用说明.md》）。之后在 <code>/admin</code> 后台改内容，保存即自动重新发布。</li>
              <li><b>方式 B（纯静态，无后台）</b>：打开 app.netlify.com 注册登录，把整个文件夹拖到 “Deploy manually” 区域，几十秒后得到免费子域名即可对外宣传。每次修改 <code>data.json</code> 后重新拖上去覆盖即可。</li>
            </ul>
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
                <p class="form-note">提交即表示同意主办方与您联系对接参展事宜。本示例表单在前端校验后本地保存，正式上线可对接表单/CRM 系统。</p>
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
              <div class="guide-block" style="margin-top:18px;">
                <h3 style="margin-top:0;">专属顾问</h3>
                <p style="margin:0;">电话：${esc(SITE.contact.phone)} · 邮箱：${esc(SITE.contact.email)}</p>
              </div>
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

    form.addEventListener("submit", (e) => {
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
      try { localStorage.setItem("ciie_apply_" + Date.now(), JSON.stringify(data)); } catch (_) {}
      const okBox = $("#applyOk");
      okBox.textContent = `✅ 报名提交成功！${esc(data.company)}，${esc(data.contact)}，组委会将尽快与您联系对接展位事宜。`;
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

  /* ---------- 启动（先异步加载数据再渲染） ---------- */
  async function boot() {
    try {
      const res = await fetch("assets/js/data.json", { cache: "no-store" });
      if (!res.ok) throw new Error("HTTP " + res.status);
      const D = await res.json();
      SITE = D.SITE; NAV = D.NAV; ABOUT = D.ABOUT;
      EXHIBIT_SCOPE = D.EXHIBIT_SCOPE; EXHIBITORS = D.EXHIBITORS;
      NEWS = D.NEWS; SCHEDULE = D.SCHEDULE; TRANSPORT = D.TRANSPORT;
      HOTELS = D.HOTELS; APPLY_INFO = D.APPLY_INFO;
    } catch (e) {
      const box = document.getElementById("page-content");
      const msg = esc(String((e && e.message) || e));
      if (box) box.innerHTML = '<section class="section container"><p style="color:#c0392b;">内容加载失败：' + msg + '。请通过本地服务器或部署后的网址访问（直接双击 index.html 因浏览器安全限制可能无法加载数据文件）。</p></section>';
      return;
    }
    buildHeader();
    buildFooter();
    setupToTop();
    const page = document.body.getAttribute("data-page");
    const map = {
      home: renderHome, about: renderAbout, exhibits: renderExhibits,
      exhibitors: renderExhibitors, news: renderNews, newsDetail: renderNewsDetail,
      schedule: renderSchedule, travel: renderTravel, register: renderRegister,
      apply: renderApply, contact: renderContact, guide: renderGuide
    };
    (map[page] || renderHome)();
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
