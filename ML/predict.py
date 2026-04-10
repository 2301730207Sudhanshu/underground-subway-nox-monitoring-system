
import numpy as np
from model import Model

def predict_sample(features):
    """
    Predict using trained model
    """
    # Load model
    model = Model()
    model.load_model("model.pkl")

    # Convert input to numpy array
    features = np.array(features).reshape(1, -1)

    # Make prediction
    prediction = model.predict(features)

    return prediction[0]


if __name__ == "__main__":
    # Example input (same format as training data)
    sample = [5.1, 3.5, 1.4, 0.2]

    result = predict_sample(sample)
    print("Prediction:", result)
