import pandas as pd

def load_processed_data(file_path="Data\Processed_Data_Y.xlsx"):
    """
    Load data from Processed_Data_Y.xlsx as in original code
    """
    ck_bs = pd.read_excel(file_path, sheet_name="CK_BS")   
    ck_is = pd.read_excel(file_path, sheet_name="CK_IS")   
    ck_cf = pd.read_excel(file_path, sheet_name="CK_CF")   
    ck_nt = pd.read_excel(file_path, sheet_name="CK_Note") 
    return ck_bs, ck_is, ck_cf, ck_nt

def sort_report(df):
    """
    Sort report as in original code
    """
    df = df.copy()
    df = df.sort_values(
        by=['Ticker', 'YearReport', 'LengthReport'],
        ascending=[True, False, False]
    )
    return df

