# Travel Planner Template

このリポジトリは、旅行の private planning と public-safe な共有ページ作成を分けて進めるためのテンプレートです。

ユーザーは Codex に次を話すだけで始められます。

- 行き先
- 行きたい場所
- 日数
- 条件や希望

## 使う Skill

1. `travel-trip-intake`
2. `travel-itinerary-planner`
3. 必要なときだけ `travel-public-html`

## Skill の役割

`travel-trip-intake`
会話から旅行条件を整理し、`scripts/create_trip.py` を使って `trips/<trip-id>/` を作り、`inputs/` を埋めます。

`travel-itinerary-planner`
`inputs/` をもとに調査と日程作成を行い、`outputs/places.md` と `outputs/itinerary.md` を作ります。

`travel-public-html`
private の旅程を public-safe な要約に変換し、`public/site.json` を作って `docs/` を更新します。

## データの分け方

- `trips/<trip-id>/` は private planning 用です
- `docs/` は public-safe な共有物だけを置きます
- public HTML の正本は `specs/html-ui.md` です

public 側には、時刻、予約番号、航空券番号、電話番号、実名を出しません。

## 内部メモ

- trip 作成: `scripts/create_trip.py`
- site build: `scripts/build_site.py`
- site validate: `scripts/validate_site.py`
