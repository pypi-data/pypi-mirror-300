import unittest
import pandas as pd
import numpy as np
from ndata.preprocess import DataPreprocessor

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        data = {
            'age': [25, 30, np.nan, 40],
            'salary': [50000, np.nan, 75000, 60000],
            'gender': ['male', 'female', 'female', np.nan]
        }
        self.df = pd.DataFrame(data)
        self.preprocessor = DataPreprocessor(self.df)

    def test_handle_missing_values(self):
        processed_df = self.preprocessor.handle_missing_values(strategy='mean')
        self.assertFalse(processed_df.isnull().any().any())

    def test_scale_features(self):
        processed_df = self.preprocessor.scale_features()
        self.assertAlmostEqual(processed_df['age'].mean(), 0, delta=1e-6)

    def test_encode_categorical(self):
        processed_df = self.preprocessor.encode_categorical()
        self.assertIn('gender_male', processed_df.columns)

if __name__ == '__main__':
    unittest.main()
