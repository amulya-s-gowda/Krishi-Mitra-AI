@echo off
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
  echo Virtual environment not found.
  echo First create it with: py -3.13 -m venv venv
  echo Then activate it and run: pip install -r requirements.txt
  pause
  exit /b 1
)
call "venv\Scripts\activate.bat"
streamlit run app.py --server.port 8511
pause
