# Định nghĩa các nhóm metrics
metrics_r1 = [
    "Hệ số tài trợ",
    "ROE",
    "ROIC",
    "ROCE",
    "BEP",
    "Tốc độ tăng trưởng bền vững",
    "Tốc độ tăng trưởng doanh thu thuần",
    "Tốc độ tăng trưởng lợi nhuận",
    "Số lần thanh toán tiền hàng",
    "Hệ số khả năng chuyển đổi thành tiền của TSNH",
    "Tốc độ gia tăng lợi nhuận trước thuế và lãi vay",
    #"Tốc độ gia tăng lợi nhuận sau thuế",
    "Số lần luân chuyển TSCĐ",
    "Số lần luân chuyển TSNH",
    "Số lần luân chuyển HTK",
    "Hệ số tài trợ thường xuyên",
    "Mức biến động tăng/giảm doanh thu thuần kỳ phân tích so với kỳ gốc (%)",
    "Tỷ trọng doanh thu thuần về bán hàng và cung cấp dịch vụ trong tổng doanh thu thuần (%)",
    "Tỷ trọng doanh thu HĐTC trong tổng doanh thu thuần (%)",
    "Mức biến động tăng/giảm LNST kỳ phân tích so với kỳ gốc",
    "ROA",
    "Sức sinh lợi của TSCĐ",
    "Sức sinh lợi của tài sản thuần thuộc HĐKD",
    "Sức sinh lợi của TSDH sử dụng cho HĐKD",
    "Sức sinh lợi của tài sản sử dụng cho HĐKD",
    "Sức sinh lợi của giá vốn hàng bán tính theo lợi nhuận sau thuế từ HĐKD",
    "Sức sinh lợi của giá vốn hàng bán",
    "Hệ số chênh lệch giá",
    "Sức sinh lợi của chi phí kinh doanh",
    "Sức sinh lợi của chi phí bán hàng",
    "Sức sinh lợi của chi phí quản lý DN",
    "Sức sinh lợi của chi phí hoạt động",
    "ROS",
    "Sức sinh lợi của doanh thu thuần từ HĐKD",
    "Hệ số lợi nhuận gộp",
    "Hệ số lợi nhuận thuần từ HĐKD",
    "Số lần luân chuyển cho TSDH sử dụng cho HĐKD",
    "Số lần luân chuyển của tài sản (TAT)",
    "Hệ số giữa nợ phải trả so với VCSH",
    "Số lần luân chuyển của tài sản thuần thuộc HĐKD",
    "Số lần luân chuyển của tài sản sử dụng cho HĐKD"
]
# càng thấp càng tốt
metrics_r2 = [
    "Tỷ lệ giữa nợ phải thu so với nợ phải trả",
    "Tỷ trọng nợ phải thu chiếm trong TTS",
    "Tỷ trọng nợ phải trả chiếm trong tổng NV",
    "Tỷ lệ giữa nợ phải thu người mua so với tổng tiền hàng bán ra trong kỳ",
    "Tỷ lệ giữa dự phòng nợ phải thu khó đòi so với tổng số nợ phải thu người mua",
    "Tỷ lệ giữa nợ còn phải thu cuối kỳ so với tổng số nợ phải thu trong kỳ",
    "Số lần thu hồi tiền hàng",
    #"Thời gian thu hồi tiền hàng",
    
    "Đòn bẩy tài chính (theo quan hệ giữa Nợ phải trả với VCSH)",
    "Độ nhạy của đòn bẩy kinh doanh",
    "Độ nhạy của đòn bẩy tài chính",
    "Tỷ trọng nợ phải thu khó đòi so với tổng số nợ phải thu",
    "Tỷ trọng nợ phải thu khó đòi so với tổng số tài sản (%)",
    "Tỷ lệ giữa dự phòng nợ phải thu khó đòi so với tổng số nợ phải thu",
    "Hệ số tài trợ tạm thời",
    "Độ nhạy của đòn bẩy tổng hợp"
]


#>=1 là tốt
metrics_r3 = [
    "Hệ số khả năng thanh khoản dòng tiền",
    "Hệ số khả năng thanh toán nợ ngắn hạn",
    "Hệ số khả năng thanh toán nhanh",
    "Hệ số khả năng thanh toán nợ dài hạn",
    "Hệ số khả năng thanh toán theo thời gian"
]

#>1 là tốt
metrics_r4 = [
    'Hệ số khả năng thanh toán của dòng tiền'
    'Hệ số khả năng thanh toán tổng quát',
    'Hệ số khả năng chi trả lãi vay'
]
#<1 là tốt
metrics_r5 = [
    "Đòn bẩy tài chính (theo quan hệ giữa TTS với VCSH)",
    "Hệ số khả năng thanh toán tức thời",
    "Hệ số nợ so với tài sản",
    "Hệ số giữa nợ dài hạn so với VCSH",
    "Đòn bẩy tài chính (theo quan hệ giữa Nợ phải trả với TTS)",
    "Hệ số tự tài trợ TSNH",
    'Hệ số giữa TSDH so với nguồn tài trợ thường xuyên'
]

# <= 100 là tốt
metrics_r6 = [
    'Tỷ lệ giữa nợ phải thu so với nợ phải trả'
]

#<=1 là tốt
metrics_r7 = [
    'Hệ sô giữa TSDH so với nguồn tài trợ thường xuyên'
]
#>0 là tốt
metrics_r8 = [
    "Hệ số giữa vốn hoạt động thuần so với nợ dài hạn",
    "Mức biến động tăng/giảm LNST kỳ phân tích so với kỳ gốc"
]
# Trường hợp đặc biệt
metrics_r9=[
    'Hệ số tự tài trợ TSDH',
    
]
# Tạo mapping rules
column_rule_map = {}
for col in metrics_r1: column_rule_map[col] = 'higher_better'
for col in metrics_r2: column_rule_map[col] = 'lower_better'
for col in metrics_r3: column_rule_map[col] = 'ge_1'
for col in metrics_r4:  column_rule_map[col] = 'gt_1'
for col in metrics_r5: column_rule_map[col] = 'lt_1'
for col in metrics_r6:  column_rule_map[col] = 'le_100'
for col in metrics_r7:  column_rule_map[col] = 'le_1'
for col in metrics_r8: column_rule_map[col] = 'gt_0'
for col in metrics_r9: column_rule_map[col] = 'gt_db'
