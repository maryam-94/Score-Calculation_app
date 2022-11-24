import pandas as pd
import gc
import pickle

df_bureau_path = "../bureau.csv"
agg_bureau_for_app_path = r'./data/bureau_for_app.pickle'

# Preprocess bureau.csv and bureau_balance.csv
def bureau_for_app(num_rows=None, nan_as_category=True):
    bureau = pd.read_csv(df_bureau_path, nrows=num_rows)
    # bb = pd.read_csv(df_bureau_balance_path, nrows=num_rows)
    # bb, bb_cat = one_hot_encoder(bb, nan_as_category)
    # bureau, bureau_cat = one_hot_encoder(bureau, nan_as_category)

    # Bureau balance: Perform aggregations and merge with bureau.csv
    # bb_aggregations = {'MONTHS_BALANCE': ['min', 'max', 'size']}
    # for col in bb_cat:
    #     bb_aggregations[col] = ['mean']
    # bb_agg = bb.groupby('SK_ID_BUREAU').agg(bb_aggregations)
    # bb_agg.columns = pd.Index([e[0] + "_" + e[1].upper() for e in bb_agg.columns.tolist()])
    # bureau = bureau.join(bb_agg, how='left', on='SK_ID_BUREAU')
    bureau.drop(['SK_ID_BUREAU'], axis=1, inplace=True)
    # del bb, bb_agg
    gc.collect()

    # Bureau and bureau_balance numeric features
    num_aggregations = {
        'DAYS_CREDIT': ['min', 'max', 'mean'],
        'DAYS_CREDIT_ENDDATE': ['min', 'max'],
        'DAYS_CREDIT_UPDATE': ['mean'],
        'CREDIT_DAY_OVERDUE': ['max', 'mean'],
        'AMT_CREDIT_MAX_OVERDUE': ['mean'],
        'AMT_CREDIT_SUM': ['sum'], #'max', 'mean',
        'AMT_CREDIT_SUM_DEBT': ['sum'], #'max', 'mean',
        'AMT_CREDIT_SUM_OVERDUE': ['mean'],
        # 'AMT_CREDIT_SUM_LIMIT': ['mean', 'sum'],
        # 'AMT_ANNUITY': ['max', 'mean'],
        # 'CNT_CREDIT_PROLONG': ['sum']
    }
    # Bureau and bureau_balance categorical features
    # cat_aggregations = {}
    # for cat in bureau_cat: cat_aggregations[cat] = ['mean']
    # for cat in bb_cat: cat_aggregations[cat + "_MEAN"] = ['mean']

    bureau_agg = bureau.groupby('SK_ID_CURR').agg({**num_aggregations})
    bureau_agg.columns = pd.Index(['BURO_' + e[0] + "_" + e[1].upper() for e in bureau_agg.columns.tolist()])
    # Bureau: Active credits - using only numerical aggregations
    active = bureau[bureau['CREDIT_ACTIVE'] == 'Active']
    active_agg = active.groupby('SK_ID_CURR').agg(num_aggregations)
    active_agg.columns = pd.Index(['ACTIVE_' + e[0] + "_" + e[1].upper() for e in active_agg.columns.tolist()])
    bureau_agg = bureau_agg.join(active_agg, how='left', on='SK_ID_CURR')
    del active, active_agg
    gc.collect()
    # Bureau: Closed credits - using only numerical aggregations
    closed = bureau[bureau['CREDIT_ACTIVE'] == 'Closed']
    closed_agg = closed.groupby('SK_ID_CURR').agg(num_aggregations)
    closed_agg.columns = pd.Index(['CLOSED_' + e[0] + "_" + e[1].upper() for e in closed_agg.columns.tolist()])
    bureau_agg = bureau_agg.join(closed_agg, how='left', on='SK_ID_CURR')
    del closed, closed_agg, bureau
    gc.collect()
    return bureau_agg

agg_bureau_for_app = bureau_for_app()
f = open(agg_bureau_for_app_path, 'wb')
pickle.dump(agg_bureau_for_app, f)
f.close()