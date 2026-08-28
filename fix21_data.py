#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix21_data.py: 重写 TRANSPORT 为新结构"""
import sys

DATA_PATH = r'C:\Users\ASUS\Desktop\2027大连工博会网站\assets\js\data.json'

with open(DATA_PATH, 'rb') as f:
    data = f.read()

i = data.find(b'  "TRANSPORT": ')
end_marker = b'],\r\n  "HOTELS": ['
j = data.find(end_marker)
assert i >= 0 and j >= 0

NL = '\r\n'
def line(indent_s, s):
    return (indent_s + s + NL).encode('utf-8')

new_lines = []
new_lines.append(line('  ', '"TRANSPORT": {'))
new_lines.append(line('    ', '"intro": "大连自贸区国际会展中心地理位置优越，环境优美，毗邻城市主干道，交通便捷。"'))
new_lines.append(line('    ', '"addr": "大连市保税区爱港路 18 号",'))
new_lines.append(line('    ', '"distances": ['))
distances = [
    ("地铁 3 号线", "3 公里", "保税区轻轨站"),
    ("大窑湾高速口", "3 公里", "沈大、鹤大高速"),
    ("大连火车站", "2 公里", "市内主要铁路"),
    ("大连北站", "19 公里", "哈大高铁"),
    ("大连机场", "26 公里", "周水子国际机场"),
]
for label, value, note in distances:
    new_lines.append(line('      ', '{"label": "%s", "value": "%s", "note": "%s"},' % (label, value, note)))
new_lines.append(line('    ', '],'))
new_lines.append(line('    ', '"routes": ['))
routes = [
    (1, "免费接驳巴士", "地铁 3 号线保税区站 ↔ 展馆"),
    (2, "大连国际机场 → 大连自贸区国际会展中心", "乘坐机场大巴至大连北站 → 转乘公交 2001 路至保税区南门 → 转乘公交（保税区管委会至东风日产）到会展中心站下车"),
    (3, "大连火车站 → 大连自贸区国际会展中心", "乘坐地铁 3 号线至保税区站 → 接驳大巴 / 乘坐公交 2001 路至保税区南门 → 转乘公交（保税区管委会至东风日产）到会展中心站下车"),
    (4, "大连北站（高铁站） → 大连自贸区国际会展中心", "乘坐公交 2001 路至保税区南门 → 转乘公交（保税区管委会至东风日产）到会展中心站下车"),
    (5, "高速 → 大连自贸区国际会展中心", "鹤大高速大连湾出口 → 海滨大道 → 黄海路 → 中港路 → 爱港路 → 到达大连自贸区国际会展中心"),
]
for num, title, desc in routes:
    new_lines.append(line('      ', '{"num": %d, "title": "%s", "desc": "%s"},' % (num, title, desc)))
new_lines.append(line('    ', ']'))
new_lines.append(line('  ', '},'))

new_chunk = b''.join(new_lines)

new_data = data[:i] + new_chunk + data[j+len(end_marker):]
with open(DATA_PATH, 'wb') as f:
    f.write(new_data)
print('written, new size:', len(new_data))

# JSON 校验
import json
with open(DATA_PATH, 'rb') as f:
    text = f.read()
d = json.loads(text)
print('parse OK, keys:', list(d.keys()))
print('TRANSPORT keys:', list(d['TRANSPORT'].keys()))
print('distances:', len(d['TRANSPORT']['distances']))
print('routes:', len(d['TRANSPORT']['routes']))
