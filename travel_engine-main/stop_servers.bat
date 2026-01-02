@echo off
echo Stopping all Python servers...

REM Kill all python.exe processes
taskkill /F /IM python.exe 2>nul

if %errorlevel% == 0 (
    echo All servers stopped successfully.
) else (
    echo No servers were running.
)

echo.
pause
