# Agent Instructions

AIエージェント（Codex / Claude / Cursor 等）がこのリポジトリで作業する際の指示。

## 最初に読むべきファイル

1. **[HANDOFF.md](HANDOFF.md)** — プロジェクト全体像・設計判断・未実装タスク
2. **[README.md](README.md)** — 技術スタックとセットアップ

## 作業する前に

1. ユーザーの言葉を字義通り受け取る（「〜してほしい」は指示）
2. 動くものを先に出す、長い説明は後
3. `position: relative` を `.quiz` や `#complete` に追加しない（画面が崩れる既知のバグ）

## デプロイ

`git push` だけで GitHub Pages に自動反映（`main` ブランチ直下）。

```bash
git add -A
git commit -m "説明的なメッセージ"
git push
# → https://makoban.github.io/gekicha/ に1〜2分で反映
```

## 秘密情報

- API キーは `/Users/banmako/dev/.env.txt` にあり、**このリポジトリには含めない**
- `GEMINI_API_KEY` は画像生成に必要、シェルに `export` して使う

## 画像生成コマンド

```bash
export $(grep -E "^GEMINI_API_KEY=" /Users/banmako/dev/.env.txt | xargs)
python3 generate_scenes.py  # or generate_logo.py / generate_thanks.py / generate_ticket.py
```

生成後は `python3 remove_bg.py` でチェック柄を透過に変換（対象ファイル名はスクリプト内で指定）。

## バージョン番号

`index.html` と `explain.html` の右下/左下に `v0.x.y · YYYY.MM.DD` の表記あり。
機能追加ごとにマイナー上げ、小修正はパッチ。
