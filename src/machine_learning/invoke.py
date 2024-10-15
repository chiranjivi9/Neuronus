# File which invokes the workflow steps
from data_preprocessing import preprocess_data
from feature_engineering import feature_engineering
from model_training import train_model
import logging

# Setup logging to capture errors in a log file
logging.basicConfig(filename='ml_workflow.log', level=logging.ERROR)

def invoke():
  
    # Step 1: Preprocess the data
    try:
        processed_data = preprocess_data()
        
        if preprocess_data is None:
            raise ValueError("Processed data is empty or None.")
        
        print("Data preprocessing completed successfully.")
        
    except Exception as e:
        logging.error(f"Error in data preprocessing {e}")
        return f"Error in data preprocessing {e}"
    
    # Step 2: Perform feature engineering
    try:
        engineered_data = feature_engineering(processed_data)
        if engineered_data is None:
            raise ValueError("Feature engineering failed or returned None.")

        print("Feature engineering completed successfully.")

    except Exception as e:
        logging.error(f"Error in feature engineering: {e}")
        return f"Error in feature engineering: {e}"

    # Step 3: Train the model + Evaluation
    try:
        model = train_model(engineered_data)
        if model is None:
            raise ValueError("Model training failed or returned None.")

        print("Model training completed successfully.")

    except Exception as e:
        logging.error(f"Error in model training: {e}")
        return f"Error in model training: {e}"
    
    return "Workflow completed successfully."


if __name__ == '__main__':
    result = invoke()
    print(result)
