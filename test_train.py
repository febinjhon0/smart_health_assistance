import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

print("Training test start")
df = pd.read_csv('dataset.csv')
symptoms_columns = [col for col in df.columns if 'Symptom' in col]
for col in symptoms_columns:
    df[col] = df[col].str.replace(' ', '').str.strip()

all_symptoms = sorted(list(set([val for col in symptoms_columns for val in df[col].dropna().unique() if val])))
s_idx = {s: i for i, s in enumerate(all_symptoms)}

X = np.zeros((len(df), len(all_symptoms)))
for i, row in df.iterrows():
    for col in symptoms_columns:
        if pd.notna(row[col]) and row[col] in s_idx:
            X[i, s_idx[row[col]]] = 1
y = df['Disease'].str.strip()

model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X, y)
print("Model trained")

with open('disease_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Saved model")
