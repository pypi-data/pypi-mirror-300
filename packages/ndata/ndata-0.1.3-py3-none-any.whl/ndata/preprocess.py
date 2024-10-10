import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import numpy as np
from scipy.stats import zscore

class DataPreprocessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # Handling missing values
    def handle_missing_values(self, strategy='mean', fill_value=None):
        imputer = SimpleImputer(strategy=strategy, fill_value=fill_value)
        self.df[self.df.columns] = imputer.fit_transform(self.df)
        return self.df

    # Scaling numerical features
    def scale_features(self, columns=None, scaler=None):
        if scaler is None:
            scaler = StandardScaler()
        if columns is None:
            columns = self.df.select_dtypes(include=np.number).columns
        self.df[columns] = scaler.fit_transform(self.df[columns])
        return self.df

    # Encoding categorical variables
    def encode_categorical(self, columns=None, drop_first=True):
        if columns is None:
            columns = self.df.select_dtypes(include='object').columns
        encoder = OneHotEncoder(drop=drop_first, sparse=False)
        encoded = pd.DataFrame(encoder.fit_transform(self.df[columns]), columns=encoder.get_feature_names_out(columns))
        self.df.drop(columns, axis=1, inplace=True)
        self.df = pd.concat([self.df.reset_index(drop=True), encoded.reset_index(drop=True)], axis=1)
        return self.df

    # Detecting and removing outliers
    def detect_outliers(self, method='zscore', threshold=3):
        if method == 'zscore':
            z_scores = np.abs(zscore(self.df.select_dtypes(include=np.number)))
            self.df = self.df[(z_scores < threshold).all(axis=1)]
        elif method == 'iqr':
            Q1 = self.df.quantile(0.25)
            Q3 = self.df.quantile(0.75)
            IQR = Q3 - Q1
            self.df = self.df[~((self.df < (Q1 - 1.5 * IQR)) | (self.df > (Q3 + 1.5 * IQR))).any(axis=1)]
        return self.df

    # Full preprocessing pipeline
    def preprocess(self, strategy='mean', scaler=None, drop_first=True, outlier_method=None):
        self.handle_missing_values(strategy=strategy)
        self.scale_features(scaler=scaler)
        self.encode_categorical(drop_first=drop_first)
        if outlier_method:
            self.detect_outliers(method=outlier_method)
        return self.df
