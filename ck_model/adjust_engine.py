import pandas as pd
from typing import Optional


def load_scores_as_map(scores_path: str) -> pd.Series:
    """
    Load scores file (CSV/Excel) and return a Series mapping Ticker -> grade.
    Accepts columns: Ticker + grade (or Mã/Grade/GRADE).
    """
    if scores_path.lower().endswith(('.xlsx', '.xls')):
        scores = pd.read_excel(scores_path)
    else:
        scores = pd.read_csv(scores_path)

    scores = scores.rename(columns={"Mã": "Ticker", "Grade": "grade", "GRADE": "grade"})
    if "Ticker" not in scores.columns or "grade" not in scores.columns:
        raise ValueError("Scores file missing Ticker/grade columns.")

    scores["Ticker"] = scores["Ticker"].astype(str).str.strip().str.upper()
    g_map = (
        scores.dropna(subset=["Ticker", "grade"])\
              .drop_duplicates("Ticker", keep="last")\
              .set_index("Ticker")["grade"]
    )
    return g_map


def ensure_market_share(ct: pd.DataFrame, numer_col: str, total_col: str, share_col: str):
    """
    Ensure market share column exists. If total not present, compute per (YearReport, LengthReport) or YearReport.
    """
    if share_col in ct.columns:
        return
    if total_col not in ct.columns and numer_col in ct.columns:
        grp_cols = []
        if "YearReport" in ct.columns:
            grp_cols.append("YearReport")
        if "LengthReport" in ct.columns:
            grp_cols.append("LengthReport")
        if not grp_cols:
            raise ValueError(f"Missing period columns to sum totals for {numer_col}")
        ct[total_col] = ct.groupby(grp_cols)[numer_col].transform("sum")

    if numer_col in ct.columns and total_col in ct.columns:
        ct[share_col] = ct[numer_col] / ct[total_col]


def compute_market_points(ct: pd.DataFrame) -> pd.DataFrame:
    """
    Compute 0/1 points vs median for market share metrics per period (YearReport, LengthReport if available).
    """
    grp_cols = []
    if "YearReport" in ct.columns:
        grp_cols.append("YearReport")
    if "LengthReport" in ct.columns:
        grp_cols.append("LengthReport")

    def points_vs_median(col):
        if grp_cols:
            med = ct.groupby(grp_cols)[col].transform("median")
            return (ct[col] > med).astype(int)
        return (ct[col] > ct[col].median()).astype(int)

    ct["pt_broker"] = points_vs_median("Market Share by Brokerage Revenue")
    ct["pt_revenue"] = points_vs_median("Market Share by Revenue")
    ct["pt_assets"] = points_vs_median("Market Share by Assets")
    ct["market_points"] = ct[["pt_broker", "pt_revenue", "pt_assets"]].sum(axis=1)
    return ct


def adjust_grade_logic(g, p):
    order = {"E": 0, "D": 1, "C": 2, "B": 3, "A": 4}
    inv = {v: k for k, v in order.items()}

    def bump(grade, steps):
        i = order.get(grade, 0)
        return inv[min(i + steps, 4)]

    g = (str(g) if pd.notna(g) else "E").strip().upper()
    p = int(p)
    if g == "A":
        return "C" if p == 0 else ("B" if p == 1 else "A")
    if g == "B":
        return "C" if p <= 1 else "A"
    if g == "C":
        return "D" if p == 0 else ("B" if p == 1 else "A")
    if g in ("D", "E", "F"):
        if p == 0:
            return g
        if p == 1:
            return bump(g, 1)
        return bump(g, 2)
    return g


def run_adjustment(
    ct: pd.DataFrame,
    scores_path: str = "final_rank.csv",
    filter_years=(2024,),
    filter_lengths=(5,),
    output_excel: Optional[str] = None,
) -> pd.DataFrame:
    """
    Map grades to ct, compute market share points vs median, adjust grades, filter, and optionally export.
    Returns the adjusted DataFrame for further printing/saving by caller.
    """
    ct = ct.copy()
    ct["Ticker"] = ct["Ticker"].astype(str).str.strip().str.upper()

    # Map grade from scores file
    g_map = load_scores_as_map(scores_path)
    if "grade" in ct.columns:
        ct.rename(columns={"grade": "grade_old"}, inplace=True)
    ct["grade"] = ct["Ticker"].map(g_map)

    # Ensure market share metrics
    ensure_market_share(ct, "Tổng cộng tài sản", "Tổng tài sản thị trường", "Market Share by Assets")
    ensure_market_share(ct, "Doanh thu hoạt động", "Tổng doanh thu thị trường", "Market Share by Revenue")
    ensure_market_share(ct, "Doanh thu môi giới chứng khoán", "Tổng doanh thu môi giới thị trường", "Market Share by Brokerage Revenue")

    # Compute points vs median
    ct = compute_market_points(ct)

    # Adjust grades
    ct["grade_adj"] = [adjust_grade_logic(g, p) for g, p in zip(ct["grade"], ct["market_points"])]

    # Optional diagnostics
    order = {"E": 0, "D": 1, "C": 2, "B": 3, "A": 4}
    ct["grade_num"] = ct["grade"].map(order)
    ct["grade_num_adj"] = ct["grade_adj"].map(order)
    ct["grade_shift"] = ct["grade_num_adj"] - ct["grade_num"]

    # Filter by desired years/periods
    mask_year = ct["YearReport"].isin(filter_years) if "YearReport" in ct.columns else True
    mask_len = ct["LengthReport"].isin(filter_lengths) if "LengthReport" in ct.columns else True
    filtered = ct[mask_year & mask_len].copy()

    cols = [
        "Ticker",
        "YearReport",
        "LengthReport",
        "grade",
        "pt_broker",
        "pt_revenue",
        "pt_assets",
        "market_points",
        "grade_adj",
    ]
    cols = [c for c in cols if c in filtered.columns]
    df_adj = filtered.loc[:, cols].copy()

    if output_excel:
        try:
            df_adj.to_excel(output_excel, index=False)
        except Exception:
            df_adj.to_csv(output_excel.replace(".xlsx", ".csv"), index=False, encoding="utf-8-sig")

    return df_adj
