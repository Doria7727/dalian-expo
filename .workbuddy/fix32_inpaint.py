"""fix32: 去掉 travel-overview-raw.jpg 上'大连自贸区国际会展中心 展会计划'两行字
策略：cv2.inpaint (Telea) + 手工 mask
"""
import cv2
import numpy as np
from PIL import Image

SRC = r"C:\Users\ASUS\Desktop\2027大连工博会网站\assets\img\travel\travel-overview-raw.jpg"
DST = r"C:\Users\ASUS\Desktop\2027大连工博会网站\assets\img\travel\travel-overview.jpg"

# 路径有中文，cv2.imread 不行，用 PIL+numpy 读
pil = Image.open(SRC).convert("RGB")
img_bgr = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
img = img_bgr  # alias for downstream code
H, W = img.shape[:2]
print("size:", W, H)

# 文字位置（目测估）：两行白色字 + 阴影
# 第一行 "大连自贸区国际会展中心"
# 第二行 "展会计划"
mask = np.zeros((H, W), dtype=np.uint8)
# 在每行文字外扩 ~10 像素，确保覆盖阴影
mask[20:90, 70:570] = 255      # 第一行（包含阴影）
mask[90:155, 215:425] = 255    # 第二行（包含阴影）

# cv2.inpaint (Telea 算法擅长边缘处小区域)
out = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)
# 也试 NS 算法的备份（如果 Telea 不够好）—— 这里直接用 Telea 即可

# 写出时用 PIL（同样避免 cv2 中文路径问题）
out_rgb = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
Image.fromarray(out_rgb).save(DST, "JPEG", quality=92, optimize=True)
print("saved:", DST)

# 同时清掉 raw 中间产物
import os
os.remove(SRC)
print("removed raw:", SRC)

# 输出文件大小
print("file size:", os.path.getsize(DST), "bytes")
