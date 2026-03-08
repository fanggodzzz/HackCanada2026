@echo off
echo Starting Backend Server (FastAPI)...

cd backend

.\venv\Scripts\python -m uvicorn main:app --reload --port 8000

pause