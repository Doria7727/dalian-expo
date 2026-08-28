"""fix32b: 用 PIL 把文字区域用上下两侧纯净像素覆盖，再做平滑过渡
策略：
1) 文字 y≈15~155，x≈70~570
2) 上方纯净天空：y=0~10
3) 下方"建筑顶部"：y=180~200（建筑/天空交界的低建筑区）—— 这部分其实也是天空
4) 把文字区域用 y=0~10 的天空像素直接填充，然后 feather 一下边缘
"""
from PIL import Image
import numpy as np

SRC = r"C:\Users\ASUS\Desktop\2027大连工博会网站\assets\img\travel\travel-overview-raw.jpg"
DST = r"C:\Users\ASUS\Desktop\2027大连工博会网站\assets\img\travel\travel-overview.jpg"

pil = Image.open(SRC).convert("RGB")
arr = np.array(pil)
H, W, _ = arr.shape
print("size:", W, H)

# 文字行大致范围
y0, y1 = 12, 158   # 文字垂直区间（包含阴影）
x0, x1 = 60, 580   # 文字水平区间

# 取"文字上方"的天空中部 8 像素作为天空样本（y=0~8，整行平均）
sky_top = arr[0:8, :, :].mean(axis=0, keepdims=True)  # (1, W, 3)
# 取"文字下方"建筑区域上方 8 像素（y=170~178）作为低空样本
sky_low = arr[170:178, :, :].mean(axis=0, keepdims=True)  # (1, W, 3)

# 构造一个从 sky_top 到 sky_low 垂直渐变的 2D 数组 (H, W, 3)
# 渐变范围：从 y=0 到 y=H/2
ys = np.linspace(0, 1, num=max(y1, 1), dtype=np.float32)[:, None, None]  # (y1, 1, 1)
gradient = (1 - ys) * sky_top + ys * sky_low  # (y1, W, 3)
# 扩展到 y1 高度
# 把 arr 的对应行替换为 gradient
arr2 = arr.copy()
arr2[y0:y1, x0:x1, :] = np.broadcast_to(gradient[y0:y1], (y1 - y0, W, 3))[:, x0:x1, :]

# 为了让边缘自然，做一个轻微高斯模糊（用 PIL 的 filter）
out = Image.fromarray(arr2)

# 把替换区域用 5px 的边缘羽化
from PIL import ImageFilter
# 简单做法：先做一个蒙版，mask 内 0~255 渐变
mask = Image.new("L", (W, H), 0)
from PIL import ImageDraw
md = ImageDraw.Draw(mask)
# 内部 mask 全部 255，边缘做渐变（用 4 个矩形叠加模拟）
# 简化：内部填 255
md.rectangle([x0+8, y0+4, x1-8, y1-4], fill=255)
# 边缘羽化：再做一次 GaussianBlur
mask = mask.filter(ImageFilter.GaussianBlur(radius=8))

# 把 out 和 原图按 mask 合成
out2 = Image.composite(out, pil, mask)
out2.save(DST, "JPEG", quality=92, optimize=True)
print("saved:", DST)
import os
print("size:", os.path.getsize(DST))
