import pandas as pd

def apply_conditions(filtered):
    """Áp dụng các điều kiện đánh giá"""
    # Điều kiện 1: P > N cùng kỳ
    dk1 = filtered[
        (filtered['YearReport'] == 2025) &
        (filtered['LengthReport'] == 2)
    ]
    dk1['dk'] = (dk1['Tong_p'] > dk1['Tong_n']).astype(int)

    # Điều kiện 2: P > P của quý trước
    dk2 = filtered[
        (filtered['YearReport'] == 2025) &
        (filtered['LengthReport'].isin([1, 2]))
    ].sort_values(['Ticker', 'LengthReport'], ascending=[True, False])
    dk2['dk'] = dk2.groupby('Ticker').apply(
        lambda x: (x['Tong_p'] > x['Tong_p'].shift(-1)).astype(int)
    ).reset_index(level=0, drop=True)
    dk2 = dk2[
        (dk2['YearReport'] == 2025) &
        (dk2['LengthReport'] == 2)
    ]

    # Điều kiện 3: P > P cùng kỳ năm trước
    dk3 = filtered[
        (filtered['YearReport'].isin([2024, 2025])) &
        (filtered['LengthReport'] == 2)
    ].sort_values(['Ticker', 'YearReport'], ascending=[True, False])
    dk3['dk'] = dk3.groupby('Ticker').apply(
        lambda x: (x['Tong_p'] > x['Tong_p'].shift(-1)).astype(int)
    ).reset_index(level=0, drop=True)
    dk3 = dk3[
        (dk3['YearReport'] == 2025) &
        (dk3['LengthReport'] == 2)
    ]
    
    return dk1, dk2, dk3

def calculate_final_grades(dk1, dk2, dk3, df_y):
    """Tính điểm cuối cùng và xếp hạng"""
    dk_total = dk1[['Ticker', 'dk']] 
    dk_total['dk2'] = dk2['dk']
    dk_total['dk3'] = dk3['dk']
    
    cols = ['dk', 'dk2', 'dk3']
    dk_total['so_luong_1'] = dk_total[cols].sum(axis=1)
    df_sorted = dk_total.sort_values('so_luong_1', ascending=False)
    df_sorted['grade'] = df_sorted['so_luong_1'].map({3: 'A', 2: 'B', 1: 'C', 0: 'D'})
    
    # Merge với dữ liệu năm
    df_merge = pd.merge(df_sorted, df_y, on="Ticker", how="outer")
    df_merge["tong_dk"] = df_merge[["dk", "dk2", "dk3", "dk4", "dk5"]].sum(axis=1)
    
    grade_map = {
        5: "A",
        4: "B",
        3: "C",
        2: "D",
        1: "E",
        0: "F"
    }
    df_merge["grade_final"] = df_merge["tong_dk"].map(grade_map)
    
    result = df_merge[["Ticker", "dk", "dk2", "dk3", "dk4", "dk5", "tong_dk", "grade_final"]]
    result = result.sort_values('grade_final', ascending=True)
    
    return result