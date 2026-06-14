# Planning Rules

## Trigger

- 日程を組みたい
- 旅程を作りたい
- 行きたい場所を元にプラン化したい

## 読む入力

- `inputs/wishlist.md`
- `inputs/trip_overview.md`
- `inputs/planning_rules.md`

## 調査の優先順位

1. 営業時間と休業日
2. 予約済みや固定予定の制約
3. エリアまとまりと移動しやすさ
4. 体力、予算、食事、休憩バランス

## 進め方

- まず候補地をエリアでまとめる
- 旅程に入れる前に営業時間を確認する
- 1 日に詰め込みすぎない
- 足りない情報は、本当に blocking のときだけ聞く

## `outputs/places.md` に入れること

- 候補地名
- エリア
- なぜ入れるか
- 営業時間や休業日
- 予約メモ
- 旅の条件との相性

## `outputs/itinerary.md` に入れること

- day ごとの private itinerary
- 移動順
- 必要なら時刻
- 予備案や代替候補

## やらないこと

- public JSON は作らない
- `docs/` は触らない

## Done

- `places.md` と `itinerary.md` がある
- 大きな矛盾が残っていない

## 最後の案内

- 作成した出力を伝える
- 公開ページが必要なら `travel-public-html` と案内する
