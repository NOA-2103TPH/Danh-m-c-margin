import pandas as pd
from _01_load_data import bs_df, cf_df, is_df, note_df 

DICT_PATH = "data/BankFieldDictionary.xlsx" 
KEY = ["Ticker", "YearReport", "LengthReport"]
SHEET_MAP = {
    "IS": "IncomeStatement - Bank",
    "BS": "BalanceSheet - Bank",
    "CF": "CashFlow - Bank",
    "NT": "NoteBank",
}

def load_dict(sheet_name: str) -> dict:
    m = pd.read_excel(DICT_PATH, sheet_name=sheet_name,
                      usecols=["Field Name", "Description_VN"])
    m["Field Name"] = m["Field Name"].astype(str).str.strip().str.upper()
    m["Description_VN"] = m["Description_VN"].astype(str).str.strip()
    return dict(zip(m["Field Name"], m["Description_VN"]))

def map_columns_unique(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    cols, used = [], set()
    for c in df.columns:
        if c in KEY:
            new = c
        else:
            new = mapping.get(c, c)
            if new in used or new in KEY: 
                new = f"{new} [{c}]"
        cols.append(new); used.add(new)
    out = df.copy()
    out.columns = cols
    return out

# 1) load 4 từ điển
is_dict = load_dict(SHEET_MAP["IS"])
bs_dict = load_dict(SHEET_MAP["BS"])
cf_dict = load_dict(SHEET_MAP["CF"])
nt_dict = load_dict(SHEET_MAP["NT"])

# 2) map tên cột cho từng bảng
is_m = map_columns_unique(is_df, is_dict)
bs_m = map_columns_unique(bs_df, bs_dict)
cf_m = map_columns_unique(cf_df, cf_dict)
nt_m = map_columns_unique(note_df, nt_dict)

# 3) merge BS+IS+CF thành 1 bảng tổng theo 3 khóa
total = bs_m.merge(is_m, on=KEY, how="outer").merge(cf_m, on=KEY, how="outer")

# 4) lưu 1 file tổng với 2 sheet: TOTAL (BS+IS+CF) và NOTE (NoteBank)
out_path = "data/NHDATA_Mapped.xlsx"
with pd.ExcelWriter(out_path, engine="openpyxl") as w:
    total.to_excel(w, sheet_name="TOTAL", index=False)
    nt_m.to_excel(w, sheet_name="NOTE",  index=False)

print("Saved:", out_path, "| TOTAL shape:", total.shape, "| NOTE shape:", nt_m.shape)
