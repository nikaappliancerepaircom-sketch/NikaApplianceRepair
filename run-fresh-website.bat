@echo off
echo ========================================
echo Starting Nika Appliance Repair Website
echo ========================================
echo.
echo Opening website in your browser...
start http://localhost:8000
echo.
echo Starting server...
node server-fresh.js
pause