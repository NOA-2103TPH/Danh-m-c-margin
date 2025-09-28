# ck_model/scoring_engine.py

import pandas as pd

from ck_model.metrics_config import create_column_rule_map
from ck_model.metrics_config import SCORING_YEARS


def score_by_rule(series, rule):
    """
    Quy tắc chấm điểm cho từng metric.
    """
    if rule == 'higher_better':
        return (series > series.shift(1)).astype(int)
    elif rule == 'lower_better':
        return (series < series.shift(1)).astype(int)
    elif rule == 'ge_1':
        return (series >= 1).astype(int)
    elif rule == 'gt_1':
        return (series > 1).astype(int)
    elif rule == 'lt_1':
        return (series < 1).astype(int)
    else:
        return pd.Series([None] * len(series), index=series.index)


def apply_scoring(cf2):
    """
    Áp dụng scoring dựa trên mapping rule từ metrics_config.
    """
    column_rule_map = create_column_rule_map()

    available_metrics = [col for col in column_rule_map if col in cf2.columns]
    print(f"Applying scoring to {len(available_metrics)} metrics")

    sort_cols = [c for c in ['Ticker', 'YearReport', 'LengthReport'] if c in cf2.columns]
    cf2 = cf2.sort_values(sort_cols, ascending=[True] * len(sort_cols)).copy()

    for col, rule in column_rule_map.items():
        if col not in cf2.columns:
            continue
        if rule in ['higher_better', 'lower_better', 'ge_1', 'gt_1', 'lt_1']:
            cf2[f'{col}_score'] = (
                cf2.groupby('Ticker', sort=False)[col]
                   .apply(lambda x: score_by_rule(x, rule))
                   .reset_index(level=0, drop=True)
            )
        else:
            cf2[f'{col}_score'] = score_by_rule(cf2[col], rule)

    return cf2


def calculate_quarterly_conditions(cf2):
    """
    3 điều kiện quý (Q2 2025 vs Q1 2025, Q2 2024).
    """
    score_cols = [c for c in cf2.columns if c.endswith('_score')]
    cf_sum = cf2.copy()
    cf_sum['Tong_p'] = cf_sum[score_cols].sum(axis=1)
    cf_sum['Tong_n'] = (cf_sum[score_cols] == 0).sum(axis=1)

    filtered = cf_sum[
        (cf_sum['YearReport'].isin([2024, 2025])) &
        (cf_sum['LengthReport'].isin([1, 2]))
    ].copy()

    # dkq1: P > N tại Q2/2025
    dk1 = filtered[(filtered['YearReport'] == 2025) & (filtered['LengthReport'] == 2)].copy()
    dk1['dkq1'] = (dk1['Tong_p'] > dk1['Tong_n']).astype(int)
    dk1 = dk1[['Ticker', 'dkq1']]

    # dkq2: Tong_p Q2/2025 > Q1/2025
    d2025 = filtered[filtered['YearReport'] == 2025][['Ticker', 'LengthReport', 'Tong_p']]
    dk2 = pd.DataFrame(columns=['Ticker', 'dkq2'])
    if not d2025.empty:
        piv = d2025.pivot(index='Ticker', columns='LengthReport', values='Tong_p')
        dk2_series = ((piv.get(2, pd.Series(-1)) > piv.get(1, pd.Series(float('inf'))))).astype(int)
        dk2 = dk2_series.rename('dkq2').reset_index()

    # dkq3: Tong_p Q2/2025 > Q2/2024
    q2 = filtered[filtered['LengthReport'] == 2][['Ticker', 'YearReport', 'Tong_p']]
    dk3 = pd.DataFrame(columns=['Ticker', 'dkq3'])
    if not q2.empty:
        piv = q2.pivot(index='Ticker', columns='YearReport', values='Tong_p')
        dk3_series = ((piv.get(2025, pd.Series(-1)) > piv.get(2024, pd.Series(float('inf'))))).astype(int)
        dk3 = dk3_series.rename('dkq3').reset_index()

    res = dk1.merge(dk2, on='Ticker', how='outer').merge(dk3, on='Ticker', how='outer')
    for c in ['dkq1', 'dkq2', 'dkq3']:
        if c not in res.columns:
            res[c] = 0
    res[['dkq1', 'dkq2', 'dkq3']] = res[['dkq1', 'dkq2', 'dkq3']].fillna(0).astype(int)
    res['YearReport'] = 2025
    res['LengthReport'] = 2

    return res[['Ticker', 'YearReport', 'LengthReport', 'dkq1', 'dkq2', 'dkq3']]


def calculate_yearly_conditions(cf2):
    """
    2 điều kiện năm (2024 vs 2023).
    """
    score_cols = [c for c in cf2.columns if c.endswith('_score')]
    cf2_summary = cf2[cf2['YearReport'].isin(SCORING_YEARS)].copy()
    cf2_summary['Tong_p'] = cf2_summary[score_cols].sum(axis=1)
    cf2_summary['Tong_n'] = (cf2_summary[score_cols] == 0).sum(axis=1)

    yearly = cf2_summary[(cf2_summary['LengthReport'] == 5) &
                         (cf2_summary['YearReport'].isin([2023, 2024]))].copy()

    # dky1: P > N năm 2024
    dky1 = yearly[yearly['YearReport'] == 2024].copy()
    dky1['dky1'] = (dky1['Tong_p'] > dky1['Tong_n']).astype(int)
    dky1 = dky1[['Ticker', 'YearReport', 'dky1']]

    # dky2: P_2024 > P_2023
    dky2 = (yearly.sort_values(['Ticker', 'YearReport'])
                  .groupby('Ticker')
                  .apply(lambda g: g.assign(dky2=(g['Tong_p'] > g['Tong_p'].shift(1)).astype(int)))
                  .reset_index(drop=True))
    dky2 = dky2[dky2['YearReport'] == 2024][['Ticker', 'YearReport', 'dky2']]

    res = dky1.merge(dky2, on=['Ticker', 'YearReport'], how='left')
    res['dky2'] = res['dky2'].fillna(0).astype(int)
    return res


def calculate_final_rank(cf2):
    """
    Kết hợp 2 rule Năm (2024) + 3 rule Quý (Q2/2025).
    """
    y = calculate_yearly_conditions(cf2)
    q = calculate_quarterly_conditions(cf2)

    final = y.merge(q[['Ticker', 'dkq1', 'dkq2', 'dkq3']], on='Ticker', how='outer')
    for c in ['dky1', 'dky2', 'dkq1', 'dkq2', 'dkq3']:
        if c not in final.columns:
            final[c] = 0
        final[c] = final[c].fillna(0).astype(int)

    final['so_luong_1'] = final[['dky1', 'dky2', 'dkq1', 'dkq2', 'dkq3']].sum(axis=1)

    grade_map = {5: 'A', 4: 'B', 3: 'C', 2: 'D', 1: 'E', 0: 'F'}
    final['grade'] = final['so_luong_1'].map(grade_map)

    final['YearReport'] = 2025
    final['LengthReport'] = 2

    return final[['Ticker', 'YearReport', 'LengthReport',
                  'dky1', 'dky2', 'dkq1', 'dkq2', 'dkq3',
                  'so_luong_1', 'grade']]
