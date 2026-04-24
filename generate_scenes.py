#!/usr/bin/env python3
"""LP用の全シーン画像をNano Banana Proで一括生成"""
import os
import base64
import json
import urllib.request
import urllib.error
import sys

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise SystemExit("GEMINI_API_KEY not set")

SCENES = [
    (
        "01_qr_scan",
        """Warm illustration of a Japanese ramen restaurant interior at the checkout counter.
A young adult man (25, casual clothes) stands with his smartphone held up, scanning a colorful poster on the wall.
The poster shows bold text "🎰 ゲキッチャ 抽選" at the top, a large QR code in the middle, and text "LINE友達追加で激アツ抽選参加" at the bottom.
The man has a curious expression. Warm lighting, cozy ramen shop atmosphere with a bowl of ramen blurred on the counter.
Style: friendly Japanese manga/anime illustration, clean lines, vibrant warm colors (orange, cream, brown).
Aspect ratio 4:3. No text watermarks or extra labels."""
    ),
    (
        "02_line_friend",
        """A smartphone screen displayed vertically, centered in the frame.
The screen shows the LINE messaging app chat interface with an official account 'たなかラーメン' (ramen bowl icon avatar at top).
Chat bubbles visible:
 - 'こんにちは！🍜 田中ラーメンです'
 - '今なら【激アツ抽選】実施中！'
A prominent large orange-to-red gradient button at bottom reads '🎰 アンケートに参加する'.
Clean modern LINE UI, Japanese text rendered clearly and correctly, green LINE accent colors, white background.
Style: UI illustration, flat professional design.
Aspect ratio 4:3."""
    ),
    (
        "03_gekicha_open",
        """A smartphone screen showing a vibrant mobile app hero screen.
Background: bright radial gradient from golden yellow center to orange to crimson red edges, with light rays.
Top: a glossy chrome slot machine with '777' red reels and a gold frame.
Center: MASSIVE 3D puffy white Japanese text 'ゲキッチャ' with thick bright orange outline and deep red drop shadows, bubble letters.
Above the title: smaller text '激アツアンケート' in white with orange outline and star decorations ✦.
Below the title: white pill-shaped 'スタート ▶' button with shadow.
Floating around: gold coins, confetti, sparkles, stars.
Style: premium mobile game hero screen, crisp vector illustration, highly detailed.
Aspect ratio 4:3."""
    ),
    (
        "04_question_gauge",
        """A smartphone screen showing a survey quiz interface.
Top: small text 'Q1/8' and timer '⏱ 2秒'.
Middle-top: a white rounded card with a horizontal gauge bar filled 30% in orange-to-red gradient with a heart icon ❤️ and text '応援ゲージ'.
Center question: bold large Japanese text '今日、満足した？'
Four large rounded square emoji buttons in a row:
 1. 😍 with pink radial glow circle behind (label: 最高)
 2. 😄 with yellow radial glow (label: いい)
 3. 😐 with green radial glow (label: 普通)
 4. 😣 with purple radial glow (label: うーん)
Sparkle particles ✨⭐💫 flying in an arc from the first button toward the gauge with motion trails.
Cream/peach background with subtle sparkles.
Style: polished mobile app UI illustration.
Aspect ratio 4:3."""
    ),
    (
        "05_praise_popup",
        """A smartphone screen mid-animation.
A big white rounded popup card is popping up center-screen with a rotating yellow border and drop shadow.
Inside the popup: big emoji 👏 and huge bold Japanese text 'ナイス！' in orange 3D letters.
Behind the popup: the same survey quiz interface with emoji buttons slightly dimmed.
Star bursts ✨ radiating outward from the popup.
Top: the progress gauge is now 50% full, glowing.
Style: mobile game satisfaction feedback moment, joyful and rewarding.
Aspect ratio 4:3."""
    ),
    (
        "06_thanks_ticket",
        """A smartphone screen showing a celebration completion screen.
Background: brilliant radial gradient from golden yellow top to crimson red, with light rays.
Top-center: MASSIVE 3D golden Japanese letters 'ありがとう' with rich glittering metallic shine, red drop shadows, and surrounding pink cherry blossom petals 🌸 and hearts ❤️.
Middle: a large luxurious RED and GOLD lottery ticket shown mid-fall from the sky, rotated slightly, with motion blur trail. The ticket reads '抽選券 LOTTERY TICKET' with '#02374' printed on it.
Falling: gold coins 🪙, confetti streamers, more mini tickets in the background.
Bottom: text '📮 締切後にLINEで通知します！' in white with shadow.
Style: joyful luxurious celebration moment.
Aspect ratio 4:3."""
    ),
    (
        "07_waiting",
        """Three-panel manga-style illustration of a young Japanese man anticipating a lottery.
Panel 1: morning coffee at cafe, man checks phone with '抽選いつ？' thought bubble.
Panel 2: lunch at office desk, quickly glances at phone with 'まだかな' thought bubble.
Panel 3: evening on train, smiling with '日曜日だ！' thought bubble.
Soft muted colors with one warm orange accent highlighting the phone screens.
Style: friendly Japanese manga illustration, three horizontal panels side by side.
Aspect ratio 4:3."""
    ),
    (
        "08_notification",
        """Close-up of a smartphone resting on a dinner table in evening lighting.
The phone screen glows brightly showing a LINE notification banner:
 'たなかラーメン' official account
 '🎰 抽選の時間だよ！あなたの番号は出るか…？'
 Button: [確認する]
A hand is reaching down toward the phone with anticipation.
Background: blurred dinner table with a half-eaten ramen bowl in warm golden light.
Style: dramatic cinematic moment, soft focus background, warm orange glow.
Aspect ratio 4:3."""
    ),
    (
        "09_slot_reach",
        """Close-up smartphone screen showing an intense pachinko-style slot machine interface.
Three vertical reels visible:
 - Left reel: STOPPED on '7' in bold red
 - Middle reel: STOPPED on '7' in bold red
 - Right reel: SPINNING FAST with motion blur, showing vertical blur streaks of symbols
Background: dark dramatic red and black with lightning bolts ⚡ and red glow rays emanating outward.
Giant text at top of screen: '⚡リーチ！⚡' in bright yellow 3D letters with thick red outline, glowing.
Smaller text: 'あなたの番号：#02374' at top edge.
Flame/fire effects around the reels.
Style: high-stakes pachinko moment, maximum tension and excitement.
Aspect ratio 4:3."""
    ),
    (
        "10_win_coupon",
        """Explosive celebration smartphone screen.
Three '7's lined up in a row in red bold digits at top, surrounded by starburst rays.
Huge 3D gold text '🎉 777 WIN! 🎉' with 'おめでとう！' in rich golden puffy letters with red outline and stacked shadows.
Multi-colored confetti, fireworks, gold coins 🪙 bursting outward from the center.
Below: a large red and gold coupon ticket showing '🍜 ラーメン大盛 無料クーポン' with a bright orange '[受け取る]' button.
Style: jackpot win moment, maximum celebratory energy, gold and confetti everywhere.
Aspect ratio 4:3."""
    ),
    (
        "11_profile_input",
        """Smartphone screen showing a transition moment.
Top third: a small celebration with the won coupon '🎁 クーポン獲得！'
Middle: a clean profile input form appears, with a glowing highlight:
 Title: '🎁 賞品を受け取るために情報を入力'
 Fields:
  - お名前 [_____]
  - 年齢 [_____]
  - メール [_____]
  - [✓] 利用規約に同意
 Button: [登録する →] in orange
Right side of the form, a floating speech bubble annotation: '小さな当たりでも自然にプロフィール取得！' with an arrow pointing at the form.
Style: product explainer illustration with annotations, clean UI design, showing the business value clearly.
Aspect ratio 4:3."""
    ),
    (
        "12_repeat_cycle",
        """A circular flow diagram infographic.
Seven nodes arranged in a circle connected by glowing orange arrows flowing clockwise:
 1. 🏪 店舗 (shop)
 2. 📱 QR
 3. 👥 LINE友達追加
 4. 🎮 アンケート
 5. 🎫 抽選券
 6. 🎰 抽選演出
 7. 🎁 クーポン
 → back to 🏪 店舗
Each node is a small colorful circular badge icon. Bold flowing orange arrows with directional gradient.
Center of circle: large bold text 'リピートサイクル' in Japanese, with '激アツ抽選→再来店' subtitle.
Background: soft cream/peach gradient with subtle dotted pattern.
Style: clean friendly infographic, modern flat design.
Aspect ratio 4:3."""
    ),
]


def generate_scene(name, prompt):
    model = "gemini-3-pro-image-preview"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]}
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(f"  HTTP {e.code}: {err[:200]}", file=sys.stderr)
        return False

    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and "data" in inline:
                png_bytes = base64.b64decode(inline["data"])
                out = f"/Users/banmako/dev/アンケート/scenes/{name}.png"
                with open(out, "wb") as f:
                    f.write(png_bytes)
                print(f"  ✓ {name}.png ({len(png_bytes):,} bytes)")
                return True

    print(f"  ✗ no image in response for {name}", file=sys.stderr)
    return False


def main():
    print(f"Generating {len(SCENES)} scenes...")
    success = 0
    for i, (name, prompt) in enumerate(SCENES, 1):
        print(f"[{i}/{len(SCENES)}] {name}")
        # Skip if already exists (allow rerunning without regenerating)
        path = f"/Users/banmako/dev/アンケート/scenes/{name}.png"
        if os.path.exists(path) and os.path.getsize(path) > 10000:
            print(f"  (skip - exists)")
            success += 1
            continue
        if generate_scene(name, prompt):
            success += 1
    print(f"\nDone: {success}/{len(SCENES)}")


if __name__ == "__main__":
    main()
