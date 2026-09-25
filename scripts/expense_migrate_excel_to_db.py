import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import sqlite3
import pandas as pd
from db_utils import insert_expense, insert_payroll_monthly
from category_map import category_map, map_record_to_schema


# Excelのパスを配列に格納
excel_paths = [
    r"C:\Users\naoki\OneDrive\家計簿\家計簿_大学生_.xlsx",
    r"C:\Users\naoki\OneDrive\家計簿\家計簿_社会人_1年目.xlsx",
    r"C:\Users\naoki\OneDrive\家計簿\家計簿_社会人_2年目.xlsx",
]

# 1. 全ブック・全シート読み込み
all_dfs = []
for path in excel_paths:
    sheets = pd.read_excel(path, sheet_name=None, usecols="A:D", header=1)
    for name, df in sheets.items():
        df["source_file"] = path
        all_dfs.append(df)


df_all = pd.concat(all_dfs, ignore_index=True)


# 2. 不要行(空欄・合計行)を除外
df_all["項目"] = df_all["項目"].str.strip()
df_all = df_all[df_all["項目"].notna() & (df_all["項目"] != "計")]

# 3. カテゴリのマッピング適用
df_all["category"] = df_all["項目"].map(category_map)

# 念のため未マッピングチェック(ここで必ず0件を確認してから進む)
unmapped = df_all[df_all["category"].isna()]
assert unmapped.empty, f"未マッピングのカテゴリが{len(unmapped)}件あります"

# 4. カラム名をテーブルの物理名に揃える
df_final = df_all.rename(columns={
    "日付":"transaction_date",
    "支出":"amount",
})[["transaction_date", "category", "amount"]]


# 5. 型を整える
df_final["transaction_date"] = pd.to_datetime(df_final["transaction_date"]).dt.date
df_final["amount"] = df_final["amount"].astype(int)
df_final["memo"] = ""

# print(df_final.head(10))

# # 6. INSERT実行
# for _, row in df_final.iterrows():
#     insert_expense(row["transaction_date"], row["category"], int(row["amount"]), row["memo"])

# print(f"{len(df_final)}件INSERTしました")

