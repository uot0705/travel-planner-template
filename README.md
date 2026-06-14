# Travel Planner Template

国内外どちらの旅行でも使える、`private データ` と `public 公開物` を分けた旅行計画テンプレです。

## 方針

- このリポに置くのは `テンプレ / スクリプト / 公開してよい仕様` だけ
- 実旅行データは `trips/<trip-id>/` に置く
- `trips/` 配下は git に上げない
- 公開 HTML は `要約-only` にする

## public に上げてよいもの

- このテンプレの使い方
- 公開ページの作り方
- UI や公開ルールの仕様
- 個人情報を含まない雛形ファイル
- 個人情報を含まないサンプルデータ
- 公開ページを生成するためのスクリプトや見た目のコード

## public に上げないもの

- `trips/` 配下の実データ
- チケット、PDF、スクリーンショット
- 氏名、電話番号、メール、緊急連絡先
- 予約番号、航空券番号、予約詳細
- 分刻みの日程
- スポット詳細ページ用の内部調査メモ

## 最短の使い方

1. ユーザーが Codex に `行き先` `行きたい場所` `旅行日数` `条件` を伝える
2. Codex が `trips/<trip-id>/` を作って、会話内容を `inputs/` に整理する
3. Codex がスポットを調べて `outputs/places.md` と `outputs/itinerary.md` を作る
4. 公開用ページが必要なときだけ、Codex が `public/site.json` を作って `docs/` を更新する

ユーザーが毎回コマンドを打つ前提ではなく、基本は会話だけで進める想定です。

`trips/` は ignore 済みなので、Codex がここに作った実データはそのままでは git に入りません。

## trips の中身

```text
trips/<trip-id>/
  inputs/
    wishlist.md
    trip_overview.md
    planning_rules.md
  outputs/
    places.md
    itinerary.md
  public/
    site.json
  private/
    README.md
```

## public HTML ルール

HTML を作る前に `specs/html-ui.md` を確認すること。公開ページの内容・UI・禁止事項はそちらを正本とします。

## コマンド

通常は Codex が内部で実行すればよく、ユーザーが意識しなくてよいコマンドです。

デモの public ページを生成:

```bash
python3 scripts/build_site.py
python3 scripts/validate_site.py
```

特定の旅行フォルダから public ページを生成:

```bash
python3 scripts/build_site.py trips/<trip-id>
python3 scripts/validate_site.py trips/<trip-id>
```

## 補足

- `trips/` はすべて local private データ用です
- root の `docs/` は public に出してよい内容だけを置く前提です
