
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

class Model:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X_train, y_train):
        """
        Train the model
        """
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        """
        Make predictions
        """
        return self.model.predict(X_test)

    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        """
        y_pred = self.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy

    def save_model(self, filepath="model.pkl"):
        """
        Save the trained model
        """
        joblib.dump(self.model, filepath)

    def load_model(self, filepath="model.pkl"):
        """
        Load a saved model
        """
        self.model = joblib.load(filepath)
