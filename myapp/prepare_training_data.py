import pandas as pd

# Load original CSV
df = pd.read_csv("ernakulam_crime_data.csv")

# Create training data (area-level summary)
train_data = df.groupby('place').agg(
    crime_count=('crime_type', 'count'),
    avg_risk=('risk_level', 'mean')
).reset_index()

# Create label (0=LOW, 1=MEDIUM, 2=HIGH)
def label_risk(x):
    if x >= 7:
        return 2
    elif x >= 4:
        return 1
    else:
        return 0

train_data['risk_label'] = train_data['avg_risk'].apply(label_risk)

train_data.to_csv("ml_training_data.csv", index=False)

print("ML training dataset created")
