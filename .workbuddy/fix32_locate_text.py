"""定位文字像素位置（暗像素行/列密度峰值）"""
import sys
from PIL import Image
import numpy as np

PATH = r"C:\Users\ASUS\Desktop\2027大连工博会网站\assets\img\travel\travel-overview-raw.jpg"

im = Image.open(PATH).convert("RGB")
W, H = im.size
arr = np.array(im)
print("size:", W, H, "shape:", arr.shape)

# 文字是白底带阴影的实心白/浅色，背景是天空（蓝+白云），所以"文字"区域像素是
# 整块高亮且饱和度低（接近灰白）。
# 简单办法：找灰度 > 200 且 y < 0.45*H 的"行密度"
gray = arr.mean(axis=2)
bright = (gray > 200).astype(np.uint8)  # 浅色像素

# 每行亮像素数（只看上半部）
upper = bright[: int(H * 0.5)]
row_density = upper.sum(axis=1)

# 打印有 >50% 列亮的行
print("\n上半部高亮行(y, bright_count):")
for y in range(0, len(row_density)):
    if row_density[y] > W * 0.25:
        print(f"  y={y}: {row_density[y]}")
