@echo off
REM Twitter Advanced Search Scraper Setup Script for Windows

echo =========================================
echo Twitter Advanced Search Scraper Setup
echo =========================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo OK Python found
) else (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check pip
echo Checking pip...
pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo OK pip found
) else (
    echo ERROR: pip not found. Please install pip.
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo OK Virtual environment created
) else (
    echo OK Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing requirements...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo OK Requirements installed successfully
) else (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

REM Check Chrome installation
echo.
echo Checking Chrome installation...
where chrome >nul 2>&1
if %errorlevel% equ 0 (
    echo OK Chrome found
) else (
    echo WARNING: Chrome not found
    echo Please install Chrome from: https://www.google.com/chrome/
)

REM Create output directory
echo.
echo Creating output directory...
if not exist "output" mkdir output
echo OK Output directory created

REM Check for cookies file
echo.
if exist "twitter_cookies.json" (
    echo OK Cookie file found: twitter_cookies.json
) else (
    echo WARNING: Cookie file not found
    echo For better results, export your Twitter cookies to twitter_cookies.json
    echo See COOKIE_GUIDE.md for instructions
)

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Run example: python example_usage.py 1
echo 3. Or customize config.py and run: python twitter_scraper.py
echo.
echo For authentication (recommended):
echo - Export Twitter cookies (see COOKIE_GUIDE.md)
echo - Save as twitter_cookies.json in project directory
echo.
echo Happy scraping! 🚀
echo.
pause
