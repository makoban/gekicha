#!/usr/bin/env python3
"""豪華抽選券ロゴをNano Banana Proで生成"""
import os
import base64
import json
import urllib.request
import urllib.error

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise SystemExit("GEMINI_API_KEY not set")

PROMPT = """Create an ULTRA-LUXURIOUS Japanese lottery ticket (抽選券) design.

Design specifications:
- Horizontal rectangular premium lottery ticket with classic serrated edges on both left and right sides
- Rich GOLDEN ornate decorative frame with ornate corner flourishes
- Deep crimson red background with subtle Japanese traditional patterns (seigaiha waves OR asanoha hemp leaves) in darker red
- Bold gold kanji text "抽選券" at the top center, large, with decorative flourishes and glossy metallic shine
- Below that, smaller gold English text "LOTTERY TICKET"
- A decorative red hanko/stamp accent "当選" in the top-right corner
- Gold decorative swirls, cherry blossoms 🌸, and stars scattered elegantly
- Glossy premium metallic finish with light reflections
- Raised embossed 3D look with subtle drop shadows
- Overall feel: like a traditional Japanese omikuji fortune slip but premium Grand Prize quality

Color scheme: brilliant gold (#FFD700, #DAA520) + deep red (#8B0000, #A52A2A) + cream highlights

Style: luxurious traditional Japanese yet modern design, premium prize ticket. Ultra crisp rendering. Photorealistic metallic shine.

Background: COMPLETELY TRANSPARENT (alpha channel PNG). Only the ticket visible, no surrounding color fill.

Composition: Centered horizontal ticket filling most of the image width. Aspect ratio 3:2. Clean edge separation from transparent background."""


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
                out = "/Users/banmako/dev/アンケート/ticket_logo.png"
                with open(out, "wb") as f:
                    f.write(png_bytes)
                print(f"Saved: {out} ({len(png_bytes):,} bytes)")
                return

    print("No image in response:")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])


if __name__ == "__main__":
    generate()
