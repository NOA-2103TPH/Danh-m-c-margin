import pandas as pd
import numpy as np
from ck_model.data_loader import sort_report
def merge_data(ck_bs, ck_is, ck_cf, ck_nt):
    """
    Merge data as in original code
    """
    # Sắp xếp từng DataFrame
    bs_sorted = sort_report(ck_bs)
    is_sorted = sort_report(ck_is)
    cf_sorted = sort_report(ck_cf)
    nt_sorted = sort_report(ck_nt)

    bctc_df = pd.concat([
        ck_bs[['Ticker', 'YearReport', 'LengthReport']],
        ck_is[['Ticker', 'YearReport', 'LengthReport']],
        ck_cf[['Ticker', 'YearReport', 'LengthReport']],
        ck_nt[['Ticker', 'YearReport', 'LengthReport']],
    ]).drop_duplicates().reset_index(drop=True)

    # Gộp dữ liệu với bctc_df
    df = bctc_df.merge(bs_sorted, how="left", on=["Ticker", "YearReport", "LengthReport"])
    df = df.merge(cf_sorted, how="left", on=["Ticker", "YearReport", "LengthReport"])
    df = df.merge(is_sorted, how="left", on=["Ticker", "YearReport", "LengthReport"])
    df = df.merge(
        nt_sorted,
        how="left",
        on=["Ticker","YearReport","LengthReport"],
        suffixes=("", "_nt")
    )
    return df

def map_data_to_ct(df, ck_bs, ck_is, ck_nt, ck_cf):
    """
    Mapping data to ct as in original code
    """

    # Create base dataframe with Ticker and YearReport
    ct = df[['Ticker', 'YearReport', 'LengthReport']].copy()
    
    ck_cf = ct.merge(
    ck_cf, 
    on=["Ticker","YearReport","LengthReport"], 
    how="left"
    )

    ck_bs = ct.merge(
    ck_bs, 
    on=["Ticker","YearReport","LengthReport"], 
    how="left"
    )

    ck_is = ct.merge(
    ck_is, 
    on=["Ticker","YearReport","LengthReport"], 
    how="left"
    )
    ck_nt = ct.merge(
    ck_nt, 
    on=["Ticker","YearReport","LengthReport"], 
    how="left"
    )


    # bs - tài sản
    ct["Tài sản ngắn hạn"] = ck_bs["BSA1"]
    ct["Tiền và tương đương tiền"] = ck_bs["BSA2"]
    ct["Giá trị thuần đầu tư tài sản tài chính ngắn hạn"] = ck_bs["BSA5"]
    ct["Các tài sản tài chính ghi nhận thông qua lãi lỗ (FVTPL)"] = ck_bs["BSA6"]
    ct["Dự phòng giảm giá chứng khoán kinh doanh"] = ck_bs["BSA7"]
    ct["Các khoản đầu tư nắm giữ đến ngày đáo hạn (HTM)"] = ck_bs["BSB108"]
    ct["Tài sản cố định"] = ck_bs["BSA29"]
    ct["GTCL TSCĐ hữu hình"] = ck_bs["BSA30"]
    ct["Nguyên giá TSCĐ hữu hình"] = ck_bs["BSA31"]
    ct["Khấu hao lũy kế TSCĐ hữu hình"] = ck_bs["BSA32"]
    ct["Tổng cộng tài sản"] = ck_bs["BSA53"]
    ct["Tiền chi nộp quỹ hỗ trợ thanh toán"] = ck_bs["BSS212"]
    ct["Tổng cộng nguồn vốn"] = ck_bs["BSA96"]
    ct["Tài sản tài chính ngắn hạn"] = ck_bs["BSS214"]
    ct["Các khoản cho vay"] = ck_bs["BSS215"]
    ct["Các khoản tài chính sẵn sàng để bán (AFS)"] = ck_bs["BSS216"]
    ct["Các khoản phải thu"] = ck_bs["BSS217"]
    ct["Phải thu bán các tài sản tài chính"] = ck_bs["BSS218"]
    ct["Phải thu và sự thu cổ tức, tiền lãi các tài sản tài chính"] = ck_bs["BSS219"]
    ct["Phải thu cổ tức, tiền lãi đến ngày nhận"] = ck_bs["BSS220"]
    ct["Phải thu các dịch vụ CTCK cung cấp"] = ck_bs["BSS224"]
    ct["Các khoản trích nộp phúc lợi nhân viên"] = ck_bs["BSS245"]
        #nguồn vốn
    ct["Nợ phải trả"] = ck_bs["BSA54"]
    ct["Nợ ngắn hạn"] = ck_bs["BSA55"]
    ct["Vay và nợ thuê tài sản tài chính ngắn hạn"] = ck_bs["BSA56"]
    ct["Phải trả hoạt động giao dịch chứng khoán"] = ck_bs["BSS135"]
    ct["Phải trả người bán ngắn hạn"] = ck_bs["BSA57"]
    ct["Người mua trả tiền trước ngắn han"] = ck_bs["BSA58"]
    ct["Các khoản phải trả về thuế"] = ck_bs["BSA59"]
    ct["Phải trả người lao động"] = ck_bs["BSA60"]
    ct["Chi phí phải trả"] = ck_bs["BSA61"]  
    ct["Phải trả nội bộ"] = ck_bs["BSA62"]
    ct["Phải trả khác"] = ck_bs["BSA64"]
    ct["Nợ dài hạn"] = ck_bs["BSA67"]
    ct["Vay và nợ thuê tài sản tài chính dài hạn"] = ck_bs["BSA71"]
    ct["Vốn chủ sở hữu"] = ck_bs["BSA78"]
    ct["Cổ phiếu phổ thông"] = ck_bs["BSA175"]
    ct["Lợi nhuận chưa phân phối"] = ck_bs["BSA90"]
    ct["Vốn đầu tư của chủ sở hữu"] = ck_bs["BSS252"]
    ct["Quỹ dự trữ điều lệ"] = ck_bs["BSS253"]
    ct["Lợi nhuận đã thực hiện"] = ck_bs["BSS254"]
    ct["Lợi nhuận chưa thực hiện"] = ck_bs["BSS255"]

    #IS

    ct["Doanh thu hoạt động"] = ck_is["ISA1"]
    ct["Lãi từ tài sản tài chính ghi nhận thông qua lãi/lỗ (FVTPL)"] = ck_is["ISS115"]
    ct["Lãi bán các tài sản tài chính PVTPL"] = ck_is["ISS116"]
    ct["Lãi từ các khoản đầu tư nắm giữ đến ngày đáo hạn (HTM)"] = ck_is["ISS119"]
    ct["Lãi từ các khoản cho vay và phải thu"] = ck_is["ISS120"]
    ct["Lãi từ các tài sản tài chính sẵn sàng để bán (AFS)"] = ck_is["ISS121"]
    ct["Lãi từ công cụ phái sinh phòng ngừa rủi ro"] = ck_is["ISS122"]
    ct["Doanh thu môi giới chứng khoán"] = ck_is["ISS42"]
    ct["Doanh thu bảo lãnh phát hành chứng khoán"] = ck_is["ISS44"]
    ct["Doanh thu đại lý phát hành chứng khoán"] = ck_is["ISS45"]
    ct["Doanh thu hoạt động tư vấn đầu tư chứng khoán"] = ck_is["ISS46"]
    ct["Doanh thu hoạt động ủy thác, đấu giá"] = ck_is["ISS48"]
    ct["Chi phí hoạt động tự doanh"] = ck_is["ISS132"]
    ct["Chi phí môi giới chứng khoán"] = ck_is["ISS133"]
    ct["Chi phí bảo lãnh, đại lý phát hành"] = ck_is["ISS134"]
    ct["Chi phí tư vấn đầu tư chứng khoán"] = ck_is["ISS135"]
    ct["Tổng lợi nhuận kế toán trước thuế"] = ck_is["ISA16"]
    ct["Chi phí thuế TNDN hiện hành"] = ck_is["ISA17"]
    ct["Chi phí thuế TNDN hoãn lại"] = ck_is["ISA18"]
    ct["Lợi nhuận kế toán sau thuế"] = ck_is["ISA20"]
    ct["Lãi cơ bản trên cổ phiếu"] = ck_is["ISA23"]
    #cf
    ct["Chi phí lãi vay"] = ck_cf["CFA7"]

    #nt
    ct["Tiền gửi của khách hàng"] = ck_nt["NOS395"]
    ct["Phải trả cổ tức, gốc và lãi trái phiếu"] = ck_nt["NOS413"]
    ct["Tiền và tương đương tiền"] = ck_nt["NOS88"]
    ct["Tiền mặt"] = ck_nt["NOS89"]
    ct["Tiền gửi ngân hàng"] = ck_nt["NOS90"]
    ct["Khối lượng Giao dịch thực hiện trong kỳ của CTCK"] = ck_nt["NOS96"]
    ct["Khối lượng Cổ phiếu"] = ck_nt["NOS97"]
    ct["Khối lượng Trái phiếu"] = ck_nt["NOS98"]
    ct["Khối lượng chứng khoán khác"] = ck_nt["NOS99"]
    ct["Giá trị Giao dịch thực hiện trong kỳ của CTCK"] = ck_nt["NOS100"]
    ct["Giá trị Cổ phiếu"] = ck_nt["NOS101"]
    ct["Giá trị Trái phiếu"] = ck_nt["NOS102"]
    ct["Khối lượng Giao dịch thực hiện trong kỳ của NĐT"] = ck_nt["NOS104"]
    ct["Khối lượng Cổ phiếu"] = ck_nt["NOS105"]
    ct["Khối lượng Trái phiếu"] = ck_nt["NOS106"]
    ct["Khối lượng chứng khoán khác"] = ck_nt["NOS107"]
    ct["Giá trị Giao dịch thực hiện trong kỳ của NĐT"] = ck_nt["NOS108"]
    ct["Giá trị Cổ phiếu"] = ck_nt["NOS109"]
    ct["Giá trị Trái phiếu"] = ck_nt["NOS110"]
    ct["Giá trị chứng khoán khác"] = ck_nt["NOS111"]
    ct["Giá gốc đầu tư tài chính"] = ck_nt["NOS119"]
    ct["Giá trị ghi sổ Tài sản tài chính ghi nhận thông qua lãi/lỗ (FVTPL)"] = ck_nt["NOS120"]
    ct["Chứng khoán thương mại"] = ck_nt["NOS121"]
    ct["Cổ phiếu niêm yết"] = ck_nt["NOS122"]
    ct["Cổ phiếu chưa niêm yết"] = ck_nt["NOS123"]
    ct["Chứng chỉ quỹ"] = ck_nt["NOS124"]
    ct["Trái phiếu"] = ck_nt["NOS125"]
    ct["Đầu tư tài chính ngắn hạn khác"] = ck_nt["NOS126"]
    ct["Đầu tư tài chính dài hạn"] = ck_nt["NOS127"]
    ct["Vay và nợ ngắn hạn"] = ck_nt["NOS231"]
    ct["Vay ngân hàng"] = ck_nt["NOS269"]
    ct["Chi phí hoạt động kinh doanh"] = ck_nt["NOS284" ]
    ct["Chi phí môi giới, lưu ký chứng khoán"] = ck_nt["NOS285"]
    ct["Chi phí hoạt động đầu tư chứng khoán, góp vốn"] = ck_nt["NOS286"]
    ct["Lãi tiền gửi, tiền cho vay"] = ck_nt["NOS331"]
    ct["Chi phí sản xuất theo yếu tố"] = ck_nt["NOS348"]
    ct["Chi phí nguyên liệu, vật liệu"] = ck_nt["NOS349"]
    ct["Chi phí nhân công"] = ck_nt["NOS350"]
    ct["Chi phí khấu hao tài sản cố định"] = ck_nt["NOS351"]
    ct["Chi phí dịch vụ mua ngoài"] = ck_nt["NOS352"]
    ct["Chi phí khác bằng tiền"] = ck_nt["NOS353"]
    ct["Các khoản cho vay và phải thu"] = ck_nt["NOS445"]
    ct["Cho vay nghiệp vụ ký quỹ (margin)"] = ck_nt["NOS446"]
    ct["Cho vay ứng trước tiền bán chứng khoán của khách hàng"] = ck_nt["NOS447"]
    ct["Các khoản phải thu và dự thu cổ tức, tiền lãi các khoản đầu tư"] = ck_nt["NOS512"]
    ct["Phải thu các dịch vụ CTCK cung cấp"] = ck_nt["NOS523"]
    ct["Phải thu hoạt động môi giới chứng khoán"] = ck_nt["NOS524"]
    ct["Phải thu hoạt động bảo lãnh, đại lý phát hành chứng khoán"] = ck_nt["NOS525"]
    ct["Phải thu hoạt động tư vấn"] = ck_nt["NOS526"]
    ct["Phải thu hoạt động lưu ký chứng khoán"] = ck_nt["NOS527"]
    ct["Dự phòng các khoản phải thu khó đòi"] = ck_nt["NOS542"]
    ct["Phải trả vay CTCK của NĐT"] = ck_nt["NOS637"]
    ct["Cổ tức và tiền lãi phát sinh"] = ck_nt["NOS680"]
    ct["Từ tài sản tài chính FVTPL"] = ck_nt["NOS681"]
    ct["Từ tài sản tài chính HTM"] = ck_nt["NOS682"]
    ct["Từ AFS"] = ck_nt["NOS683"]
    ct["Từ các khoản cho vay"] = ck_nt["NOS684"]
    ct["Doanh thu ngoài thu nhập các tài sản tài chính"] = ck_nt["NOS685"]
    ct["Doanh thu hoạt động môi giới chứng khoán"] = ck_nt["NOS686"]
    ct["Doanh thu ban đầu"] = ck_nt["NOS687"]
    ct["Các khoản giảm trừ doanh thu"] = ck_nt["NOS688"]
    ct["Doanh thu thuần"] = ck_nt["NOS689"]
    ct["Doanh thu hoạt động bảo lãnh, đại lý phát hành chứng khoán"] = ck_nt["NOS690"]
    ct["Doanh thu ban đầu"] = ck_nt["NOS691"]
    ct["Các khoản giảm trừ doanh thu"] = ck_nt["NOS692"]
    ct["Doanh thu thuần"] = ck_nt["NOS693"]
    ct["Doanh thu hoạt động tư vấn"] = ck_nt["NOS694"]
    ct["Doanh thu khác"] = ck_nt["NOS695"]
    
    # Assuming other columns like Vốn chủ sở hữu, Các khoản phải thu, Cho vay nghiệp vụ ký quỹ (margin) exist in merged df or sources
    # ct["Vốn chủ sở hữu"] = df["Vốn chủ sở hữu"]  # From merged df
    # ct["Các khoản phải thu"] = df["Các khoản phải thu"]
    # ct["Cho vay nghiệp vụ ký quỹ (margin)"] = df["Cho vay nghiệp vụ ký quỹ (margin)"]
    
    return ct