import pandas as pd

excel_path = "data/_01_load_data.xlsx"

dfs = pd.read_excel(excel_path, sheet_name=["NH_BS", "NH_CF", "NH_IS", "NH_Note"])
bs_df   = dfs["NH_BS"].copy()
cf_df   = dfs["NH_CF"].copy()
is_df   = dfs["NH_IS"].copy()
note_df = dfs["NH_Note"].copy()

def sort_df(df: pd.DataFrame) -> pd.DataFrame:
    df["YearReport"] = pd.to_numeric(df["YearReport"], errors="coerce")
    df["LengthReport"] = pd.to_numeric(df["LengthReport"], errors="coerce")
    return df.sort_values(["Ticker", "YearReport", "LengthReport"],
                          ascending=True, kind="mergesort").reset_index(drop=True)

# Sort từng sheet
bs_df   = sort_df(bs_df)
cf_df   = sort_df(cf_df)
is_df   = sort_df(is_df)
note_df = sort_df(note_df)
