import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from datetime import date
import pandas as pd
from db_utils import insert_payroll_monthly, insert_payroll_bonus
from category_map import  map_record_to_schema,monthly_column_map,bonus_column_map



# 1. 給与データを持つブックと、その開始年(4月始まり)
book_start_year = {
    r"C:\Users\naoki\OneDrive\家計簿\家計簿_社会人_1年目.xlsx": 2025,
    r"C:\Users\naoki\OneDrive\家計簿\家計簿_社会人_2年目.xlsx": 2026,
}
# 家計簿_大学生_.xlsx は給与データなしのため対象外




def read_payroll_block(path, sheet_name, start_label):
    """start_label(例:'基本給')を起点に、その行をヘッダー、次の行を値として辞書化する"""
    df_raw = pd.read_excel(path, sheet_name=sheet_name, header=None)

    pos = None
    for r in range(df_raw.shape[0]):
        for c in range(df_raw.shape[1]):
            if df_raw.iat[r, c] == start_label:
                pos = (r, c)
                break
        if pos:
            break
    if pos is None:
        return None

    header_row, start_col = pos
    headers = []
    col = start_col
    while col < df_raw.shape[1] and pd.notna(df_raw.iat[header_row, col]):
        headers.append(df_raw.iat[header_row, col])
        col += 1

    values = df_raw.iloc[header_row + 1, start_col:start_col + len(headers)].tolist()
    record = dict(zip(headers, values))

    if pd.isna(record.get(start_label)):
        return None  # 未来の空月など、未入力ブロックは除外

    return record


def sheet_to_payment_date(path, sheet_name):
    """シート名('4月'等)とブックの開始年から、その月1日のdateを組み立てる"""
    start_year = book_start_year.get(path)
    if start_year is None:
        return None
    month = int(sheet_name.replace("月", ""))
    year = start_year if month >= 4 else start_year + 1
    return date(year, month, 1)




# 3. 全ブック・全シートから月次給与ブロックを収集
monthly_records = []
for path in book_start_year.keys():
    xls = pd.ExcelFile(path)
    for sheet_name in xls.sheet_names:
        record = read_payroll_block(path, sheet_name, "基本給")
        if record:
            record["source_file"] = path
            record["sheet"] = sheet_name
            monthly_records.append(record)

print(f"読み込んだ月次給与レコード数: {len(monthly_records)}")

# # 4. INSERT実行
# inserted_count = 0
# for record in monthly_records:
#     payment_date = sheet_to_payment_date(record["source_file"], record["sheet"])
#     if payment_date is None:
#         continue

#     schema_row = map_record_to_schema(record, monthly_column_map)

#     insert_payroll_monthly(
#         payment_date=payment_date,
#         base_salary=int(schema_row.get("base_salary", 0)),
#         overtime_allowance=int(schema_row.get("overtime_allowance", 0)),
#         other_allowance=int(schema_row.get("other_allowance", 0)),
#         rent_deduction=int(schema_row.get("rent_deduction", 0)),
#         employment_insurance=int(schema_row.get("employment_insurance", 0)),
#         employee_pension=int(schema_row.get("employee_pension", 0)),
#         health_insurance_basic=int(schema_row.get("health_insurance_basic", 0)),
#         health_insurance_special=int(schema_row.get("health_insurance_special", 0)),
#         child_support_contribution=int(schema_row.get("child_support_contribution", 0)),
#         income_tax=int(schema_row.get("income_tax", 0)),
#         resident_tax=int(schema_row.get("resident_tax", 0)),
#         labor_union_fee=int(schema_row.get("labor_union_fee", 0)),
#         other_deduction=int(schema_row.get("other_deduction", 0)),
#     )
#     inserted_count += 1

# print(f"{inserted_count}件INSERTしました")


# 全ブック・全シートから賞与ブロックを収集(read_payroll_block, sheet_to_payment_dateは既存のものを再利用)
bonus_records = []
for path in book_start_year.keys():
    xls = pd.ExcelFile(path)
    for sheet_name in xls.sheet_names:
        record = read_payroll_block(path, sheet_name, "基本賞与")
        if record:
            record["source_file"] = path
            record["sheet"] = sheet_name
            bonus_records.append(record)

print(f"読み込んだ賞与レコード数: {len(bonus_records)}")

# INSERT実行
inserted_bonus_count = 0
for record in bonus_records:
    payment_date = sheet_to_payment_date(record["source_file"], record["sheet"])
    if payment_date is None:
        continue

    schema_row = map_record_to_schema(record, bonus_column_map)

    insert_payroll_bonus(
        payment_date=payment_date,
        base_bonus=int(schema_row.get("base_bonus", 0)),
        employment_insurance=int(schema_row.get("employment_insurance", 0)),
        employee_pension=int(schema_row.get("employee_pension", 0)),
        health_insurance_basic=int(schema_row.get("health_insurance_basic", 0)),
        health_insurance_special=int(schema_row.get("health_insurance_special", 0)),
        child_support_contribution=int(schema_row.get("child_support_contribution", 0)),
        income_tax=int(schema_row.get("income_tax", 0)),
    )
    inserted_bonus_count += 1

print(f"{inserted_bonus_count}件INSERTしました")