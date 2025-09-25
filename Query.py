import os
import pandas as pd

# Đường dẫn tới file summary.xlsx
project_root = os.path.dirname(__file__)
result_dir = os.path.join(project_root, "result")
summary_path = os.path.join(result_dir, "summary.xlsx")

def show_top(n=10, model=None):
    """
    Hiển thị n mã đầu tiên trong summary.xlsx
    Nếu model = 'bk' hoặc 'ct' thì chỉ lọc theo loại đó
    """
    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"Chưa có file {summary_path}, hãy chạy main.py trước.")

    df = pd.read_excel(summary_path)

    if model:
        df = df[df["Model"] == model]   # lọc theo model
        print(f"Hiển thị {n} mã đầu tiên thuộc model = {model}")
    else:
        print(f"Hiển thị {n} mã đầu tiên (tất cả model)")

    top_n = df.head(n)
    print(top_n.to_string(index=False))
    return top_n

def query_ticker(ticker):
    """Tra cứu thông tin một mã trong summary.xlsx"""
    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"Chưa có file {summary_path}, hãy chạy main.py trước.")

    df = pd.read_excel(summary_path)
    result = df[df["Ticker"].str.upper() == ticker.upper()]  

    if result.empty:
        print(f"Không tìm thấy mã {ticker}")
    else:
        print(f"Kết quả cho {ticker}:")
        print(result.to_string(index=False))
    return result

if __name__ == "__main__":
    # Ví dụ
    show_top(30, model="Bank")  # 30 mã đầu tiên của bank_model
    #show_top(30, model="Company")  # 30 mã đầu tiên của ct_model
    #show_top(30)              # 30 mã đầu tiên bất kỳ
    # query_ticker("vre")
    # query_ticker("STB")
    # query_ticker("VRE")
    # query_ticker("VIC")
    # query_ticker("VTP")
