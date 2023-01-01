import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold

from ProjectPackage.util import *
from ProjectPackage.DataProcessing import *

def MAPE(y_true, y_pred):
    '''
    MAPE is the mean absolute percentage error.
    '''
    
    return np.abs((y_true - y_pred) / y_true).sum() / y_true.shape[0]

score_fun_dict={
    'MAE': mean_absolute_error,
#     'MAPE': MAPE,
    'RMSE': lambda x, y: np.sqrt(mean_squared_error(x, y)),
#     'rRMSE': lambda x, y: np.sqrt(mean_squared_error(x, y)) / np.mean(x),
    'R2': r2_score,
}

def get_score_dict(y_true, y_pred, model_score_dict, score_fun_dict=score_fun_dict):
    
    if not model_score_dict:
        model_score_dict = {metric: [] for metric in score_fun_dict.keys()}
        
    for metric, fun in score_fun_dict.items():
        model_score_dict[metric].append(fun(y_true, y_pred))
        
    return model_score_dict


def conduct_cv(
    model_class,
    X,
    y,
    model_params={},
    model_fit_params={},
    n_folds=5,
    score_fun_dict=score_fun_dict):
    
    
    cv = KFold(n_folds)
    model_score_dict = {}
    
    predictions = np.zeros(y.shape)
    
    for i, (train_index, test_index) in enumerate(cv.split(X, y)):
        X_train = X[train_index]
        y_train = y[train_index]
        X_test = X[test_index]
        y_test = y[test_index]
        
        model = model_class(**model_params)
        
        model.fit(X_train, y_train, **model_fit_params)
        
        y_pred = model.predict(X_test)
        
        predictions[test_index] = y_pred
        
        model_score_dict = get_score_dict(y_test, y_pred, model_score_dict)
        
    return model_score_dict, predictions


def run_general_pct_model(
    model_class,
    model_params={},
    model_fit_params={},
    month_range=range(1, 7),
    drop_corr_features=True,
    encoding_method='one-hot',
    drop=True,
    year_range=(2008, 2017),
):
    
    all_scores = {}
    
    for n_months in month_range:
        data, X, y = load_data_general(
            n_months=n_months,
            pct_change=True,
            drop_corr_features=drop_corr_features,
            encoding_method=encoding_method,
            drop=drop,
            year_range=year_range)

        # Defining random state for shuffling data
        random_state = 763

        X = X.sample(n=X.shape[0], random_state=random_state)
        shuffle_idx = X.index
        y = y.loc[shuffle_idx]

        X = X.to_numpy()
        y = y.to_numpy()

        # Conducting cross validation
        model_score_dict, predictions = conduct_cv(model_class, X, y, model_params, model_fit_params)

        all_scores[n_months] = model_score_dict
        
    return all_scores



def run_sector_pct_model(
    model_class,
    model_params={},
    model_fit_params={},
    month_range=range(1, 7),
    drop_corr_features=True,
    encoding_method='one-hot',
    drop=True,
    year_range=(2008, 2017),
):
    
    all_scores = {}
    
    # Defining random state for shuffling data
    random_state = 763
        
    for n_months in month_range:
        data_dict = load_data_sector(
            n_months=n_months,
            pct_change=True,
            drop_corr_features=drop_corr_features,
            encoding_method=encoding_method,
            drop=drop,
            year_range=year_range)
        
        all_scores[n_months] = {}
        
        for sector, sector_data_dict in data_dict.items():
            
            X = sector_data_dict['X']
            y = sector_data_dict['y']
        
            X = X.sample(n=X.shape[0], random_state=random_state)
            shuffle_idx = X.index
            y = y.loc[shuffle_idx]

            X = X.to_numpy()
            y = y.to_numpy()

            # Conducting cross validation
            model_score_dict, predictions = conduct_cv(model_class, X, y, model_params, model_fit_params)

            all_scores[n_months][sector] = model_score_dict
            
    return all_scores


def run_general_value_model(
    model_class,
    model_params={},
    model_fit_params={},
    month_range=range(1, 7),
    drop_corr_features=True,
    encoding_method='one-hot',
    drop=True,
    year_range=(2008, 2017),
):
    
    feature, df = load_dataframes()
    df = trim_sectors(df, min_tickers=5)
    df = df[['date', 'year', 'month', 'ticker', 'marketcap']]
    df = df.rename(columns={'marketcap': 'y_true'})
    
    tickers = df['ticker'].unique()
    
    all_scores = {}
    
    for i, n_months in enumerate(month_range):
        data, X, y = load_data_general(
            n_months=n_months,
            pct_change=False,
            drop_corr_features=drop_corr_features,
            encoding_method=encoding_method,
            drop=drop,
            year_range=year_range)

        # Defining random state for shuffling data
        random_state = 763

        X = X.sample(n=X.shape[0], random_state=random_state)
        shuffle_idx = X.index
        y = y.loc[shuffle_idx]

        X = X.to_numpy()
        y = y.to_numpy()

        # Conducting cross validation
        model_score_dict, predictions = conduct_cv(model_class, X, y, model_params, model_fit_params)

        all_scores[n_months] = model_score_dict
        
        # Saving predictions
        data = data[['date', 'ticker']]
        data.loc[shuffle_idx, f'y_pred_{n_months}'] = predictions
        
        df_list = []
        for ticker in tickers:
            cond = data['ticker'] == ticker
            data_ = data.loc[cond].reset_index(drop=True)
            data_[f'y_pred_{n_months}'] = data_[f'y_pred_{n_months}'].shift(n_months)
            df_list.append(data_)
        
        data = pd.concat(df_list, ignore_index=True)
        df = df.merge(data, on=['date', 'ticker'], how='left')
        
    return df, all_scores