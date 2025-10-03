"""
Configuration for financial metrics and scoring rules (no clustering)
"""

# Càng cao càng tốt
metrics_r1 = [
    "Tăng trưởng dư nợ cho vay margin",
    "Tăng trưởng Tổng tài sản",
    "Tăng trưởng Vốn chủ sở hữu",
    "Hiệu suất nhân viên",
    "Receivables Turnover",
    "Doanh thu cho vay margin/ Dư nợ cho vay margin",
    "Doanh thu môi giới/ Tổng giá trị giao dịch",
]

# Càng thấp càng tốt
metrics_r2 = [
    "Days Sales Outstanding (DSO)",
    "Payables Turnover",
    "Tỷ lệ giảm giá chứng khoán kinh doanh",
    "Days Payable Outstanding (DPO)",
    "Short term Debt to Margin Loan",
]

# Lớn hơn hoặc bằng trung bình ngành
metrics_r3 = [
    "Market Share by Assets",
    "Market Share by Equity",
    "Market Share by Margin Loan",
    "Market Share by Revenue",
    "Market Share by Brokerage Revenue",
    "Asset Turnover",
    "ROE",
    "ROA",
    "ROCE",
    "Net Profit Margin",
    "Operating Margin",
    "Tỷ trọng doanh thu môi giới",
    "Tỷ trọng doanh thu tự doanh",
    "ACT",
    "CVR",
    "Cơ cấu chứng chỉ quỹ và trái phiếu trong danh mục FVTPL",
    "Current Ratio",
    "Quick Ratio",
    "Cash Ratio",
    "Debt Service Coverage Ratio (DSCR)",
]

# Thấp hơn hoặc bằng trung bình ngành
metrics_r4 = [
    "D/E",
    "D/A",
    "Financial Leverage",
    "Debt-to-Capital",
    "High Risk Assets Ratio",
    "Cơ cấu dư nợ",
    "Dư nợ cho vay margin/ Vốn chủ sở hữu",
]

# >= 1
metrics_r5 = [
    "Hiệu suất môi giới",
    "Hiệu suất tự doanh",
    "Interest Coverage Ratio",
    "DIR",
    "YEA",
    "Brokerage Margin",
]

# > 0 
metrics_r6 = [
    "Tăng trưởng doanh thu",
    "Tăng trưởng lợi nhuận ròng",
    "Khả năng tự doanh",
    "Net Working Capital",
    "margin spread",
    "EPS",
]

# Mapping từ metric sang rule
def create_column_rule_map():
    column_rule_map = {}
    # Gán theo thứ tự để rule ngưỡng (gt/lt) có thể override rule xu hướng
    for col in metrics_r1:
        column_rule_map[col] = 'higher_better'
    for col in metrics_r2:
        column_rule_map[col] = 'lower_better'
    for col in metrics_r3:
        column_rule_map[col] = 'ge_avg'
    for col in metrics_r4:
        column_rule_map[col] = 'le_avg'
    for col in metrics_r5:
        column_rule_map[col] = 'ge_1'
    for col in metrics_r6:
        column_rule_map[col] = 'gt_0'
    return column_rule_map

def get_all_metrics():
    all_metrics = (
        metrics_r1
        + metrics_r2
        + metrics_r3
        + metrics_r4
        + metrics_r5
        + metrics_r6
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
