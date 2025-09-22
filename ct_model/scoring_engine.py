import pandas as pd

def score_gt_db_rule(cf2, col):
    """Xử lý rule đặc biệt 'gt_db' cho 'Hệ số tự tài trợ TSDH'"""
    return cf2.apply(
        lambda row: 1 if row[col] >= 1 else (
            1 if row['Hệ số tự tài trợ TSCĐ'] >= 1 else 0
        ), axis=1
    )

def score_by_rule(series, rule):
    """Áp dụng quy tắc tính điểm cho một series"""
    if rule == 'higher_better':
        return series.diff(-1).apply(lambda x: 1 if x >= 0 else 0)
    elif rule == 'lower_better':
        return series.diff(-1).apply(lambda x: 1 if x <= 0 else 0)
    elif rule == 'ge_1':
        return series.apply(lambda x: 1 if x >= 1 else 0)
    elif rule == 'gt_1':
        return series.apply(lambda x: 1 if x > 1 else 0)
    elif rule == 'lt_1':
        return series.apply(lambda x: 1 if x < 1 else 0)
    elif rule == 'le_100':
        return series.apply(lambda x: 1 if x <= 100 else 0)
    elif rule == 'le_1':
        return series.apply(lambda x: 1 if x <= 1 else 0)
    elif rule == 'gt_0':
        return series.apply(lambda x: 1 if x > 0 else 0)
    
    else:
        return None

def apply_scoring_rules(cf2, column_rule_map):
    """Áp dụng tất cả quy tắc tính điểm"""
    for col, rule in column_rule_map.items():
        if col in cf2.columns:
            if rule == 'gt_db':
                # Xử lý rule đặc biệt
                cf2[f'{col}_score'] = score_gt_db_rule(cf2, col)
            elif rule in ['higher_better', 'lower_better']:
                cf2[f'{col}_score'] = (
                    cf2.groupby('Ticker')[col]
                      .apply(lambda x: score_by_rule(x, rule))
                      .reset_index(level=0, drop=True)
                )
            else:
                cf2[f'{col}_score'] = score_by_rule(cf2[col], rule)
    
    return cf2

def calculate_total_scores(cf2):
    """Tính tổng điểm tích cực và tiêu cực"""
    score_cols = [col for col in cf2.columns if col.endswith('_score')]
    cf2['Tong_p'] = cf2[score_cols].sum(axis=1)
    cf2['Tong_n'] = (cf2[score_cols] == 0).sum(axis=1)
    
    return cf2