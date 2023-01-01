import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_metric_by_months_general(all_scores, metric='MAE', ax=None, color='black', std=True, linestyle='-'):
    
    if ax is None:
        fig, ax = plt.subplots()
        
    x = list(all_scores.keys())
    x = list(map(int, x))
    
    score_arr = []
    std_arr = []

    for key, model_scores in all_scores.items():
        score_arr.append(np.mean(model_scores[metric]))
        std_arr.append(np.std(model_scores[metric]))

    score_arr = np.array(score_arr)
    std_arr = np.array(std_arr)

    

    ax.plot(x, score_arr, label=f'General Avg 5-fold {metric}', color=color, linestyle=linestyle)
    if std:
        low = score_arr - 2*std_arr
        upp = score_arr + 2*std_arr
        ax.fill_between(x=x, y1=low, y2=upp, color=color, alpha=0.2, label='+-2 Std')
        
    ax.set_xlabel('Months ahead')
    ax.set_ylabel(metric)
    ax.set_xlim(x[0], x[-1])
    ax.legend()
    
    return ax



def plot_metric_by_months_sector(all_scores, metric='MAE', ax=None, linestyle='-'):
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))
       
    x = list(all_scores.keys())
    sectors = all_scores[x[0]].keys()
    
    x = list(map(int, x))
    
    colors = ["#fd7f6f", "#7eb0d5", "#b2e061", "#ffee65", "#8bd3c7"]
    for sector, color in zip(sectors, colors):
        score_arr = []
        std_arr = []
        
        for n_months in all_scores.keys():
            model_scores = all_scores[n_months][sector]
            score_arr.append(np.mean(model_scores[metric]))
            std_arr.append(np.std(model_scores[metric]))

        score_arr = np.array(score_arr)
        std_arr = np.array(std_arr)

        low = score_arr - 2*std_arr
        upp = score_arr + 2*std_arr

        ax.plot(x, score_arr, label=f'{sector} Avg 5-fold {metric}', color=color, linestyle=linestyle)
#         ax.fill_between(x=x, y1=low, y2=upp, alpha=0.2, color=color)
        
    ax.set_xlabel('Months ahead')
    ax.set_ylabel(metric)
    ax.set_xlim(x[0], x[-1])
    ax.legend()
    
    return ax


def plot_model_predictions(data, ticker, n_month=None, ax=None, metric='MAE'):

    if n_month:
        pred_col = f'y_pred_{n_month}'
    else:
        pred_col = 'y_pred'
        
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 4))
    
    cond = data['ticker'] == ticker
    graph_data = data.loc[cond].sort_values(by='date').reset_index(drop=True)
    graph_data = graph_data.dropna(subset=pred_col)
    
    # Plotting true values
    ax.plot('date', 'y_true', data=graph_data, color='gray', alpha=0.6, label='True value')

    # Plotting the 5-fold Test predictions
    ax.plot('date', pred_col, data=graph_data, color='limegreen', alpha=0.6, label='5-fold Test predictions')
    
    # Model score
    fun = score_fun_dict[metric]
    score = fun(graph_data['y_true'], graph_data[pred_col])
    
    ax.set_title(f'{ticker} / 5-fold {metric} = {score:.3f}')
    ax.set_xlabel('Date')
    

    ax.legend()
    
    return ax