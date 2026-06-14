# Repository Rules

- 旅行データは `trips/<trip-id>/` に置き、git に含めない。
- ユーザーには、なるべくコマンド実行を求めない。基本は会話だけで進める。
- 新しい旅行を始めるときは、Codex 側で `trips/<trip-id>/` を自動作成してから作業を始める。
- public HTML を作る前に `README.md` と `specs/html-ui.md` を読む。
- public HTML は `public/site.json` から生成し、時刻入り日程や詳細スポットページを出さない。
- `outputs/places.md` と `outputs/itinerary.md` は private 運用前提で扱う。
