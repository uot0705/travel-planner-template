# Public HTML Rules

## Trigger

- 公開ページを作りたい
- 要約 HTML を作りたい
- public-safe な旅行ページを作りたい

## 入力

- `outputs/places.md`
- `outputs/itinerary.md`
- 必要なら `inputs/`

## 正本

- `specs/html-ui.md`

## public に出してはいけない情報

- 正確な時刻
- timed itinerary
- 予約番号
- 航空券番号
- 電話番号
- メールアドレス
- 実名
- private な連絡先
- 個別すぎる内部メモ

## 変換ルール

- 正確な時刻は `朝` `昼` `夕方` `夜` に丸めるか、省略する
- 予約番号は出さず、必要なら `予約あり` `事前予約推奨` にする
- 宿や交通の細かい private 情報は public-safe な粒度に落とす

## 作業手順

1. `public/site.json` を作る
2. `scripts/build_site.py` を使って `docs/` を更新する
3. `scripts/validate_site.py` を通す
4. `specs/html-ui.md` とズレていないか確認する
5. 残っている private 情報を除去する

## Done

- `public/site.json` がある
- `docs/` が更新済み
- forbidden 情報が public 側にない

## 最後の案内

- 生成したものを伝える
- 伏せた情報、一般化した情報を伝える
