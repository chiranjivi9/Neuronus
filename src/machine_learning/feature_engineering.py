import time
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier

def feature_engineering(processed_data):
    # Load and preprocess the data
    
    df = processed_data
    # Check that the data loaded correctly
    print("Initial Data:")
    print(df.head())

    print("Performing Feature Engineering")

    # Create the 'time_since_last_accessed' feature based on the time difference
    if 'last_accessed' in df.columns:
        df['time_since_last_accessed'] = time.time() - df['last_accessed']
    else:
        raise KeyError("Column 'last_accessed' not found in the dataset.")

    # Create the 'access_ttl_interaction' feature
    if 'access_count' in df.columns and 'ttl' in df.columns:
        df['access_ttl_interaction'] = df['access_count'] * df['ttl']
    else:
        raise KeyError("Columns 'access_count' or 'ttl' not found in the dataset.")

    # Create the 'evict' column where ttl == 0 indicates eviction
    df['evict'] = df['ttl'].apply(lambda ttl: 1 if ttl == 0 else 0)

    # Check for missing values (NaNs) that might cause issues
    if df.isnull().values.any():
        print("Warning: Data contains missing values. Consider handling them before proceeding.")
        print(df.isnull().sum())

    # Perform Feature Selection using Recursive Feature Elimination (RFE)
    print("Selecting Features using RFE")

    # RandomForest model for feature selection
    model = RandomForestClassifier()

    # Selecting 5 features using RFE
    selector = RFE(model, n_features_to_select=5)

    # Check available columns before dropping
    print("Columns before feature selection:", df.columns)

    # Make sure to drop 'evict' as it's the target column
    X = df.drop('evict', axis=1)
    y = df['evict']

    # Perform RFE to select top features
    selector = selector.fit(X, y)

    # Get the names of the selected features
    selected_features = X.columns[selector.support_]
    print("Selected features:", selected_features)
    
    return { "selected_features": selected_features, "df": df }
