import os
import numpy as np
import pandas as pd
INPUT_XLS  = "data/_03_compute_ratios.xlsx"
OUTPUT_XLS = "data/_04_compute_pn.xlsx"   

METRICS_HIGH = [
    "ROA","ROE","NIM","Lãi suất đầu ra bình quân","Chênh lệch lãi suất",
    "Biên lợi nhuận từ hoạt động dịch vụ (NSFM)","Tỷ lệ thu nhập phi lãi thuần (NNIM)",
    "Tỷ lệ lợi nhuận trước thuế/ thu nhập lãi","NPM","Thu nhập hoạt động trên thu nhập lãi",
    "Tỷ suất sinh lời bình quân trên dư nợ","Tỷ suất sinh lời trên tổng tài sản",
    "Tỷ lệ CASA","Nợ nhóm 1 %","Earning Assets to Total Assets",
    "Annual Credit Growth (Market 1)","Annual Credit Growth (Market 2)",
    "Annual Interest Income Growth","Annual Net Income Growth","Annual Asset Growth",
    "QYoY Credit Growth (M1)","QYoY Credit Growth (M2)",
    "QYoY Interest Income Growth","QYoY Net Income Growth","QYoY Asset Growth",
]

METRICS_LOW = [
    "Lãi suất đầu vào bình quân","Tỷ lệ chi phí lãi / thu nhập lãi",
    "Tỷ lệ chi phí dịch vụ/ thu nhập dịch vụ",
    "Dự phòng rủi ro tín dụng/ Dư nợ cho vay","DPRRTD/CV Khách hàng và CK đầu tư",
    "Nợ nhóm 2 %","Nợ nhóm 3 %","Nợ nhóm 4 %","Nợ nhóm 5 %",
    "Overdue debt ratio (2-5)","NPL Ratio (3-5)",
    "Tỷ lệ sử dụng DP để xử lý nợ khó đòi/Customer Loan",
    "Tổng nợ phải trả / VCSH","Tỷ lệ đòn bẩy tài chính",
]

THRESHOLDS = {
    "CAR": 0.08,                         
    "Tỷ lệ chi phí/thu nhập (CIR)": 0.50 
}

# Đảm bảo thư mục tồn tại
os.makedirs("data", exist_ok=True)

xls = pd.ExcelFile(INPUT_XLS, engine="openpyxl")
year_df    = pd.read_excel(xls, sheet_name="YEAR")
quarter_df = pd.read_excel(xls, sheet_name="QUARTER_ANN")

# 1 XỬ LÝ DỮ LIỆU NĂM (YEAR)
KEYS_YEAR   = ["Ticker","YearReport"]
ORDER_YEAR  = ["Ticker","YearReport"]

HIGH_YEAR   = [c for c in METRICS_HIGH if c in year_df.columns]
LOW_YEAR    = [c for c in METRICS_LOW  if c in year_df.columns]
THR_YEAR    = [c for c in THRESHOLDS.keys() if c in year_df.columns]

year_sorted = year_df.sort_values(ORDER_YEAR).reset_index(drop=True)
year_index  = year_sorted.set_index(KEYS_YEAR).index

year_pn = pd.DataFrame(index=year_index)

for col in HIGH_YEAR:
    prev = year_sorted.groupby("Ticker")[col].shift(1)
    diff = year_sorted[col] - prev
    year_pn[f"PN__{col}"] = np.where(diff > 0, "P", np.where(diff < 0, "N", np.nan))

for col in LOW_YEAR:
    prev = year_sorted.groupby("Ticker")[col].shift(1)
    diff = year_sorted[col] - prev
    year_pn[f"PN__{col}"] = np.where(diff > 0, "N", np.where(diff < 0, "P", np.nan))

for col in THR_YEAR:
    threshold_val = THRESHOLDS[col]
    series = year_df.set_index(KEYS_YEAR)[col].reindex(year_index)
    year_pn[f"PN__{col}"] = np.where(series > threshold_val, "P",
                              np.where(series < threshold_val, "N", np.nan))

pn_cols_year = [c for c in year_pn.columns if c.startswith("PN__")]
thr_cols_year = [f"PN__{c}" for c in THR_YEAR]
inc_cols_year = [c for c in pn_cols_year if c not in thr_cols_year]

year_pn["P_inc"]   = (year_pn[inc_cols_year] == "P").sum(axis=1) if inc_cols_year else 0
year_pn["N_inc"]   = (year_pn[inc_cols_year] == "N").sum(axis=1) if inc_cols_year else 0
year_pn["P_thr"]   = (year_pn[thr_cols_year] == "P").sum(axis=1) if thr_cols_year else 0
year_pn["N_thr"]   = (year_pn[thr_cols_year] == "N").sum(axis=1) if thr_cols_year else 0
year_pn["P_total"] = year_pn["P_inc"] + year_pn["P_thr"]
year_pn["N_total"] = year_pn["N_inc"] + year_pn["N_thr"]

out_year = year_pn.reset_index().sort_values(KEYS_YEAR).reset_index(drop=True)


# 2 XỬ LÝ DỮ LIỆU QUÝ (QUARTER_ANN)
KEYS_QUARTER  = ["Ticker","YearReport","LengthReport"]
ORDER_QUARTER = ["Ticker","YearReport","LengthReport"]

HIGH_QUARTER  = [c for c in METRICS_HIGH if c in quarter_df.columns]
LOW_QUARTER   = [c for c in METRICS_LOW  if c in quarter_df.columns]
THR_QUARTER   = [c for c in THRESHOLDS.keys() if c in quarter_df.columns]
# BỎ NGƯỠNG CAR Ở PHẦN QUÝ
EXCLUDED_THRESHOLDS_QUARTER = {"CAR"}
THR_QUARTER = [
    c for c in THRESHOLDS.keys()
    if c in quarter_df.columns and c not in EXCLUDED_THRESHOLDS_QUARTER
]

quarter_sorted = quarter_df.sort_values(ORDER_QUARTER).reset_index(drop=True)
quarter_index  = quarter_sorted.set_index(KEYS_QUARTER).index

quarter_pn = pd.DataFrame(index=quarter_index)

for col in HIGH_QUARTER:
    prev = quarter_sorted.groupby("Ticker")[col].shift(1)
    diff = quarter_sorted[col] - prev
    quarter_pn[f"PN__{col}"] = np.where(diff > 0, "P", np.where(diff < 0, "N", np.nan))

for col in LOW_QUARTER:
    prev = quarter_sorted.groupby("Ticker")[col].shift(1)
    diff = quarter_sorted[col] - prev
    quarter_pn[f"PN__{col}"] = np.where(diff > 0, "N", np.where(diff < 0, "P", np.nan))

for col in THR_QUARTER:
    threshold_val = THRESHOLDS[col]
    series = quarter_df.set_index(KEYS_QUARTER)[col].reindex(quarter_index)
    quarter_pn[f"PN__{col}"] = np.where(series > threshold_val, "P",
                                 np.where(series < threshold_val, "N", np.nan))

pn_cols_quarter  = [c for c in quarter_pn.columns if c.startswith("PN__")]
thr_cols_quarter = [f"PN__{c}" for c in THR_QUARTER]
inc_cols_quarter = [c for c in pn_cols_quarter if c not in thr_cols_quarter]

quarter_pn["P_inc"]   = (quarter_pn[inc_cols_quarter] == "P").sum(axis=1) if inc_cols_quarter else 0
quarter_pn["N_inc"]   = (quarter_pn[inc_cols_quarter] == "N").sum(axis=1) if inc_cols_quarter else 0
quarter_pn["P_thr"]   = (quarter_pn[thr_cols_quarter] == "P").sum(axis=1) if thr_cols_quarter else 0
quarter_pn["N_thr"]   = (quarter_pn[thr_cols_quarter] == "N").sum(axis=1) if thr_cols_quarter else 0
quarter_pn["P_total"] = quarter_pn["P_inc"] + quarter_pn["P_thr"]
quarter_pn["N_total"] = quarter_pn["N_inc"] + quarter_pn["N_thr"]

out_quarter = quarter_pn.reset_index().sort_values(KEYS_QUARTER).reset_index(drop=True)


# GHI FILE KẾT QUẢ
with pd.ExcelWriter(OUTPUT_XLS, engine="openpyxl") as writer:
    out_year.to_excel(writer,    sheet_name="YEAR_PN",    index=False)
    out_quarter.to_excel(writer, sheet_name="QUARTER_PN", index=False)

print("Done")
