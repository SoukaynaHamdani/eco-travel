@echo off
echo Starting EcoVoyage Morocco Application...
echo.

echo Starting Backend Server on port 8000...
start "Backend Server" cmd /k "cd /d %~dp0 && python -m uvicorn backend.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server on port 8080...
start "Frontend Server" cmd /k "cd /d %~dp0 && python -m http.server 8080 --directory frontend"

timeout /t 2 /nobreak >nul

echo.
echo Servers started!
echo Backend API: http://localhost:8000
echo Frontend App: http://localhost:8080
echo.
echo Opening application in browser...
timeout /t 2 /nobreak >nul
start http://localhost:8080

echo.
echo Press any key to exit this window (servers will keep running)...
pause >nul
