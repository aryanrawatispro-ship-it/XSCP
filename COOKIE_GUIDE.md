# Twitter Cookie Export Guide

This guide explains how to export your Twitter cookies for use with the scraper.

## Why Use Cookies?

Using authentication cookies provides:
- Access to more tweets
- Better rate limits
- Full search functionality
- Reduced chance of being blocked

## Method 1: Using Browser Extension (Recommended)

### Chrome / Edge

1. **Install Extension:**
   - Visit Chrome Web Store
   - Search for "Get cookies.txt LOCALLY" or "EditThisCookie"
   - Install the extension

2. **Login to Twitter:**
   - Go to https://twitter.com
   - Log in to your account
   - Make sure you're fully logged in

3. **Export Cookies:**
   - Click the extension icon
   - Select "Export" or "Export as JSON"
   - Save the file as `twitter_cookies.json` in the project directory

### Firefox

1. **Install Extension:**
   - Visit Firefox Add-ons store
   - Search for "Cookie Quick Manager" or "Cookie Exporter"
   - Install the extension

2. **Login to Twitter:**
   - Go to https://twitter.com
   - Log in to your account

3. **Export Cookies:**
   - Click the extension icon
   - Find cookies for "twitter.com"
   - Export as JSON format
   - Save as `twitter_cookies.json`

## Method 2: Using Browser DevTools

### Chrome / Edge / Firefox

1. **Login to Twitter:**
   - Go to https://twitter.com
   - Log in to your account

2. **Open DevTools:**
   - Press `F12` or `Ctrl+Shift+I` (Windows/Linux)
   - Press `Cmd+Option+I` (Mac)

3. **Export Cookies:**
   - Go to "Application" tab (Chrome) or "Storage" tab (Firefox)
   - Expand "Cookies" in the left sidebar
   - Click on "https://twitter.com"
   - You'll see all cookies

4. **Copy Cookies:**
   - In the Console tab, paste this code:
   ```javascript
   copy(JSON.stringify(document.cookie.split('; ').map(c => {
     const [name, ...v] = c.split('=');
     return {
       name,
       value: v.join('='),
       domain: '.twitter.com',
       path: '/',
       secure: true,
       httpOnly: false,
       sameSite: 'None'
     };
   })))
   ```
   - This copies cookies to clipboard
   - Paste into a new file `twitter_cookies.json`

## Method 3: Using Python Script

Create a file `export_cookies.py`:

```python
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Setup Chrome
options = Options()
driver = webdriver.Chrome(options=options)

# Navigate to Twitter
driver.get("https://twitter.com")

# Manual login
print("Please log in to Twitter in the browser window...")
print("Press Enter after you've logged in...")
input()

# Get cookies
cookies = driver.get_cookies()

# Save to file
with open('twitter_cookies.json', 'w') as f:
    json.dump(cookies, f, indent=2)

print("Cookies saved to twitter_cookies.json")
driver.quit()
```

Run:
```bash
python export_cookies.py
```

## Cookie File Format

Your `twitter_cookies.json` should look like this:

```json
[
  {
    "name": "auth_token",
    "value": "1234567890abcdef...",
    "domain": ".twitter.com",
    "path": "/",
    "secure": true,
    "httpOnly": true,
    "sameSite": "None"
  },
  {
    "name": "ct0",
    "value": "abcdef1234567890...",
    "domain": ".twitter.com",
    "path": "/",
    "secure": true,
    "httpOnly": false,
    "sameSite": "Lax"
  }
]
```

## Important Cookies

The most important cookies for Twitter authentication:
- `auth_token` - Main authentication token
- `ct0` - CSRF token
- `twid` - Twitter ID

## Using Cookies with the Scraper

```python
from twitter_scraper import TwitterAdvancedScraper

config = {
    'cookies_file': 'twitter_cookies.json',  # Path to your cookie file
    'headless': False,
    'scroll_loops': 20,
}

scraper = TwitterAdvancedScraper(config)
scraper.run(
    keywords="your search",
    output_file="tweets.csv",
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

## Security Best Practices

### 1. Keep Cookies Private

**Never:**
- Commit cookies to Git repositories
- Share cookies with others
- Post cookies online
- Store in public locations

**Always:**
- Add `twitter_cookies.json` to `.gitignore`
- Store in secure location
- Use environment-specific cookies
- Rotate cookies regularly

### 2. Cookie Expiration

- Twitter cookies typically expire after 30-90 days
- If scraper fails to authenticate, export new cookies
- Check cookie expiration dates

### 3. Validate Cookies

Test if cookies work:

```python
from twitter_scraper import TwitterAdvancedScraper

config = {'cookies_file': 'twitter_cookies.json'}
scraper = TwitterAdvancedScraper(config)
scraper.setup_driver()
scraper.load_cookies('twitter_cookies.json')

# Navigate to Twitter
scraper.driver.get('https://twitter.com/home')

# If logged in, you should see your home timeline
input("Check if you're logged in. Press Enter to close...")
scraper.driver.quit()
```

## Troubleshooting

### Cookies not working

1. **Check cookie format:**
   - Must be valid JSON
   - Must include required fields
   - Check for syntax errors

2. **Re-export cookies:**
   - Clear browser cookies
   - Log in again
   - Export fresh cookies

3. **Verify authentication:**
   - Open browser with cookies loaded
   - Check if logged in to Twitter
   - Look for error messages

### Common Issues

**"Invalid cookie" errors:**
- Cookie format is incorrect
- Missing required fields
- Expired cookies

**"Not logged in" after loading cookies:**
- Cookies are expired
- Wrong domain (.twitter.com vs twitter.com)
- Missing auth_token or ct0

**Rate limiting even with cookies:**
- Twitter still has rate limits
- Use appropriate delays
- Don't abuse the API

## Alternative: Use Without Cookies

The scraper works without cookies, but:
- Limited number of results
- May hit rate limits faster
- Some tweets might not be accessible

```python
config = {
    'cookies_file': None,  # Don't use cookies
    'scroll_loops': 10,
}

scraper = TwitterAdvancedScraper(config)
scraper.run(...)
```

## Automated Cookie Refresh

For long-running scrapers, implement cookie refresh:

```python
import schedule
import time

def refresh_cookies():
    """Re-export cookies periodically"""
    print("Time to refresh cookies!")
    # Manual process or automated login

# Refresh cookies every 30 days
schedule.every(30).days.do(refresh_cookies)

while True:
    schedule.run_pending()
    time.sleep(86400)  # Check daily
```

## Legal & Ethical Considerations

- **Terms of Service:** Using cookies may violate Twitter's ToS
- **Account Safety:** Your account could be suspended
- **Data Privacy:** Don't scrape private/protected accounts
- **Fair Use:** Use for research, not commercial purposes

**Recommendation:**
- Use cookies from a dedicated research account
- Don't use your main personal account
- Understand the risks involved

---

**Note:** Cookie-based authentication is a gray area. Use responsibly and at your own risk.
