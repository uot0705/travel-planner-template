# Intake Rules

## Trigger

- 旅行を始めたい
- 行きたい場所を整理したい
- trip の雛形を作りたい

## まず整理する情報

- 行き先
- 日数または日付範囲
- 行きたい場所ややりたいこと
- 予算、ペース、同行者、食事、移動などの条件

## 質問のしかた

- まず会話中に出ている情報を抽出する
- 足りない情報だけ聞く
- すでに答えたことを聞き直さない
- ユーザーにコマンド実行は求めない

## trip-id の付け方

- ASCII の kebab-case を使う
- 月が分かるなら `<YYYYMM>-<destination-slug>`
- まだ曖昧なら `<destination-slug>-draft`
- slug 化しづらいなら `trip-<YYYYMMDD>`

## 作成手順

1. trip-id を決める
2. `scripts/create_trip.py` を使って `trips/<trip-id>/` を作る
3. `inputs/wishlist.md` を埋める
4. `inputs/trip_overview.md` を埋める
5. `inputs/planning_rules.md` を埋める

## Done

- 入力ファイル 3 つが埋まっている
- itinerary や public 出力には進んでいない

## 最後の案内

- 作成した `trip-id` と path を伝える
- 次は `travel-itinerary-planner` と案内する
