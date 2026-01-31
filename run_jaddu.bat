@echo off
echo Starting Jaddu Voice Assistant...
set PY_PATH="C:\Users\Lenovo\AppData\Local\Programs\Python\Python314\python.exe"
echo Found Python at %PY_PATH%
%PY_PATH% -m pip install -r requirements.txt --default-timeout=100
if %errorlevel% neq 0 (
    echo.
    echo Network error detected. Retrying installation...
    %PY_PATH% -m pip install -r requirements.txt --default-timeout=100 --retries 10
)
%PY_PATH% main.py
pause
