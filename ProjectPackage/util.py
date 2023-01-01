import pandas as pd
import json

HIGHLY_CORRELATED_FEATURES = ['MIG_CAG', 'MIG_ING', 'MIG_NDCOG', 'ExchangeRate', 'import_unit_value_index_usd']

def get_ticker(df, name):
    cond = df['ticker'] == name
    return df.loc[cond].reset_index(drop=True)

def load_dataframes():
    # Loading data
    path = 'processed_data/Features_2008.csv'
    feature = pd.read_csv(path, index_col=0, parse_dates=['date'])

    path = 'processed_data/Target.csv'
    target = pd.read_csv(path, index_col=[0], parse_dates=['date'])
    
    return feature, target


def save_scores(score_dict, path):
    with open(path, 'w') as f:
        json.dump(score_dict, f)
 
def load_scores(path):
    with open(path, 'r') as f:
        score_dict = json.load(f)
    return score_dict
        
    