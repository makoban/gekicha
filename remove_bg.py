#!/usr/bin/env python3
"""チェック柄の背景を検出して透過に変換"""
from PIL import Image

img = Image.open("gekiccha_logo.png").convert("RGBA")
pixels = img.load()
w, h = img.size

changed = 0
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        # Detect grayish pixels (the checker pattern)
        is_gray = abs(r - g) < 20 and abs(g - b) < 20 and abs(r - b) < 20
        if is_gray and 50 < r < 240:
            pixels[x, y] = (r, g, b, 0)
            changed += 1

img.save("gekiccha_logo.png")
print(f"Converted {changed:,} pixels to transparent")
