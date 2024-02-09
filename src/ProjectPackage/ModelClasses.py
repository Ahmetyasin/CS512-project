import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor


class RFRegressor:

    def __init__(self):
        self.algorithm = 'RF'

    def create_grid(self, n_estimators, min_samples_leaf, max_samples, cv):
        """
        Create a grid search for a SVR model with RBF kernel
        """

        pipe = RandomForestRegressor(n_jobs=2)

        param_grid = {'n_estimators': n_estimators,
                      'min_samples_leaf': min_samples_leaf,
                      'max_samples': max_samples
                      }

        scoring = {'R2': 'r2', 'MSE': 'neg_mean_squared_error'}

        grid = GridSearchCV(estimator=pipe, param_grid=param_grid,
                            scoring=scoring, refit='MSE', cv=cv, verbose=2)

        return pipe, grid

    def fit(self,
            X_train,
            y_train,
            n_estimators=[50, 100, 300],
            min_samples_leaf=[10, 20, 50, 100],
            max_samples=[0.5, 0.75, 1],
            cv=5, fit_grid=False):
        """
        Find the best parameters using grid search and fit the model using these parameters.
        """
        
        if fit_grid:
            # Creating pipeline and grid search
            pipe, grid = self.create_grid(n_estimators, min_samples_leaf, max_samples, cv)

            # Fitting grid search
            grid.fit(X_train, y_train)

            # Updating pipeline parameters
            print(grid.best_params_)
            
            model = RandomForestRegressor(n_jobs=2, **grid.best_params_)
            
        else:
            model = RandomForestRegressor(n_estimators=n_estimators,
                                          min_samples_leaf=min_samples_leaf,
                                          max_samples=max_samples,
                                          n_jobs=2)

        
        model.fit(X_train, y_train)
        self.model = model
        
        
    def predict(self, X_test):
        y_hat = self.model.predict(X_test)

        return y_hat

    
    def get_params(self):
        """
        Returns a dictionary of the model parameters
        """

        params = ['n_estimators', 'min_samples_leaf', 'max_samples']
        param_dict = {}

        for param in params:
            param_dict[param] = getattr(self.model, param)

        return param_dict


class SVRRegressorRBF:

    def __init__(self, scaler=StandardScaler()):
        self.algorithm = 'SVR'
        self.scaler = scaler

    def create_svr_grid(self, C, gamma, cv):
        """
        Create a grid search for a SVR model with RBF kernel
        """

        steps = [
            ('scaler', self.scaler),
            ('svr', SVR(kernel='rbf', cache_size=500))
        ]

        pipe = Pipeline(steps=steps)

        param_grid = {'svr__C': C,
                      'svr__gamma': gamma}

        scoring = {'R2': 'r2', 'MSE': 'neg_mean_squared_error'}
        grid = GridSearchCV(estimator=pipe, param_grid=param_grid,
                            scoring=scoring, return_train_score=True,
                            refit='R2', cv=cv, verbose=2)
        return pipe, grid

    def fit(self, X_train, y_train, C=[1, 5, 50, 100], gamma=[0.05, 0.1, 0.5, 1], cv=5, fit_grid=False):
        """
        Find the best parameters using grid search and fit the model using these parameters.
        """
        
        if fit_grid:
            # Creating pipeline and grid search
            pipe, grid = self.create_svr_grid(C, gamma, cv)

            # Fitting grid search
            grid.fit(X_train, y_train)

            # Updating pipeline parameters
            print(grid.best_params_)

            C_ = grid.best_params_['svr__C']
            gamma_ = grid.best_params_['gamma']

            model = SVR(kernel='rbf', cache_size=500, C=C_, gamma=gamma_)
            
        else:
            model = SVR(kernel='rbf', cache_size=500, C=C, gamma=gamma)
        
        self.scaler.fit(X_train)
        
        X_train_norm = self.scaler.transform(X_train)
        model.fit(X_train_norm, y_train)
        
        self.model = model

    def predict(self, X_test):
        
        X_test_norm = self.scaler.transform(X_test)
        y_hat = self.model.predict(X_test_norm)

        return y_hat

    def get_params(self):
        """
        Returns a dictionary of the model parameters
        SVR RBF parameters: kernel, C, gamma
        """

        params = ['kernel', 'C', 'gamma']
        param_dict = {}

        for param in params:
            param_dict[param] = getattr(self.model['svr'], param)

        return param_dict