# テーブル定義書

## テーブル概要

| 項目 | 内容 |
|---|---|
| テーブル物理名 | `transactions` |
| テーブル論理名 | 家計簿取引 |
| 概要 | 日々の収支データを1件1行で管理する |
| 作成日 | 2026-08-11 |
| 更新日 | 2026-08-11 |

## カラム定義

| No | 物理名 | 論理名 | データ型 | 桁数/長さ | NULL許可 | PK | FK参照先 | デフォルト値 | 備考 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 取引ID | INTEGER | - | NOT NULL | ○ | - | AUTOINCREMENT | 主キー |
| 2 | transaction_date | 取引日 | DATE | - | NOT NULL | - | - | - | YYYY-MM-DD形式 |
| 3 | category | カテゴリ | TEXT | 50 | NOT NULL | - | categories.name | - | 例: 食費, 交通費 |
| 4 | amount | 金額 | INTEGER | - | NOT NULL | - | - | - | 円単位。支出はマイナス等、符号ルールを別途決める |
| 5 | payment_method | 支払方法 | TEXT | 30 | NULL許可 | - | - | NULL | 例: 現金, クレジットカード |
| 6 | memo | メモ | TEXT | 200 | NULL許可 | - | - | NULL | 自由記述 |
| 7 | created_at | 登録日時 | TIMESTAMP | - | NOT NULL | - | - | CURRENT_TIMESTAMP | レコード作成時刻（自動） |
| 8 | updated_at | 更新日時 | TIMESTAMP | - | NULL許可 | - | - | NULL | 編集時に更新（未編集ならNULL） |

## インデックス

| No | インデックス名 | 対象カラム | 種別 | 目的 |
|---|---|---|---|---|
| 1 | idx_transactions_date | transaction_date | 通常 | 期間検索・月次集計の高速化 |

## 制約・ルール

- `amount` は円単位の整数で統一する（小数は扱わない）
- `category` はある程度カテゴリを固定化したい場合、将来的に `categories` テーブルへ外部キー化する想定
- 論理削除は行わず、物理削除のみとする（家計簿という性質上、履歴保持の必要性は低いため）

## 変更履歴

| 日付 | 変更内容 | 変更者 |
|---|---|---|
| 2026-08-11 | 初版作成 | NAOKI |
