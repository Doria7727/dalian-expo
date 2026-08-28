#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix21_main.py: 重写 renderTravel() 为新结构（CRLF 字节精确替换）"""
MAIN_PATH = r'C:\Users\ASUS\Desktop\2027大连工博会网站\assets\js\main.js'

NL = '\r\n'

# 旧段：函数 renderTravel 整段（从 function 起到闭合花括号 }
old_lines = [
    '  function renderTravel() {',
    '    const tp = TRANSPORT.map(t => `',
    '      <div class="info-row"><div class="ic">${t.ic}</div><div><h4>${esc(t.h)}</h4><p>${esc(t.p)}</p></div></div>`).join("");',
    '    const ht = HOTELS.map(h => `',
    '      <div class="card hotel-card">',
    '        <h3 style="margin-top:0;">${esc(h.name)}</h3>',
    '        <p class="muted">📍 ${esc(h.dist)}</p>',
    '        <p>${esc(h.note)}</p>',
    '        <p class="price">${esc(h.price)}</p>',
    '      </div>`).join("");',
    '    $("#page-content").innerHTML = `',
    '      <section class="page-hero">',
    '        <div class="container">',
    '          <div class="breadcrumb"><a href="index.html">首页</a> / 交通与酒店</div>',
    '          <h1>交通与酒店指南</h1>',
    '          <p>多种出行方案与周边协议酒店，助您轻松规划行程</p>',
    '        </div>',
    '      </section>',
    '      <section class="section">',
    '        <div class="container">',
    '          <div class="grid grid-2">',
    '            <div>',
    '              <h2 style="font-size:1.4rem;">如何抵达</h2>',
    '              <div style="background:#fff; border:1px solid var(--c-line); border-radius:var(--radius); padding:20px;">${tp}</div>',
    '            </div>',
    '            <div>',
    '              <h2 style="font-size:1.4rem;">展馆地址</h2>',
    '              <div style="background:var(--c-navy); color:#fff; border-radius:var(--radius); padding:26px;">',
    '                <p style="font-size:1.2rem; margin:0 0 8px;">${esc(SITE.venue)}</p>',
    '                <p style="color:#cfe0f0; margin:0;">${esc(SITE.venueAddr)}</p>',
    '                <p style="color:#cfe0f0; margin:14px 0 0;">建议导航至「国家会展中心 P 停车场」，展期提供免费接驳摆渡车。</p>',
    '              </div>',
    '            </div>',
    '          </div>',
    '        </div>',
    '      </section>',
    '      <section class="section alt">',
    '        <div class="container">',
    '          <div class="section-head"><span class="eyebrow">Hotels</span><h2>周边协议酒店</h2><p>预登记观众可凭确认短信享受协议价（示例数据）</p></div>',
    '          <div class="grid grid-4">${ht}</div>',
    '        </div>',
    '      </section>`;',
    '  }',
]
old_chunk = (NL.join(old_lines) + NL).encode('utf-8')

# 新段：按用户给的版式（顶部展馆图 + 距离表 + 地址+5 条路线编号说明 + 酒店区）
new_lines = []
def L(s, indent='  '):
    new_lines.append(indent + s)
new_lines.append('  function renderTravel() {')
new_lines.append('    const distancesHtml = TRANSPORT.distances.map(d => `')
new_lines.append('      <div class="distance-tile">')
new_lines.append('        <div class="distance-value">${esc(d.value)}</div>')
new_lines.append('        <div class="distance-label">${esc(d.label)}</div>')
new_lines.append('        <div class="distance-note">${esc(d.note || "")}</div>')
new_lines.append('      </div>`).join("");')
new_lines.append('    const routesHtml = TRANSPORT.routes.map(r => `')
new_lines.append('      <li class="route-item">')
new_lines.append('        <span class="route-num">${r.num}</span>')
new_lines.append('        <div class="route-body">')
new_lines.append('          <h4>${esc(r.title)}</h4>')
new_lines.append('          <p>${esc(r.desc)}</p>')
new_lines.append('        </div>')
new_lines.append('      </li>`).join("");')
new_lines.append('    const ht = HOTELS.map(h => `')
new_lines.append('      <div class="card hotel-card">')
new_lines.append('        <h3 style="margin-top:0;">${esc(h.name)}</h3>')
new_lines.append('        <p class="muted">📍 ${esc(h.dist)}</p>')
new_lines.append('        <p>${esc(h.note)}</p>')
new_lines.append('        <p class="price">${esc(h.price)}</p>')
new_lines.append('      </div>`).join("");')
new_lines.append('    $("#page-content").innerHTML = `')
new_lines.append('      <section class="page-hero">')
new_lines.append('        <div class="container">')
new_lines.append('          <div class="breadcrumb"><a href="index.html">首页</a> / 交通与酒店</div>')
new_lines.append('          <h1>交通与酒店指南</h1>')
new_lines.append('          <p>展馆位于大连保税区，多种出行方案与周边协议酒店，助您轻松规划行程</p>')
new_lines.append('        </div>')
new_lines.append('      </section>')
new_lines.append('      <section class="section">')
new_lines.append('        <div class="container">')
new_lines.append('          <div class="grid grid-2" style="align-items:stretch; gap:32px;">')
new_lines.append('            <div class="venue-figure">')
new_lines.append('              <img src="assets/img/travel/travel-overview.jpg" alt="大连自贸区国际会展中心实景及周边" />')
new_lines.append('            </div>')
new_lines.append('            <div>')
new_lines.append('              <h2 style="font-size:1.3rem; margin:0 0 10px;">展馆介绍</h2>')
new_lines.append('              <p style="color:var(--c-steel); margin:0 0 20px;">${esc(TRANSPORT.intro)}</p>')
new_lines.append('              <h2 style="font-size:1.3rem; margin:0 0 14px;">展馆地址</h2>')
new_lines.append('              <div style="background:var(--c-navy); color:#fff; border-radius:var(--radius); padding:18px 22px; margin-bottom:18px;">')
new_lines.append('                <p style="font-size:1.15rem; font-weight:700; margin:0 0 6px;">${esc(SITE.venue)}</p>')
new_lines.append('                <p style="color:#cfe0f0; margin:0; font-size:.95rem;">${esc(TRANSPORT.addr)}</p>')
new_lines.append('              </div>')
new_lines.append('              <h3 style="font-size:1rem; color:var(--c-steel); margin:0 0 10px; text-transform:uppercase; letter-spacing:1px;">距展馆</h3>')
new_lines.append('              <div class="distance-grid">${distancesHtml}</div>')
new_lines.append('            </div>')
new_lines.append('          </div>')
new_lines.append('        </div>')
new_lines.append('      </section>')
new_lines.append('      <section class="section alt">')
new_lines.append('        <div class="container">')
new_lines.append('          <div class="section-head"><span class="eyebrow">Route</span><h2>出行路线</h2><p>5 种主要出行方式，从机场 / 火车站 / 高铁 / 高速直达展馆</p></div>')
new_lines.append('          <ul class="route-list">${routesHtml}</ul>')
new_lines.append('        </div>')
new_lines.append('      </section>')
new_lines.append('      <section class="section alt">')
new_lines.append('        <div class="container">')
new_lines.append('          <div class="section-head"><span class="eyebrow">Hotels</span><h2>周边协议酒店</h2><p>预登记观众可凭确认短信享受协议价（示例数据）</p></div>')
new_lines.append('          <div class="grid grid-4">${ht}</div>')
new_lines.append('        </div>')
new_lines.append('      </section>`;')
new_lines.append('  }')

new_chunk = (NL.join(new_lines) + NL).encode('utf-8')

with open(MAIN_PATH, 'rb') as f:
    data = f.read()

# 起点：'function renderTravel' 必须带前导 2 空格缩进
start_marker = b'  function renderTravel() {'
i = data.find(start_marker)
# 终点：下一个 'function render'（register/home等）的开头（带 2 空格缩进）
end_marker = b'  function renderRegister()'
j = data.find(end_marker, i)
assert i >= 0 and j > i, f'start={i} end={j}'

old_chunk = data[i:j]  # 切到 next func 之前
print('old chunk size:', len(old_chunk), 'first 80:', old_chunk[:80], 'last 80:', old_chunk[-80:])

new_data = data[:i] + new_chunk + data[j:]
with open(MAIN_PATH, 'wb') as f:
    f.write(new_data)
print('written, new size:', len(new_data))

# JS 校验
import subprocess
r = subprocess.run([r'C:\Users\ASUS\.workbuddy\binaries\node\versions\22.22.2\node.exe', '--check', MAIN_PATH], capture_output=True, text=True)
print('node --check stdout:', r.stdout)
print('node --check stderr:', r.stderr)
print('exit:', r.returncode)
