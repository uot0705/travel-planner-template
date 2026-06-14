# Travel Planner Template

国内外どちらの旅行でも使える、`private データ` と `public 公開物` を分けた旅行計画テンプレです。

## 方針

- このリポに置くのは `テンプレ / スクリプト / 公開してよい仕様` だけ
- 実旅行データは `trips/<trip-id>/` に置く
- `trips/` 配下は git に上げない
- 公開 HTML は `要約-only` にする

## public に上げてよいもの

- `scripts/`
- `site_src/`
- `specs/`
- `templates/`
- `examples/`
- `docs/`
- この `README.md`

## public に上げないもの

- `trips/` 配下の実データ
- チケット、PDF、スクリーンショット
- 氏名、電話番号、メール、緊急連絡先
- 予約番号、航空券番号、予約詳細
- 分刻みの日程
- スポット詳細ページ用の内部調査メモ

## 最短の使い方

1. このリポを clone する
2. `cp -R templates/trip-template trips/<trip-id>` で雛形を作る
3. 最低限 `inputs/wishlist.md` に行きたい場所を書く
4. 必要なら `inputs/trip_overview.md` に旅程条件を書く
5. エージェントに `REQUEST.md` の内容で依頼する
6. 公開用ページが必要なら `public/site.json` を埋めて `python3 scripts/build_site.py trips/<trip-id>` を実行する

`trips/` は ignore 済みなので、ここに置いた実データはそのままでは git に入りません。

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

- 1ページ完結を基本にする
- 載せるのは `概要 / エリア / カテゴリ / 持ち物 / 予算の大枠` まで
- `時刻入り日程` は載せない
- `スポット詳細ページ` は作らない
- `ホテル / 航空券 / 予約 / 連絡先 / 実名` は載せない

HTML を作る前に `specs/html-ui.md` を確認すること。

## コマンド

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
