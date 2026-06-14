---
name: travel-trip-intake
description: >-
  旅行 planning を始めるときに使う。ユーザーが行き先、日数、行きたい場所、
  条件を話し始めたら使い、会話から既知情報を整理し、不足分だけ確認して
  `scripts/create_trip.py` で `trips/<trip-id>/` を作成し、
  `inputs/wishlist.md` `inputs/trip_overview.md` `inputs/planning_rules.md`
  を埋める。
---

# Travel Trip Intake

この skill は、新しい旅行の入力整理に使う。

## いつ使うか

- 旅行を始めたい
- 行きたい場所を整理したい
- trip の雛形を作りたい

## 最初に読むもの

- `references/intake-rules.md`
- `../../../scripts/create_trip.py`
- `../../../templates/trip-template/`

## やること

- 会話から既知の条件を整理する
- 足りない情報だけ質問する
- `scripts/create_trip.py` を使って `trips/<trip-id>/` を作る
- `inputs/wishlist.md` を埋める
- `inputs/trip_overview.md` を埋める
- `inputs/planning_rules.md` を埋める

## やらないこと

- `outputs/` はまだ作らない
- public HTML はまだ作らない

## 完了条件

- `trips/<trip-id>/inputs/` が作成済み
- `wishlist.md` `trip_overview.md` `planning_rules.md` が埋まっている

## 完了後

作成した `trip-id` を伝え、次は `travel-itinerary-planner` を使うよう案内する。
