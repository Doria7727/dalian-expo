"""fix32c: 裁掉上半部（带字），保留建筑航拍主体，再补少量天空 padding
"""
from PIL import Image
import numpy as np

SRC = r"C:\Users\ASUS\Desktop\2027大连工博会网站\assets\img\travel\travel-overview-raw.jpg"
DST = r"C:\Users\ASUS\Desktop\2027大连工博会网站\assets\img\travel\travel-overview.jpg"

pil = Image.open(SRC).convert("RGB")
W, H = pil.size
print("orig:", W, H)

# 文字在 y=12~155（连阴影），稳妥起见从 y=158 开始切
new_pil = pil.crop((0, 158, W, H))
nw, nh = new_pil.size
print("cropped:", nw, nh)

# 上方补 10px 纯天空色 padding（构图更紧凑）
# 天空色取原图最顶部居中一块的均值（避开建筑）
top_strip = np.array(pil.crop((280, 0, 360, 8)))
sky_color = top_strip.mean(axis=(0, 1)).astype(np.uint8)
print("sky_color:", sky_color)

pad_h = 10
final = Image.new("RGB", (nw, nh + pad_h), tuple(sky_color))
final.paste(new_pil, (0, pad_h))
final.save(DST, "JPEG", quality=92, optimize=True)
print("saved:", DST)
import os
print("size:", os.path.getsize(DST), "final", final.size)
