# -*- coding: utf-8 -*-
"""fix38: 用用户给的干净文字重写 TRANSPORT.addr + TRANSPORT.routes，
修正之前 OCR 错字（家业机场大巴/崇意/保税区西 等）。仅替换这两处，保留其余格式。"""
import re

PATH = r"C:\Users\ASUS\Desktop\2027大连工博会网站\assets\js\data.json"

with open(PATH, "r", encoding="utf-8") as f:
    raw = f.read()

# 行尾探测
NL = "\r\n" if "\r\n" in raw[:2000] else "\n"
print("行尾:", "CRLF" if NL == "\r\n" else "LF")

# 1) 地址：去掉空格
old_addr = '"addr": "大连市保税区爱港路 18 号",'
new_addr = '"addr": "大连市保税区爱港路18号",'
assert raw.count(old_addr) == 1, f"addr 出现 {raw.count(old_addr)} 次"
raw = raw.replace(old_addr, new_addr)
print("addr 已替换")

# 2) routes 数组整体替换
m = re.search(r'"routes"\s*:\s*\[.*?\]', raw, re.S)
assert m, "未找到 routes 数组"
print("匹配到 routes 段，长度:", m.end() - m.start())

new_routes = (
    '"routes": [' + NL +
    '      {"num": 1, "title": "免费接驳巴士", "desc": "地铁3号线保税区站→展馆"},' + NL +
    '      {"num": 2, "title": "大连国际机场 → 大连自贸区国际会展中心", "desc": "乘坐机场大巴至大连北站 → 转乘公交2001路到保税区南门 → 转乘公交（保税区管委会至东风日产）到会展中心站下车"},' + NL +
    '      {"num": 3, "title": "大连火车站 → 大连自贸区国际会展中心", "desc": "乘坐地铁3号线至保税区站 → 接驳大巴/乘坐公交2001路至保税区南门 → 转乘公交（保税区管委会至东风日产）到会展中心站下车"},' + NL +
    '      {"num": 4, "title": "大连北站（高铁站）→ 大连自贸区国际会展中心", "desc": "乘坐公交2001路至保税区南门 → 转乘公交（保税区管委会至东风日产）到会展中心站下车"},' + NL +
    '      {"num": 5, "title": "高速 → 大连自贸区国际会展中心", "desc": "鹤大高速大连港出口 → 海港大道 → 黄海路 → 中港路 → 爱港路 → 到达大连自贸区国际会展中心"}' + NL +
    '    ]'
)

raw = raw[:m.start()] + new_routes + raw[m.end():]

# 校验 JSON 合法
import json
json.loads(raw)
print("JSON 校验通过")

with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(raw)
print("已写回")
