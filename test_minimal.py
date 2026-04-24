import pandas as pd
import numpy as np
import pickle

print("Minimal test start")
df = pd.read_csv('dataset.csv')
print("Loaded CSV")

symptoms_columns = [col for col in df.columns if 'Symptom' in col]
for col in symptoms_columns:
    df[col] = df[col].str.replace(' ', '').str.strip()

all_symptoms = set()
for col in symptoms_columns:
    unique_vals = df[col].dropna().unique()
    for val in unique_vals:
        if val:
            all_symptoms.add(val)

all_symptoms = sorted(list(all_symptoms))
print(f"Symptoms: {len(all_symptoms)}")

metadata = {'all_symptoms': all_symptoms}
with open('test_meta.pkl', 'wb') as f:
    pickle.dump(metadata, f)
print("Saved test_meta.pkl")
