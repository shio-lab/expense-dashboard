# テーブル定義書

## テーブル概要

| 項目 | 内容 |
|---|---|
| テーブル物理名 | `payroll_monthly` |
| テーブル論理名 | 給与明細(月次) |
| 概要 | 毎月の給与明細を1件1行で管理する |
| 作成日 | 2026-08-12 |
| 更新日 | 2026-08-12 |

## カラム定義

| No | 物理名 | 論理名 | データ型 | 桁数/長さ | NULL許可 | PK | FK参照先 | デフォルト値 | 備考 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 給与明細ID | INTEGER | - | NOT NULL | ○ | - | AUTOINCREMENT | 主キー |
| 2 | payment_date | 支給日 | DATE | - | NOT NULL | - | - | - | YYYY-MM-DD形式 |
| 3 | base_salary | 基本給 | INTEGER | - | NOT NULL | - | - | - | 円単位 |
| 4 | overtime_allowance | 時間外手当 | INTEGER | - | NOT NULL | - | - | 0 | 円単位 |
| 5 | other_allowance | その他給与 | INTEGER | - | NOT NULL | - | - | 0 | 円単位 |
| 6 | rent_deduction | 家賃 | INTEGER | - | NOT NULL | - | - | 0 | 社宅・寮費等の控除。円単位 |
| 7 | employment_insurance | 雇用保険 | INTEGER | - | NOT NULL | - | - | 0 | 控除額。円単位 |
| 8 | employee_pension | 厚生年金 | INTEGER | - | NOT NULL | - | - | 0 | 控除額。円単位 |
| 9 | health_insurance_basic | 健康保険(基本) | INTEGER | - | NOT NULL | - | - | 0 | 控除額。円単位 |
| 10 | health_insurance_special | 健康保険(特定) | INTEGER | - | NOT NULL | - | - | 0 | 特定保険料分。円単位 |
| 11 | child_support_contribution | 子ども・子育て支援金 | INTEGER | - | NOT NULL | - | - | 0 | 円単位 |
| 12 | income_tax | 所得税 | INTEGER | - | NOT NULL | - | - | 0 | 源泉徴収額。円単位 |
| 13 | resident_tax | 住民税 | INTEGER | - | NOT NULL | - | - | 0 | 特別徴収額。円単位 |
| 14 | labor_union_fee | 労働組合費 | INTEGER | - | NOT NULL | - | - | 0 | 円単位 |
| 15 | memo | 備考 | TEXT | 200 | NULL許可 | - | - | NULL | 自由記述 |

## インデックス

| No | インデックス名 | 対象カラム | 種別 | 目的 |
|---|---|---|---|---|
| 1 | idx_payroll_monthly_date | payment_date | 通常 | 期間検索・月次集計の高速化 |

## 制約・ルール

- 各金額項目は円単位の整数で統一する(小数は扱わない)
- 控除項目(雇用保険〜労働組合費)は控除額そのものを正の整数で格納する(手取り計算は`基本給+時間外手当+その他給与-各種控除`で算出する想定)
- 論理削除は行わず、物理削除のみとする

## 変更履歴

| 日付 | 変更内容 | 変更者 |
|---|---|---|
| 2026-08-12 | 初版作成 | NAOKI |