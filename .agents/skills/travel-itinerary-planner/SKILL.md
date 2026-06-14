---
name: travel-itinerary-planner
description: >-
  入力済み trip をもとに private itinerary を作るときに使う。
  ユーザーが日程を組みたい、旅程を作りたい、行きたい場所をプラン化したい
  と言ったら使い、`trips/<trip-id>/inputs/` を読んで営業時間、休業日、
  固定予定、移動しやすさを確認しながら
  `outputs/places.md` と `outputs/itinerary.md` を作成する。
---

# Travel Itinerary Planner

この skill は、入力済み trip から調査と日程作成を進めるために使う。

## いつ使うか

- 日程を組みたい
- 旅程を作りたい
- 行きたい場所を元にプラン化したい

## 最初に読むもの

- `references/planning-rules.md`
- `trips/<trip-id>/inputs/`

## やること

- `inputs/` を読む
- 営業時間と休業日を確認する
- 移動しやすさとエリアまとまりを確認する
- `outputs/places.md` を作る
- `outputs/itinerary.md` を作る

## やらないこと

- `public/site.json` はまだ作らない
- `docs/` はまだ更新しない

## 完了条件

- `outputs/places.md` がある
- `outputs/itinerary.md` がある
- 主要な営業日や動線の矛盾が整理されている

## 完了後

公開ページが必要なら `travel-public-html` を使うよう案内する。
