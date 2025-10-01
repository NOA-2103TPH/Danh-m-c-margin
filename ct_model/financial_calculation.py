import pandas as pd


def calculate_financial_metrics(cf3, bs_sorted, cf_sorted, is_sorted):
    cf2 = cf3[['Ticker', 'YearReport', 'LengthReport']].copy()
    #cf
    cf_sorted = cf2.merge(
        cf_sorted, 
        on=["Ticker","YearReport","LengthReport"], 
        how="left"
    )
    bs_sorted = cf2.merge(
        bs_sorted, 
        on=["Ticker","YearReport","LengthReport"], 
        how="left"
    )
    is_sorted = cf2.merge(
        is_sorted, 
        on=["Ticker","YearReport","LengthReport"], 
        how="left"
    )
    """Tính toán các chỉ số tài chính"""
    # CF metrics
    cf2["Lợi nhuận kế toán trước thuế"] = cf_sorted["CFA1"] # Mã số 1
    cf2["Khấu hao và phân bổ"] = cf_sorted["CFA2"] # Mã số 2
    cf2["Các khoản dự phòng"] = cf_sorted["CFA3"] # Mã số 3
    cf2["Lãi/lỗ chênh lệch tỷ giá chưa thực hiện"] = cf_sorted["CFA4"] # Mã số 4
    cf2["Lãi/lỗ từ hoạt động đầu tư"] = cf_sorted["CFA6"] # Mã số 5 (bao gồm 2 mã số 05)
    cf2["Chi phí lãi vay"] = cf_sorted["CFA7"] # Mã số 6
    cf2["Lãi/lỗ trước những thay đổi vốn lưu động"] = cf_sorted["CFA9"] # Mã số 8
    cf2["Tăng/giảm các khoản phải thu"] = cf_sorted["CFA10"] # Mã số 9
    cf2["Tăng/giảm các khoản phải trả"] =cf_sorted["CFA12"] # Mã số 11
    cf2["Tăng/giảm chi phí trả trước"] = cf_sorted["CFA13"] # Mã số 12
    cf2["Chi phí lãi vay đã trả"] = cf_sorted["CFA14"] # Mã số 14
    cf2["Thuế thu nhập doanh nghiệp đã trả"] = cf_sorted["CFA15"] # Mã số 15
    cf2["Tiền thu khác từ các hoạt động kinh doanh"] = cf_sorted["CFA16"] # Mã số 16
    cf2["Tiền chi khác từ các hoạt động kinh doanh"] = cf_sorted["CFA17"] # Mã số 17
    cf2["Tiền mua tài sản cố định và các tài sản dài hạn khác"] = cf_sorted["CFA19"] # Mã số 21
    cf2["Tiền thu được từ thanh lý tài sản cố định"] = cf_sorted["CFA20"] # Mã số 22
    cf2["Tiền thu từ cho vay hoặc thu từ phát hành công cụ nợ"] = cf_sorted["CFA22"] # Mã số 24
    cf2["Tiền thu từ việc bán các khoản đầu tư vào các doanh nghiệp khác"] = cf_sorted['CFA24'] # Mã số 26
    cf2["Cổ tức và tiền lãi nhận được"] = cf_sorted["CFA25"] # Mã số 27
    cf2["Tiền thu từ phát hành cổ phiếu và vốn góp"] = cf_sorted["CFA27"] # Mã số 31
    cf2["Tiền thu được các khoản đi vay"] = cf_sorted["CFA29"] # Mã số 33
    cf2['Tiền trả các khoản đi vay'] = cf_sorted["CFA30"] # Mã số 34
    cf2["Lưu chuyển tiền thuần trong kỳ"] = cf_sorted["CFA35"] # Mã số 50
    cf2["Tiền và tương đương tiền đầu kỳ"] = cf_sorted["CFA36"] # Mã số 60
    cf2["Ảnh hưởng của chênh lệch tỷ giá"] = cf_sorted["CFA37"] # Mã số 61 và 62
    cf2["Tiền và tương đương tiền cuối kỳ"] = cf_sorted["CFA38"] # Mã số 70



    
    cf2['(Lợi ích)/chi phí thuế TNDN hoãn lại'] = cf_sorted['CFA3'] 
    cf2['Lưu chuyển tiền thuần từ HĐKD'] = cf_sorted['CFA18'] # Mã số 20
    cf2["Biến động hàng tồn kho"] = cf_sorted["CFA11"] # Mã số 10
    cf2["Chi tiêu vốn"] = cf_sorted["CFA19"]
    cf2["Lưu chuyển tiền thuần từ HĐĐT"] = cf_sorted["CFA26"] # Mã số 30
    cf2['Cổ tức đã trả'] = cf_sorted['CFA32'] # Mã số 36
    cf2["Lưu chuyển tiền thuần từ HĐTC"] = cf_sorted["CFA34"] # Mã số 40


    #bs
    cf2['TSNH'] = bs_sorted['BSA1']
    cf2['Tiền và các khoản tương đương tiền'] = bs_sorted['BSA2']
    cf2['Đầu tư tài chính ngắn hạn'] = bs_sorted['BSA5']
    cf2['Các khoản phải thu ngắn hạn'] = bs_sorted['BSA8']
    cf2['Phải thu khách hàng ngắn hạn'] = bs_sorted['BSA9']
    cf2['Dự phòng phải thu khó đòi ngắn hạn'] = bs_sorted['BSA14']
    cf2['HTK'] = bs_sorted["BSA15"]
    cf2['Chi phí trả trước ngắn hạn'] = bs_sorted["BSA19"]
    cf2['TSDH'] = bs_sorted['BSA23']
    cf2['Các khoản phải thu dài hạn'] = bs_sorted['BSA24']
    cf2['Phải thu khách hàng dài hạn'] = bs_sorted['BSA25']
    cf2['Dự phòng phải thu khó đòi dài hạn'] = bs_sorted['BSA28'] 
    cf2['Tài sản cố định'] = bs_sorted['BSA29']
    cf2["Tài sản cố định hữu hình"] = bs_sorted["BSA30"]
    cf2["Tài sản cố định vô hình"] = bs_sorted["BSA36"]
    cf2["Bất động sản đầu tư"] = bs_sorted['BSA40']
    cf2['Đầu tư tài chính dài hạn'] = bs_sorted['BSA43']
    cf2["Tài sản dài hạn khác"] = bs_sorted["BSA49"]
    cf2['Tổng tài sản'] = bs_sorted['BSA53'] 
    cf2['Nợ phải trả'] = bs_sorted['BSA54'] 
    cf2['Nợ ngắn hạn'] = bs_sorted['BSA55']
    cf2["Vay nợ thuê tài chính ngắn hạn"] = bs_sorted['BSA56']
    cf2["Phải trả người bán ngắn hạn"] = bs_sorted['BSA57']
    cf2["Người mua trả tiền trước"] = bs_sorted['BSA58']
    cf2["Thuế phải nộp Ngân sách Nhà nước"] = bs_sorted['BSA59']
    cf2["Phải trả người lao động"] = bs_sorted['BSA60']

    cf2["Chi phí phải trả"] = bs_sorted['BSA61']
    cf2["Phải trả ngắn hạn khác"] = bs_sorted['BSA64']
    cf2["Phải trả người bán dài hạn"] = bs_sorted['BSA68']


    cf2['Vay nợ thuê tài chính dài hạn'] = bs_sorted['BSA71']

    cf2['Nợ dài hạn'] = bs_sorted['BSA67'] 
    cf2['Vốn chủ sở hữu'] = bs_sorted['BSA78'] 
    cf2['Tổng nguồn vốn'] = bs_sorted['BSA96'] 
    cf2["Tài sản dở dang dài hạn"] = bs_sorted["BSA163"]
    cf2['Xây dựng cơ bản dở dang'] = bs_sorted['BSA188'] 

    #is
    cf2['Doanh thu thuần về bán hàng và cung cấp dịch vụ'] = is_sorted['ISA3']
    cf2["Giá vốn hàng bán"] = -is_sorted["ISA4"]
    cf2['Lợi nhuận gộp về bán hàng và cung cấp dịch vụ'] = is_sorted['ISA5']
    
    cf2['Doanh thu hoạt động tài chính'] = is_sorted['ISA6'] 
    cf2['Chi phí lãi vay is'] = - is_sorted['ISA8'] 
    cf2["Chi phí bán hàng"] = - is_sorted["ISA9"]
    cf2["Chi phí quản lý doanh nghiệp"] = - is_sorted["ISA10"]
    cf2["Lợi nhuận thuần từ HĐKD"] = is_sorted["ISA11"]
    cf2['LNTT'] = is_sorted['ISA16'] 
    cf2['Thuế TNDN hoãn lại'] = - is_sorted['ISA18']
    cf2['Chi phí thuế TNDN'] = - is_sorted['ISA19'] 

    cf2['LNST'] = is_sorted['ISA20']
    # ... (thêm tất cả các metrics từ IS)
    
    return cf2


  


def calculate_financial(cf2):
    #VCSH
    cf2["VCSH_binh_quan_prev"] = cf2.groupby("Ticker")["Vốn chủ sở hữu"].shift(-1)
    cf2["VCSH_binh_quan"] = (cf2["Vốn chủ sở hữu"] + cf2["VCSH_binh_quan_prev"]) / 2
    #Nợ ngắn hạn
    cf2["No_ngan_han_prev"] = cf2.groupby("Ticker")["Nợ ngắn hạn"].shift(-1)
    cf2["No_ngan_han_binh_quan"] = (cf2["Nợ ngắn hạn"] + cf2["No_ngan_han_prev"]) / 2
    # Nợ dài hạn
    cf2["No_dai_han_prev"] = cf2.groupby("Ticker")["Nợ dài hạn"].shift(-1)
    cf2["No_dai_han_binh_quan"] = (cf2["Nợ dài hạn"] + cf2["No_dai_han_prev"]) / 2
    # Tổng tài sản
    cf2["TTS_prev"] = cf2.groupby("Ticker")["Tổng tài sản"].shift(-1)
    cf2["TTS_binh_quan"] = (cf2["Tổng tài sản"] + cf2["TTS_prev"]) / 2
    # Vốn vay
    cf2["Von_vay_prev"] = cf2.groupby("Ticker")["Vay nợ thuê tài chính ngắn hạn"].shift(-1) + cf2.groupby("Ticker")["Vay nợ thuê tài chính dài hạn"].shift(-1)
    cf2["Von_vay_binh_quan"] = (cf2["Vay nợ thuê tài chính ngắn hạn"] + cf2["Vay nợ thuê tài chính dài hạn"] + cf2["Von_vay_prev"]) / 2
    # Phải trả người bán
    cf2['Phải trả người bán'] = cf2['Phải trả người bán ngắn hạn'] + cf2['Phải trả người bán dài hạn']
    cf2["Phai_tra_nguoi_ban_prev"] = cf2.groupby("Ticker")["Phải trả người bán"].shift(-1)
    cf2["Phai_tra_nguoi_ban_binh_quan"] = (cf2["Phải trả người bán"] + cf2["Phai_tra_nguoi_ban_prev"]) / 2
    # Phải thu khách hàng ngắn hạn bình quân
    cf2["Phai_thu_khach_hang_NH_prev"] = cf2.groupby("Ticker")["Phải thu khách hàng ngắn hạn"].shift(-1)
    cf2["Phai_thu_khach_hang_NH_binh_quan"] = (cf2["Phải thu khách hàng ngắn hạn"] + cf2["Phai_thu_khach_hang_NH_prev"]) / 2
    #Tài sản cố định bình quân
    cf2["TSCĐ_prev"] = cf2.groupby("Ticker")["Tài sản cố định"].shift(-1)
    cf2["TSCĐ_binh_quan"] = (cf2["Tài sản cố định"] + cf2["TSCĐ_prev"]) / 2
    # TSNH bình quân
    cf2["TSNH_prev"] = cf2.groupby("Ticker")["TSNH"].shift(-1)
    cf2["TSNH_binh_quan"] = (cf2["TSNH"] + cf2["TSNH_prev"]) / 2

    # Doanh thu thuần về bán hàng và cung cấp dịch vụ bình quân 
    cf2["DTT_banhang_prev"] = cf2.groupby("Ticker")["Doanh thu thuần về bán hàng và cung cấp dịch vụ"].shift(-1)
    cf2["DTT_banhang_binh_quan"] = (cf2["Doanh thu thuần về bán hàng và cung cấp dịch vụ"] + cf2["DTT_banhang_prev"]) / 2

    # TSNH bình quân
    cf2["HTK_prev"] = cf2.groupby("Ticker")["HTK"].shift(-1)
    cf2["HTK_binh_quan"] = (cf2["HTK"] + cf2["HTK_prev"]) / 2
    cf2['Doanh thu thuần'] = cf2['Doanh thu thuần về bán hàng và cung cấp dịch vụ'] + cf2['Doanh thu hoạt động tài chính'] 
    cf2['DTT_prev'] = cf2.groupby('Ticker')['Doanh thu thuần'].shift(-1)

    #Thành phần công thức

    cf2['Lợi nhuận trước thuế và lãi vay'] = cf2['LNTT'] + cf2['Chi phí lãi vay is'] - cf2['Thuế TNDN hoãn lại'] #1
    cf2['Dự phòng nợ phải thu khó đòi'] = cf2['Dự phòng phải thu khó đòi ngắn hạn'] + cf2['Dự phòng phải thu khó đòi dài hạn']
    cf2['Tổng số nợ phải thu'] = cf2['Các khoản phải thu ngắn hạn'] + cf2['Các khoản phải thu dài hạn']
    cf2['Nguồn tài trợ thường xuyên'] = cf2["Vốn chủ sở hữu"] + cf2["Nợ dài hạn"]
    cf2['Vốn vay'] = cf2["Vay nợ thuê tài chính ngắn hạn"] + cf2['Vay nợ thuê tài chính dài hạn']
    cf2["TSCĐ đã và đang đầu tư"] = (cf2["Tài sản cố định"]+cf2["Xây dựng cơ bản dở dang"])
    #cf2["Lợi nhuận trước thuế và lãi vay"] = (cf2["LNST"]+cf2["Chi phí thuế TNDN"]+cf2["Chi phí lãi vay is"])
    cf2["Tổng số nợ phải thu người mua"] = (cf2["Phải thu khách hàng ngắn hạn"] + cf2["Phải thu khách hàng dài hạn"])
    cf2["Nợ phải thu người mua_prev"] = cf2.groupby("Ticker")["Tổng số nợ phải thu người mua"].shift(-1)
    cf2["Nợ phải thu người mua bình quân"] = (cf2["Tổng số nợ phải thu người mua"] + cf2["Nợ phải thu người mua_prev"]) / 2

    cf2["Vốn hoạt động thuần"] = (cf2["TSNH"]-cf2["Nợ ngắn hạn"])
    cf2['Tài sản ngắn hạn sau điều chỉnh'] = cf2['TSNH'] - cf2['Chi phí trả trước ngắn hạn'] 
    # Công thức tài chính
    # Chương 4 Đánh giá tinh hình và phân tích cấu trúc tài chính

    cf2["Tỷ trọng VCSH trong NV"] = cf2["Vốn chủ sở hữu"] / cf2["Tổng nguồn vốn"]
    cf2["Tỷ trọng NPT trong NV"] = cf2["Nợ phải trả"] / cf2["Tổng nguồn vốn"]
    cf2["Hệ số tài trợ"] = cf2["Vốn chủ sở hữu"]/cf2["Tổng tài sản"] # càng cao càng tốt
    # Nguồn tài trợ thường xuyên = VCSH + Nợ dài dạn
    cf2["Hệ số tự tài trợ TSDH"] = cf2['Nguồn tài trợ thường xuyên']/cf2["TSDH"] # >=1 là tốt
    cf2["Hệ số tự tài trợ TSCĐ"] = cf2['Nguồn tài trợ thường xuyên']/ cf2["TSCĐ đã và đang đầu tư"] # Nếu Hệ số tự tài trợ TSDH =<1 thì mới tính ct này, ct này >=1 tốt
    cf2["Hệ số khả năng thanh toán của dòng tiền"] = cf2["Lưu chuyển tiền thuần từ HĐKD"]/cf2["No_ngan_han_binh_quan"] # >1 là tốt
    cf2["Hệ số khả năng thanh toán tổng quát"] = cf2["Tổng tài sản"]/cf2["Nợ phải trả"] # >=1 là tốt
    #cf2["Hệ số khả năng thanh khoản của dòng tiền"] =
    cf2["ROE"] = cf2["LNST"]/cf2["VCSH_binh_quan"] # càng cao càng tốt
    cf2["ROIC"] = cf2["Lợi nhuận trước thuế và lãi vay"]*0.8 / (cf2["VCSH_binh_quan"]+cf2["Von_vay_binh_quan"]) # Vốn vay = vay nợ thuê tài chính ngắn hạn + Vay và nợ tài chính dài hạn + Trái phiếu chuyển đổi
    cf2["ROCE"] = cf2["Lợi nhuận trước thuế và lãi vay"]/(cf2["VCSH_binh_quan"]+cf2["No_dai_han_binh_quan"]) 
    cf2["BEP"] = cf2["Lợi nhuận trước thuế và lãi vay"]/cf2["TTS_binh_quan"]
    cf2["Tốc độ tăng trưởng bền vững"]= cf2["LNST"]* (1- (cf2["Cổ tức đã trả"] / cf2["LNST"])) / cf2["Vốn chủ sở hữu"] # càng cao càng tốt
    cf2['Tốc độ tăng trưởng doanh thu thuần'] = cf2.groupby('Ticker')['Doanh thu thuần'].pct_change(-1) * 100
    cf2['Tốc độ thay đổi của tổng doanh thu thuần tiêu thụ'] = (cf2['Doanh thu thuần'] / cf2['DTT_prev'] - 1)*100
    cf2["Tốc độ tăng trưởng lợi nhuận"] =cf2.groupby('Ticker')['LNTT'].pct_change(-1) * 100
    cf2['Tốc độ thay đổi của lợi nhuận trước thuế và lãi vay'] = cf2.groupby('Ticker')['Lợi nhuận trước thuế và lãi vay'].pct_change(-1) * 100

    #cf2['Tốc độ thay đổi của lợi nhuận trước thuế và lãi vay'] = (cf2['Lợi nhuận trước thuế và lãi vay'] / cf2['LNTT_lV_prev'] - 1)*100
    cf2['Tốc độ thay đổi của lợi nhuận sau thuế'] = cf2.groupby('Ticker')['LNST'].pct_change(-1) * 100
    cf2["Hệ số nợ so với tài sản"] = cf2["Nợ phải trả"]/cf2["Tổng tài sản"]

    #Chương 5 Phân tích tình hình và khả năng thanh toán
    #Thành phần
    cf2["Mức tiền hàng bán chịu"] =  cf2['Doanh thu thuần về bán hàng và cung cấp dịch vụ']
    cf2["Mức tiền hàng bán chịu_prev"] = cf2.groupby("Ticker")["Mức tiền hàng bán chịu"].shift(-1)
    cf2["Mức tiền hàng bán chịu bình quân"] = (cf2["Mức tiền hàng bán chịu"] + cf2["Mức tiền hàng bán chịu_prev"]) / 2
    cf2["Mức tiền hàng mua chịu"] = cf2["Giá vốn hàng bán"]
    cf2["Mức tiền hàng mua chịu_prev"] = cf2.groupby("Ticker")["Mức tiền hàng mua chịu"].shift(-1)
    cf2["Mức tiền hàng mua chịu bình quân"] = (cf2["Mức tiền hàng mua chịu"]+cf2["Mức tiền hàng mua chịu_prev"]) /2
    # Đánh giá khái quát tình hình bị chiếm dụng hay đi chiếm dụng trong thanh toán
    cf2["Tỷ lệ giữa nợ phải thu so với nợ phải trả"] = cf2['Tổng số nợ phải thu'] / cf2["Nợ phải trả"]
    cf2["Tỷ trọng nợ phải thu chiếm trong TTS"] = cf2['Tổng số nợ phải thu'] / cf2["Tổng tài sản"]
    cf2["Tỷ trọng nợ phải trả chiếm trong tổng NV"] = cf2["Nợ phải trả"]/cf2["Tổng nguồn vốn"]
    cf2["Tỷ lệ giữa nợ phải thu người mua so với tổng tiền hàng bán ra trong kỳ"] = cf2["Tổng số nợ phải thu người mua"]/cf2["Doanh thu thuần về bán hàng và cung cấp dịch vụ"] #TỔng số nợ phải thu người mua phát sinh trong kì = phải thu ngắn hạn của khách hàng + phải thu dài hạn của khách hàng
    cf2["Tỷ lệ giữa dự phòng nợ phải thu khó đòi so với tổng số nợ phải thu người mua"] = cf2["Dự phòng nợ phải thu khó đòi"] /cf2["Tổng số nợ phải thu người mua"]
    #cf2["Tỷ lệ giữa nợ phải thu quá hạn so với nợ phải trả quá hạn"]
    #cf2["Tỷ lệ giữa nợ đã thu trong kỳ so với tổng số nợ phải thu trong kỳ"]
    cf2["Tỷ lệ giữa nợ còn phải thu cuối kỳ so với tổng số nợ phải thu trong kỳ"] = cf2['Tổng số nợ phải thu']/ (cf2['Tổng số nợ phải thu'] - cf2['Dự phòng phải thu khó đòi ngắn hạn'])
    cf2["Số lần thu hồi tiền hàng"] = cf2['Doanh thu thuần về bán hàng và cung cấp dịch vụ']/(cf2["Phải thu khách hàng ngắn hạn"]+cf2["Phải thu khách hàng dài hạn"])
    cf2["Thời gian thu hồi tiền hàng"] = cf2["Nợ phải thu người mua bình quân"]/ (cf2["Mức tiền hàng bán chịu_prev"]/360)
    cf2["Số lần thanh toán tiền hàng"] = cf2["Giá vốn hàng bán"] / cf2["Phai_tra_nguoi_ban_binh_quan"]
    cf2["Thời gian thanh toán tiền hàng"] = cf2["Phai_tra_nguoi_ban_binh_quan"]/(cf2["Mức tiền hàng mua chịu bình quân"]/360)
    cf2["Hệ số khả năng thanh toán nợ ngắn hạn"] = cf2['Tài sản ngắn hạn sau điều chỉnh']/cf2["Nợ ngắn hạn"]
    cf2["Hệ số khả năng thanh toán nhanh"] = (cf2['Tài sản ngắn hạn sau điều chỉnh'] - cf2["HTK"])/cf2["Nợ ngắn hạn"]
    cf2["Hệ số khả năng thanh toán tức thời"] = cf2["Tiền và các khoản tương đương tiền"]/cf2["Nợ ngắn hạn"]
    #cf2["Hệ số khả năng thanh toán nợ đến hạn"] = cf2["Tiền và các khoản tương đương tiền"]/
    #cf2["Hệ số khả năng thanh toán nợ quán hạn trong vòng 3 tháng"]
    cf2["Hệ số khả năng chuyển đổi thành tiền của TSNH"] = cf2["Tiền và các khoản tương đương tiền"]/cf2['Tài sản ngắn hạn sau điều chỉnh']
    cf2["Hệ số khả năng thanh toán nợ dài hạn"] = cf2["TSDH"]/cf2["Nợ dài hạn"]
    #Nguồn tài trợ thường xuyên = Tổng tài sản - Nợ ngắn hạn
    cf2["Hệ số giữa TSDH so với nguồn tài trợ thường xuyên"]= cf2["TSDH"]/cf2['Nguồn tài trợ thường xuyên']
    cf2["Hệ số giữa vốn hoạt động thuần so với nợ dài hạn"]= cf2["Vốn hoạt động thuần"]/cf2["Nợ dài hạn"]#>0 là tốt
    cf2["Hệ số giữa nợ phải trả so với VCSH"] = cf2["Nợ phải trả"]/cf2["Vốn chủ sở hữu"]
    cf2["Hệ số giữa nợ dài hạn so với VCSH"] = cf2["Nợ dài hạn"]/cf2["Vốn chủ sở hữu"]
    cf2["Hệ số khả năng chi trả lãi vay"] = cf2['Lợi nhuận trước thuế và lãi vay'] / cf2["Chi phí lãi vay is"] #1
    # cf2['Hệ số khả năng chi trả lãi cố định']
    cf2["Hệ số giữa nợ phải trả so với giá trị thuần của TSHH"] = cf2["Nợ phải trả"] / (cf2["Vốn chủ sở hữu"]- cf2["Tài sản cố định vô hình"])


    # Đòn bẩy tài chính theo quan hệ giữa NV(TTS) với VCSH, giữa nợ phải trả với VCSH, Nợ phải trả giữa TTS
    # Công thức
    cf2['Đòn bẩy tài chính (theo quan hệ giữa TTS với VCSH)'] = cf2["Tổng nguồn vốn"] / cf2['Vốn chủ sở hữu']
    cf2['Đòn bẩy tài chính (theo quan hệ giữa Nợ phải trả với VCSH)'] = cf2["Nợ phải trả"] / cf2['Vốn chủ sở hữu']
    cf2['Đòn bẩy tài chính (theo quan hệ giữa Nợ phải trả với TTS)'] = cf2["Nợ phải trả"] / cf2['Tổng tài sản']
    #cf2['Độ nhạy của đòn bẩy kinh doanh'] = cf2['Tốc độ thay đổi của lợi nhuận trước thuế và lãi vay']/ cf2['Tốc độ thay đổi của tổng doanh thu thuần']
    # bctc của vinamilk chỉ có Dự phòng phải thu khó đòi mã 137
    cf2['Độ nhạy của đòn bẩy kinh doanh'] = cf2['Tốc độ thay đổi của lợi nhuận trước thuế và lãi vay'] / cf2['Tốc độ thay đổi của tổng doanh thu thuần tiêu thụ']
    cf2['Tốc độ gia tăng lợi nhuận trước thuế và lãi vay'] = cf2['Tốc độ thay đổi của lợi nhuận trước thuế và lãi vay']
    cf2['Độ nhạy của đòn bẩy tài chính'] = cf2['Tốc độ thay đổi của lợi nhuận sau thuế'] / cf2['Tốc độ thay đổi của lợi nhuận trước thuế và lãi vay']
    #cf2['Tốc độ gia tăng lợi nhuận sau thuế'] = cf2['Tốc độ thay đổi của lợi nhuận sau thuế']
    cf2['Độ nhạy của đòn bẩy tổng hợp'] = cf2['Tốc độ thay đổi của lợi nhuận sau thuế'] / cf2['Tốc độ thay đổi của tổng doanh thu thuần tiêu thụ']
    #cf2['Tốc độ tăng trưởng lợi nhuận'] = cf2.groupby('Ticker')['LNTT'].pct_change(-1) * 100
    #cf2["Tỷ trọng nợ phải thu khó đòi so với tổng số nợ phải thu"]
    cf2['Tỷ lệ giữa dự phòng nợ phải thu khó đòi so với tổng số nợ phải thu'] = cf2['Dự phòng nợ phải thu khó đòi'] / cf2['Tổng số nợ phải thu']
    #cf2["Tỷ trọng nợ phải thu khó đòi so với tổng số tài sản (%)"] = 
    cf2["Số lần luân chuyển TSCĐ"] = cf2["Doanh thu thuần"]/cf2["TSCĐ_binh_quan"]
    cf2["Số lần luân chuyển TSNH"] = cf2["Doanh thu thuần"]/cf2["TSNH_binh_quan"]
    cf2["Số lần luân chuyển HTK"] = cf2["Giá vốn hàng bán"]/cf2["HTK_binh_quan"]
    cf2['Hệ số tài trợ thường xuyên'] = cf2['Nguồn tài trợ thường xuyên']/cf2['Tổng nguồn vốn']
    cf2['Hệ số tài trợ tạm thời'] = cf2['Nợ ngắn hạn']/cf2['Tổng nguồn vốn']
    cf2['Hệ số tự tài trợ TSNH'] = cf2['Nợ ngắn hạn']/cf2['Tài sản ngắn hạn sau điều chỉnh']

    # chương 7
    cf2['Mức biến động tăng/giảm doanh thu thuần kỳ phân tích so với kỳ gốc'] = cf2.groupby('Ticker')['Doanh thu thuần'].diff(-1)
    #cf2['Mức biến động tăng/giảm doanh thu thuần kỳ phân tích so với kỳ gốc'] = cf2['Doanh thu thuần'] - cf2['DTT_prev']

    cf2['Tỷ lệ (%) doanh thu thuần kỳ phân tích so với kỳ gốc (%)'] = cf2['Doanh thu thuần'] / cf2['DTT_prev'] * 100

    #cf2['Tỷ lệ (%) doanh thu thuần kỳ phân tích so với kỳ gốc (%)'] = cf2['Doanh thu thuần'] / cf2['DTT_prev'] * 100
    cf2['Tỷ trọng doanh thu thuần về bán hàng và cung cấp dịch vụ trong tổng doanh thu thuần (%)'] = cf2['Doanh thu thuần về bán hàng và cung cấp dịch vụ'] / cf2['Doanh thu thuần'] * 100
    cf2['Tỷ trọng doanh thu HĐTC trong tổng doanh thu thuần (%)'] = cf2['Doanh thu hoạt động tài chính'] / cf2['Doanh thu thuần'] * 100
    cf2['Mức biến động tăng/giảm LNST kỳ phân tích so với kỳ gốc'] = cf2.groupby('Ticker')['LNST'].diff(-1)
    #cf2['Mức biến động tăng/giảm LNST kỳ phân tích so với kỳ gốc'] = cf2['LNST'] - cf2['LNST_prev']
    cf2['LNST_prev'] = cf2.groupby('Ticker')['LNST'].shift(-1)
    cf2['Tỷ lệ % LNST kỳ phân tích so với kỳ gốc (%)'] = cf2['LNST'] / cf2['LNST_prev'] * 100
    #cf2['Tỷ lệ % LNST kỳ phân tích so với kỳ gốc (%)'] = cf2['LNST'] / cf2['LNST_prev'] * 100
    #Bình quân
    #Tài sản cố định bình quân


    # Thành phần công thức
    cf2["LNST từ HĐKD"] = cf2["Lợi nhuận thuần từ HĐKD"] * 0.8
    cf2["Tài sản thuần thuộc HĐKD"] = (cf2['Tổng tài sản']+ cf2['Tiền và các khoản tương đương tiền']+cf2['Đầu tư tài chính ngắn hạn']+cf2['Đầu tư tài chính dài hạn']) - (cf2["Phải trả người bán"]+cf2["Người mua trả tiền trước"]+cf2["Thuế phải nộp Ngân sách Nhà nước"] +cf2["Chi phí phải trả"] + cf2['Phải trả người lao động']+ cf2["Phải trả ngắn hạn khác"])
    cf2['TSDH sử dụng cho HĐKD'] = (cf2["Tài sản cố định hữu hình"] + cf2["Tài sản cố định vô hình"] + cf2["Bất động sản đầu tư"] +cf2["Tài sản dở dang dài hạn"]+ cf2["Tài sản dài hạn khác"])
    cf2["Tài sản thuộc HĐKD"] = (cf2['Tổng tài sản']-cf2['Tiền và các khoản tương đương tiền']-cf2['Đầu tư tài chính ngắn hạn']-cf2['Đầu tư tài chính dài hạn'])
    cf2['Tổng chi phí kinh doanh'] = (cf2["Giá vốn hàng bán"]+cf2["Chi phí bán hàng"]+cf2["Chi phí quản lý doanh nghiệp"])
    cf2['Chi phí hoạt động'] = cf2['Tổng chi phí kinh doanh']

    # BÌnh quân thành phần
    cf2["Tài sản thuần thuộc HĐKD_prev"] = cf2.groupby("Ticker")["Tài sản thuần thuộc HĐKD"].shift(-1)
    cf2["Tài sản thuần bình quân thuộc HĐKD"] = (cf2["Tài sản thuần thuộc HĐKD"] + cf2["Tài sản thuần thuộc HĐKD_prev"]) / 2
    cf2["TSDH sử dụng cho HĐKD_prev"] = cf2.groupby("Ticker")["TSDH sử dụng cho HĐKD"].shift(-1)
    cf2["TSDH bình quân sử dụng cho HĐKD"] = (cf2["TSDH sử dụng cho HĐKD"] + cf2["TSDH sử dụng cho HĐKD_prev"]) / 2
    cf2["Tài sản thuộc HĐKD_prev"] = cf2.groupby("Ticker")["Tài sản thuộc HĐKD"].shift(-1)
    cf2["Tài sản bình quân thuộc HĐKD"] = (cf2["Tài sản thuộc HĐKD"] + cf2["Tài sản thuộc HĐKD_prev"]) / 2

    # Chương 8
    #cf2['Tỷ suất sinh lợi của từng đối tượng']
    #cf2['Mức hoa phí của từng đối tượng']
    #cf2['Tỷ suất hao phí của từng đối tượng']
    cf2['ROA'] = cf2["LNST"]/ cf2["TTS_binh_quan"]
    cf2['Sức sinh lợi của TSCĐ'] = cf2["LNST"] / cf2["TSCĐ_binh_quan"]
    cf2["Sức sinh lợi của tài sản thuần thuộc HĐKD"] = cf2["LNST từ HĐKD"] / cf2["Tài sản thuần bình quân thuộc HĐKD"]
    cf2["Sức sinh lợi của TSDH sử dụng cho HĐKD"] = cf2['LNST'] / cf2["TSDH bình quân sử dụng cho HĐKD"]
    cf2['Sức sinh lợi của tài sản sử dụng cho HĐKD'] = cf2["LNST từ HĐKD"]/cf2["Tài sản bình quân thuộc HĐKD"]
    #cf2["Sức sinh lợi của vốn cổ phần thường"] = (cf2["LNST"] - cf2["Cổ tức ưu đãi"])
    cf2["Sức sinh lợi của giá vốn hàng bán tính theo lợi nhuận sau thuế từ HĐKD"] = cf2['LNST từ HĐKD']/ cf2["Giá vốn hàng bán"]
    cf2["Hệ số chênh lệch giá"] = cf2['Lợi nhuận gộp về bán hàng và cung cấp dịch vụ'] / cf2["Giá vốn hàng bán"]
    cf2["Sức sinh lợi của chi phí kinh doanh"] = cf2["LNST từ HĐKD"]/cf2['Tổng chi phí kinh doanh']
    cf2["Sức sinh lợi của chi phí bán hàng"] = cf2["LNST từ HĐKD"]/ cf2["Chi phí bán hàng"]
    cf2["Sức sinh lợi của chi phí quản lý DN"] = cf2["LNST từ HĐKD"]/cf2["Chi phí quản lý doanh nghiệp"]
    cf2["Sức sinh lợi của chi phí hoạt động"] = cf2["LNST từ HĐKD"]/cf2['Chi phí hoạt động']
    cf2['ROS'] = cf2["LNST"] / cf2["Doanh thu thuần"]
    #cf2['Sức sinh lợi của doanh thu thuần đã điều chỉnh'] = (cf2['LNST']-cf2['Cổ tức ưu đãi'])/cf2['Doanh thu thuần'] chưa có cổ tức ưu đãi
    cf2['Sức sinh lợi của doanh thu thuần từ HĐKD'] = cf2["Lợi nhuận thuần từ HĐKD"]/cf2['Doanh thu thuần']
    cf2["Hệ số lợi nhuận gộp"] =cf2['Lợi nhuận gộp về bán hàng và cung cấp dịch vụ']/ cf2['Doanh thu thuần']
    cf2['Hệ số lợi nhuận thuần từ HĐKD'] = cf2['LNST từ HĐKD']/cf2["Doanh thu thuần"]
    cf2["Số lần luân chuyển cho TSDH sử dụng cho HĐKD"] = cf2['Doanh thu thuần'] / cf2["TSDH bình quân sử dụng cho HĐKD"]
    cf2['Số lần luân chuyển của tài sản (TAT)'] = cf2['Doanh thu thuần']/ cf2["TTS_binh_quan"]
    cf2["Số lần luân chuyển của tài sản thuần thuộc HĐKD"] = cf2["Doanh thu thuần"] / cf2["Tài sản thuần thuộc HĐKD"]
    cf2["Số lần luân chuyển của tài sản sử dụng cho HĐKD"] = cf2["Doanh thu thuần"] / cf2["Tài sản bình quân thuộc HĐKD"]
    #cf2["Thời gian luân chuyển TSNH"]
    #cf2["Lãi cơ bản trên cổ phiếu"]
    #cf2["EPS suy giảm"]
    #cf2['P/B']
    #cf2["P/E"]
    #cf2["Mức cổ tức chi trả"]
    #cf2["Mức cổ tức so với giá thị trường của cổ phần"]

    #Chương 9
    # Thành phần
    cf2["Biến động hàng tồn kho_now"] = cf2.groupby("Ticker")["Biến động hàng tồn kho"].shift(0)
    cf2["Biến động hàng tồn kho_prev1"] = cf2.groupby("Ticker")["Biến động hàng tồn kho"].shift(-1)
    cf2["Biến động hàng tồn kho_prev2"] = cf2.groupby("Ticker")["Biến động hàng tồn kho"].shift(-2)
    cf2["Biến động hàng tồn kho 3 năm liên tiếp"] = cf2["Biến động hàng tồn kho_now"] + cf2["Biến động hàng tồn kho_prev1"] + cf2["Biến động hàng tồn kho_prev2"]
    cf2["Chi tiêu vốn_now"] = cf2.groupby("Ticker")["Chi tiêu vốn"].shift(0)
    cf2["Chi tiêu vốn_prev1"] = cf2.groupby("Ticker")["Chi tiêu vốn"].shift(-1)
    cf2["Chi tiêu vốn_prev2"] = cf2.groupby("Ticker")["Chi tiêu vốn"].shift(-2)
    cf2["Chi tiêu vốn 3 năm liên tiếp"] = cf2["Chi tiêu vốn_now"] + cf2["Chi tiêu vốn_prev1"] + cf2["Chi tiêu vốn_prev2"]
    cf2["Cổ tức đã trả_now"] = cf2.groupby("Ticker")["Cổ tức đã trả"].shift(0)
    cf2["Cổ tức đã trả_prev1"] = cf2.groupby("Ticker")["Cổ tức đã trả"].shift(-1)
    cf2["Cổ tức đã trả_prev2"] = cf2.groupby("Ticker")["Cổ tức đã trả"].shift(-2)
    cf2["Cổ tức đã trả 3 năm liên tiếp"] = cf2["Cổ tức đã trả_now"] + cf2["Cổ tức đã trả_prev1"] + cf2["Cổ tức đã trả_prev2"]
    cf2["Lưu chuyển tiền thuần từ HĐKD_now"] = cf2.groupby("Ticker")["Lưu chuyển tiền thuần từ HĐKD"].shift(0)
    cf2["Lưu chuyển tiền thuần từ HĐKD_prev1"] = cf2.groupby("Ticker")["Lưu chuyển tiền thuần từ HĐKD"].shift(-1)
    cf2["Lưu chuyển tiền thuần từ HĐKD_prev2"] = cf2.groupby("Ticker")["Lưu chuyển tiền thuần từ HĐKD"].shift(-2)
    cf2["Lưu chuyển tiền thuần từ HĐKD 3 năm liên tiếp"] = cf2["Lưu chuyển tiền thuần từ HĐKD_now"] + cf2["Lưu chuyển tiền thuần từ HĐKD_prev1"] + cf2["Lưu chuyển tiền thuần từ HĐKD_prev2"]
    cf2["Tổng các khoản chi tiêu trong 3 năm liên tiếp"] = cf2["Biến động hàng tồn kho 3 năm liên tiếp"] + cf2["Chi tiêu vốn 3 năm liên tiếp"] + cf2["Cổ tức đã trả 3 năm liên tiếp"]
    cf2["Dòng tiền dự do trong kỳ"] = cf2["Lưu chuyển tiền thuần từ HĐKD 3 năm liên tiếp"] -  cf2["Chi tiêu vốn 3 năm liên tiếp"] - cf2["Cổ tức đã trả 3 năm liên tiếp"]
    cf2["Tổng dòng tiền lưu chuyển thuần"] = cf2["Lưu chuyển tiền thuần từ HĐKD"] + cf2["Lưu chuyển tiền thuần từ HĐTC"] + cf2["Lưu chuyển tiền thuần từ HĐĐT"]
    cf2["Dòng tiền vào của HĐKD"] = (

        cf2["Lợi nhuận kế toán trước thuế"] +
        cf2["Khấu hao và phân bổ"] +
        cf2["Các khoản dự phòng"] +
        cf2["Lãi/lỗ chênh lệch tỷ giá chưa thực hiện"] +
        cf2["Lãi/lỗ từ hoạt động đầu tư"] +
        cf2["Chi phí lãi vay"] +
        cf2["Tăng/giảm các khoản phải thu"] +
        cf2["Biến động hàng tồn kho"] +
        cf2["Tăng/giảm các khoản phải trả"] +
        cf2["Tăng/giảm chi phí trả trước"] +
        cf2["Tiền thu khác từ các hoạt động kinh doanh"]
    )

    cf2["Dòng tiền vào của HĐTC"] = (
        cf2["Tiền thu được từ thanh lý tài sản cố định"]+
        cf2["Tiền thu từ cho vay hoặc thu từ phát hành công cụ nợ"]+
        cf2["Tiền thu từ việc bán các khoản đầu tư vào các doanh nghiệp khác"]+
        cf2["Cổ tức và tiền lãi nhận được"]
    )

    cf2["Dòng tiền vào của HĐĐT"] = (
        cf2["Tiền thu từ phát hành cổ phiếu và vốn góp"]+
        cf2["Tiền thu được các khoản đi vay"]

    )
    
    cf2["Dòng tiền vào"] = (
        cf2["Lợi nhuận kế toán trước thuế"] +
        cf2["Khấu hao và phân bổ"] +
        cf2["Các khoản dự phòng"] +
        cf2["Lãi/lỗ chênh lệch tỷ giá chưa thực hiện"] +
        cf2["Lãi/lỗ từ hoạt động đầu tư"] +
        cf2["Chi phí lãi vay"] +
        cf2["Tăng/giảm các khoản phải thu"] +
        cf2["Biến động hàng tồn kho"] +
        cf2["Tăng/giảm các khoản phải trả"] +
        cf2["Tăng/giảm chi phí trả trước"] +
        cf2["Tiền thu khác từ các hoạt động kinh doanh"]+
        cf2["Tiền thu được từ thanh lý tài sản cố định"]+
        cf2["Tiền thu từ cho vay hoặc thu từ phát hành công cụ nợ"]+
        cf2["Tiền thu từ việc bán các khoản đầu tư vào các doanh nghiệp khác"]+
        cf2["Cổ tức và tiền lãi nhận được"] +
        cf2["Tiền thu từ phát hành cổ phiếu và vốn góp"] +
        cf2["Tiền thu được các khoản đi vay"]
        
    )

    cf2["Dòng tiền ra từ HĐKD"] = cf2["Dòng tiền vào của HĐKD"] - cf2['Lưu chuyển tiền thuần từ HĐKD']
    cf2["Dòng tiền ra"] = (
        (cf2["Lợi nhuận kế toán trước thuế"] +
        cf2["Khấu hao và phân bổ"] +
        cf2["Các khoản dự phòng"] +
        cf2["Lãi/lỗ chênh lệch tỷ giá chưa thực hiện"] +
        cf2["Lãi/lỗ từ hoạt động đầu tư"] +
        cf2["Chi phí lãi vay"] +
        cf2["Tăng/giảm các khoản phải thu"] +
        cf2["Biến động hàng tồn kho"] +
        cf2["Tăng/giảm các khoản phải trả"] +
        cf2["Tăng/giảm chi phí trả trước"] +
        cf2["Tiền thu khác từ các hoạt động kinh doanh"]+
        cf2["Tiền thu được từ thanh lý tài sản cố định"]+
        cf2["Tiền thu từ cho vay hoặc thu từ phát hành công cụ nợ"]+
        cf2["Tiền thu từ việc bán các khoản đầu tư vào các doanh nghiệp khác"]+
        cf2["Cổ tức và tiền lãi nhận được"] +
        cf2["Tiền thu từ phát hành cổ phiếu và vốn góp"] +
        cf2["Tiền thu được các khoản đi vay"]) - 
        (
        cf2['Lưu chuyển tiền thuần từ HĐKD']+
        cf2["Lưu chuyển tiền thuần từ HĐTC"]+
        cf2["Lưu chuyển tiền thuần từ HĐĐT"]
        )
    )

    cf2["Dòng tiền ra từ HĐTC"] = cf2["Dòng tiền vào của HĐTC"] - cf2["Lưu chuyển tiền thuần từ HĐTC"]
    cf2["Dòng tiền ra từ HĐĐT"] = cf2["Dòng tiền vào của HĐĐT"] - cf2["Lưu chuyển tiền thuần từ HĐĐT"]
    # Công thức
    cf2["Tỷ suất an toàn của dòng tiền (%)"] = cf2["Lưu chuyển tiền thuần từ HĐKD 3 năm liên tiếp"] / cf2["Tổng các khoản chi tiêu trong 3 năm liên tiếp"] # đã thêm vào metric
    cf2["Tỷ suất dòng tiền tự do (%)"] = cf2["Dòng tiền dự do trong kỳ"] / cf2["Lưu chuyển tiền thuần từ HĐKD"] # đã thêm vào metric
    cf2["Tỷ trọng dòng tiền lưu chuyển thuần từ HĐKD chiếm trong tổng dòng tiền lưu chuyển thuần (%)"] = cf2["Lưu chuyển tiền thuần từ HĐKD"] / cf2["Tổng dòng tiền lưu chuyển thuần"] # đã thêm vào metric
    #cf2["Tỷ trọng dòng tiền lưu chuyển thuần từ HĐĐT chiếm trong tổng dòng tiền lưu chuyển thuần (%)"] = cf2["Lưu chuyển tiền thuần từ HĐĐT"] / cf2["Tổng dòng tiền lưu chuyển thuần"]
    #cf2["Tỷ trọng dòng tiền lưu chuyển thuần từ HĐTC chiếm trong tổng dòng tiền lưu chuyển thuần (%)"] = cf2["Lưu chuyển tiền thuần từ HĐTC"] / cf2["Tổng dòng tiền lưu chuyển thuần"]
    cf2["Tỷ trọng của từng dòng tiền vào từ HĐKD chiếm trong tổng số dòng tiền vào trong kỳ"] = cf2["Dòng tiền vào của HĐKD"]/cf2["Dòng tiền vào"]
    cf2["Tỷ trọng của từng dòng tiền vào từ HĐTC chiếm trong tổng số dòng tiền vào trong kỳ"] = cf2["Dòng tiền vào của HĐTC"]/cf2["Dòng tiền vào"]
    cf2["Tỷ trọng của từng dòng tiền vào từ HĐĐT chiếm trong tổng số dòng tiền vào trong kỳ"] = cf2["Dòng tiền vào của HĐĐT"]/cf2["Dòng tiền vào"]
    cf2["Tỷ trọng của từng dòng tiền ra từ HĐKD chiếm trong tổng số dòng tiền ra trong kỳ"] = cf2["Dòng tiền ra từ HĐKD"]/cf2["Dòng tiền ra"]
    cf2["Tỷ trọng của từng dòng tiền ra từ HĐTC chiếm trong tổng số dòng tiền ra trong kỳ"] =  cf2["Dòng tiền ra từ HĐTC"]/cf2["Dòng tiền ra"]
    cf2["Tỷ trọng của từng dòng tiền ra từ HĐĐT chiếm trong tổng số dòng tiền ra trong kỳ"] = cf2["Dòng tiền ra từ HĐĐT"]/cf2["Dòng tiền ra"]
    cf2["Tỷ lệ giữa tổng dòng tiền ra so với tổng số dòng tiền vào (%)"] = cf2["Dòng tiền ra"]/cf2["Dòng tiền vào"]
    cf2["Tỷ lệ giữa dòng tiền ra từ HĐKD so với tổng dòng tiền vào (%)"] = cf2["Dòng tiền ra từ HĐKD"]/cf2["Dòng tiền vào"]
    cf2["Tỷ lệ giữa dòng tiền ra từ HĐTC so với tổng dòng tiền vào (%)"] = cf2["Dòng tiền ra từ HĐTC"]/cf2["Dòng tiền vào"]
    cf2["Tỷ lệ giữa dòng tiền ra từ HĐĐT so với tổng dòng tiền vào (%)"] = cf2["Dòng tiền ra từ HĐĐT"]/cf2["Dòng tiền vào"]
    cf2["Tỷ lệ giữa dòng tiền ra để trả nợ dài hạn so với tổng dòng tiền vào (%)"] = cf2['Tiền trả các khoản đi vay']/cf2["Dòng tiền vào"]
    cf2["Tỷ lệ giữa dòng tiền ra để chi trả cổ tức so với tổng dòng tiền vào từ HĐKD (%)"] =  cf2['Cổ tức đã trả']/cf2["Dòng tiền vào của HĐKD"]
    # Các nhân tố làm tăng dòng tiền lưu chuyển thuần từ HĐKD
    cf2["Các nhân tố làm tăng dòng tiền lưu chuyển thuần từ HĐKD trong kỳ"] = (
        cf2["Lãi/lỗ trước những thay đổi vốn lưu động"]+
        cf2["Tăng/giảm các khoản phải thu"]+
        cf2["Biến động hàng tồn kho"]+
        cf2["Tăng/giảm các khoản phải trả"]+
        cf2["Tăng/giảm chi phí trả trước"]+
        cf2["Tiền thu khác từ các hoạt động kinh doanh"]
    )
    cf2["Các nhân tố làm giảm dòng tiền lưu chuyển thuần từ HĐKD trong kỳ"] = (
        cf2["Lãi/lỗ trước những thay đổi vốn lưu động"]+
        cf2["Tăng/giảm các khoản phải thu"]+
        cf2["Biến động hàng tồn kho"]+
        cf2["Tăng/giảm các khoản phải trả"]+
        cf2["Tăng/giảm chi phí trả trước"]+
        cf2["Chi phí lãi vay đã trả"]+
        cf2["Thuế thu nhập doanh nghiệp đã trả"]+
        cf2["Tiền chi khác từ các hoạt động kinh doanh"]

    )
    cf2["Lợi nhuận/Lỗ kinh doanh trước những thay đổi của vốn lưu đồng"] = cf2["Lãi/lỗ trước những thay đổi vốn lưu động"]
    # Tỷ trọng của từng nhân tố làm tăng tiền chiếm trong tổng dòng tiền vào từ HĐKD trong kỳ
    cf2["Nhân tố làm tăng tiền HĐKD 1"] = cf2["Lãi/lỗ trước những thay đổi vốn lưu động"]/cf2["Dòng tiền vào của HĐKD"]
    cf2["Nhân tố làm tăng tiền HĐKD 2"] = cf2["Tăng/giảm các khoản phải thu"]/cf2["Dòng tiền vào của HĐKD"]
    cf2["Nhân tố làm tăng tiền HĐKD 3"] = cf2["Biến động hàng tồn kho"]/cf2["Dòng tiền vào của HĐKD"]
    cf2["Nhân tố làm tăng tiền HĐKD 4"] = cf2["Tăng/giảm các khoản phải trả"]/cf2["Dòng tiền vào của HĐKD"]
    cf2["Nhân tố làm tăng tiền HĐKD 5"] = cf2["Tăng/giảm chi phí trả trước"]/cf2["Dòng tiền vào của HĐKD"]
    cf2["Nhân tố làm tăng tiền HĐKD 6"] = cf2["Tiền thu khác từ các hoạt động kinh doanh"]/cf2["Dòng tiền vào của HĐKD"]
    # Tỷ trọng của từng nhân tố làm giảm tiền chiếm trong tổng dòng tiền ra từ HĐKD trong kỳ
    cf2["Nhân tố làm giảm tiền HĐKD 1"] = cf2["Lãi/lỗ trước những thay đổi vốn lưu động"]/cf2["Dòng tiền ra từ HĐKD"]
    cf2["Nhân tố làm giảm tiền HĐKD 2"] = cf2["Tăng/giảm các khoản phải thu"]/cf2["Dòng tiền ra từ HĐKD"]
    cf2["Nhân tố làm giảm tiền HĐKD 3"] = cf2["Biến động hàng tồn kho"]/cf2["Dòng tiền ra từ HĐKD"]
    cf2["Nhân tố làm giảm tiền HĐKD 4"] = cf2["Tăng/giảm các khoản phải trả"]/cf2["Dòng tiền ra từ HĐKD"]
    cf2["Nhân tố làm giảm tiền HĐKD 5"] = cf2["Tăng/giảm chi phí trả trước"]/cf2["Dòng tiền ra từ HĐKD"]
    cf2["Nhân tố làm giảm tiền HĐKD 6"] = cf2["Chi phí lãi vay đã trả"]/cf2["Dòng tiền ra từ HĐKD"]
    cf2["Nhân tố làm giảm tiền HĐKD 7"] = cf2["Thuế thu nhập doanh nghiệp đã trả"]/cf2["Dòng tiền ra từ HĐKD"]
    cf2["Nhân tố làm giảm tiền HĐKD 8"] = cf2["Tiền chi khác từ các hoạt động kinh doanh"]/cf2["Dòng tiền ra từ HĐKD"]
    # Tỷ trọng của từng nhân tố làm tăng tiền chiếm trong tổng dòng tiền vào từ HDĐT trong kỳ
    cf2["Nhân tố làm tăng tiền HĐĐT 1"] = cf2["Tiền thu được từ thanh lý tài sản cố định"]/cf2["Dòng tiền vào của HĐĐT"]
    cf2["Nhân tố làm tăng tiền HĐĐT 2"] = cf2["Tiền thu từ cho vay hoặc thu từ phát hành công cụ nợ"]/cf2["Dòng tiền vào của HĐĐT"]
    cf2["Nhân tố làm tăng tiền HĐĐT 3"] = cf2["Tiền thu từ việc bán các khoản đầu tư vào các doanh nghiệp khác"]/cf2["Dòng tiền vào của HĐĐT"]
    cf2["Nhân tố làm tăng tiền HĐĐT 4"] = cf2["Cổ tức và tiền lãi nhận được"]/cf2["Dòng tiền vào của HĐĐT"]
    # Tỷ trọng của từng nhân tố làm giảm tiền chiếm trong tổng dòng tiền ra từ HĐĐT trong kỳ
    cf2["Nhân tố làm giảm tiền HĐĐT 1"] = cf2["Tiền mua tài sản cố định và các tài sản dài hạn khác"]/cf2["Dòng tiền ra từ HĐĐT"]
    # Tỷ trọng của từng nhân tố làm tăng tiền chiếm trong tồng dòng tiền vào từ HĐTC trong kỳ
    cf2["Nhân tố làm tăng tiền HĐTC 1"] = cf2["Tiền thu từ phát hành cổ phiếu và vốn góp"]/cf2["Dòng tiền vào của HĐTC"]
    cf2["Nhân tố làm tăng tiền HĐTC 2"] = cf2["Tiền thu được các khoản đi vay"]/cf2["Dòng tiền vào của HĐTC"]
    # Tỷ trọng của từng nhân tố làm giảm tiền chiếm trong tổng dòng tiền ra từ HĐTC trong kỳ
    cf2["Nhân tố làm giảm tiền HĐTC 1"] = cf2["Tiền trả các khoản đi vay"]/cf2["Dòng tiền ra từ HĐTC"]
    cf2["Nhân tố làm giảm tiền HĐTC 2"] = cf2["Cổ tức đã trả"]/cf2["Dòng tiền ra từ HĐTC"]
    
    cf2["Hệ số khả năng thanh khoản của dòng tiền"] = cf2['Lưu chuyển tiền thuần từ HĐKD']/ cf2['Nợ ngắn hạn'] # đã thêm vào metric
    cf2["Hệ số khả năng thanh toán nợ của dòng tiền"] = cf2["Lưu chuyển tiền thuần từ HĐKD"]/ cf2["Nợ phải trả"] # đã thêm vào metric
    cf2["Hệ số đảm bảo khả năng chi trả lãi vay"] =(cf2["Lưu chuyển tiền thuần từ HĐKD"] + cf2['Chi phí lãi vay is'])/cf2['Chi phí lãi vay is'] # đã thêm vào metric
    cf2["Hệ số khả năng trả nợ dài hạn của dòng tiền thuần từ HĐKD"] = cf2["Lưu chuyển tiền thuần từ HĐKD"]/cf2["No_dai_han_binh_quan"]
    #cf2["Hệ số khả năng chi trả cổ tức"] = cf2["Lưu chuyển tiền thuần từ HĐKD"]/ cf2["Cổ tức phải trả"]
    cf2["Hệ số khả năng chi trả cho HĐĐT và HĐTC"] = cf2["Lưu chuyển tiền thuần từ HĐKD"]/(cf2["Dòng tiền ra từ HĐĐT"]+cf2["Dòng tiền ra từ HĐTC"]) # đã thêm vào metric
    return cf2