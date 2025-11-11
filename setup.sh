#!/bin/bash

# Twitter Advanced Search Scraper Setup Script

echo "========================================="
echo "Twitter Advanced Search Scraper Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "✓ Python found: $python_version"
else
    echo "✗ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check pip
echo "Checking pip..."
pip_version=$(pip3 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "✓ pip found: $pip_version"
else
    echo "✗ pip not found. Please install pip."
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing requirements..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Requirements installed successfully"
else
    echo "✗ Failed to install requirements"
    exit 1
fi

# Check Chrome installation
echo ""
echo "Checking Chrome installation..."
if command -v google-chrome &> /dev/null; then
    chrome_version=$(google-chrome --version)
    echo "✓ Chrome found: $chrome_version"
elif command -v chromium &> /dev/null; then
    chromium_version=$(chromium --version)
    echo "✓ Chromium found: $chromium_version"
else
    echo "⚠ Chrome/Chromium not found"
    echo "  Please install Chrome from: https://www.google.com/chrome/"
fi

# Create output directory
echo ""
echo "Creating output directory..."
mkdir -p output
echo "✓ Output directory created"

# Check for cookies file
echo ""
if [ -f "twitter_cookies.json" ]; then
    echo "✓ Cookie file found: twitter_cookies.json"
else
    echo "⚠ Cookie file not found"
    echo "  For better results, export your Twitter cookies to twitter_cookies.json"
    echo "  See COOKIE_GUIDE.md for instructions"
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run example: python example_usage.py 1"
echo "3. Or customize config.py and run: python twitter_scraper.py"
echo ""
echo "For authentication (recommended):"
echo "- Export Twitter cookies (see COOKIE_GUIDE.md)"
echo "- Save as twitter_cookies.json in project directory"
echo ""
echo "Happy scraping! 🚀"
