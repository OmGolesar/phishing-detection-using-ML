import numpy as np
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from model.feature_extraction import extract_features_batch

class PhishingURLClassifier:
    """A classifier for detecting phishing URLs"""
    
    def __init__(self):
        """Initialize the classifier"""
        self.model = None
        self.model_path = "model/phishing_model.pkl"
        self.load_or_create_model()
    
    def load_or_create_model(self):
        """Load a saved model or create a new one if none exists"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
            else:
                # If no model exists, create a new RandomForest classifier
                self.model = RandomForestClassifier(
                    n_estimators=100, 
                    max_depth=10,
                    min_samples_split=10,
                    random_state=42
                )
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fall back to a new model
            self.model = RandomForestClassifier(
                n_estimators=100, 
                max_depth=10,
                min_samples_split=10,
                random_state=42
            )
    
    def train_model(self, X=None, y=None):
        """
        Train the model on the provided data or generate synthetic data if none provided.
        
        Args:
            X: Features (optional)
            y: Target labels (optional)
        """
        if X is None or y is None:
            # Generate synthetic training data
            # In a real application, you would use real phishing and legitimate URLs
            # This is a placeholder to ensure the model works without real data
            
            # Create features for synthetic legitimate URLs
            legitimate_features = []
            for _ in range(1000):
                features = {
                    'url_length': np.random.randint(15, 80),
                    'has_ip': np.random.choice([0, 1], p=[0.9, 0.1]),
                    'has_at_symbol': np.random.choice([0, 1], p=[0.95, 0.05]),
                    'has_multiple_subdomains': np.random.choice([0, 1], p=[0.7, 0.3]),
                    'has_suspicious_chars': np.random.choice([0, 1], p=[0.85, 0.15]),
                    'has_https': np.random.choice([0, 1], p=[0.2, 0.8]),
                    'domain_age_less_than_6months': np.random.choice([0, 1], p=[0.8, 0.2])
                }
                legitimate_features.append(features)
            
            # Create features for synthetic phishing URLs
            phishing_features = []
            for _ in range(1000):
                features = {
                    'url_length': np.random.randint(50, 150),
                    'has_ip': np.random.choice([0, 1], p=[0.3, 0.7]),
                    'has_at_symbol': np.random.choice([0, 1], p=[0.6, 0.4]),
                    'has_multiple_subdomains': np.random.choice([0, 1], p=[0.4, 0.6]),
                    'has_suspicious_chars': np.random.choice([0, 1], p=[0.3, 0.7]),
                    'has_https': np.random.choice([0, 1], p=[0.7, 0.3]),
                    'domain_age_less_than_6months': np.random.choice([0, 1], p=[0.2, 0.8])
                }
                phishing_features.append(features)
            
            # Combine features and create labels
            all_features = legitimate_features + phishing_features
            labels = [0] * len(legitimate_features) + [1] * len(phishing_features)
            
            # Convert to DataFrame
            X = pd.DataFrame(all_features)
            y = np.array(labels)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Save the model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
    
    def predict(self, features):
        """
        Predict whether a URL is phishing or legitimate.
        
        Args:
            features (dict): Extracted features from a URL
            
        Returns:
            tuple: (prediction, confidence) where prediction is 0 (legitimate) or 1 (phishing)
                  and confidence is a percentage
        """
        if self.model is None:
            raise ValueError("Model not loaded or trained. Call train_model() first.")
        
        # Convert features dictionary to a DataFrame
        features_df = pd.DataFrame([features])
        
        # Make prediction
        prediction = self.model.predict(features_df)[0]
        
        # Get prediction probabilities
        proba = self.model.predict_proba(features_df)[0]
        confidence = proba[prediction] * 100
        
        return prediction, confidence
