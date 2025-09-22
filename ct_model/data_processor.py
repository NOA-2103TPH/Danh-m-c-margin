import pandas as pd

def sort_report(df):
    """Sắp xếp báo cáo theo ticker, năm và độ dài báo cáo"""
    df = df.copy()
    df = df[df['LengthReport'] < 5]
    df = df.sort_values(
        by=['Ticker', 'YearReport', 'LengthReport'],
        ascending=[True, False, False]
    )
    return df

def process_data(bs_1, cf_1, is_1):
    """Xử lý và hợp nhất dữ liệu từ các báo cáo"""
    # Sắp xếp từng DataFrame
    bs_sorted = sort_report(bs_1)
    cf_sorted = sort_report(cf_1)
    is_sorted = sort_report(is_1)

    # Tạo base DataFrame
    base_df = pd.concat([
        bs_sorted[['Ticker', 'YearReport', 'LengthReport']],
        cf_sorted[['Ticker', 'YearReport', 'LengthReport']],
        is_sorted[['Ticker', 'YearReport', 'LengthReport']]
    ]).drop_duplicates().reset_index(drop=True)

    # Gộp dữ liệu với base_df
    df = base_df.merge(bs_sorted, how="left", on=["Ticker", "YearReport", "LengthReport"])
    df = df.merge(cf_sorted, how="left", on=["Ticker", "YearReport", "LengthReport"])
    df = df.merge(is_sorted, how="left", on=["Ticker", "YearReport", "LengthReport"]) 
    df = df[df['LengthReport'] < 5]
    
    return df, bs_sorted, cf_sorted, is_sorted