# Repository Rules

- 新しい旅行を始めるときは、まず `.agents/skills/travel-trip-intake` を使う
- trip の入力整理が終わったら `.agents/skills/travel-itinerary-planner` を使う
- 公開ページが必要なときだけ `.agents/skills/travel-public-html` を使う
- ユーザーには極力コマンド実行を求めず、会話ベースで進める
- `trips/<trip-id>/` は private planning 用で、コミットしない
- public HTML の正本は `specs/html-ui.md`
- public HTML 作成では `scripts/build_site.py` と `scripts/validate_site.py` を使う
- public 側には時刻、予約番号、航空券番号、電話番号、実名を出さない
