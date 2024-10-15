# Neuronus ML Component - Key Eviction Strategy

This folder contains scripts and data for implementing an ML-based key eviction strategy in Neuronus. The goal is to predict which keys in the Neuronus key-value store should be evicted based on access patterns such as access frequency, size, and time-to-live (TTL).

## Steps

### Prerequisite 
1. **Generate Data**: 
   - The `generate_entries.py` script simulates random `SET`, `GET`, `DEL`, and `EXPIRE` operations on the Neuronus key-value store.
   - It collects access patterns like access count, last accessed time, and key size into a file (`generated_analytics.json`) for later use in ML models.

2. **Simulate Operations**:
   - Run the script to simulate key operations and generate the dataset for ML preprocessing:
     ```
      python src/ml/generate_entries.py
     ```
   - This script will generate 5000 operations by default and save the analytics data in JSON format (`generated_analytics.json`).

### Workflow
1. **Data Preprocessing**: 
   - The data collected from generate_entries.py needs to be cleaned and prepared for model training. This step includes:
      - Loading the JSON file (generated_analytics.json).
      - Handling missing or erroneous data.
      - Converting data types (e.g., timestamps to numerical values).
      - This process is handled in the `data_preprocessing.py` script.
      ```
      python src/machine_learning/helpers/data_preprocessing.py
      ```
2. **Feature Engineering**: 
   - This step transforms the raw data into features that can help the model better understand the eviction patterns. It includes:
      - Creating time-based features such as time_since_last_accessed.
      - Interaction features such as access_ttl_interaction, which combines the number of accesses with TTL.
      - Eviction Labeling: The evict column is created, where ttl == 0 means the key should be evicted.
      - Feature selection is done using Recursive Feature Elimination (RFE) to identify the most important features.
      - This process is handled in the feature_engineering.py script.
      ```
      python src/machine_learning/helpers/feature_engineering.py
      ```
3. **Model Development**: 
   - After feature engineering, we use the selected features to train a machine learning model. The steps include:
      - Splitting the data into training and testing sets.
      - Training a RandomForestClassifier to predict whether a key should be evicted or not.
      - Model training is handled in the model_training.py script.
      ```
      python src/machine_learning/helpers/model_training.py
      ```

4. **Model Evaluation**: 
   - Evaluate the trained model to ensure it performs well on unseen data. This includes:
      - Confusion Matrix: To visualize how many evictions were correctly predicted.
      - Cross-Validation: To assess how well the model generalizes to unseen data.
      - Metrics: Evaluate accuracy, precision, recall, and F1-score to get a balanced view of model performance.
      ```
      python src/machine_learning/helpers/model_training.py
      ```
5. **Model Integration(TODO)**: 
   - Once the model is trained and evaluated, it can be integrated into the Neuronus key-value store to make real-time decisions about key eviction based on the learned patterns.
6. **Invocation Script**:
   - All the steps in the workflow can be invoked through the invoke.py script, which handles data preprocessing, feature engineering, model training, and evaluation in one flow.
      ```
      python src/machine_learning/helpers/invoke.py
      ```
