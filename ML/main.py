###########################
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from model import Model

def main():
    # 1. Load dataset
    data = load_iris()
    X, y = data.data, data.target

    # 2. Split data into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 3. Create model object
    model = Model()

    # 4. Train model
    model.train(X_train, y_train)
    print("Model trained successfully!")

    # 5. Evaluate model
    accuracy = model.evaluate(X_test, y_test)
    print(f"Model Accuracy: {accuracy:.2f}")

    # 6. Save trained model
    model.save_model("model.pkl")
    print("Model saved as model.pkl")

if __name__ == "__main__":
    main()
