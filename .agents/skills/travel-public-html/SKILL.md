---
name: travel-public-html
description: >-
  private planning から public-safe な共有ページを作るときに使う。
  ユーザーが公開ページや要約 HTML を求めたら使い、
  `trips/<trip-id>/outputs/` を読んで `public/site.json` を作成し、
  `specs/html-ui.md` を正本として `scripts/build_site.py` と
  `scripts/validate_site.py` で `docs/` を更新する。時刻、予約番号、
  航空券番号、電話番号、実名は public に出さない。
---

# Travel Public HTML

この skill は、private planning の内容を public-safe な共有ページに変換するときに使う。

## いつ使うか

- 公開ページを作りたい
- 要約 HTML を作りたい
- public-safe な旅行ページを作りたい

## 最初に読むもの

- `references/public-html-rules.md`
- `../../../specs/html-ui.md`
- `trips/<trip-id>/outputs/`

## やること

- `outputs/` を読む
- `public/site.json` を作る
- `specs/html-ui.md` に沿って `docs/` を更新する
- `scripts/build_site.py` を使う
- `scripts/validate_site.py` を使う
- public に出してはいけない情報がないか確認する

## 完了条件

- `public/site.json` がある
- `docs/` が更新されている
- private 情報が public 側に残っていない

## 完了後

生成したファイルと、伏せた情報・一般化した情報を伝える。
