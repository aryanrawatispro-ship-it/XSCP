# VPS Deployment Guide

Complete guide for deploying the Twitter Advanced Search Scraper on a VPS (Virtual Private Server).

## Table of Contents

1. [VPS Provider Setup](#vps-provider-setup)
2. [Initial Server Configuration](#initial-server-configuration)
3. [Installing Dependencies](#installing-dependencies)
4. [Deploying the Scraper](#deploying-the-scraper)
5. [Running in Production](#running-in-production)
6. [Scheduling with Cron](#scheduling-with-cron)
7. [Managing Cookies on VPS](#managing-cookies-on-vps)
8. [Monitoring & Logs](#monitoring--logs)
9. [Security Best Practices](#security-best-practices)
10. [Troubleshooting](#troubleshooting)

---

## VPS Provider Setup

### Recommended VPS Providers

| Provider | Starting Price | Pros |
|----------|---------------|------|
| **DigitalOcean** | $6/month | Easy to use, great documentation |
| **Vultr** | $6/month | Good performance, multiple locations |
| **Linode** | $5/month | Reliable, good support |
| **AWS EC2** | Variable | Scalable, free tier available |
| **Hetzner** | €4/month | Very affordable, good specs |

### Minimum Requirements

```
CPU:     2 cores (recommended)
RAM:     2 GB (minimum), 4 GB (recommended)
Storage: 20 GB SSD
OS:      Ubuntu 22.04 LTS or 24.04 LTS (recommended)
```

### Creating a VPS

**DigitalOcean Example:**
1. Sign up at digitalocean.com
2. Click "Create" → "Droplets"
3. Choose Ubuntu 22.04 LTS
4. Select Basic plan ($12/month for 2GB RAM recommended)
5. Choose datacenter region
6. Add SSH key (recommended) or use password
7. Click "Create Droplet"

**AWS EC2 Example:**
1. Sign up at aws.amazon.com
2. Navigate to EC2 Dashboard
3. Click "Launch Instance"
4. Select Ubuntu 22.04 LTS
5. Choose t2.small or t3.small instance type
6. Configure security group (SSH port 22)
7. Create/select key pair
8. Launch instance

---

## Initial Server Configuration

### Step 1: Connect to Your VPS

```bash
# Replace with your VPS IP address
ssh root@YOUR_VPS_IP

# Or if using a key pair
ssh -i your-key.pem ubuntu@YOUR_VPS_IP
```

### Step 2: Update System

```bash
# Update package list
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl wget git unzip software-properties-common
```

### Step 3: Create Non-Root User (Optional but Recommended)

```bash
# Create new user
adduser scraper

# Add to sudo group
usermod -aG sudo scraper

# Switch to new user
su - scraper
```

### Step 4: Set Up Firewall (Optional)

```bash
# Install UFW
sudo apt install -y ufw

# Allow SSH
sudo ufw allow 22

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

## Installing Dependencies

### Step 1: Install Python 3.11

```bash
# Add deadsnakes PPA for latest Python
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Install pip
sudo apt install -y python3-pip

# Verify installation
python3.11 --version
```

### Step 2: Install Chrome

```bash
# Download Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install Chrome
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# Verify installation
google-chrome --version

# Clean up
rm google-chrome-stable_current_amd64.deb
```

### Step 3: Install ChromeDriver

```bash
# Get latest ChromeDriver version
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)

# Download ChromeDriver
wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip

# Unzip
unzip chromedriver_linux64.zip

# Move to /usr/local/bin
sudo mv chromedriver /usr/local/bin/

# Make executable
sudo chmod +x /usr/local/bin/chromedriver

# Verify installation
chromedriver --version

# Clean up
rm chromedriver_linux64.zip
```

**Alternative: Automatic ChromeDriver Management**

The scraper uses `webdriver-manager` which automatically downloads and manages ChromeDriver. You can skip manual ChromeDriver installation if you prefer.

### Step 4: Install Additional Dependencies

```bash
# Install required system libraries
sudo apt install -y \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libcups2 \
    libxss1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0
```

---

## Deploying the Scraper

### Step 1: Clone Repository

```bash
# Navigate to home directory
cd ~

# Clone the repository
git clone https://github.com/your-username/XSCP.git

# Navigate to project directory
cd XSCP
```

### Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 3: Configure for Headless Mode

Edit `config.py`:

```bash
nano config.py
```

Change the following:

```python
SCRAPER_CONFIG = {
    'headless': True,  # IMPORTANT: Set to True for VPS
    'scroll_loops': 20,
    'page_load_wait': 5,
    'request_delay': 2,
}
```

Save and exit (Ctrl+X, Y, Enter).

### Step 4: Test Installation

```bash
# Run test script
python test_setup.py

# Should see all tests pass
```

---

## Running in Production

### Method 1: Direct Execution

```bash
# Activate virtual environment
cd ~/XSCP
source venv/bin/activate

# Run scraper
python example_usage.py 7  # Headless mode example

# Or run custom script
python my_scraper.py
```

### Method 2: Using Screen (Keep Running After Disconnect)

```bash
# Install screen
sudo apt install -y screen

# Create new screen session
screen -S twitter-scraper

# Run your scraper
cd ~/XSCP
source venv/bin/activate
python example_usage.py 7

# Detach from screen: Press Ctrl+A, then D

# List screens
screen -ls

# Reattach to screen
screen -r twitter-scraper

# Kill screen session
screen -X -S twitter-scraper quit
```

### Method 3: Using Tmux

```bash
# Install tmux
sudo apt install -y tmux

# Create new tmux session
tmux new -s scraper

# Run your scraper
cd ~/XSCP
source venv/bin/activate
python example_usage.py 7

# Detach: Press Ctrl+B, then D

# List sessions
tmux ls

# Reattach
tmux attach -t scraper

# Kill session
tmux kill-session -t scraper
```

### Method 4: Using systemd Service

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/twitter-scraper.service
```

Add the following:

```ini
[Unit]
Description=Twitter Advanced Search Scraper
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/XSCP
Environment="PATH=/home/your-username/XSCP/venv/bin"
ExecStart=/home/your-username/XSCP/venv/bin/python example_usage.py 7
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable twitter-scraper

# Start service
sudo systemctl start twitter-scraper

# Check status
sudo systemctl status twitter-scraper

# View logs
sudo journalctl -u twitter-scraper -f
```

---

## Scheduling with Cron

### Daily Scraping Example

```bash
# Open crontab
crontab -e

# Add cron job to run daily at 2 AM
0 2 * * * cd /home/your-username/XSCP && /home/your-username/XSCP/venv/bin/python example_usage.py 7 >> /home/your-username/XSCP/logs/cron.log 2>&1

# Or run every 6 hours
0 */6 * * * cd /home/your-username/XSCP && /home/your-username/XSCP/venv/bin/python my_scraper.py >> /home/your-username/XSCP/logs/cron.log 2>&1
```

### Create Cron Script

Create `run_scraper.sh`:

```bash
nano ~/XSCP/run_scraper.sh
```

Add:

```bash
#!/bin/bash

# Navigate to project directory
cd /home/your-username/XSCP

# Activate virtual environment
source venv/bin/activate

# Run scraper
python example_usage.py 7

# Optional: Send notification when done
echo "Scraper completed at $(date)" | mail -s "Twitter Scraper" your-email@example.com
```

Make executable:

```bash
chmod +x ~/XSCP/run_scraper.sh
```

Add to cron:

```bash
# Run daily at 2 AM
0 2 * * * /home/your-username/XSCP/run_scraper.sh >> /home/your-username/XSCP/logs/cron.log 2>&1
```

### Cron Time Examples

```bash
# Every day at 2 AM
0 2 * * *

# Every 6 hours
0 */6 * * *

# Every Monday at 9 AM
0 9 * * 1

# First day of month at midnight
0 0 1 * *

# Every 30 minutes
*/30 * * * *
```

---

## Managing Cookies on VPS

### Option 1: Upload from Local Machine

```bash
# From your local machine, copy cookies to VPS
scp twitter_cookies.json root@YOUR_VPS_IP:/home/your-username/XSCP/

# Or using rsync
rsync -avz twitter_cookies.json root@YOUR_VPS_IP:/home/your-username/XSCP/
```

### Option 2: Export Directly on VPS (with GUI)

**Not recommended** - VPS typically doesn't have GUI. Use Option 1 or 3.

### Option 3: Use Cookie String

Create a Python script to convert cookie string to JSON:

```python
# save_cookies.py
import json

cookies_string = "your_cookie_string_here"

cookies = []
for cookie in cookies_string.split('; '):
    name, value = cookie.split('=', 1)
    cookies.append({
        'name': name,
        'value': value,
        'domain': '.twitter.com',
        'path': '/',
        'secure': True,
        'httpOnly': False,
        'sameSite': 'None'
    })

with open('twitter_cookies.json', 'w') as f:
    json.dump(cookies, f, indent=2)

print("Cookies saved!")
```

### Option 4: Secure Cookie Storage

Use environment variables or encrypted storage:

```bash
# Install encryption tool
pip install cryptography

# Create encrypted cookies
python -c "
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(f'Encryption key: {key.decode()}')
"

# Save key to .env file
echo "COOKIE_KEY=your-encryption-key" > .env
```

### Security Tips for Cookies

1. **Never commit cookies to Git**
   ```bash
   # Verify .gitignore includes cookies
   cat .gitignore | grep cookies
   ```

2. **Restrict file permissions**
   ```bash
   chmod 600 twitter_cookies.json
   ```

3. **Use environment variables**
   ```bash
   # Store in environment
   export TWITTER_COOKIES="/secure/path/twitter_cookies.json"
   ```

4. **Rotate cookies regularly**
   - Export new cookies every 30 days
   - Monitor for auth failures

---

## Monitoring & Logs

### Create Logs Directory

```bash
mkdir -p ~/XSCP/logs
```

### Configure Logging

Edit your scraper to log to file:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler()
    ]
)
```

### View Logs

```bash
# View latest logs
tail -f ~/XSCP/logs/scraper.log

# View last 100 lines
tail -n 100 ~/XSCP/logs/scraper.log

# Search for errors
grep ERROR ~/XSCP/logs/scraper.log

# View logs by date
grep "2024-01-15" ~/XSCP/logs/scraper.log
```

### Log Rotation

Install logrotate:

```bash
sudo nano /etc/logrotate.d/twitter-scraper
```

Add:

```
/home/your-username/XSCP/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0644 your-username your-username
}
```

### Monitor Disk Space

```bash
# Check disk usage
df -h

# Check project directory size
du -sh ~/XSCP

# Check output CSV size
du -sh ~/XSCP/*.csv

# Clean old CSVs
find ~/XSCP -name "*.csv" -mtime +30 -delete
```

### Set Up Email Alerts

```bash
# Install mail utilities
sudo apt install -y mailutils

# Configure mail (optional)
sudo dpkg-reconfigure postfix

# Test email
echo "Test message" | mail -s "Test" your-email@example.com
```

Add to your scraper script:

```bash
# In run_scraper.sh
if [ $? -eq 0 ]; then
    echo "Scraper completed successfully" | mail -s "✓ Scraper Success" your@email.com
else
    echo "Scraper failed" | mail -s "✗ Scraper Failed" your@email.com
fi
```

---

## Security Best Practices

### 1. Use SSH Keys (Not Passwords)

```bash
# On your local machine, generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to VPS
ssh-copy-id root@YOUR_VPS_IP

# Disable password authentication on VPS
sudo nano /etc/ssh/sshd_config

# Set: PasswordAuthentication no
# Restart SSH
sudo systemctl restart sshd
```

### 2. Keep System Updated

```bash
# Create update script
nano ~/update.sh
```

Add:

```bash
#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
```

Make executable and run weekly:

```bash
chmod +x ~/update.sh
```

Add to cron:

```bash
# Update every Sunday at 3 AM
0 3 * * 0 /home/your-username/update.sh
```

### 3. Secure File Permissions

```bash
# Restrict scraper directory
chmod 750 ~/XSCP

# Restrict cookies
chmod 600 ~/XSCP/twitter_cookies.json

# Restrict output CSVs
chmod 600 ~/XSCP/*.csv
```

### 4. Use Fail2Ban (Prevent Brute Force)

```bash
# Install fail2ban
sudo apt install -y fail2ban

# Configure
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local

# Enable for SSH
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Check status
sudo fail2ban-client status sshd
```

### 5. Backup Your Data

```bash
# Create backup script
nano ~/backup.sh
```

Add:

```bash
#!/bin/bash
BACKUP_DIR="/home/your-username/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup CSVs
tar -czf $BACKUP_DIR/tweets_$DATE.tar.gz ~/XSCP/*.csv

# Keep only last 7 days
find $BACKUP_DIR -name "tweets_*.tar.gz" -mtime +7 -delete
```

Schedule backups:

```bash
# Daily at 1 AM
0 1 * * * /home/your-username/backup.sh
```

---

## Troubleshooting

### Issue 1: Chrome Crashes on VPS

**Symptoms:** "Chrome crashed" or "Session deleted" errors

**Solutions:**

```bash
# Increase shared memory
sudo mount -o remount,size=2G /dev/shm

# Or add to /etc/fstab
echo "tmpfs /dev/shm tmpfs defaults,size=2g 0 0" | sudo tee -a /etc/fstab
```

Or disable dev-shm in Chrome options:

```python
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
```

### Issue 2: Memory Issues

**Symptoms:** OOM (Out of Memory) errors

**Solutions:**

```bash
# Check memory usage
free -h

# Add swap space (4GB example)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Verify
free -h
```

Or reduce scroll loops:

```python
config = {
    'scroll_loops': 5,  # Reduce from 20
}
```

### Issue 3: Display Issues in Headless Mode

**Symptoms:** "Display not found" errors

**Solutions:**

```bash
# Install Xvfb (Virtual Display)
sudo apt install -y xvfb

# Run with Xvfb
xvfb-run python example_usage.py 7

# Or in script
#!/bin/bash
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
python example_usage.py 7
```

### Issue 4: ChromeDriver Version Mismatch

**Symptoms:** "Chrome version mismatch" errors

**Solution 1: Use webdriver-manager (automatic)**

Already included in requirements.txt - it auto-updates ChromeDriver.

**Solution 2: Manual update**

```bash
# Check Chrome version
google-chrome --version

# Download matching ChromeDriver
# Visit: https://chromedriver.chromium.org/downloads

# Replace old driver
sudo rm /usr/local/bin/chromedriver
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

### Issue 5: Permission Denied Errors

```bash
# Fix ownership
sudo chown -R your-username:your-username ~/XSCP

# Fix permissions
chmod -R 755 ~/XSCP
chmod 600 ~/XSCP/twitter_cookies.json
```

### Issue 6: Cron Jobs Not Running

```bash
# Check cron logs
grep CRON /var/log/syslog

# Verify crontab
crontab -l

# Test script manually
/home/your-username/XSCP/run_scraper.sh

# Check permissions
chmod +x /home/your-username/XSCP/run_scraper.sh

# Use absolute paths in crontab
```

### Issue 7: Network/Timeout Errors

```bash
# Increase timeout in scraper
config = {
    'page_load_wait': 10,  # Increase from 5
    'request_delay': 5,    # Increase delay
}

# Check network connectivity
ping -c 4 twitter.com
curl -I https://twitter.com
```

---

## Performance Optimization

### 1. Use SSD Storage

Ensure your VPS uses SSD storage (most modern VPS providers do).

### 2. Optimize Chrome Options

```python
chrome_options.add_argument('--disable-images')  # Don't load images
chrome_options.add_argument('--disable-javascript')  # If not needed
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
```

### 3. Parallel Scraping

Run multiple scrapers for different keywords:

```python
# scraper1.py - Bitcoin
# scraper2.py - Ethereum
# scraper3.py - DeFi
```

Use screen/tmux sessions:

```bash
screen -S bitcoin -d -m python scraper1.py
screen -S ethereum -d -m python scraper2.py
screen -S defi -d -m python scraper3.py
```

### 4. Database Storage (Instead of CSV)

For large datasets, use SQLite or PostgreSQL:

```bash
sudo apt install -y postgresql
```

### 5. Monitor Resource Usage

```bash
# Install htop
sudo apt install -y htop

# Monitor resources
htop

# Check Chrome processes
ps aux | grep chrome
```

---

## Complete Deployment Example

### End-to-End Setup Script

Create `vps_deploy.sh`:

```bash
#!/bin/bash

echo "========================================="
echo "Twitter Scraper VPS Deployment"
echo "========================================="

# Update system
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "Installing dependencies..."
sudo apt install -y curl wget git unzip python3.11 python3.11-venv python3-pip

# Install Chrome
echo "Installing Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

# Install system libraries
sudo apt install -y libnss3 libgconf-2-4 libfontconfig1 libx11-xcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libcups2 \
    libxss1 libxrandr2 libasound2 libpangocairo-1.0-0 libatk1.0-0 \
    libatk-bridge2.0-0 libgtk-3-0

# Clone repository
echo "Cloning repository..."
cd ~
git clone https://github.com/your-username/XSCP.git
cd XSCP

# Set up virtual environment
echo "Setting up virtual environment..."
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configure for headless
echo "Configuring for headless mode..."
sed -i "s/'headless': False/'headless': True/" config.py

# Create directories
mkdir -p logs output backups

# Test installation
echo "Testing installation..."
python test_setup.py

echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo "Next steps:"
echo "1. Upload cookies: scp twitter_cookies.json user@vps:~/XSCP/"
echo "2. Run scraper: cd ~/XSCP && source venv/bin/activate && python example_usage.py 7"
echo "3. Set up cron: crontab -e"
```

Run on VPS:

```bash
chmod +x vps_deploy.sh
./vps_deploy.sh
```

---

## Summary Checklist

- [ ] VPS created with Ubuntu 22.04/24.04
- [ ] Initial server configuration completed
- [ ] Python 3.11 installed
- [ ] Chrome and ChromeDriver installed
- [ ] Repository cloned and dependencies installed
- [ ] Config set to headless mode
- [ ] Test script passed
- [ ] Cookies uploaded (if using authentication)
- [ ] Scraper tested successfully
- [ ] Cron job scheduled (if needed)
- [ ] Logging configured
- [ ] Security measures implemented
- [ ] Backup strategy in place

---

## Support

For VPS-specific issues:
- Check provider documentation
- Review system logs: `sudo journalctl -xe`
- Monitor resources: `htop`
- Check scraper logs: `tail -f logs/scraper.log`

**Happy scraping on your VPS! 🚀**
