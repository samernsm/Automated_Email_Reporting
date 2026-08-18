@echo off

echo Starting Automated Email Reporting...
echo.

cd /d C:\training\Automated_Email_Reporting

call .venv\Scripts\activate.bat

python src\main.py

echo.
echo ========================================
echo Process finished.
echo ========================================
echo.

pause