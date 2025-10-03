
import pandas as pd

DATA_PATH = "data/_02_mapping_data.xlsx"

# Helpers
def avg2_col(df, col, by="Ticker"):
    prev = df.groupby(by)[col].shift(1)
    return ((df[col] + prev) / 2).fillna(df[col])

def avg2_series(s, by_series):
    prev = s.groupby(by_series).shift(1)
    return ((s + prev) / 2).fillna(s)

def align_note_to_bctc(b: pd.DataFrame, n: pd.DataFrame,
                       keys=("Ticker","YearReport","LengthReport")) -> pd.DataFrame:
    n1 = n.groupby(list(keys), as_index=False).first()
    idx = b.set_index(list(keys)).index
    n1 = n1.set_index(list(keys)).reindex(idx).reset_index()
    return n1

def to_numeric_cols(df: pd.DataFrame, cols) -> pd.DataFrame:
    """Ép numeric các cột cần dùng; giữ nguyên cột không tồn tại."""
    exist = [c for c in cols if c in df.columns]
    if exist:
        df[exist] = df[exist].apply(pd.to_numeric, errors="coerce")
    return df

# Nhóm cột cấu phần
YOEA_COLS = [
    "2. Tiền gửi tại ngân hàng nhà nước Việt Nam",
    "3. Tiền gửi tại các TCTD khác và cho vay các TCTD khác",
    "4.1. Chứng khoán kinh doanh",
    "6.1. Cho vay khách hàng",
    "8.1. Chứng khoán đầu tư sẵn sàng để bán",
    "8.2. Chứng khoán đầu tư giữ đến ngày đáo hạn",
]

def build_base(bctc: pd.DataFrame, note: pd.DataFrame, freq: str):
    scale = 1 if freq == "year" else 4
    yoea = bctc[YOEA_COLS].sum(axis=1, min_count=1)
    debt_ib = (
        bctc["I. TỔNG NỢ PHẢI TRẢ"]
        - bctc["5. Các công cụ tài chính phái sinh và các tài sản tài chính khác"]
        - bctc["7. Các khoản nợ khác"]
    )

    base = {
        "BCTC": bctc,
        "NOTE": note,
        "SCALE": scale,
        "STOCK": {
            "ASSETS_AVG": avg2_col(bctc, "A. TỔNG CỘNG TÀI SẢN"),
            "EQUITY_AVG": avg2_col(bctc, "II. VỐN CHỦ SỞ HỮU"),
            "YOEA": yoea,
            "YOEA_AVG": avg2_series(yoea, bctc["Ticker"]),
            "DEBT_IB": debt_ib,
            "DEBT_IB_AVG": avg2_series(debt_ib, bctc["Ticker"]),
        },
        "FLOW": {
            "NI": bctc["16. Cổ đông của Công ty mẹ"],
            "NII": bctc["1. Thu nhập lãi thuần"],
            "INT_INC": bctc["1.1. Thu nhập lãi và các khoản thu nhập tương tự"],
            "INT_EXP": bctc["1.2. Chi phí lãi và các chi phí tương tự"],
            "SERV_NET": bctc["2. Lãi thuần từ hoạt động dịch vụ"],
            "SERV_COST": bctc["2.2. Chi phí hoạt động dịch vụ"],
            "OTHER_NET": bctc["6. Lãi/lỗ thuần từ hoạt động khác"],
            "INVEST_INC": bctc["7. Thu nhập từ góp vốn, mua cổ phần"],
            "PBT": bctc["12. Tổng lợi nhuận trước thuế"],
            "OPEX": bctc["9. Chi phí hoạt động"],
            "TOT_OP_INC": bctc["8. Tổng thu nhập hoạt động"],
        },
    }
    return base

def compute_master(base: dict) -> pd.DataFrame:
    b = base["BCTC"] 
    n_raw = base["NOTE"]
    S = base["STOCK"]; F = base["FLOW"]; k = base["SCALE"]

    # Align NOTE theo đúng khóa của BCTC
    n = align_note_to_bctc(b, n_raw)

    # (khuyến nghị) ép numeric cho các cột NOTE/BCTC dùng ngay bên dưới
    note_need_numeric = [
        "Tiền gửi không kỳ hạn", "Tiền gửi có kỳ hạn", "Chỉ số CAR",
        "Nợ đủ tiêu chuẩn", "Nợ cần chú ý", "Nợ dưới tiêu chuẩn", "Nợ nghi ngờ", "Nợ xấu có khả năng mất vốn",
        "Chi phí dự phòng giảm giá các khoản đầu tư dài hạn và dự phòng nợ khó đòi",
    ]
    bctc_need_numeric = [
        "2.1. Thu nhập từ hoạt động dịch vụ", "3. Tiền gửi của khách hàng",
        "6.1. Cho vay khách hàng", "2. Tiền gửi và vay các Tổ chức tín dụng khác",
        "A. TỔNG CỘNG TÀI SẢN",
    ]
    n = to_numeric_cols(n, note_need_numeric)
    b = to_numeric_cols(b, bctc_need_numeric)

    # ---- Frame kết quả ----
    m = b[["Ticker", "YearReport", "LengthReport"]].copy()

    # ===== Profitability =====
    m["ROA"] = F["NI"] / S["ASSETS_AVG"] * k
    m["ROE"] = F["NI"] / S["EQUITY_AVG"] * k
    m["Tài sản sinh lời (YOEA)"] = S["YOEA"]
    m["Nợ phải trả có lãi"] = S["DEBT_IB"]
    m["NIM"] = F["NII"] / S["YOEA_AVG"] * k
    m["Lãi suất đầu ra bình quân"] = F["INT_INC"] / S["YOEA_AVG"] * k
    m["Lãi suất đầu vào bình quân"] = - F["INT_EXP"] / S["DEBT_IB_AVG"] * k
    m["Chênh lệch lãi suất"] = m["Lãi suất đầu ra bình quân"] - m["Lãi suất đầu vào bình quân"]
    # >>> bỏ dấu trừ để tỷ lệ dương (lower is better ở logic PN)
    m["Tỷ lệ chi phí lãi / thu nhập lãi"] = - F["INT_EXP"] / F["INT_INC"]
    m["Biên lợi nhuận từ hoạt động dịch vụ (NSFM)"] = F["SERV_NET"] / S["YOEA_AVG"] * k
    m["Tỷ lệ chi phí dịch vụ/ thu nhập dịch vụ"] = - F["SERV_COST"] / b["2.1. Thu nhập từ hoạt động dịch vụ"]
    m["Tỷ lệ thu nhập phi lãi thuần (NNIM)"] = (F["OTHER_NET"] - F["INVEST_INC"]) / S["YOEA_AVG"] * k
    m["Tỷ lệ lợi nhuận trước thuế/ thu nhập lãi"] = F["PBT"] / F["INT_INC"]
    m["Tỷ lệ chi phí/thu nhập (CIR)"] = - F["OPEX"] / F["TOT_OP_INC"]

    # ===== Asset Management / Liquidity =====
    m["CASA"] = n["Tiền gửi không kỳ hạn"] + n["Tiền gửi có kỳ hạn"]
    m["Tiền gửi thanh toán"] = n["Tiền gửi không kỳ hạn"]
    m["Tỷ lệ CASA"] = n["Tiền gửi không kỳ hạn"] / b["3. Tiền gửi của khách hàng"]

    # ===== Risk / Credit quality =====
    m["Dự phòng rủi ro tín dụng/ Dư nợ cho vay"] = - b["6.2. Dự phòng rủi ro cho vay khách hàng"] / b["6.1. Cho vay khách hàng"]
    m["LDR (Market 1)"] = b["6.1. Cho vay khách hàng"] / b["3. Tiền gửi của khách hàng"]
    m["LDR (Market 2)"] = b["3. Tiền gửi tại các TCTD khác và cho vay các TCTD khác"] / b["2. Tiền gửi và vay các Tổ chức tín dụng khác"]
    m["DPRRTD/CV Khách hàng và CK đầu tư"] = - b["11. Chi phí dự phòng rủi ro tín dụng"] / (
        b["7. Thu nhập từ góp vốn, mua cổ phần"]
        + b["10. LN thuần từ hoạt động kinh doanh trước CP dự phòng rủi ro tín dụng"]
        - b["11. Chi phí dự phòng rủi ro tín dụng"]
    )
    m["Lãi, phí phải thu/Lãi, phí phải trả"] = b["12.2. Các khoản lãi và phí phải thu"] / b["7.1. Các khoản lãi, phí phải trả"]
    m["Earning Assets to Total Assets"] = m["Tài sản sinh lời (YOEA)"] / b["A. TỔNG CỘNG TÀI SẢN"]
    m["CAR"] = n["Chỉ số CAR"]
    m["LDR"] = (b["6.1. Cho vay khách hàng"] + b["3. Tiền gửi tại các TCTD khác và cho vay các TCTD khác"]) / (
        b["2. Tiền gửi và vay các Tổ chức tín dụng khác"] + b["3. Tiền gửi của khách hàng"]
    )
    m["Tổng nợ phải trả / VCSH"] = b["I. TỔNG NỢ PHẢI TRẢ"] / b["II. VỐN CHỦ SỞ HỮU"]
    m["LLR (NEW)"] = - b["6.2. Dự phòng rủi ro cho vay khách hàng"] / (n["Nợ dưới tiêu chuẩn"] + n["Nợ nghi ngờ"] + n["Nợ xấu có khả năng mất vốn"])

    # ===== Nợ nhóm =====
    m["Nợ nhóm 1 %"] = n["Nợ đủ tiêu chuẩn"] / b["6.1. Cho vay khách hàng"]
    m["Nợ nhóm 2 %"] = n["Nợ cần chú ý"] / b["6.1. Cho vay khách hàng"]
    m["Nợ nhóm 3 %"] = n["Nợ dưới tiêu chuẩn"] / b["6.1. Cho vay khách hàng"]
    m["Nợ nhóm 4 %"] = n["Nợ nghi ngờ"] / b["6.1. Cho vay khách hàng"]
    m["Nợ nhóm 5 %"] = n["Nợ xấu có khả năng mất vốn"] / b["6.1. Cho vay khách hàng"]
    m["Overdue debt ratio (2-5)"] = m["Nợ nhóm 2 %"] + m["Nợ nhóm 3 %"] + m["Nợ nhóm 4 %"] + m["Nợ nhóm 5 %"]
    m["NPL Ratio (3-5)"] = m["Nợ nhóm 3 %"] + m["Nợ nhóm 4 %"] + m["Nợ nhóm 5 %"]
    m["Tỷ lệ sử dụng DP để xử lý nợ khó đòi/Customer Loan"] = n["Chi phí dự phòng giảm giá các khoản đầu tư dài hạn và dự phòng nợ khó đòi"] / b["6.1. Cho vay khách hàng"]

    # ===== Margins & efficiency =====
    m["NPM"] = F["NI"] / F["TOT_OP_INC"]
    m["Thu nhập hoạt động trên thu nhập lãi"] = F["TOT_OP_INC"] / F["INT_INC"]
    m["Tỷ suất sinh lời bình quân trên dư nợ"] = F["INT_INC"] / b["6.1. Cho vay khách hàng"]
    m["Tỷ lệ cho vay/Tổng tài sản"] = b["6.1. Cho vay khách hàng"] / S["ASSETS_AVG"]
    m["Tỷ suất sinh lời trên tổng tài sản"] = F["TOT_OP_INC"] / S["ASSETS_AVG"] * k
    m["Tỷ lệ đòn bẩy tài chính"] = S["ASSETS_AVG"] / S["EQUITY_AVG"]

    # ===== Growth =====
    if k == 1:
        # Annual growth (YoY by year)
        m["Annual Credit Growth (Market 1)"] = b.groupby("Ticker")["6.1. Cho vay khách hàng"].pct_change(fill_method=None)
        m["Annual Credit Growth (Market 2)"] = b.groupby("Ticker")["3. Tiền gửi tại các TCTD khác và cho vay các TCTD khác"].pct_change(fill_method=None)
        m["Annual Interest Income Growth"]   = b.groupby("Ticker")["1.1. Thu nhập lãi và các khoản thu nhập tương tự"].pct_change(fill_method=None)
        m["Annual Net Income Growth"]        = b.groupby("Ticker")["16. Cổ đông của Công ty mẹ"].pct_change(fill_method=None)
        m["Annual Asset Growth"]             = b.groupby("Ticker")["A. TỔNG CỘNG TÀI SẢN"].pct_change(fill_method=None)
    else:
        # QYoY (cùng quý năm trước) — ổn định mùa vụ
        gq = b.groupby(["Ticker","LengthReport"])
        m["QYoY Credit Growth (M1)"]        = gq["6.1. Cho vay khách hàng"].pct_change(fill_method=None)
        m["QYoY Credit Growth (M2)"]        = gq["3. Tiền gửi tại các TCTD khác và cho vay các TCTD khác"].pct_change(fill_method=None)
        m["QYoY Interest Income Growth"]    = gq["1.1. Thu nhập lãi và các khoản thu nhập tương tự"].pct_change(fill_method=None)
        m["QYoY Net Income Growth"]         = gq["16. Cổ đông của Công ty mẹ"].pct_change(fill_method=None)
        m["QYoY Asset Growth"]              = gq["A. TỔNG CỘNG TÀI SẢN"].pct_change(fill_method=None)

    # Dọn NaN/Inf nếu có (tùy chọn)
    m.replace([float("inf"), float("-inf")], pd.NA, inplace=True)
    return m

# ========= LOAD & SPLIT =========
bctc_total = pd.read_excel(DATA_PATH, sheet_name="TOTAL")
note_total = pd.read_excel(DATA_PATH, sheet_name="NOTE")

bctc_y = bctc_total.query("LengthReport == 5").sort_values(["Ticker","YearReport"]).reset_index(drop=True)
note_y  = note_total.query("LengthReport == 5").sort_values(["Ticker","YearReport"]).reset_index(drop=True)

bctc_q = bctc_total.query("LengthReport in [1,2,3,4]").sort_values(["Ticker","YearReport","LengthReport"]).reset_index(drop=True)
note_q  = note_total.query("LengthReport in [1,2,3,4]").sort_values(["Ticker","YearReport","LengthReport"]).reset_index(drop=True)

# ========= BUILD & COMPUTE =========
base_y = build_base(bctc_y, note_y, freq="year")
base_q = build_base(bctc_q, note_q, freq="quarter")
master_y = compute_master(base_y)
master_q = compute_master(base_q)

with pd.ExcelWriter("data/_03_compute_ratios.xlsx", engine="openpyxl") as w:
    master_y.to_excel(w, sheet_name="YEAR", index=False)
    master_q.to_excel(w, sheet_name="QUARTER_ANN", index=False)
print("Done")
