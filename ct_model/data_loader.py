import os
import pandas as pd

BASE_DIR = os.path.dirname(__file__)  # thư mục ct_model

def load_data():
    """Tải dữ liệu từ các file CSV trong thư mục Data của ct_model"""
    data_dir = os.path.join(BASE_DIR, "Data")

    bs_path = os.path.join(data_dir, "CT_BS_filled.csv")
    cf_path = os.path.join(data_dir, "CT_CF_filled.csv")
    is_path = os.path.join(data_dir, "CT_IS_filled.csv")

    print("Đọc file:", bs_path)
    print("Đọc file:", cf_path)
    print("Đọc file:", is_path)

    bs_1 = pd.read_csv(bs_path)
    cf_1 = pd.read_csv(cf_path)
    is_1 = pd.read_csv(is_path)

    return bs_1, cf_1, is_1

def test_data_loader():
    bs_1, cf_1, is_1 = load_data()
    
    # Kiểm tra dữ liệu đã được tải
    assert bs_1 is not None, "Balance sheet data not loaded"
    assert cf_1 is not None, "Cash flow data not loaded"
    assert is_1 is not None, "Income statement data not loaded"
    
    # Kiểm tra cấu trúc dữ liệu
    assert 'Ticker' in bs_1.columns, "Ticker column missing in BS"
    assert 'Ticker' in cf_1.columns, "Ticker column missing in CF"
    assert 'Ticker' in is_1.columns, "Ticker column missing in IS"
    
    print("✅ Data loader test passed!")

if __name__ == "__main__":
    test_data_loader()
