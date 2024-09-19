# trade_decision.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Create features and labels for the machine learning model
def create_features_and_labels(data):
    data['MACD_Signal_Diff'] = data['MACD'] - data['Signal']
    data['RSI_overbought'] = np.where(data['RSI'] > 70, 1, 0)
    data['RSI_oversold'] = np.where(data['RSI'] < 30, 1, 0)
    data['BB_above_upper'] = np.where(data['close'] > data['BB_upper'], 1, 0)
    data['BB_below_lower'] = np.where(data['close'] < data['BB_lower'], 1, 0)

    # Label: 1 for Buy (price goes up), 0 for Sell (price goes down)
    data['Target'] = np.where(data['close'].shift(-1) > data['close'], 1, 0)
    return data.dropna()

# Train the machine learning model
def train_ml_model(data):
    X = data[['MACD_Signal_Diff', 'RSI', 'RSI_overbought', 'RSI_oversold', 'BB_above_upper', 'BB_below_lower']]  # Features
    y = data['Target']  # Label

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy:.2f}")

    return model

# Make a trade decision based on the trained ML model
def make_ml_trade_decision(model, data):
    features = data[['MACD_Signal_Diff', 'RSI', 'RSI_overbought', 'RSI_oversold', 'BB_above_upper', 'BB_below_lower']].iloc[-1:]
    prediction = model.predict(features)
    return "BUY" if prediction == 1 else "SELL"
