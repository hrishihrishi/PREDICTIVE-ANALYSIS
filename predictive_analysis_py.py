# -*- coding: utf-8 -*-
"""PREDICTIVE ANALYSIS.PY"""

# Install necessary libraries
'''!pip install fastapi uvicorn scikit-learn pandas
!pip install python-multipart
!pip install pyngrok
!pip install nest_asyncio
!ngrok authtoken <your authtoken>  # Replace <your_authtoken> with your actual token'''

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import pickle
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from pyngrok import ngrok
import uvicorn
import nest_asyncio
import pandas as pd
import numpy as np

nest_asyncio.apply()

# Generates a synthetic manufacturing data
np.random.seed(42)
data = {
    "Machine_ID": np.arange(1, 101),
    "Temperature": np.random.randint(50, 100, 100),
    "Run_Time": np.random.randint(100, 500, 100),
    "Downtime_Flag": np.random.choice([0, 1], size=100, p=[0.8, 0.2])  # 20% downtime
}

df = pd.DataFrame(data)
df.to_csv("manufacturing_data.csv", index=False)
print("Dataset saved as 'manufacturing_data.csv'")
df.head()

# Load the dataset
df = pd.read_csv("manufacturing_data.csv")

# Features and target
X = df[["Temperature", "Run_Time"]]
y = df["Downtime_Flag"]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

# Save the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved as 'model.pkl'")

app = FastAPI()

# Load the model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

class PredictRequest(BaseModel):
    Temperature: float
    Run_Time: float

# uploads a data set
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    df.to_csv("uploaded_data.csv", index=False)
    return {"message": "File uploaded successfully!"}

# trains the model
@app.post("/train")
def train():
    df = pd.read_csv("uploaded_data.csv")
    X = df[["Temperature", "Run_Time"]]
    y = df["Downtime_Flag"]
    model.fit(X, y)
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
    return {"message": "Model trained successfully!"}

# gives predicted result
@app.post("/predict")
def predict(request: PredictRequest):
    input_data = [[request.Temperature, request.Run_Time]]
    prediction = model.predict(input_data)[0]
    confidence = model.predict_proba(input_data).max()
    return {"Downtime": "Yes" if prediction == 1 else "No", "Confidence": confidence}

public_url = ngrok.connect(addr='127.0.0.1:8000')
print(f"FastAPI is now available at: {public_url}")

uvicorn.run(app, host="127.0.0.1", port=8000)
