from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Verifying the Results
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score

def train_model(engineered_data):
    
    # *** Model Training ***
    print("\n Model Training \n")
    
    # Access the selected features and DataFrame from the dictionary
    try:
        selected_features = engineered_data["selected_features"]
        df = engineered_data["df"]
    except KeyError as e:
        return f"Error: Missing key in engineered data - {e}"

    # Split the data into training and testing sets
    try:
        X = df[selected_features]  # Features for the model
        y = df['evict']  # Target: whether to evict the key
        
        print(f"Shape of X (features): {X.shape}")
        print(f"Shape of y (target): {y.shape}")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print(f"Training data shape: X_train: {X_train.shape}, y_train: {y_train.shape}")
        print(f"Testing data shape: X_test: {X_test.shape}, y_test: {y_test.shape}")
    
    except Exception as e:
        return f"Error during data splitting: {e}"

    try:
        # Train RandomForest model
        model = RandomForestClassifier()

        # fit() trains the model using the training data (X_train and y_train).
        model.fit(X_train, y_train)

        print("Model training completed successfully.")
    
    except Exception as e:
        return f"Error during model training: {e}"

    # *** Model Evaluation ***
    try:
        y_pred = model.predict(X_test)
        print("\n Model Evaluation \n")
        
        # Evaluate the model:
        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
        print(f"Precision: {precision_score(y_test, y_pred)}")
        print(f"Recall: {recall_score(y_test, y_pred)}")
        print(f"F1 Score: {f1_score(y_test, y_pred)}")

        # Verifying the Results
        y_pred = model.predict(X_test)

        # Compute the confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        print("\nConfusion Matrix: This will show the number of correct and incorrect predictions for each class, helping to identify any data issues.\n")
        
        # Plot the confusion matrix
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.show()

        # Perform cross-validation
        scores = cross_val_score(model, X, y, cv=5)
        print("\n Cross-Validation: To get a better estimate of your model’s generalization performance, you can use k-fold cross-validation.\n")
        print(f"Cross-validation scores: {scores}")
        print(f"Mean accuracy: {scores.mean()}")
        
        print("\n Check Data Distribution: Check the class distribution to ensure there’s no major imbalance. \n")
        print(df['evict'].value_counts())

    except Exception as e:
        return f"Error during model evaluation: {e}"

    return model
