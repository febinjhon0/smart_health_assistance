# 🏥 Smart Health AI Assistant System

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?style=for-the-badge&logo=django)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge&logo=mysql)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-red?style=for-the-badge&logo=scikit-learn)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap)

> An intelligent healthcare web platform that predicts possible diseases based on user-entered symptoms using Machine Learning, and connects patients with doctors for online consultation.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Database Schema](#database-schema)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [ML Model Details](#ml-model-details)
- [User Roles](#user-roles)
- [Future Enhancements](#future-enhancements)
- [Limitations](#limitations)
- [Author](#author)
- [Acknowledgements](#acknowledgements)

---

## 📖 About the Project

The **Smart Health AI Assistant System** is a full-stack web application developed as a final year project for the Master of Computer Applications (MCA) degree at **School of Technology and Applied Sciences (STAS), Edappally**, affiliated to Mahatma Gandhi University, Kottayam.

The system allows users to enter their symptoms through **text or voice input**, analyses them using a trained **Machine Learning model**, and predicts possible diseases along with confidence levels. It also provides basic medication guidance, suggests doctors, and enables **online appointment booking and consultation**.

### 🎯 Goal

To bridge the gap between patients and healthcare by offering a smart, accessible, and secure preliminary diagnosis platform — reducing dependency on immediate hospital visits, especially for users in remote areas.

---

## ✨ Features

### 🔐 Authentication & Roles
- Secure login and registration for Patients, Doctors, and Admin
- Role-based dashboard and access control
- Session management

### 🤖 AI Disease Prediction
- Symptom input via text or voice (speech-to-text)
- Machine Learning based disease prediction with confidence score
- Basic medication suggestions for predicted diseases
- Prediction history stored per patient

### 🩺 Doctor Module
- Doctor registration with admin approval
- Manage appointment slots with capacity control
- View patient details and prediction history
- Write consultation reports and upload prescriptions
- Token-based appointment queue system

### 👤 Patient Module
- Register, login, and manage personal profile
- Enter symptoms and view AI prediction results
- Browse and filter doctors by specialization
- Book appointments from available slots
- View prescriptions and health reports
- Submit feedback and rate doctors

### 💬 AI Chatbot
- Keyword-based medical chatbot (HealthBot)
- Answers common health queries
- Stores conversation history per patient
- Includes quick doctor booking from chat

### 🛡️ Admin Module
- Manage all patients and doctors (CRUD)
- View all system appointments
- Respond to patient feedback
- Monitor system activity

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| HTML5 | Page structure |
| CSS3 | Styling |
| Bootstrap 5 | Responsive design |
| JavaScript | Client-side interactivity |

### Backend
| Technology | Purpose |
|---|---|
| Python 3.8+ | Core programming language |
| Django 4.x | Web framework (MVT pattern) |
| Django ORM | Database interactions |

### Machine Learning
| Library | Purpose |
|---|---|
| scikit-learn | ML model (Decision Tree / Random Forest) |
| NumPy | Numerical operations, feature vector creation |
| Pandas | Data manipulation and preprocessing |
| Pickle | Model serialization and loading |

### Database
| Technology | Purpose |
|---|---|
| MySQL 8.0 | Relational database |
| MySQL Workbench | DB management (development) |

### Tools & IDE
- PyCharm
- MySQL Workbench
- Git & GitHub

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────┐
│              User Interface                  │
│     HTML + CSS + Bootstrap + JavaScript      │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│              Django Backend                  │
│                                              │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐  │
│  │  Views   │ │  Models  │ │  Templates  │  │
│  │(Business │ │(Database │ │    (UI      │  │
│  │  Logic)  │ │ Schema)  │ │  Rendering) │  │
│  └────┬─────┘ └────┬─────┘ └─────────────┘  │
│       │            │                         │
│  ┌────▼────────────▼──────────────────────┐  │
│  │           ML Prediction Engine         │  │
│  │  disease_model.pkl + model_metadata.pkl│  │
│  │  scikit-learn | NumPy | Pandas         │  │
│  └────────────────────────────────────────┘  │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│              MySQL Database                  │
│  Patient | Doctor | Appointment | Slot       │
│  Prediction | Consultation | Prescription    │
│  Feedback | Chatbot | Review                 │
└─────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

Key tables in the system:

| Table | Description |
|---|---|
| `patient` | Patient registration and profile data |
| `doctor` | Doctor profile, specialization, experience |
| `appointment` | Booking records linking patient and doctor |
| `slot` | Doctor availability slots with capacity |
| `prediction` | ML prediction results per patient |
| `consultation` | Doctor remarks and consultation records |
| `prescription` | Medicines and prescription files |
| `feedback` | Patient feedback with admin responses |
| `chatbot` | Chatbot conversation history |
| `review` | Patient reviews and ratings for doctors |

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure you have the following installed:
- Python 3.8 or above
- MySQL 8.0
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/smart-health-ai.git
cd smart-health-ai
```

### 2. Create and Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

Open `settings.py` and update the database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smart_health_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Create the database in MySQL:

```sql
CREATE DATABASE smart_health_db;
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Place ML Model Files

Ensure the following files are in the project root directory:

```
smart-health-ai/
├── disease_model.pkl
├── model_metadata.pkl
```

> If these files are not included, refer to the [ML Model Details](#ml-model-details) section to train and generate them.

### 7. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

### Default Admin Login

```
Email    : admin@gmail.com
Password : admin
```

---

## 🚀 Usage

### As a Patient
1. Register at `/register/`
2. Login at `/login/`
3. Navigate to **Prediction** — enter your symptoms in the text box
4. View predicted disease and confidence score
5. Browse doctors under **Doctors** tab and book a slot
6. Use **Health Chat** for quick health queries
7. Track your history under **History** and **Health Reports**

### As a Doctor
1. Register at `/doctor/` — requires admin approval
2. Add availability slots from **Add Slot**
3. View patient appointments on your dashboard
4. Create consultation reports and upload prescriptions from patient records

### As Admin
1. Login with admin credentials
2. Manage doctors, patients, and appointments
3. Respond to patient feedback from the **Crisis & Resolution Hub**
4. Monitor all system activity

---

## 📁 Project Structure

```
smart-health-ai/
│
├── smart_db/                   # Main Django app
│   ├── models.py               # Database models
│   ├── views.py                # All view functions
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin panel config
│
├── templates/                  # HTML templates
│   ├── index.html              # Home / Dashboard
│   ├── login.html              # Login page
│   ├── register.html           # Patient registration
│   ├── predict.html            # Disease prediction
│   ├── chatbot.html            # AI chatbot
│   ├── viewdoctor.html         # Doctor listing
│   ├── appointments.html       # Appointment management
│   ├── history.html            # Patient health history
│   ├── view_reports.html       # Consultant reports
│   ├── profile.html            # Patient profile
│   └── ...                     # Other templates
│
├── static/
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript files
│   ├── images/                 # Static images
│   └── plots/
│       ├── accuracy_graph.png  # ML model accuracy graph
│       └── classification_report.txt
│
├── media/
│   └── prescriptions/          # Uploaded prescription files
│
├── disease_model.pkl           # Trained ML model
├── model_metadata.pkl          # Symptom index metadata
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🤖 ML Model Details

### How Prediction Works

1. User enters symptoms as free text
2. The system loads `disease_model.pkl` and `model_metadata.pkl`
3. A **binary feature vector** is created — one position per known symptom, marked 1 if present in user's text
4. The vector is fed into the trained classifier
5. The model returns a predicted disease and probability score
6. A hardcoded advice map returns basic medication guidance

### Training the Model (if pkl files are missing)

```python
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load dataset
df = pd.read_csv('dataset.csv')

# Prepare features and labels
X = df.drop('prognosis', axis=1)
y = df['prognosis']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")
print(classification_report(y_test, predictions))

# Save model
with open('disease_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save metadata
all_symptoms = list(X.columns)
symptom_to_idx = {s: i for i, s in enumerate(all_symptoms)}
meta = {'all_symptoms': all_symptoms, 'symptom_to_idx': symptom_to_idx}
with open('model_metadata.pkl', 'wb') as f:
    pickle.dump(meta, f)

print("Model and metadata saved successfully.")
```

### Dataset
The model is trained on a symptom-disease dataset containing approximately **41 diseases** and **132 symptoms**.

Dataset source: [UCI ML Repository](https://archive.ics.uci.edu/) / Kaggle Disease Symptom Prediction Dataset

---

## 👥 User Roles

| Role | Access Level | Key Capabilities |
|---|---|---|
| **Admin** | Full system access | Manage users, view reports, respond to feedback |
| **Doctor** | Doctor dashboard | Manage slots, write prescriptions, view patients |
| **Patient** | Patient dashboard | Predict disease, book appointments, chat with bot |

---

## 📸 Screenshots

| Page | Description |
|---|---|
| Home Dashboard | Smart Care for Better Living landing page |
| Doctor Registration | Professional medical network registration form |
| Find a Doctor | Browse doctors by specialization with ratings |
| Disease Prediction | Symptom input and AI prediction result |
| Medical AI Assistant | HealthBot chatbot interface |
| My Appointments | Appointment tracking with token system |
| Health Records | Past predictions with confidence scores |
| Doctor Dashboard | Appointment management for doctors |

---

## 🔮 Future Enhancements

- [ ] Integrate deep learning models (LSTM / Transformer) for better NLP symptom understanding
- [ ] Develop Android / iOS mobile application
- [ ] Connect with IoT wearable devices for real-time vitals monitoring
- [ ] Add multilingual support for regional languages
- [ ] Integrate with hospital management systems
- [ ] Enable online prescription and pharmacy ordering
- [ ] Implement blockchain for stronger medical data privacy
- [ ] Add real-time emergency alert system
- [ ] Upgrade chatbot with a proper LLM backend (e.g. GPT / Claude API)

---

## ⚠️ Limitations

- Symptom matching uses simple string-contains logic — misspellings or informal language reduce accuracy
- The chatbot is rule-based, not truly conversational AI
- The system provides **preliminary guidance only** — it is **not a replacement** for professional medical diagnosis
- Password storage should be upgraded to Django's hashed storage (`make_password`) before any production deployment
- Voice input depends on browser Web Speech API support (Chrome recommended)

---

## 📋 Requirements

```
Django>=4.0
mysqlclient>=2.1.0
scikit-learn>=1.0.0
numpy>=1.21.0
pandas>=1.3.0
Pillow>=9.0.0
```

Install with:

```bash
pip install -r requirements.txt
```

---
<p align="center">
  Made with ❤️ for better healthcare accessibility
  <br/>
  STAS Edappally — MCA 2024-2026
</p>
