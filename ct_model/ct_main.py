import pandas as pd
from ct_model.data_loader import load_data
from ct_model.data_processor import process_data
from ct_model.financial_calculation import (
    calculate_financial_metrics, 
    calculate_financial
)
from ct_model.metrics_config import column_rule_map
from ct_model.scoring_engine import apply_scoring_rules, calculate_total_scores
from ct_model.analysis_engine import apply_conditions, calculate_final_grades
import os

def main():
    # Bước 1: Tải dữ liệu
    bs_1, cf_1, is_1 = load_data()
    
    # Bước 2: Xử lý dữ liệu
    df, bs_sorted, cf_sorted, is_sorted = process_data(bs_1, cf_1, is_1)

    # Bước 3: Tính toán metrics
    cf2 = df[['Ticker', 'YearReport', 'LengthReport']].copy()
    cf2 = calculate_financial_metrics(cf2, bs_sorted, cf_sorted, is_sorted)
    cf2 = calculate_financial(cf2)

    # Bước 4: Tính điểm
    cf2 = apply_scoring_rules(cf2, column_rule_map)
    cf2 = calculate_total_scores(cf2)

    # Bước 5: Phân tích
    cf2_quarterly_summary = cf2[cf2['YearReport'].isin([2023, 2024, 2025])].copy()
    filtered = cf2_quarterly_summary[
        (cf2_quarterly_summary['YearReport'].isin([2024, 2025])) &
        (cf2_quarterly_summary['LengthReport'].isin([1, 2]))
    ]
    filtered = filtered.sort_values(
        by=['Ticker', 'YearReport', 'LengthReport'],
        ascending=[True, False, False]
    )
    dk1, dk2, dk3 = apply_conditions(filtered)
    PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
    RESULT_DIR = os.path.join(PROJECT_ROOT, "result")
    os.makedirs(RESULT_DIR, exist_ok=True)

    filtered_path = os.path.join(RESULT_DIR, "filtered.csv")
    filtered.to_csv(filtered_path, encoding="utf-8-sig", index=False)
    print("✅ Filtered CSV saved:", filtered_path)
    
    # Bước 6: Tính điểm cuối cùng
    BASE_DIR = os.path.dirname(__file__)
    df_y_path = os.path.join(BASE_DIR, "Data", "ye_ye4.csv")
    df_y = pd.read_csv(df_y_path)

    result = calculate_final_grades(dk1, dk2, dk3, df_y)
    
    # Bước 7: Xuất kết quả vào thư mục result ngoài cùng
    PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
    RESULT_DIR = os.path.join(PROJECT_ROOT, "result")
    os.makedirs(RESULT_DIR, exist_ok=True)

    out_path = os.path.join(RESULT_DIR, "final_grades.xlsx")
    result.to_excel(out_path, index=False)
    print("✅ Final grades saved:", out_path)

if __name__ == "__main__":
    main()
