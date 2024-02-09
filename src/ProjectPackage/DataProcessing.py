import pandas as pd
import numpy as np
import os
from ProjectPackage.util import *

def process_target_data(data, n_months, pct_change=True):
    '''
    Shifts the target data by the defined number of months "n_months".
    If pct_change is set to True, computes the percentage change between the current month
    and n_months earlier.
    '''
    df = data.sort_values(by=['ticker', 'date']).reset_index(drop=True)
    tickers = df['ticker'].unique()

    df_list = []

    for ticker in tickers:
        cond = df["ticker"] == ticker
        df_ = df.loc[cond].reset_index(drop=True)
        
        if pct_change:
            df_['marketcap'] = df_['marketcap'].pct_change(n_months)
            
        df_["marketcap"] = df_["marketcap"].shift(-n_months)
        df_list.append(df_)

    shifted_df = pd.concat(df_list, ignore_index=True)
    
    shifted_df = shifted_df.dropna(subset=['marketcap']).reset_index(drop=True)
    
    return shifted_df


def trim_sectors(data, min_tickers=5):
    df = data.copy()
    
    sectors = df.drop_duplicates(subset=['ticker']).drop(columns=['date', 'year', 'month', 'marketcap'])
    ticker_count = sectors['Sector'].value_counts()
    cond = ticker_count >= min_tickers
    sectors_to_keep = ticker_count[cond].index
    
    cond = df['Sector'].isin(sectors_to_keep)
    df = df.loc[cond].reset_index(drop=True)
    
    return df


def encode_variable(data, variable, method, drop=False):
    df = data.copy()
    
    if method == 'one-hot':
        dummy_cols = pd.get_dummies(df[variable], drop_first=drop)
        df.loc[:, dummy_cols.columns] = dummy_cols.copy()
        
    elif method == 'numeric':
        categories = df[variable].unique()
        num_cat = np.arange(categories.shape[0])
        replace_dict = dict(zip(categories, num_cat))
        df[variable] = df[variable].map(lambda x: replace_dict[x])
        
    return df


def load_data_general(
    n_months=6,
    pct_change=True,
    drop_corr_features=True,
    encoding_method=None,
    drop=False,
    feature_pct_change=0,
    year_range=(2008, 2016)
):
    '''
    Loads data for models type 1 (all sectors in one model).
    '''
    
    feature, target = load_dataframes()
    
    # Computing the monthly change in features
    if feature_pct_change > 0:
        feature[feature.columns[3:]] = feature[feature.columns[3:]].pct_change(feature_pct_change)
        
    target = trim_sectors(target, min_tickers=5)
    shifted_target = process_target_data(target, n_months, pct_change)
    
    shifted_target = encode_variable(shifted_target, 'ticker', encoding_method, drop=drop)
    shifted_target = encode_variable(shifted_target, 'Sector', encoding_method, drop=drop)
    
    shifted_target = shifted_target.drop(columns=['year', 'month', 'firm'])
    
    if drop_corr_features:
        feature = feature.drop(columns=HIGHLY_CORRELATED_FEATURES)
        
    data = feature.merge(shifted_target, on='date')
    
    cond = (year_range[0] <= data['year']) & (data['year'] <= year_range[1])
    data = data.loc[cond].sort_values(by=['ticker', 'date']).reset_index(drop=True)
    
    cols_to_drop = ['date', 'year', 'month', 'marketcap']
    if encoding_method == 'one-hot':
        cols_to_drop += ['ticker', 'Sector']
    X = data.drop(columns=cols_to_drop)
    y = data['marketcap']
    
    return data, X, y


def load_data_sector(
    n_months=6,
    pct_change=True,
    drop_corr_features=True,
    encoding_method=None,
    drop=False,
    feature_pct_change=0,
    year_range=(2008, 2016)
):
    '''
    Loads data for models type 2 (one model for each sector).
    '''
    
    feature, target = load_dataframes()
    
    # Computing the monthly change in features
    if feature_pct_change > 0:
        feature[feature.columns[3:]] = feature[feature.columns[3:]].pct_change(feature_pct_change)
        
    target = trim_sectors(target, min_tickers=5)
    shifted_target = process_target_data(target, n_months, pct_change)
    
    shifted_target = encode_variable(shifted_target, 'ticker', encoding_method, drop=drop)
    shifted_target = shifted_target.drop(columns=['year', 'month', 'firm'])
    
    if drop_corr_features:
        feature = feature.drop(columns=HIGHLY_CORRELATED_FEATURES)
        
    df_dict = {}
    variable='Sector'
    for val in shifted_target[variable].unique():
        df_dict[val] = {}
        
        cond = shifted_target[variable] == val
        target_ = shifted_target.loc[cond].copy()
        data = feature.merge(target_, on='date')
        cond = (year_range[0] <= data['year']) & (data['year'] <= year_range[1])
        data = data.loc[cond].sort_values(by=['ticker', 'date']).reset_index(drop=True)
        
        cols_to_drop = ['date', 'year', 'month', 'marketcap', 'Sector']
        if encoding_method == 'one-hot':
            cols_to_drop += ['ticker']
            
        X = data.drop(columns=cols_to_drop)
        y = data['marketcap']
        
        df_dict[val]['X'] = X
        df_dict[val]['y'] = y
        df_dict[val]['data'] = data
        
    return df_dict