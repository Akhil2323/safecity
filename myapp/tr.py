import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load prepared training data
data = pd.read_csv("ml_training_data.csv")

# Features and label
X = data[['crime_count', 'avg_risk']]
y = data['risk_label']

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model as .pkl
with open("crime_ai_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("crime_ai_model.pkl created successfully")
