import os
import pandas as pd
from bank_model import _05_pn_score as bank_score
from ct_model import ct_main
from ck_model import main_ck

# Thư mục gốc của project
project_root = os.path.dirname(__file__)
result_dir = os.path.join(project_root, "result")
os.makedirs(result_dir, exist_ok=True)

def run_all():
    # Bank model
    print("=== Chạy bank_model (_05_pn_score) ===")
    bank_score.main()
    bank_output = os.path.join(result_dir, "ScoreRank.xlsx")
    df_bank = pd.read_excel(bank_output, sheet_name="RULES")
    df_bank["Model"] = "Bank"

    # Ct model
    print("=== Chạy ct_model (ct_main) ===")
    ct_main.main()
    ct_output = os.path.join(result_dir, "final_grades.xlsx")
    df_ct = pd.read_excel(ct_output)

    # Chuẩn hóa cột ct_model -> giống bank_model
    rename_map = {
        "dk": "Rule1", "dk2": "Rule2", "dk3": "Rule3",
        "dk4": "Rule4", "dk5": "Rule5",
        "tong_dk": "Rules_Sum", "grade_final": "Grade"
    }
    df_ct = df_ct.rename(columns=rename_map)
    df_ct = df_ct[["Ticker", "Rule1","Rule2","Rule3","Rule4","Rule5","Rules_Sum","Grade"]]
    df_ct["Model"] = "Company"   # thêm cột đánh dấu

    # --- CK MODEL ---
    print("=== Chạy ck_model (main_ck) ===")
    main_ck.main()
    ck_output = os.path.join(result_dir, "ck_final.xlsx")
    df_ck = pd.read_excel(ck_output)
    # Giữ cột giống bank/ct

    rename_map_ck = {
        "dky1": "Rule1", "dky2": "Rule2", "dkq1": "Rule3",
        "dkq2": "Rule4", "dkq3": "Rule5",
        "so_luong_1": "Rules_Sum", "grade": "Grade"
    }
    df_ck = df_ck.rename(columns=rename_map_ck)
    df_ck = df_ck[["Ticker","Rule1","Rule2","Rule3","Rule4","Rule5","Rules_Sum","Grade"]]
    df_ck["Model"] = "Securities"

    # --- Gộp 2 kết quả theo chiều dọc ---
    summary = pd.concat([df_bank, df_ct, df_ck], ignore_index=True)
    # Thêm cột Margin dựa theo Grade
    margin_map = {
        "A": "50%",
        "B": "40%",
        "C": "30%",
        "D": "20%",
        "E": "10%",
        "F": "0%"
    }
    summary["Margin"] = summary["Grade"].map(margin_map)

    # Đổi tên Rule1..Rule5 thành tên rõ nghĩa
    col_rename_final = {
        "Rule1": "Tăng Trưởng Năm",
        "Rule2": "Hiệu Suất Vượt Trội",
        "Rule3": "Tăng Trưởng Liên Tiếp Quý",
        "Rule4": "Tăng Trưởng Đồng Kỳ Quý",
        "Rule5": "Ưu Thế Quý Hiện Tại"
    }
    summary = summary.rename(columns=col_rename_final)

    # Xuất file summary.xlsx
    summary_path = os.path.join(result_dir, "summary.xlsx")
    summary.to_excel(summary_path, index=False)

    print(" Đã tạo file summary.xlsx:", summary_path)

if __name__ == "__main__":
    run_all()