"""
Configuration for financial metrics and scoring rules (no clustering)
"""

# Càng cao càng tốt
metrics_r1 = [
    "ROA",
    "ROE",
    "ROCE",
    "Asset Turnover",
    "Receivables Turnover",
    "Payables Turnover",
    "High Risk Assets Ratio",
    "Net Working Capital",
    "Defensive Interval Ratio",
    "Debt Service Coverage Ratio (DSCR)",
    "Interest Coverage Ratio",
    "Net Profit Margin",
    "Operating Margin",
    "EPS",
    "YEA",
    "Hiệu suất môi giới",
    "Khả năng tự doanh",
    "Brokerage Margin",
    "Hiệu suất tự doanh",
    "Tỷ trọng doanh thu môi giới",
    "Tỷ trọng doanh thu tự doanh",
    "ACT",
    "CVR",
    "Tăng trưởng doanh thu",
    "Tăng trưởng lợi nhuận ròng",
    "Tăng trưởng tổng tài sản",
    "Tăng trưởng vốn chủ sở hữu",
    "Tăng trưởng EPS",
    "Tăng trưởng dòng tiền từ hoạt động",
    "Tăng trưởng dư nợ cho vay margin",
    "Khả năng trả nợ bằng dòng tiền hoạt động",
    "Doanh thu cho vay margin/ Dư nợ cho vay margin",
    "Doanh thu môi giới/ Tổng giá trị giao dịch",
    "margin spread",
    "Cơ cấu chứng chỉ quỹ và trái phiếu trong danh mục FVTPL",
    "Hiệu suất nhân viên",
]

# Thấp càng tốt
metrics_r2 = [
    "Days Sales Outstanding (DSO)",
    "Days Payable Outstanding (DPO)",
    "D/E",
    "D/A",
    "Debt-to-Capital",
    "Short term Debt to Margin Loan",
    "Cơ cấu dư nợ",
    "Tỷ lệ giảm giá chứng khoán kinh doanh",
]

# >= 1 là tốt
metrics_r3 = [
    "Current Ratio",
    "QuickRatio",
    "Cash Ratio",
]

# > 1 là tốt
metrics_r4 = [
    "Debt Service Coverage Ratio (DSCR)",
    "Interest Coverage Ratio",
]

# < 1 là tốt
metrics_r5 = [
    "D/A",
    "D/E",
    "Short term Debt to Margin Loan",
]

# Mapping từ metric sang rule
def create_column_rule_map():
    column_rule_map = {}
    # Gán theo thứ tự để rule ngưỡng (gt/lt) có thể override rule xu hướng
    for col in metrics_r1: column_rule_map[col] = 'higher_better'
    for col in metrics_r2: column_rule_map[col] = 'lower_better'
    for col in metrics_r3: column_rule_map[col] = 'ge_1'
    for col in metrics_r4: column_rule_map[col] = 'gt_1'
    for col in metrics_r5: column_rule_map[col] = 'lt_1'
    return column_rule_map

def get_all_metrics():
    all_metrics = (
        metrics_r1 + metrics_r2 + metrics_r3 + metrics_r4 + metrics_r5
    )
    return list(dict.fromkeys(all_metrics))

# Chỉ còn cấu hình file input dữ liệu (không còn file ratios riêng cho clustering)
INPUT_FILES = {
    "data": "Data/Processed_Data_Y.xlsx",
    "data_quarter": "Data/Processed_Data_Q.xlsx",
}

# Năm dùng để tổng hợp/xếp hạng (bao gồm 2025 trong phần summary)
SCORING_YEARS = [2023, 2024, 2025]

# OUTPUT_FILES = {
#     "clustered": "chi_so_theo_cum.xlsx",
#     "cluster_avg": "Financial_Ratios_with_Cluster_Avg.xlsx",
#     "scored": "cf2_before_scoring.xlsx",
#     "summary": "scoring_summary_short.xlsx",
#     "final_scores": "Financial_Scores_Yearly.xlsx"
# }
