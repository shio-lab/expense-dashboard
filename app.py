"""app.py"""
import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
from db_utils import (
    get_expense_by_month,
    insert_expense,
    delete_expense,
    get_payroll_monthly_by_month,
    get_payroll_bonus_by_month,
    insert_payroll_monthly,
    insert_payroll_bonus,
    get_payroll_monthly_by_year,
    get_expense_by_year_ground_by_category,
    get_payroll_bonus_by_year,
)

st.set_page_config(
    page_title="MoneyBook",
    page_icon="img/MoneyBook.ico",  
    layout="wide"  
)


st.title('MoneyBook')

with st.sidebar:

        st.subheader("支出を追加")
        with st.form("expense_form", clear_on_submit=True):
            input_date = st.date_input("日付", value = date.today())
            input_category = st.selectbox("カテゴリ", ["食費", "日用品", "ファッション", "交通費", "娯楽", "光熱費", "通信費", "医療費", "教育費", "サブスクリプション","その他"])
            input_amount = st.number_input("金額", min_value= 0, step=100)
            input_memo = st.text_input("メモ")

            submitted = st.form_submit_button("追加")

            if submitted:
                insert_expense(input_date, input_category, input_amount, input_memo)
                st.success("追加しました！")
                st.rerun()

        
col1, col2 = st.columns(2)
with col1:
        year = st.selectbox("年", options = range(2020, date.today().year + 1),
                            index = date.today().year - 2020)

with col2:
        month = st.selectbox("月", options = range(1, 13),
                            index = date.today().month - 1)

tab_list, tab_graph = st.tabs(["一覧", "グラフ"])

with tab_list:
        
        st.subheader('給与明細')
        payroll_monthly_df = get_payroll_monthly_by_month(year, month)
        st.dataframe(
            payroll_monthly_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id":None,
                "payment_date":st.column_config.DateColumn(
                    "支給日",
                    format="YYYY-MM"),
                "gross_total": "支給合計",
                "deduction_total": "控除合計",
                "net_total": "差引支給額",
                "base_salary":"基本給",
                "overtime_allowance":"時間外手当",
                "other_allowance":"その他給与",
                "rent_deduction":"家賃",
                "employment_insurance":"雇用保険",
                "employee_pension":"厚生年金",
                "health_insurance_basic":"健康保険(基本)",
                "health_insurance_special":"健康保険(特定)",
                "child_support_contribution":"子ども・子育て支援金",
                "income_tax":"所得税",
                "resident_tax":"住民税",
                "labor_union_fee":"労働組合費",
                "other_deduction":"その他控除",
                "memo":"備考"
            },
        )


        payroll_bonus_df = get_payroll_bonus_by_month(year, month)

        if not payroll_bonus_df.empty:
            st.subheader('賞与明細')
            st.dataframe(
                payroll_bonus_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id":None,
                "payment_date":st.column_config.DateColumn(
                    "支給日",
                    format="YYYY-MM"),
                    "gross_total": "支給合計",
                    "deduction_total": "控除合計",
                    "net_total": "差引支給額",
                    "base_bonus":"基本賞与",
                    "employment_insurance":"雇用保険",
                    "employee_pension":"厚生年金",
                    "health_insurance_basic":"健康保険(基本)",
                    "health_insurance_special":"健康保険(特定)",
                    "child_support_contribution":"子ども・子育て支援金",
                    "income_tax":"所得税",
                    "memo":"備考"
                },
            )

        with st.expander("月次給与を追加"):
            with st.form("payroll_monthly_form", clear_on_submit=True):
                input_payment_date = st.date_input("支払日", value=date.today())

                col1, col2 = st.columns(2)
                with col1:
                    input_base_salary = st.number_input("基本給", min_value=0, step=1000)
                    input_overtime_allowance = st.number_input("時間外手当", min_value=0, step=100)
                    input_other_allowance = st.number_input("その他給与", min_value=0, step=100)
                    input_rent_deduction = st.number_input("家賃控除", min_value=0, step=100)
                    input_employment_insurance = st.number_input("雇用保険", min_value=0, step=100)
                    input_employee_pension = st.number_input("厚生年金", min_value=0, step=100)
                    input_other_deduction = st.number_input("その他控除", min_value=0, step=100)
                with col2:
                    input_health_insurance_basic = st.number_input("健康保険(基本)", min_value=0, step=100)
                    input_health_insurance_special = st.number_input("健康保険(特定)", min_value=0, step=100)
                    input_child_support_contribution = st.number_input("子ども・子育て支援金", min_value=0, step=100)
                    input_income_tax = st.number_input("所得税", min_value=0, step=100)
                    input_resident_tax = st.number_input("住民税", min_value=0, step=100)
                    input_labor_union_fee = st.number_input("労働組合費", min_value=0, step=100)

                input_memo = st.text_input("メモ")

                submitted = st.form_submit_button("追加")

                if submitted:
                    insert_payroll_monthly(
                        payment_date=input_payment_date,
                        base_salary=input_base_salary,
                        overtime_allowance=input_overtime_allowance,
                        other_allowance=input_other_allowance,
                        rent_deduction=input_rent_deduction,
                        employment_insurance=input_employment_insurance,
                        employee_pension=input_employee_pension,
                        health_insurance_basic=input_health_insurance_basic,
                        health_insurance_special=input_health_insurance_special,
                        child_support_contribution=input_child_support_contribution,
                        income_tax=input_income_tax,
                        resident_tax=input_resident_tax,
                        labor_union_fee=input_labor_union_fee,
                        other_deduction=input_other_deduction,
                        memo=input_memo,
                    )
                    st.success("月次給与を追加しました！")
                    st.rerun()


        with st.expander("賞与を追加"):
            with st.form("payroll_bonus_form", clear_on_submit=True):
                input_payment_date_bonus = st.date_input("支払日", value=date.today(), key="bonus_date")

                col1, col2 = st.columns(2)
                with col1:
                    input_base_bonus = st.number_input("基本賞与", min_value=0, step=1000)
                    input_employment_insurance_bonus = st.number_input("雇用保険", min_value=0, step=100, key="bonus_ei")
                    input_employee_pension_bonus = st.number_input("厚生年金", min_value=0, step=100, key="bonus_pension")
                    input_income_tax_bonus = st.number_input("所得税", min_value=0, step=100, key="bonus_tax")
                with col2:
                    input_health_insurance_basic_bonus = st.number_input("健康保険(基本)", min_value=0, step=100, key="bonus_hib")
                    input_health_insurance_special_bonus = st.number_input("健康保険(特定)", min_value=0, step=100, key="bonus_his")
                    input_child_support_contribution_bonus = st.number_input("子ども・子育て支援金", min_value=0, step=100, key="bonus_child")

                input_memo_bonus = st.text_input("メモ", key="bonus_memo")

                submitted_bonus = st.form_submit_button("追加")

                if submitted_bonus:
                    insert_payroll_bonus(
                        payment_date=input_payment_date_bonus,
                        base_bonus=input_base_bonus,
                        employment_insurance=input_employment_insurance_bonus,
                        employee_pension=input_employee_pension_bonus,
                        health_insurance_basic=input_health_insurance_basic_bonus,
                        health_insurance_special=input_health_insurance_special_bonus,
                        child_support_contribution=input_child_support_contribution_bonus,
                        income_tax=input_income_tax_bonus,
                        memo=input_memo_bonus,
                    )
                    st.success("賞与を追加しました！")
                    st.rerun()

        st.subheader('支出一覧')

        df = get_expense_by_month(year, month)

        event = st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            column_config={
                "id": None,
                "transaction_date": st.column_config.DateColumn(
                    "日付",
                    format="YYYY-MM-DD",
                ),
                "category": "カテゴリ",
                "amount": "金額",
                "memo": "メモ",
            },
        )



        selected_rows = event.selection.rows

        if selected_rows:
            selected_index = selected_rows[0]
            selected_record = df.iloc[selected_index]

            st.write(f"選択中: {selected_record['transaction_date'].date()} / {selected_record['category']} / {selected_record['amount']}円")

            if st.button("このレコードを削除", type="primary"):
                delete_expense(int(selected_record["id"]))
                st.success("削除しました")
                st.rerun()

with tab_graph:
        st.subheader(f"{year}年 月収推移")
        payroll_monthly_year_df = get_payroll_monthly_by_year(year)
        payroll_bonus_year_df = get_payroll_bonus_by_year(year)

        monthly_gross_total = payroll_monthly_year_df["gross_total"].sum() if not payroll_monthly_year_df.empty else 0
        bonus_gross_total = payroll_bonus_year_df["gross_total"].sum() if not payroll_bonus_year_df.empty else 0
        annual_income = monthly_gross_total + bonus_gross_total
        st.metric(f"{year}年 年収", f"{annual_income:,.0f}円")

        if not payroll_monthly_year_df.empty:
                # 月ごとの月収データを土台にする
                chart_df = payroll_monthly_year_df[["payment_date", "gross_total"]].copy()
                chart_df["月"] = chart_df["payment_date"].dt.strftime("%m月")
                chart_df = chart_df.rename(columns={"gross_total": "月収のみ"})

                # 賞与を月ごとに合計（同月に複数回支給があるケースに対応）
                if not payroll_bonus_year_df.empty:
                    bonus_by_month = (
                        payroll_bonus_year_df
                        .assign(月=payroll_bonus_year_df["payment_date"].dt.strftime("%m月"))
                        .groupby("月")["gross_total"]
                        .sum()
                    )
                else:
                    bonus_by_month = pd.Series(dtype="float64")

                # 月収に賞与を合算した「賞与込み」列を作成
                chart_df["賞与込み"] = chart_df.apply(
                    lambda row: row["月収のみ"] + bonus_by_month.get(row["月"], 0),
                    axis=1,
                )

                st.line_chart(
                    chart_df.set_index("月")[["月収のみ", "賞与込み"]]
                )
        else:
                st.info("この年の給与データがありません")

        st.subheader(f"{year}年 カテゴリ別支出")
        category_df = get_expense_by_year_ground_by_category(year)

        if not category_df.empty:
                st.bar_chart(
                    category_df.set_index("category")["total_amount"],
                )
        else:
                st.info("この年度の支出データはありません")