import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

def load_data(filepath):
    """
    Loads data from a CSV file.
    """
    if not os.path.exists(filepath):
        print(f"Error: Dataset not found at {filepath}")
        print("Please place your NSL-KDD dataset (e.g., KDDTrain+.txt) in the data/ folder.")
        return None
    
    # Example for NSL-KDD without headers - adjust based on your exact dataset!
    # Common features for NSL-KDD
    columns = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 
        'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 
        'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root', 
        'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 
        'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate', 
        'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 
        'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 
        'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 
        'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 
        'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'attack_type', 'difficulty_level'
    ]
    df = pd.read_csv(filepath, names=columns)
    return df

def perform_eda(df):
    """
    Perform Exploratory Data Analysis.
    This correlates to the "Statistical Learning" subject.
    """
    print("\n--- Exploratory Data Analysis ---")
    print(f"Dataset shape: {df.shape}")
    print("\nClass distribution (Attack vs Normal):")
    
    # Map all specific attacks to 'attack' and normal to 'normal' for binary classification
    df['label'] = df['attack_type'].apply(lambda x: 'normal' if x == 'normal' else 'attack')
    
    print(df['label'].value_counts())
    
    # Example visualization (uncomment when running)
    # plt.figure(figsize=(8, 5))
    # sns.countplot(data=df, x='label')
    # plt.title('Distribution of Network Traffic Classes')
    # plt.show()

def preprocess_data(df):
    """
    Cleans and prepares data for Machine/Deep Learning models.
    """
    print("\n--- Data Preprocessing ---")
    
    # 1. Handle Categorical features
    cat_columns = ['protocol_type', 'service', 'flag']
    le = LabelEncoder()
    for col in cat_columns:
        if col in df.columns:
            df[col] = le.fit_transform(df[col])
            
    # 2. Map label to 0 (normal) and 1 (attack)
    df['label'] = df['label'].map({'normal': 0, 'attack': 1})
    
    # Drop original attack_type and difficulty_level
    features_to_drop = ['attack_type', 'difficulty_level']
    X = df.drop(columns=[col for col in features_to_drop if col in df.columns] + ['label'])
    y = df['label']
    
    # 3. Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Feature Scaling (Crucial for Deep Learning)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Training data shape: X={X_train_scaled.shape}, y={y_train.shape}")
    print(f"Testing data shape: X={X_test_scaled.shape}, y={y_test.shape}")
    
    # Save the processed data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    np.save(os.path.join(base_dir, 'data', 'X_train.npy'), X_train_scaled)
    np.save(os.path.join(base_dir, 'data', 'y_train.npy'), y_train)
    np.save(os.path.join(base_dir, 'data', 'X_test.npy'), X_test_scaled)
    np.save(os.path.join(base_dir, 'data', 'y_test.npy'), y_test)
    print("\nPreprocessed data saved to data/ folder.")
    
    return X_train_scaled, X_test_scaled, y_train, y_test

if __name__ == "__main__":
    # Ensure correct paths regardless of where the script is executed from
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(BASE_DIR, "data", "KDDTrain+.txt")
    
    print("Starting Phase 1: Data Acquisition & Preprocessing")
    df = load_data(dataset_path)
    
    if df is not None:
        perform_eda(df)
        preprocess_data(df)
