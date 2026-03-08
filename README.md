# Skin Scan AI

This is a full-stack application for detecting skin diseases using AI. It contains a data collector, FastAPI backend, and React frontend.

## Initial Setup

Each folder backend, frontend, and model needs inital set up. You can run the setting up by ruing the script `setup.bat`

## How to Run Locally

You can run the application components using the convenient batch scripts provided in the root directory, or by running the commands manually in your terminal.

### 1. Data Collection & Training AI

This script pulls sample images for the AI model from DuckDuckGo.
**Using the script:** Double-click `collect_data.bat`
**Using terminal:**

```powershell
python model\data_collector.py
```

Then trains the AI based on collected data.
**Using the script:** Double-click `train_model.bat`
**Using terminal:**

```powershell
python model\train_model.py
```

### 2. Start Backend Server

The backend requires its Python virtual environment to access all dependencies.
**Using the script:** Double-click `start_backend.bat`
**Using terminal:**

```powershell
.\venv\Scripts\python -m uvicorn backend.main:app --reload --port 8000
```

- The API will be available at [http://localhost:8000](http://localhost:8000)
- Swagger Documentation available at [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Start Frontend GUI

The frontend is a React application powered by Vite.
**Using the script:** Double-click `start_frontend.bat`
**Using terminal:**

```powershell
cd frontend
npm run dev
```

- The GUI will typically be available at [http://localhost:5173](http://localhost:5173) or [http://localhost:5174](http://localhost:5174) depending on port availability.
