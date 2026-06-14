# Agent Request

ユーザーは、基本的に会話で `行き先` `行きたい場所` `日数` `条件` を渡すだけでよいです。

必要なら Codex が会話内容を `inputs/` に整理してから、以下を作ってください。

- `outputs/places.md`
- `outputs/itinerary.md`
- `public/site.json`

条件:

- 行きたい場所は自分で調べて補完する
- 営業時間、休業日、移動しやすさを確認する
- 日程は同じエリアをまとめて組む
- public 用の `site.json` には時刻、予約、連絡先、個人情報を入れない
