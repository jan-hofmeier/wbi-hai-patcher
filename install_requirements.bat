@echo off
setlocal EnableExtensions

python -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo.
    echo An error occurred during installation.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Dependencies installed successfully.
pause
