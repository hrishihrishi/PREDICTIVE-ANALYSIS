Predictive Analysis API for Manufacturing Operations

Overview

This project provides a RESTful API for predictive analysis of machine downtime or production defects. The API uses a supervised machine learning model to predict outcomes based on manufacturing data, allowing for better decision-making in operations.

Features

Upload Data: Upload a CSV file containing manufacturing data.

Train Model: Train a machine learning model (Logistic Regression) on the uploaded data.

Make Predictions: Predict machine downtime or production defects using input features like Temperature and Run_Time.

Endpoints

1. Upload Endpoint

Method: POST

URL: /upload

Description: Upload a CSV file containing manufacturing data.

Payload:

Form-data key: file (type: File)

Response:

{
  "message": "File uploaded successfully!"
}

2. Train Endpoint

Method: POST

URL: /train

Description: Train the ML model on the uploaded dataset.

Response:

{
  "message": "Model trained successfully!"
}

3. Predict Endpoint

Method: POST

URL: /predict

Description: Predict machine downtime or defects based on input data.

Payload:

{
  "Temperature": 80,
  "Run_Time": 120
}

Response:

{
  "Downtime": "Yes",
  "Confidence": 0.85
}

Setup Instructions

Prerequisites

Python 3.8 or higher

pip

Installation

Clone the repository:

git clone <repository-url>
cd <repository-folder>

Install the required dependencies:

pip install -r requirements.txt

Start the FastAPI server:

python main.py

Expose the server using ngrok (optional):

ngrok http 8000

Access the API documentation at:

http://127.0.0.1:8000/docs

Or use the ngrok public URL if enabled.

Example Dataset

You can use a dataset with the following structure:

Machine_ID

Temperature

Run_Time

Downtime_Flag

1

80

120

1

2

85

150

0

Download example datasets from Kaggle or UCI ML Repository.

Testing the API

Using Postman

Open Postman and create a new request.

For /upload, select POST, use form-data, and upload your CSV file.

For /train, select POST and send the request.

For /predict, select POST, use raw JSON format, and send:

{
  "Temperature": 80,
  "Run_Time": 120
}

Using cURL

Upload Data:

curl -X POST -F "file=@data.csv" http://127.0.0.1:8000/upload

Train Model:

curl -X POST http://127.0.0.1:8000/train

Make Predictions:

curl -X POST -H "Content-Type: application/json" -d '{"Temperature": 80, "Run_Time": 120}' http://127.0.0.1:8000/predict

Dependencies

fastapi

uvicorn

scikit-learn

pandas

pyngrok

nest_asyncio

python-multipart

License

This project is licensed under the MIT License. See the LICENSE file for details.

Author

Developed as part of an internship project. If you have any questions, feel free to reach out!
