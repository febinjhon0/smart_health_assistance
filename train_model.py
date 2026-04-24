import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import pickle
import os

# Create static/plots directory
plot_dir = 'static/plots'
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

print("Loading dataset...")
df = pd.read_csv('dataset.csv')

# Cleanup symptoms
symptoms_columns = [col for col in df.columns if 'Symptom' in col]
for col in symptoms_columns:
    df[col] = df[col].str.replace(' ', '').str.strip().str.replace('_', ' ')

# Get unique symptoms
all_symptoms = set()
for col in symptoms_columns:
    unique_vals = df[col].dropna().unique()
    for val in unique_vals:
        if val:
            all_symptoms.add(val)

all_symptoms = sorted(list(all_symptoms))
symptom_to_idx = {s: i for i, s in enumerate(all_symptoms)}

# Create feature matrix
X = np.zeros((len(df), len(all_symptoms)))
for i, row in df.iterrows():
    for col in symptoms_columns:
        val = row[col]
        if pd.notna(val) and val in symptom_to_idx:
            X[i, symptom_to_idx[val]] = 1

y = df['Disease'].str.strip()

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
print("Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc * 100:.2f}%")

# Move model saving BEFORE plotting
print("Saving model and metadata...")
metadata = {
    'all_symptoms': all_symptoms,
    'symptom_to_idx': symptom_to_idx,
    'diseases': model.classes_.tolist()
}

with open('disease_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model_metadata.pkl', 'wb') as f:
    pickle.dump(metadata, f)

# Performance metrics (Old scikit-learn compatible)
print("Generating reports...")
report = classification_report(y_test, y_pred)
with open(os.path.join(plot_dir, 'classification_report.txt'), 'w') as f:
    f.write(report)

print("All artifacts stored successfully.")
