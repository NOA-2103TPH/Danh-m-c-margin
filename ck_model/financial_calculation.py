import pandas as pd
import numpy as np

def calculate_averages(ct):
    """
    Calculate averages as in original code
    """
    # Các chỉ tiêu bình quân
    ct["TTS_prev"] = ct.groupby("Ticker")["Tổng cộng tài sản"].shift(-1)
    ct["Tổng tài sản bình quân"] = (ct["Tổng cộng tài sản"] + ct["TTS_prev"]) / 2
    ct["VCSH_prev"] = ct.groupby("Ticker")["Vốn chủ sở hữu"].shift(-1)
    ct["Vốn chủ sở hữu bình quân"] = (ct["Vốn chủ sở hữu"] + ct["VCSH_prev"]) / 2
    ct["Tài sản tự doanh"] = ct["Các tài sản tài chính ghi nhận thông qua lãi lỗ (FVTPL)"] + ct["Các khoản đầu tư nắm giữ đến ngày đáo hạn (HTM)"]+ct["Các khoản tài chính sẵn sàng để bán (AFS)"]
    ct["TSTD_prev"] = ct.groupby("Ticker")["Tài sản tự doanh"].shift(-1)
    ct["Tài sản tự doanh bình quân"] = (ct["Tài sản tự doanh"] + ct["TSTD_prev"]) / 2
    ct["KPT_prev"] = ct.groupby("Ticker")["Các khoản phải thu"].shift(-1)
    ct["Khoản phải thu bình quân"] = (ct["Các khoản phải thu"] + ct["KPT_prev"]) / 2
    ct["Dư nợ margin_prev"] = ct.groupby("Ticker")["Cho vay nghiệp vụ ký quỹ (margin)"].shift(-1)
    ct["Dư nợ cho vay margin bình quân"] = (ct["Cho vay nghiệp vụ ký quỹ (margin)"] + ct["Dư nợ margin_prev"]) / 2
    return ct

def calculate_market_totals(ct):
    """
    Calculate market totals as in original code
    """
    ct["Tổng tài sản thị trường"] = ct.groupby("YearReport")["Tổng cộng tài sản"].transform("sum")
    ct["Tổng vốn chủ sở hữu thị trường"] = ct.groupby("YearReport")["Vốn chủ sở hữu"].transform("sum")
    ct["Tổng dư nợ cho vay margin thị trường"] = ct.groupby("YearReport")["Cho vay nghiệp vụ ký quỹ (margin)"].transform("sum")
    ct["Tổng doanh thu thị trường"] = ct.groupby("YearReport")["Doanh thu hoạt động"].transform("sum")
    ct["Tổng doanh thu môi giới thị trường"] = ct.groupby("YearReport")["Doanh thu môi giới chứng khoán"].transform("sum")
  
    ct["Tổng tài sản bình quân"] = ct["Tổng tài sản bình quân"].fillna(ct["Tổng cộng tài sản"])
    ct["Vốn chủ sở hữu bình quân"] = ct["Vốn chủ sở hữu bình quân"].fillna(ct["Vốn đầu tư của chủ sở hữu"])
    ct["Tài sản tự doanh bình quân"] = ct["Tài sản tự doanh bình quân"].fillna(ct["Tài sản tự doanh"])
    ct["Khoản phải thu bình quân"] = ct["Khoản phải thu bình quân"].fillna(ct["Các khoản phải thu"])
    ct["Dư nợ cho vay margin bình quân"] = ct["Dư nợ cho vay margin bình quân"].fillna(ct["Cho vay nghiệp vụ ký quỹ (margin)"])

    ct["Thu nhập có lãi"] = ct["Lãi từ tài sản tài chính ghi nhận thông qua lãi/lỗ (FVTPL)"] + ct["Lãi từ các khoản đầu tư nắm giữ đến ngày đáo hạn (HTM)"] + ct["Lãi từ các khoản cho vay và phải thu"] + ct["Lãi từ các tài sản tài chính sẵn sàng để bán (AFS)"] + ct["Lãi từ công cụ phái sinh phòng ngừa rủi ro"] + ct["Lãi tiền gửi, tiền cho vay"]
    ct["Tài sản sinh lãi"] = ct["Tiền gửi ngân hàng"] + ct["Giá trị thuần đầu tư tài sản tài chính ngắn hạn"] + ct["Các tài sản tài chính ghi nhận thông qua lãi lỗ (FVTPL)"] + ct["Các khoản đầu tư nắm giữ đến ngày đáo hạn (HTM)"] + ct["Các khoản cho vay"] + ct["Các khoản tài chính sẵn sàng để bán (AFS)"]
    ct["Lãi từ hoạt động tự doanh"] = ct["Lãi từ tài sản tài chính ghi nhận thông qua lãi/lỗ (FVTPL)"] + ct["Lãi từ các khoản đầu tư nắm giữ đến ngày đáo hạn (HTM)"]
    ct['Lợi nhuận trước thuế và lãi vay'] = ct["Tổng lợi nhuận kế toán trước thuế"] + ct['Chi phí lãi vay'] - ct['Chi phí thuế TNDN hoãn lại'] 

    return ct

def calculate_ratios(ct):
    """
    Calculate financial ratios as in original code
    """
    # ==============================
    # BỘ CÔNG THỨC CHỈ TIÊU TÀI CHÍNH
    # ==============================
    #Thị phần 
    ct["Market Share by Assets"] = ct["Tổng cộng tài sản"] / ct["Tổng tài sản thị trường"]
    ct["Market Share by Equity"] = ct["Vốn chủ sở hữu"] / ct["Tổng vốn chủ sở hữu thị trường"]
    ct["Market Share by Margin Loan"] = ct["Cho vay nghiệp vụ ký quỹ (margin)"] / ct["Tổng dư nợ cho vay margin thị trường"]
    ct["Market Share by Revenue"] = ct["Doanh thu hoạt động"] / ct["Tổng doanh thu thị trường"]
    ct["Market Share by Brokerage Revenue"] = ct["Doanh thu môi giới chứng khoán"] / ct["Tổng doanh thu môi giới thị trường"]   
    # Hiệu quả sử dụng tài sản
    ct["Asset Turnover"] = ct["Doanh thu hoạt động"] / ct["Tổng tài sản bình quân"]
    # Khả năng thu hồi nợ
    ct["Receivables Turnover"] = ct["Doanh thu hoạt động"] / ct["Khoản phải thu bình quân"]
    ct["Days Sales Outstanding (DSO)"] = 365 / ct["Receivables Turnover"]
    # Khả năng thanh toán phải trả
    ct["Payables Turnover"] = -ct["Chi phí hoạt động tự doanh"] / ct["Phải trả người bán ngắn hạn"]
    ct["Days Payable Outstanding (DPO)"] = 365 / ct["Payables Turnover"]
    # Tài sản rủi ro cao
    ct["High Risk Assets Ratio"] = (ct["Các khoản cho vay"] + ct["Giá trị thuần đầu tư tài sản tài chính ngắn hạn"] + ct["Các khoản phải thu"]) / ct["Vốn chủ sở hữu"]
    # Vốn lưu động thuần
    ct["Net Working Capital"] = ct["Tài sản ngắn hạn"] - ct["Nợ ngắn hạn"]
    #Tỉ lệ thanh toán
    ct["Current Ratio"] = ct["Tài sản ngắn hạn"] / ct["Tổng cộng tài sản"]
    ct["QuickRatio"] = (ct["Tiền và tương đương tiền"] + ct["Giá trị thuần đầu tư tài sản tài chính ngắn hạn"] + ct["Các khoản phải thu"]) / ct["Nợ ngắn hạn"]
    ct["Cash Ratio"] = ct["Tiền và tương đương tiền"] / ct["Nợ ngắn hạn"]
    # Defensive Interval Ratio
    ct["DIR"] =  (ct["Tiền và tương đương tiền"] + ct["Giá trị thuần đầu tư tài sản tài chính ngắn hạn"] + ct["Các khoản phải thu"]) / -(ct["Chi phí hoạt động kinh doanh"])
    # Alias để khớp tên metric người dùng yêu cầu
    ct["Defensive Interval Ratio"] = ct["DIR"]
    # Đòn bẩy tài chính
    ct["D/E"] = ct["Nợ phải trả"] / ct["Vốn chủ sở hữu"]
    ct["D/A"] = ct["Nợ phải trả"] / ct["Tổng cộng tài sản"]
    ct["Financial Leverage"] = ct["Tổng cộng tài sản"] / ct["Vốn chủ sở hữu"]
    ct["Debt-to-Capital"] = (ct["Vay và nợ thuê tài sản tài chính ngắn hạn"] + ct["Vay và nợ thuê tài sản tài chính dài hạn"]) / ct["Vốn chủ sở hữu"]
    #Hiệu suất nhân viên chứng khoán
    ct["Hiệu suất nhân viên"]= ct["Doanh thu hoạt động"] / ct["Các khoản trích nộp phúc lợi nhân viên"]
    # Khả năng trả nợ   
    ct["Debt Service Coverage Ratio (DSCR)"] = ct["Tổng lợi nhuận kế toán trước thuế"] / ct["Nợ phải trả"]
    ct["Interest Coverage Ratio"] = ct["Tổng lợi nhuận kế toán trước thuế"] / ct["Chi phí lãi vay"]
    # Cơ cấu nợ
    ct["Short term Debt to Margin Loan"] = ct["Nợ ngắn hạn"] / ct["Các khoản cho vay"]
    ct["Cơ cấu dư nợ"] = ct["Các khoản cho vay"] / ct["Vốn chủ sở hữu"]

    # Khả năng sinh lời
    ct["Net Profit Margin"] = ct["Lợi nhuận kế toán sau thuế"] / ct["Doanh thu hoạt động"]
    ct["Operating Margin"] = ct["Tổng lợi nhuận kế toán trước thuế"] / ct["Doanh thu hoạt động"]

    # EPS
    ct["EPS"] = ct["Lãi cơ bản trên cổ phiếu"]

    # Hiệu quả sử dụng vốn
    ct["ROA"] = ct["Lợi nhuận kế toán sau thuế"] / ct["Tổng tài sản bình quân"]
    ct["ROE"] = ct["Lợi nhuận kế toán sau thuế"] / ct["Vốn chủ sở hữu bình quân"]
    ct["ROCE"] = ct["Tổng lợi nhuận kế toán trước thuế"] / (ct["Tổng cộng tài sản"] - ct["Nợ ngắn hạn"])
    ct["YEA"] = ct["Thu nhập có lãi"] / ct["Tài sản sinh lãi"]

    # Hiệu suất kinh doanh
    ct["Hiệu suất môi giới"] = ct["Doanh thu môi giới chứng khoán"] / -ct["Chi phí môi giới chứng khoán"]
    ct["Tỷ trọng doanh thu môi giới"] = ct["Doanh thu môi giới chứng khoán"] / ct["Doanh thu hoạt động"]
    ct["Hiệu suất tự doanh"] = ct["Lãi từ hoạt động tự doanh"] / -ct["Chi phí hoạt động tự doanh"]
    ct["Brokerage Margin"] = (ct["Doanh thu môi giới chứng khoán"] + ct["Chi phí môi giới chứng khoán"]) / ct["Doanh thu môi giới chứng khoán"]
    ct["Tỷ trọng doanh thu tự doanh"] = ct["Lãi từ hoạt động tự doanh"] / ct["Doanh thu hoạt động"]
    ct["Khả năng tự doanh"] = ct["Lãi từ hoạt động tự doanh"] / ct["Tài sản tự doanh bình quân"]

    #Average Commission per Trade
    ct["ACT"] = ct["Doanh thu môi giới chứng khoán"] / (ct["Khối lượng Giao dịch thực hiện trong kỳ của NĐT"] + ct["Khối lượng Giao dịch thực hiện trong kỳ của CTCK"] )
    #Commission-to-Volume Ratio
    ct["CVR"] = ct["Doanh thu môi giới chứng khoán"] / (ct["Giá trị Giao dịch thực hiện trong kỳ của NĐT"] + ct["Giá trị Giao dịch thực hiện trong kỳ của CTCK"] )
    # Tăng trưởng
    ct["Tăng trưởng doanh thu"] = ct["Doanh thu hoạt động"].pct_change(periods = -1)
    ct["Tăng trưởng lợi nhuận ròng"] = ct["Lợi nhuận kế toán sau thuế"].pct_change(periods = -1)
    ct["Tăng trưởng tổng tài sản"] = ct["Tổng cộng tài sản"].pct_change(periods = -1)
    ct["Tăng trưởng vốn chủ sở hữu"] = ct["Vốn chủ sở hữu"].pct_change(periods = -1)
    ct["Tăng trưởng dư nợ cho vay margin"] = ct["Cho vay nghiệp vụ ký quỹ (margin)"].pct_change(periods = -1)
    ct["Tăng trưởng EPS"] = ct["Lãi cơ bản trên cổ phiếu"].pct_change(periods = -1)


    #Cơ cấu chứng chỉ quỹ và trái phiếu trong danh mục FVTPL
    ct["Cơ cấu chứng chỉ quỹ và trái phiếu trong danh mục FVTPL"] = (ct["Chứng chỉ quỹ"] + ct["Trái phiếu"]) / ct["Các tài sản tài chính ghi nhận thông qua lãi lỗ (FVTPL)"]

    #Doanh thu cho vay margin/ Dư nợ cho vay margin
    ct["Doanh thu cho vay margin/ Dư nợ cho vay margin"] = ct["Lãi từ các khoản cho vay và phải thu"] / ct["Cho vay nghiệp vụ ký quỹ (margin)"]

    #Doanh thu môi giới/ Tổng giá trị giao dịch
    ct["Doanh thu môi giới/ Tổng giá trị giao dịch"] = ct["Doanh thu môi giới chứng khoán"] / (ct["Giá trị Giao dịch thực hiện trong kỳ của NĐT"] + ct["Giá trị Giao dịch thực hiện trong kỳ của CTCK"] )
    #Tỷ lệ giảm giá chứng khoán kinh doanh
    ct["Tỷ lệ giảm giá chứng khoán kinh doanh"] = ct["Dự phòng giảm giá chứng khoán kinh doanh"] / ct["Giá trị thuần đầu tư tài sản tài chính ngắn hạn"]


    #Dư nợ cho vay margin/ Vốn chủ sở hữu <200%
    ct["Dư nợ cho vay margin/ Vốn chủ sở hữu"] = ct["Cho vay nghiệp vụ ký quỹ (margin)"] / ct["Vốn chủ sở hữu"]

    #Margin Spread
    ct["margin spread"]= (ct["Lãi từ các khoản cho vay và phải thu"] - ct["Chi phí lãi vay"]) / ct["Cho vay nghiệp vụ ký quỹ (margin)"]

    # Khả năng thanh toán phải trả
    return ct
