#!/usr/bin/env python3
"""ゲキッチャのロゴをGemini Nano Banana Pro (Gemini 3 Pro Image) で生成"""
import os
import base64
import json
import urllib.request
import urllib.error

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise SystemExit("GEMINI_API_KEY not set")

PROMPT = """Create a high-quality Japanese mobile app logo banner.

Main text: "ゲキッチャ" (Japanese katakana, 5 characters) — MASSIVE bold 3D puffy letters taking up most of the width, centered.
- Pure white letter fill
- Thick bright orange outline (about 8px) around each letter
- Glossy light reflection highlight on the top half of each letter, like melted vinyl candy
- Deep stacked drop shadows beneath in red-to-dark-red gradient giving serious 3D depth
- Slight outward bulge / bubble-text style
- No line break, all 5 characters on one line

Secondary text above the main text: "激アツアンケート" in smaller clean bold white sans-serif with a subtle orange shadow. Decorative white horizontal lines with star sparkles (✦) flanking this subtitle on the left and right.

Style: playful, exciting Japanese mobile app promotional hero text, super vibrant pop style, like a hit mobile game logo. Commercial quality, crisp vector-like rendering.

Background: COMPLETELY TRANSPARENT (alpha channel PNG). No color fill behind the letters. Only the text elements visible.

Composition: Horizontal banner layout, centered. Leave some padding around the text. Output aspect ratio 3:2."""


def generate():
    model = "gemini-3-pro-image-preview"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"

    body = {
        "contents": [{
            "parts": [{"text": PROMPT}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"]
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {e.code}: {err}")

    # Extract image from response
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and "data" in inline:
                png_bytes = base64.b64decode(inline["data"])
                out = "/Users/banmako/dev/アンケート/gekiccha_logo.png"
                with open(out, "wb") as f:
                    f.write(png_bytes)
                print(f"Saved: {out} ({len(png_bytes):,} bytes)")
                return

    print("No image in response:")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])


if __name__ == "__main__":
    generate()
