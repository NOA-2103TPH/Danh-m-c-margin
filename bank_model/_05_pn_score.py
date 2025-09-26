import os
import numpy as np
import pandas as pd

# Thư mục hiện tại của file _05_pn_score.py
BASE_DIR = os.path.dirname(__file__)

# File input trong thư mục data của bank_model
INPUT_PATH = os.path.join(BASE_DIR, "data", "ComputePN.xlsx")

# Thư mục gốc Project Mega (ngoài cùng)
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Thư mục result (ngoài cùng)
RESULT_DIR = os.path.join(PROJECT_ROOT, "result")
os.makedirs(RESULT_DIR, exist_ok=True)

# File output ScoreRank.xlsx trong result
OUTPUT_PATH = os.path.join(RESULT_DIR, "ScoreRank.xlsx")

# -------------------- Xử lý dữ liệu -------------------- #

# Đọc P/N tổng
xls = pd.ExcelFile(INPUT_PATH, engine="openpyxl")
y = pd.read_excel(xls, sheet_name="YEAR_PN", usecols=["Ticker","YearReport","P_total","N_total"])
q = pd.read_excel(xls, sheet_name="QUARTER_PN", usecols=["Ticker","YearReport","LengthReport","P_total","N_total"])

# ---- Trích năm ----
y2024 = y[y["YearReport"] == 2024].copy()
y2023 = y[y["YearReport"] == 2023].copy()

y2024 = y2024.drop_duplicates(subset=["Ticker"], keep="last").set_index("Ticker")
y2023 = y2023.drop_duplicates(subset=["Ticker"], keep="last").set_index("Ticker")

y2024 = y2024.rename(columns={"P_total":"P_y2024","N_total":"N_y2024"})
y2023 = y2023.rename(columns={"P_total":"P_y2023"})[["P_y2023"]]

# ---- Trích quý ----
q25q2 = q[(q["YearReport"]==2025) & (q["LengthReport"]==2)].copy()  
q25q1 = q[(q["YearReport"]==2025) & (q["LengthReport"]==1)].copy()  
q24q2 = q[(q["YearReport"]==2024) & (q["LengthReport"]==2)].copy()  

q25q2 = q25q2.drop_duplicates(subset=["Ticker"], keep="last").set_index("Ticker")
q25q1 = q25q1.drop_duplicates(subset=["Ticker"], keep="last").set_index("Ticker")
q24q2 = q24q2.drop_duplicates(subset=["Ticker"], keep="last").set_index("Ticker")

q25q2 = q25q2.rename(columns={"P_total":"P_q2025_2","N_total":"N_q2025_2"})[["P_q2025_2","N_q2025_2"]]
q25q1 = q25q1.rename(columns={"P_total":"P_q2025_1"})[["P_q2025_1"]]
q24q2 = q24q2.rename(columns={"P_total":"P_q2024_2"})[["P_q2024_2"]]

# ---- Tập Ticker hợp nhất ----
tickers = pd.Index(pd.unique(pd.concat([
    y2024.index.to_series(),
    y2023.index.to_series(),
    q25q2.index.to_series(),
    q25q1.index.to_series(),
    q24q2.index.to_series()
], ignore_index=True))).sort_values()

df = pd.DataFrame({"Ticker": tickers}).set_index("Ticker")

# ---- Gộp dữ liệu vào khung chính ----
df = df.join(y2024, how="left")
df = df.join(y2023, how="left")
df = df.join(q25q2, how="left")
df = df.join(q25q1, how="left")
df = df.join(q24q2, how="left")

# ---- Tính 5 rule (strict '>') ----
df["Rule1"] = (df["P_y2024"]   > df["N_y2024"]).astype(int)
df["Rule2"] = (df["P_y2024"]   > df["P_y2023"]).astype(int)
df["Rule3"] = (df["P_q2025_2"] > df["N_q2025_2"]).astype(int)
df["Rule4"] = (df["P_q2025_2"] > df["P_q2025_1"]).astype(int)
df["Rule5"] = (df["P_q2025_2"] > df["P_q2024_2"]).astype(int)


df["Rules_Sum"] = df[["Rule1","Rule2","Rule3","Rule4","Rule5"]].sum(axis=1)
grade_map = {5:"A", 4:"B", 3:"C", 2:"D", 1:"E", 0:"E"}
df["Grade"] = df["Rules_Sum"].map(grade_map)

# ---- Xuất file ----
out = df.reset_index()[["Ticker","Rule1","Rule2","Rule3","Rule4","Rule5","Rules_Sum","Grade"]]
with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as w:
    out.to_excel(w, sheet_name="RULES", index=False)

print("DONE:", OUTPUT_PATH)

# -------------------- Main -------------------- #
def main():
    print("=== Bắt đầu chạy bank_model/_05_pn_score ===")
    print("DONE:", OUTPUT_PATH)

if __name__ == "__main__":
    main()
