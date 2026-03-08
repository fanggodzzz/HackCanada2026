@echo off
echo ====================================
echo AI PROJECT AUTOMATIC SETUP
echo ====================================

echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python first.
    pause
    exit /b
)

echo.
echo Checking Node.js installation...
node -v
if %errorlevel% neq 0 (
    echo Node.js is not installed. Please install Node.js first.
    pause
    exit /b
)

echo.
echo ================================
echo Setting up BACKEND
echo ================================
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing backend dependencies...
pip install -r requirements.txt

cd ..

echo.
echo ================================
echo Setting up MODEL
echo ================================
cd model

echo Installing model dependencies...
pip install -r requirements.txt

cd ..

echo.
echo ================================
echo Setting up FRONTEND
echo ================================
cd frontend

echo Installing frontend dependencies...
npm install

cd ..

echo.
echo ====================================
echo SETUP COMPLETE
echo ====================================

echo.
echo To start the project:

echo 1. Run backend:
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn main:app --reload

echo.
echo 2. Run frontend:
echo    cd frontend
echo    npm run dev

echo.
pause