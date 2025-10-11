@echo off
echo ===================================
echo WORD COUNTER FOR NIKA PAGES
echo ===================================
echo.

if "%1"=="" (
    echo Usage: count-words.bat [filename]
    echo Example: count-words.bat brands\lg-appliance-repair-toronto.html
    echo.
    echo Or use shortcuts:
    echo   count-words.bat lg     - Counts LG brand page
    echo   count-words.bat samsung - Counts Samsung brand page
    echo   count-words.bat home    - Counts homepage
    echo.
    pause
    exit /b
)

set FILE=%1

REM Handle shortcuts
if "%1"=="lg" set FILE=brands\lg-appliance-repair-toronto.html
if "%1"=="samsung" set FILE=brands\samsung-appliance-repair.html
if "%1"=="whirlpool" set FILE=brands\whirlpool-appliance-repair.html
if "%1"=="home" set FILE=index.html
if "%1"=="homepage" set FILE=index.html

REM Check if file exists
if not exist "%FILE%" (
    echo ERROR: File not found: %FILE%
    echo.
    pause
    exit /b
)

REM Run the word counter
node tools\count-visible-words.js %FILE%

pause