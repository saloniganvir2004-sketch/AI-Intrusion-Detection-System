import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Input
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import os

def load_preprocessed_data():
    """Load the preprocessed NumPy arrays generated from the EDA phase."""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        X_train = np.load(os.path.join(base_dir, 'data', 'X_train.npy'))
        y_train = np.load(os.path.join(base_dir, 'data', 'y_train.npy'))
        X_test = np.load(os.path.join(base_dir, 'data', 'X_test.npy'))
        y_test = np.load(os.path.join(base_dir, 'data', 'y_test.npy'))
        return X_train, X_test, y_train, y_test
    except FileNotFoundError:
        print("Error: Preprocessed data not found. Please run 1_eda_and_preprocessing.py first.")
        return None, None, None, None

def train_baseline_statistics_model(X_train, y_train, X_test, y_test):
    """
    Train a Random Forest classifier as a statistical baseline.
    Subject Mapping: Statistical Learning.
    """
    print("\n--- Training Baseline Statistical Model (Random Forest) ---")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    predictions = rf_model.predict(X_test)
    print("Baseline Model Performance:")
    print(classification_report(y_test, predictions))
    
    # Save the model architecture mathematically or via joblib in production
    return rf_model

def build_deep_learning_autoencoder(input_dim):
    """
    Builds an Autoencoder using TensorFlow/Keras.
    Subject Mapping: Deep Learning.
    An autoencoder learns the 'normal' traffic. Intrusions have high reconstruction error.
    """
    # Encoder
    input_layer = Input(shape=(input_dim,))
    encoder = Dense(32, activation="relu")(input_layer)
    encoder = Dropout(0.2)(encoder)
    encoder = Dense(16, activation="relu")(encoder)
    
    # Decoder
    decoder = Dense(16, activation="relu")(encoder)
    decoder = Dropout(0.2)(decoder)
    decoder = Dense(32, activation="relu")(decoder)
    decoder = Dense(input_dim, activation="linear")(decoder)
    
    autoencoder = Model(inputs=input_layer, outputs=decoder)
    autoencoder.compile(optimizer='adam', loss='mse')
    return autoencoder

def train_deep_learning_model(X_train, y_train, X_test, y_test):
    """Train the Deep Learning Anomaly Detection Model."""
    print("\n--- Training Deep Learning Model (Autoencoder) ---")
    
    # Autoencoders are trained ONLY on normal data (label 0)
    normal_data = X_train[y_train == 0]
    
    autoencoder = build_deep_learning_autoencoder(X_train.shape[1])
    
    print("\nTraining Deep Neural Network...")
    history = autoencoder.fit(
        normal_data, normal_data, 
        epochs=10, 
        batch_size=64,
        validation_split=0.2,
        verbose=1
    )
    
    # Save the model
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, 'ids_autoencoder.h5')
    autoencoder.save(model_path)
    print(f"Deep Learning model saved successfully to {model_path}")
    
    # Evaluation
    predictions = autoencoder.predict(X_test)
    mse = np.mean(np.power(X_test - predictions, 2), axis=1)
    
    # Determine anomaly threshold (e.g., 95th percentile of normal data reconstruction error)
    normal_preds = autoencoder.predict(normal_data)
    normal_mse = np.mean(np.power(normal_data - normal_preds, 2), axis=1)
    threshold = np.percentile(normal_mse, 95)
    
    # Anything above threshold is an attack
    dl_predictions = [1 if error > threshold else 0 for error in mse]
    
    print(f"\nDeep Learning Anomaly Threshold set at MSE: {threshold:.4f}")
    print("Deep Learning Model Performance:")
    print(classification_report(y_test, dl_predictions))

if __name__ == "__main__":
    print("Starting Phase 3: Deep Learning & Statistical Model Training")
    X_train, X_test, y_train, y_test = load_preprocessed_data()
    
    if X_train is not None:
        train_baseline_statistics_model(X_train, y_train, X_test, y_test)
        train_deep_learning_model(X_train, y_train, X_test, y_test)
