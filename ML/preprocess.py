
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib


class Preprocessor:
    def __init__(self):
        self.scaler = StandardScaler()

    def load_data(self, filepath):
        """
        Load dataset from CSV file
        """
        data = pd.read_csv(filepath)
        return data

    def clean_data(self, data):
        """
        Basic data cleaning
        """
        # Remove missing values
        data = data.dropna()

        return data

    def split_data(self, data, target_column):
        """
        Split dataset into features and target
        """
        X = data.drop(columns=[target_column])
        y = data[target_column]

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def scale_data(self, X_train, X_test):
        """
        Apply feature scaling
        """
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        return X_train_scaled, X_test_scaled

    def save_scaler(self, filepath="scaler.pkl"):
        """
        Save scaler
        """
        joblib.dump(self.scaler, filepath)

    def load_scaler(self, filepath="scaler.pkl"):
        """
        Load scaler
        """
        self.scaler = joblib.load(filepath)
