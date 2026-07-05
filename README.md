# 🧠 Smart Mental Health Monitoring: Activity Recommendation API

This repository contains the backend service for the Smart Mental Health Monitoring system, a final academic project designed to support university students. Built with FastAPI, this service processes physiological indicators (such as EDA/GSR and PPG) from connected wearables to detect stress patterns. Based on real-time biometric data, the system dynamically recommends personalized coping mechanisms, including specific social activities and games, to help manage stress.

This backend serves as the core intelligence engine for the companion Flutter mobile application.

---

## 🚀 Features

* **Biometric Ingestion:** Receives and processes physiological data from wearable sensors (e.g., Empatica E4, DIY sensor kits, Fitbit).  
* **Stress Analysis Engine:** Evaluates incoming heart rate and electrodermal activity data to determine the user's current stress state.  
* **Dynamic Recommendations:** Suggests context-aware interventions such as relaxing games, breathing exercises, or local social activities based on stress severity.  
* **FastAPI Backend:** High-performance, asynchronous REST API ready for mobile frontend integration.

## 📋 Prerequisites

Ensure you have the following installed on your machine before setting up the project:

* Python 3.8+  
* `pip` (Python package installer)  
* Git

---

## 🛠️ Installation & Setup

**1\. Clone the repository**

git clone https://github.com/your-username/your-repo-name.git

cd your-repo-name

**2\. Create a virtual environment** Isolate your project dependencies using a virtual environment to prevent conflicts.

\# On Windows

python \-m venv venv

\# On macOS/Linux

python3 \-m venv venv

**3\. Activate the virtual environment**

\# On Windows

venv\\Scripts\\activate

\# On macOS/Linux

source venv/bin/activate

**4\. Install dependencies** Install all required packages, including FastAPI and Uvicorn.

pip install \-r requirements.txt

**5\. Configure Environment Variables** Create a `.env` file in the root directory to store sensitive keys (e.g., database URIs, wearable API client secrets).

cp .env.example .env

*(Make sure to open the `.env` file and update it with your actual configuration values).*

---

## 💻 Running the Application

To start the local development server, open your terminal, ensure your virtual environment is active, and run Uvicorn:

uvicorn main:app \--reload

**Command Breakdown:**

* `uvicorn`: The ASGI server that runs the FastAPI framework.  
* `main`: Refers to the `main.py` file (your application's entry point).  
* `app`: The FastAPI instance created inside `main.py`.  
* `--reload`: Automatically restarts the server every time you save a code change (for development use only).

Once running, the API will be available at: **`http://127.0.0.1:8000`**

---

## 📖 API Documentation

FastAPI automatically generates interactive API documentation. While the server is running, you can explore and test your endpoints directly from your browser:

* **Swagger UI:** `http://127.0.0.1:8000/docs`  
* **ReDoc:** `http://127.0.0.1:8000/redoc`

### Example Endpoints

* `POST /api/v1/sensor-data`: Accepts physiological data payloads (PPG, GSR/EDA) from the mobile app or wearables.  
* `GET /api/v1/recommendations/{user_id}`: Returns a JSON list of recommended coping activities (games, social events) based on the latest stress calculations.

---

## 📱 Flutter Integration

To connect the Flutter mobile application to this local backend during development:

1. Ensure your mobile device or emulator is connected to the same Wi-Fi network as your development machine.  
2. Find your computer's local IPv4 address (e.g., `192.168.1.X`).  
3. Update the API base URL in your Dart/Flutter configuration to point to your machine's local IP address instead of `localhost`:  
   // Example configuration in Dart  
     
   const String baseUrl \= 'http://192.168.1.X:8000/api/v1';