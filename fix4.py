import os, sys, subprocess
os.chdir(r"C:\Users\ASUS\Desktop\2027大连工博会网站")

BASE = "613ea38"  # 当前 GitHub 提交，作为新提交的基线

def git_show(path, ref=BASE):
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

# 0. 把 index 重置成 BASE 的树
subprocess.run(["git", "read-tree", BASE], check=True)

# ============ 1. data.json ============
c = git_show("assets/js/data.json").decode("utf-8")

# 1a. 联系方式新增 person / personTitle
old_contact = '''    "contact": {
      "phone": "18624268832",
      "email": "1060200619@qq.com",
      "wechat": "18624268832",
      "address": "大连华展展览服务有限公司（展会组委会）"
    }'''
new_contact = '''    "contact": {
      "person": "李玥",
      "personTitle": "项目经理",
      "phone": "18624268832",
      "email": "1060200619@qq.com",
      "wechat": "18624268832",
      "address": "大连华展展览服务有限公司（展会组委会）"
    }'''
assert old_contact in c, "data.json contact not found"
c = c.replace(old_contact, new_contact)

# 1b. 重写 EXHIBIT_SCOPE：合并 1+4，新增电子工业类，改名为名片规范
old_scope = '''  "EXHIBIT_SCOPE": [
    { "group": "机床加工设备类", "items": [{ "text": "数控机床" }, { "text": "加工中心" }, { "text": "车床/铣床/磨床" }, { "text": "电火花/线切割" }, { "text": "激光加工设备" }] },
    { "group": "工业自动化和机器人技术类", "items": [{ "text": "工业机器人" }, { "text": "协作机器人" }, { "text": "运动控制" }, { "text": "机器视觉" }, { "text": "变频/伺服系统" }] },
    { "group": "测量计量仪器类", "items": [{ "text": "三坐标测量仪" }, { "text": "影像测量仪" }, { "text": "量具量仪" }, { "text": "无损检测" }, { "text": "实验室仪器" }] },
    { "group": "刀具工装夹具类", "items": [{ "text": "数控刀具" }, { "text": "硬质合金刀具" }, { "text": "工装夹具" }, { "text": "卡盘/顶尖" }, { "text": "切削液" }] },
    { "group": "轴承、减速机和精密机械传动部件类", "items": [{ "text": "轴承" }, { "text": "减速机" }, { "text": "精密传动部件" }, { "text": "润滑配套" }, { "text": "液压气动元件" }] },
    { "group": "铸造、焊接和热处理类", "items": [{ "text": "铸造设备" }, { "text": "焊接机器人" }, { "text": "热处理炉" }, { "text": "表面处理" }, { "text": "切割设备" }] },
    { "group": "五金机电和通用设备类", "items": [{ "text": "电机" }, { "text": "泵阀" }, { "text": "空压机" }, { "text": "电动工具" }, { "text": "通用零部件" }] },
    { "group": "节能环保和工业清洁类", "items": [{ "text": "工业节能" }, { "text": "废气废水处理" }, { "text": "工业清洁设备" }, { "text": "智能照明" }, { "text": "碳管理方案" }] },
    { "group": "仓储物流和包装输送装备类", "items": [{ "text": "智能仓储" }, { "text": "AGV/叉车" }, { "text": "输送线" }, { "text": "包装机械" }, { "text": "条码识别" }] },
    { "group": "橡塑和其他工业配套产品类", "items": [{ "text": "橡塑机械" }, { "text": "模具" }, { "text": "密封件" }, { "text": "紧固件" }, { "text": "工业耗材" }] }
  ],'''

new_scope = '''  "EXHIBIT_SCOPE": [
    { "group": "机床、刀具及工装夹具类", "items": [{ "text": "数控机床" }, { "text": "加工中心" }, { "text": "车床/铣床/磨床" }, { "text": "电火花/线切割" }, { "text": "激光加工设备" }, { "text": "数控刀具" }, { "text": "硬质合金刀具" }, { "text": "工装夹具" }, { "text": "卡盘/顶尖" }, { "text": "切削液" }] },
    { "group": "工业自动化 & 机器人技术类", "items": [{ "text": "工业机器人" }, { "text": "协作机器人" }, { "text": "运动控制" }, { "text": "机器视觉" }, { "text": "变频/伺服系统" }] },
    { "group": "测量计量仪器类", "items": [{ "text": "三坐标测量仪" }, { "text": "影像测量仪" }, { "text": "量具量仪" }, { "text": "无损检测" }, { "text": "实验室仪器" }] },
    { "group": "电子工业类", "items": [{ "text": "电子元器件" }, { "text": "半导体设备" }, { "text": "PCB制造" }, { "text": "SMT贴装" }, { "text": "连接器" }, { "text": "传感器" }] },
    { "group": "轴承、减速机 & 精密机械传动件类", "items": [{ "text": "轴承" }, { "text": "减速机" }, { "text": "精密传动部件" }, { "text": "润滑配套" }, { "text": "液压气动元件" }] },
    { "group": "铸造、焊接 & 热处理类", "items": [{ "text": "铸造设备" }, { "text": "焊接机器人" }, { "text": "热处理炉" }, { "text": "表面处理" }, { "text": "切割设备" }] },
    { "group": "五金机电 & 通用设备类", "items": [{ "text": "电机" }, { "text": "泵阀" }, { "text": "空压机" }, { "text": "电动工具" }, { "text": "通用零部件" }] },
    { "group": "节能环保 & 工业清洗类", "items": [{ "text": "工业节能" }, { "text": "废气废水处理" }, { "text": "工业清洗设备" }, { "text": "智能照明" }, { "text": "碳管理方案" }] },
    { "group": "仓储物流 & 包装输送装备类", "items": [{ "text": "智能仓储" }, { "text": "AGV/叉车" }, { "text": "输送线" }, { "text": "包装机械" }, { "text": "条码识别" }] },
    { "group": "橡塑 & 其他工业配套产品类", "items": [{ "text": "橡塑机械" }, { "text": "模具" }, { "text": "密封件" }, { "text": "紧固件" }, { "text": "工业耗材" }] }
  ],'''

assert old_scope in c, "EXHIBIT_SCOPE block not found"
c = c.replace(old_scope, new_scope)

# 1c. 更新 EXHIBITORS 中的 category 引用
old_cat1 = '"category": "机床加工设备类"'
new_cat1 = '"category": "机床、刀具及工装夹具类"'
c = c.replace(old_cat1, new_cat1)

old_cat2 = '"category": "轴承、减速机和精密机械传动部件类"'
new_cat2 = '"category": "轴承、减速机 & 精密机械传动件类"'
c = c.replace(old_cat2, new_cat2)

idx_add("assets/js/data.json", write_blob(c.encode("utf-8")))
print("OK data.json")

# ============ 2. main.js ============
c = git_show("assets/js/main.js").decode("utf-8")

# 2a. 重组 buildHeader：logo 移到最左、按钮从 nav 中拆出
old_header = '''    const html = `
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
      </div>`;'''

new_header = '''    const html = `
      <div class="header-inner container">
        <img class="brand-logo" src="assets/img/logo-ief-ufi.png" alt="IEF 中国·大连 · UFI 国际认证" />
        <a class="brand" href="index.html">
          <span class="logo">${esc(SITE.shortName.slice(0, 2))}</span>
          <span class="txt"><b>${esc(SITE.shortName)}</b><span>${esc(SITE.enName)}</span></span>
        </a>
        <button class="nav-toggle" aria-label="菜单" id="navToggle">☰</button>
        <nav class="nav" id="nav">
          ${navLinks}
        </nav>
        <div class="header-actions">
          <a class="btn btn-outline" href="apply.html">参展报名</a>
          <a class="btn btn-primary" href="register.html">参观预登记</a>
        </div>
      </div>`;'''

assert old_header in c, "buildHeader HTML not found"
c = c.replace(old_header, new_header)

# 2b. 改成"展会数据" + Expo Statistics
old_stats = '''            <span class="eyebrow">By the Numbers</span>
            <h2>一届展会的分量</h2>'''
new_stats = '''            <span class="eyebrow">Expo Statistics</span>
            <h2>展会数据</h2>'''
assert old_stats in c, "stats eyebrow+h2 not found"
c = c.replace(old_stats, new_stats)

# 2c. 英文优化：Why CIIE → Why DIIE
old_why = '<span class="eyebrow">Why CIIE</span>'
new_why = '<span class="eyebrow">Why DIIE</span>'
assert old_why in c, "Why CIIE not found"
c = c.replace(old_why, new_why)

# 2d. 首页展品范围：展示全部 10 个
old_slice = 'const scopeCats = EXHIBIT_SCOPE.slice(0, 6).map(s =>'
new_slice = 'const scopeCats = EXHIBIT_SCOPE.map(s =>'
assert old_slice in c, "scope slice not found"
c = c.replace(old_slice, new_slice)

# 2e. "六大主题展区" → "十大主题展区"（首页 h2）
old_six_h2 = '<h2>六大主题展区</h2>'
new_six_h2 = '<h2>十大主题展区</h2>'
assert old_six_h2 in c, "六大主题展区 h2 not found"
c = c.replace(old_six_h2, new_six_h2)

# 2f. "六大主题展区，覆盖工业全产业链"（展品范围页 p）
old_six_p = '<p>六大主题展区，覆盖工业全产业链</p>'
new_six_p = '<p>十大主题展区，覆盖工业全产业链</p>'
assert old_six_p in c, "六大主题展区 p not found"
c = c.replace(old_six_p, new_six_p)

# 2g. footer 增加联系人
old_footer_c = '''          <div>
            <h4>联系我们</h4>
            <p>电话：${esc(c.phone)}</p>
            <p>邮箱：${esc(c.email)}</p>
            <p>微信：${esc(c.wechat)}</p>
            <p>${esc(c.address)}</p>
          </div>'''
new_footer_c = '''          <div>
            <h4>联系我们</h4>
            <p>联系人：${esc(c.person || '')}${c.personTitle ? `（${esc(c.personTitle)}）` : ''}</p>
            <p>电话：${esc(c.phone)}</p>
            <p>邮箱：${esc(c.email)}</p>
            <p>微信：${esc(c.wechat)}</p>
            <p>${esc(c.address)}</p>
          </div>'''
assert old_footer_c in c, "footer contact block not found"
c = c.replace(old_footer_c, new_footer_c)

# 2h. 联系我们页：新增联系人 info-row
old_contact_phone = '''              <div class="info-row"><div class="ic">📞</div><div><h4>咨询电话</h4><p>${esc(c.phone)}（工作日 9:00-18:00）</p></div></div>'''
new_contact_phone = '''              <div class="info-row"><div class="ic">👤</div><div><h4>联系人</h4><p>${esc(c.person || '')}${c.personTitle ? `（${esc(c.personTitle)}）` : ''}</p></div></div>
              <div class="info-row"><div class="ic">📞</div><div><h4>咨询电话</h4><p>${esc(c.phone)}（工作日 9:00-18:00）</p></div></div>'''
assert old_contact_phone in c, "contact page phone row not found"
c = c.replace(old_contact_phone, new_contact_phone)

idx_add("assets/js/main.js", write_blob(c.encode("utf-8")))
print("OK main.js")

# ============ 3. style.css ============
c = git_show("assets/css/style.css").decode("utf-8")

# 3a. header 布局：nav 用 flex:1+justify-content:center 居中，按钮组单独放右边
old_header_css = '''.header-inner { display: flex; align-items: center; justify-content: space-between; gap: 18px; height: var(--header-h); }
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
}

.nav { display: flex; align-items: center; gap: 4px; }'''

new_header_css = '''.header-inner { display: flex; align-items: center; gap: 18px; height: var(--header-h); }
.brand-logo {
  height: 36px; width: auto; max-width: 180px; margin-right: 4px;
  filter: drop-shadow(0 1px 3px rgba(0,0,0,.35));
  object-fit: contain;
}
.brand { display: flex; align-items: center; gap: 12px; color: #fff; flex: none; }
.brand .logo {
  width: 42px; height: 42px; border-radius: 8px; flex: none;
  background: linear-gradient(135deg, var(--c-accent), #ff8a4c);
  display: grid; place-items: center; font-weight: 800; color: #fff; font-size: 1.1rem;
}
.brand .txt { line-height: 1.15; }
.brand .txt b { font-size: 1.05rem; display: block; }
.brand .txt span { font-size: .72rem; letter-spacing: .12em; color: #9fb6cf; text-transform: uppercase; }

.nav { display: flex; align-items: center; gap: 4px; flex: 1; justify-content: center; }
.header-actions { display: flex; align-items: center; gap: 8px; flex: none; }'''

assert old_header_css in c, "header CSS block not found"
c = c.replace(old_header_css, new_header_css)

# 3b. hero 内容居中
old_hero_inner = '.hero-inner { padding: 90px 0 80px; }'
new_hero_inner = '''.hero-inner { padding: 90px 0 80px; text-align: center; }
.hero-inner .sub { margin-left: auto; margin-right: auto; }
.hero-meta { justify-content: center; }
.hero-actions { justify-content: center; }'''
assert old_hero_inner in c, "hero-inner CSS not found"
c = c.replace(old_hero_inner, new_hero_inner)

# 3c. 移动端：nav 不再占满空间，header-actions 保持可见
old_nav_responsive = '''  .nav {
    position: absolute; top: var(--header-h); left: 0; right: 0;
    background: var(--c-navy-2); flex-direction: column; align-items: stretch;
    padding: 10px 16px 18px; gap: 2px; display: none; box-shadow: 0 10px 20px rgba(0,0,0,.25);
  }'''
new_nav_responsive = '''  .nav {
    position: absolute; top: var(--header-h); left: 0; right: 0;
    background: var(--c-navy-2); flex-direction: column; align-items: stretch;
    padding: 10px 16px 18px; gap: 2px; display: none; box-shadow: 0 10px 20px rgba(0,0,0,.25);
    flex: none;
  }'''
assert old_nav_responsive in c, "mobile nav CSS not found"
c = c.replace(old_nav_responsive, new_nav_responsive)

# 移除 .nav-cta 在移动端的相关样式（按钮已不在 nav 内）
old_cta = '''  .nav-cta { margin: 8px 0 0; }
  .nav-toggle { display: block; }'''
new_cta = '''  .nav-toggle { display: block; }'''
assert old_cta in c, "nav-cta CSS not found"
c = c.replace(old_cta, new_cta)

idx_add("assets/css/style.css", write_blob(c.encode("utf-8")))
print("OK style.css")

# ============ 4. exhibits.html：标题/描述 ============
c = git_show("exhibits.html").decode("utf-8")
c = c.replace(
    '<title>展品范围 - 中国国际工业装备博览会</title>',
    '<title>展品范围 - 2027大连国际工业博览会</title>'
)
c = c.replace(
    '<meta name="description" content="六大主题展区，覆盖智能制造、工业软件、动力传动、绿色能源、精密制造与工业服务全产业链。">',
    '<meta name="description" content="十大主题展区，覆盖机床刀具、工业自动化、机器人、电子工业、轴承传动、铸造焊接、五金机电、节能环保、仓储物流、橡塑配套等工业全产业链。">'
)
idx_add("exhibits.html", write_blob(c.encode("utf-8")))
print("OK exhibits.html")

# ============ 5. 其他 HTML 页面：统一修正 title 中的旧品牌名 ============
title_fixes = {
    "about.html":      '<title>展会介绍 - 中国国际工业装备博览会</title>',
    "exhibitors.html": '<title>展商名录 - 中国国际工业装备博览会</title>',
    "news.html":       '<title>新闻动态 - 中国国际工业装备博览会</title>',
    "news-detail.html":'<title>新闻详情 - 中国国际工业装备博览会</title>',
    "schedule.html":   '<title>日程安排 - 中国国际工业装备博览会</title>',
    "travel.html":     '<title>交通与酒店 - 中国国际工业装备博览会</title>',
    "register.html":   '<title>参观预登记 - 中国国际工业装备博览会</title>',
    "contact.html":    '<title>联系我们 - 中国国际工业装备博览会</title>',
    "guide.html":      '<title>内容更新指南 - 中国国际工业装备博览会</title>',
    "apply.html":      '<title>参展报名 - 中国国际工业装备博览会</title>',
}
for path, old_t in title_fixes.items():
    c = git_show(path).decode("utf-8")
    if old_t in c:
        new_t = old_t.replace("中国国际工业装备博览会", "2027大连国际工业博览会")
        c = c.replace(old_t, new_t)
        idx_add(path, write_blob(c.encode("utf-8")))
        print(f"OK {path} (title)")
    else:
        print(f"SKIP {path} (no match)")
        idx_add(path, write_blob(git_show(path)))
# about.html description 也要修
c = git_show("about.html").decode("utf-8")
c = c.replace(
    '<meta name="description" content="了解中国国际工业装备博览会的定位、规模、观众构成与同期活动。">',
    '<meta name="description" content="了解 2027（第29届）大连国际工业博览会的定位、规模、观众构成与同期活动。">'
)
idx_add("about.html", write_blob(c.encode("utf-8")))
# exhibitors.html description
c = git_show("exhibitors.html").decode("utf-8")
c = c.replace(
    '<meta name="description" content="浏览中国国际工业装备博览会参展企业名录，支持按主题展区筛选。">',
    '<meta name="description" content="浏览 2027（第29届）大连国际工业博览会参展企业名录，支持按主题展区筛选。">'
)
idx_add("exhibitors.html", write_blob(c.encode("utf-8")))

# ============ 6. 其他 tracked 文件原样加入（保持基线 blob） ============
for path in [
    "index.html",
    "assets/img/hero-bg.svg",
    "assets/img/logo-ief-ufi.png",
    "assets/vendor/decap-cms.js",
]:
    idx_add(path, write_blob(git_show(path, BASE)))
    print(f"OK {path} (unchanged)")

# ============ 7. 写 tree + commit ============
tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
parent = BASE
msg = "导航栏：logo 移到最左并整体居中；hero 内容居中；标题改'展会数据' + 'Expo Statistics'；英文统一为 Why DIIE / 2027大连国际工业博览会；展品范围按名片改为十大展区；联系人新增李玥（项目经理）"
commit = subprocess.run(["git", "commit-tree", tree, "-p", parent, "-m", msg], capture_output=True, text=True).stdout.strip()
print("tree:", tree, "commit:", commit)

subprocess.run(["git", "update-ref", "refs/heads/main", commit], check=True)
print("ref updated")

# ============ 8. 验证：与 BASE 对比，只允许预期的修改（不删任何文件） ============
head_files = subprocess.run(["git", "ls-tree", "-r", BASE], capture_output=True, text=True).stdout.strip().split("\n")
head_set = {l.split("\t")[-1] for l in head_files if l}
new_files = subprocess.run(["git", "ls-tree", "-r", commit], capture_output=True, text=True).stdout.strip().split("\n")
new_set = {l.split("\t")[-1] for l in new_files if l}
removed = head_set - new_set
added = new_set - head_set
print("REMOVED:", removed)
print("ADDED:", added)
assert removed == set(), f"非预期删除: {removed}"
assert added == set(), f"非预期新增: {added}"

# ============ 9. push ============
env = os.environ.copy()
env["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
r = subprocess.run(["git", "push", "github", "main", "--force"], capture_output=True, text=True, env=env)
print("PUSH STDOUT:", r.stdout)
print("PUSH STDERR:", r.stderr)
print("rc=", r.returncode)