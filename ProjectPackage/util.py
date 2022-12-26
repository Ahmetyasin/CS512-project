import pandas as pd

HIGHLY_CORRELATED_FEATURES = ['MIG_CAG', 'MIG_ING', 'MIG_NDCOG', 'ExchangeRate', 'import_unit_value_index_usd']

def get_ticker(df, name):
    cond = df['ticker'] == name
    return df.loc[cond].reset_index(drop=True)


