
from preprocess import Preprocessor
from model import Model

def train_pipeline(data_path, target_column):
   

  
    prep = Preprocessor()

 
    data = prep.load_data(data_path)
    print("Data loaded!")

   
    data = prep.clean_data(data)
    print("Data cleaned!")

  
    X_train, X_test, y_train, y_test = prep.split_data(data, target_column)
    print("Data split!")

    
    X_train, X_test = prep.scale_data(X_train, X_test)
    print("Data scaled!")

   
    prep.save_scaler()

   
    model = Model()

    
    model.train(X_train, y_train)
    print("Model trained!")

    
    accuracy = model.evaluate(X_test, y_test)
    print(f"Model Accuracy: {accuracy:.2f}")

   
    model.save_model("model.pkl")
    print("Model saved!")

    return accuracy


if __name__ == "__main__":
    
    data_path = "data.csv"
    target_column = "target"

    train_pipeline(data_path, target_column)
