# 🎰 ゲキッチャ（Gekiccha）

LINE公式アカウントと連携した「激アツ抽選アンケート」サービスのプロトタイプ。

**ライブデモ**: https://makoban.github.io/gekicha/
**LP / サービス説明**: https://makoban.github.io/gekicha/explain.html
**GitHub**: https://github.com/makoban/gekicha

---

## 🎯 サービス概要

店舗がLINE公式アカウントの友達に向けてアンケートを配信 → 回答者にだけ抽選権が発生 → 抽選日にパチンコ風の激アツ演出で当選/ハズレ発表 → 当選クーポン受取のためにプロフィール入力へ誘導、という「参加型くじ体験」。

### 最大のビジネスメリット
**「小さな当たり」でもプロフィール未入力ユーザーから情報を引き出せる**。
匿名LINE友達 → 名前・年齢・メール付き顧客DBへの自然な転換。

---

## 🗂 ファイル構成

```
.
├── index.html              # メインアプリ（アンケート + 抽選演出）
├── explain.html            # サービス説明LP（12シーンコンテ）
├── gekiccha.html           # 初期プロトタイプ（v0.1 相当、参考用）
│
├── gekiccha_logo.png       # ゲキッチャ ロゴ（透過PNG）
├── thanks_logo.png         # ありがとうロゴ（透過PNG、豪華版）
├── ticket_logo.png         # 抽選券 画像（透過PNG）
│
├── scenes/                 # LP用シーン画像 12枚
│   ├── 01_qr_scan.png          # QR発見
│   ├── 02_line_friend.png      # LINE友達追加
│   ├── 03_gekicha_open.png     # ゲキッチャ起動
│   ├── 04_question_gauge.png   # アンケートとゲージ
│   ├── 05_praise_popup.png     # 褒めポップ
│   ├── 06_thanks_ticket.png    # ありがとう＋抽選券
│   ├── 07_waiting.png          # 3日間の期待
│   ├── 08_notification.png     # LINE抽選通知
│   ├── 09_slot_reach.png       # 激アツリーチ
│   ├── 10_win_coupon.png       # WIN演出
│   ├── 11_profile_input.png    # ★プロフィール入力（最重要）
│   └── 12_repeat_cycle.png     # リピートサイクル図
│
├── generate_logo.py        # ゲキッチャロゴ生成（Gemini Nano Banana Pro）
├── generate_thanks.py      # ありがとうロゴ生成
├── generate_ticket.py      # 抽選券画像生成
├── generate_scenes.py      # 12シーン一括生成
├── remove_bg.py            # チェック柄→透過変換（PIL）
│
├── README.md               # このファイル
├── HANDOFF.md              # AI引き継ぎドキュメント
└── .gitignore
```

---

## 🛠 技術スタック

- **フロントエンド**: Vanilla HTML / CSS / JavaScript（フレームワーク不使用）
- **ホスティング**: GitHub Pages（`main` ブランチ直下を配信）
- **画像生成**: Google Gemini 3 Pro Image（通称 Nano Banana Pro）REST API
- **画像後処理**: Python + Pillow（PNG透過処理）
- **将来想定**:
  - LINE Messaging API（配信）
  - LIFF SDK（LINE内ブラウザでの `userId` 取得）
  - Firebase / Supabase 等（回答データ保存）

---

## 🚀 ローカル開発

```bash
# リポジトリのクローン
git clone https://github.com/makoban/gekicha.git
cd gekicha

# HTMLはそのままブラウザで開けば動く
open index.html

# または簡易サーバーで
python3 -m http.server 8000
# → http://localhost:8000
```

### LIFF確認

LIFF ID 発行後はURLパラメータで渡すと初期化される。

```bash
http://localhost:8000/index.html?liffId=YOUR_LIFF_ID
```

LINE内ブラウザでは `liff.getContext().userId` を回答ペイロードに含める。LIFF ID 未指定または初期化失敗時はデモモードでそのまま動く。

---

## 🎨 画像の再生成

Nano Banana Pro で画像を再生成したいとき：

```bash
# 環境変数セット（個別開発環境のキーを使用）
export GEMINI_API_KEY="your_key_here"

# 個別生成
python3 generate_logo.py      # → gekiccha_logo.png
python3 generate_thanks.py    # → thanks_logo.png
python3 generate_ticket.py    # → ticket_logo.png

# 一括でLP用シーン12枚生成
python3 generate_scenes.py    # → scenes/*.png

# 生成後は透過処理（チェック柄 → アルファ0）
python3 remove_bg.py          # → 対象画像を透過変換
```

生成スクリプトは **すでに存在するファイルはスキップ** するので、差分だけ再生成する場合は対象ファイルを先に削除する。

---

## 📦 デプロイ

push すれば GitHub Pages が自動で配信する（`main` ブランチ直下）。

```bash
git add -A
git commit -m "説明的なメッセージ"
git push
# → 1〜2分で https://makoban.github.io/gekicha/ に反映
```

---

## 📖 詳細は

- **AI での作業継続**: [HANDOFF.md](HANDOFF.md) を参照
- **ユーザー体験の全体像**: [explain.html](https://makoban.github.io/gekicha/explain.html) を参照

---

© 2026 makoban / ゲキッチャ
