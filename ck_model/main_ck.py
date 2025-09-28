# ck_model/main_ck.py
import os
import pandas as pd
import numpy as np

from .data_loader import load_processed_data
from .data_processor import merge_data, map_data_to_ct
from .financial_calculation import (
    calculate_averages,
    calculate_market_totals,
    calculate_ratios
)
from .scoring_engine import (
    apply_scoring,
    calculate_quarterly_conditions,
    calculate_final_rank,
)
from .metrics_config import create_column_rule_map, INPUT_FILES
from .adjust_engine import run_adjustment


# --- Đường dẫn chuẩn ---
BASE_DIR = os.path.dirname(__file__)                          # .../ck_model
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))     # .../Project Mega
RESULT_DIR = os.path.join(PROJECT_ROOT, "result")
os.makedirs(RESULT_DIR, exist_ok=True)


def _abs_path(maybe_rel_path: str, default_rel: str) -> str:
    """
    Trả về đường dẫn tuyệt đối an toàn:
    - Nếu maybe_rel_path có trong INPUT_FILES và là đường dẫn tương đối -> ghép với BASE_DIR
    - Nếu không có hoặc rỗng -> dùng default_rel (cũng ghép với BASE_DIR)
    """
    path = maybe_rel_path or default_rel
    if not os.path.isabs(path):
        path = os.path.join(BASE_DIR, path)
    return path


def main():
    print("=== Financial Analysis Pipeline (No Clustering) ===")

    # 1) Load Year data
    print("1. Loading data (Year)...")
    y_path = _abs_path(INPUT_FILES.get("data"), "Data/Processed_Data_Y.xlsx")
    ck_bs, ck_is, ck_cf, ck_nt = load_processed_data(y_path)
    print("✓ Year data loaded")

    # 2) Merge
    print("2. Merging data...")
    df = merge_data(ck_bs, ck_is, ck_cf, ck_nt)
    print(f"✓ Merged dataframe shape: {df.shape}")

    # 3) Map -> ct
    print("3. Mapping data to ct...")
    ct = map_data_to_ct(df, ck_bs, ck_is, ck_nt, ck_cf)
    print(f"✓ Mapped dataframe shape: {ct.shape}")

    # 4) Averages / Market totals / Ratios
    print("4. Calculating averages / market totals / ratios...")
    ct = calculate_averages(ct)
    ct = calculate_market_totals(ct)
    ct = calculate_ratios(ct)

    # 5) Scoring (Yearly)
    print("5. Creating scoring rules & applying (Yearly)...")
    _ = create_column_rule_map()  # vẫn khởi tạo như code gốc
    cf2_year = apply_scoring(ct.copy())

    # --- Xuất summary YEAR (LengthReport == 5) ---
    score_cols_year = [c for c in cf2_year.columns if c.endswith('_score')]
    yearly_sum = cf2_year.copy()
    yearly_sum['Tong_p'] = yearly_sum[score_cols_year].sum(axis=1)
    yearly_sum['Tong_n'] = (yearly_sum[score_cols_year] == 0).sum(axis=1)
    summary_year = yearly_sum[yearly_sum['LengthReport'] == 5][
        ['Ticker', 'YearReport', 'LengthReport', 'Tong_p', 'Tong_n']
    ]
    yearly_path = os.path.join(RESULT_DIR, "ck_summary_year.csv")
    summary_year.to_csv(yearly_path, encoding='utf-8-sig', index=False)

    # 6) Chuẩn bị dữ liệu QUÝ (fallback nếu Year không có quý)
    print("6. Preparing quarterly data for conditions...")
    has_quarter = (
        ('LengthReport' in cf2_year.columns)
        and ('YearReport' in cf2_year.columns)
        and (cf2_year.query('YearReport in [2024, 2025] and LengthReport in [1, 2]').shape[0] > 0)
    )

    cf2_all = cf2_year.copy()
    if not has_quarter:
        print("   - Yearly set lacks quarters; loading Processed_Data_Q.xlsx ...")
        q_path = _abs_path(INPUT_FILES.get("data_quarter"), "Data/Processed_Data_Q.xlsx")
        try:
            q_bs, q_is, q_cf, q_nt = load_processed_data(q_path)
            q_df = merge_data(q_bs, q_is, q_cf, q_nt)
            ct_q = map_data_to_ct(q_df, q_bs, q_is, q_nt, q_cf)
            ct_q = calculate_averages(ct_q)
            ct_q = calculate_market_totals(ct_q)
            ct_q = calculate_ratios(ct_q)
            cf2_quarter = apply_scoring(ct_q.copy())
            cf2_all = pd.concat([cf2_year, cf2_quarter], ignore_index=True)
            print(f"   ✓ Merged yearly + quarterly rows: {cf2_all.shape[0]}")
        except FileNotFoundError:
            print("   ! Quarterly file not found; quarterly ranks will be empty.")

    # --- Xuất summary QUARTER (Q1/Q2 2024-2025) ---
    score_cols_all = [c for c in cf2_all.columns if c.endswith('_score')]
    quarter_sum = cf2_all.copy()
    quarter_sum['Tong_p'] = quarter_sum[score_cols_all].sum(axis=1)
    quarter_sum['Tong_n'] = (quarter_sum[score_cols_all] == 0).sum(axis=1)
    summary_quarter = quarter_sum.query(
        'YearReport in [2024, 2025] and LengthReport in [1, 2]'
    )[['Ticker', 'YearReport', 'LengthReport', 'Tong_p', 'Tong_n']]
    quarter_summary_path = os.path.join(RESULT_DIR, "ck_summary_quarter.csv")
    summary_quarter.to_csv(quarter_summary_path, encoding='utf-8-sig', index=False)

    # 7) Quarterly 3-condition ranks
    print("7. Calculating quarterly 3-condition ranks...")
    q_rank = calculate_quarterly_conditions(cf2_all)
    q_rank_path = os.path.join(RESULT_DIR, "ck_quarter_scores.csv")
    q_rank.to_csv(q_rank_path, encoding='utf-8-sig', index=False)

    # 8) Final 5-rule rank (2 yearly + 3 quarterly)
    print("8. Calculating final 5-rule rank...")
    final_rank = calculate_final_rank(cf2_all)
    final_rank["Model"] = "Securities"
    final_path = os.path.join(RESULT_DIR, "ck_final.xlsx")
    final_rank.to_excel(final_path, index=False)
    print("   ✓ Saved:", final_path)

    # 9) Điều chỉnh theo median ngành
    print("9. Adjusting grades with market share medians...")
    df_adj = run_adjustment(
        ct,
        scores_path=final_path,  # dùng file vừa xuất
        filter_years=(2024,),
        filter_lengths=(5,),
        output_excel=None,
    )

    # In nhanh 10 dòng đầu cho quan sát
    print("Adjusted ranks (top 10):")
    try:
        print(df_adj.head(10).to_string(index=False))
    except Exception:
        print(df_adj.head(10))

    adjust_path = os.path.join(RESULT_DIR, "ck_adjust.xlsx")
    df_adj.to_excel(adjust_path, index=False)
    print("   ✓ Saved:", adjust_path)


if __name__ == "__main__":
    main()

