#!/usr/bin/env python3
"""「ありがとう」ロゴをNano Banana Proで生成"""
import os
import base64
import json
import urllib.request
import urllib.error

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise SystemExit("GEMINI_API_KEY not set")

PROMPT = """Create an ULTRA-LUXURIOUS Japanese celebration logo.

Main text: "ありがとう" (Japanese hiragana, 5 characters) — MASSIVE bold 3D puffy letters taking up most of the image width, centered.
- GOLDEN metallic fill like polished 24k gold foil, with brilliant shine and highlights
- Thick rich crimson-to-orange gradient outline (about 10px) around each letter
- Diamond-crystal glossy reflections, mirror-bright highlights
- Deep stacked 3D drop shadows beneath — dark red to black gradient for premium depth
- Shimmering gold glitter and sparkle dust across every letter surface
- Bubble text style with puffy rounded form, extra ornate
- No line break, all 5 characters on one line

Decorative elements (rich and abundant):
- Bright gold stars ⭐ and radiating sparkles ✨ around the letters
- Small rose-gold hearts ❤️ scattered in varied sizes
- Pink cherry blossom petals 🌸 floating
- Gold confetti streamers and ribbons
- Bright white light rays emanating from behind the text
- Crystal diamonds 💎 accent pieces

Style: ULTRA-PREMIUM, heartfelt, luxurious Japanese celebration, like winning a Grand Prize jackpot. Super vibrant and warm. Commercial-grade quality, ultra-crisp detail rendering. Think high-end mobile game victory screen.

Background: COMPLETELY TRANSPARENT (alpha channel PNG). No color fill behind the letters.

Composition: Horizontal banner layout, centered. Leave padding around text. Output aspect ratio 3:2."""


def generate():
    model = "gemini-3-pro-image-preview"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"

    body = {
        "contents": [{"parts": [{"text": PROMPT}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]}
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

    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and "data" in inline:
                png_bytes = base64.b64decode(inline["data"])
                out = "/Users/banmako/dev/アンケート/thanks_logo.png"
                with open(out, "wb") as f:
                    f.write(png_bytes)
                print(f"Saved: {out} ({len(png_bytes):,} bytes)")
                return

    print("No image in response:")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])


if __name__ == "__main__":
    generate()
