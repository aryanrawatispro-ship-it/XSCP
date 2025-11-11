# Quick Start Guide

Get started with Twitter Advanced Search Scraper in 5 minutes!

## Installation (Choose One)

### Option 1: Automated Setup (Linux/Mac)

```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

### Option 2: Automated Setup (Windows)

```cmd
setup.bat
venv\Scripts\activate.bat
```

### Option 3: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### Option 4: Docker

```bash
# Build and run
docker-compose up --build

# Or manually
docker build -t twitter-scraper .
docker run -v $(pwd)/output:/app/output twitter-scraper
```

## First Run

### Example 1: Simple Search

```python
from twitter_scraper import TwitterAdvancedScraper

config = {
    'headless': False,
    'scroll_loops': 10,
}

scraper = TwitterAdvancedScraper(config)

scraper.run(
    keywords="Python programming",
    output_file="python_tweets.csv",
    start_date="2024-01-01",
    end_date="2024-01-31",
    max_tweets=100
)
```

Save as `my_scraper.py` and run:
```bash
python my_scraper.py
```

### Example 2: Run Pre-built Examples

```bash
# Simple search
python example_usage.py 1

# Search with filters
python example_usage.py 2

# Time-splitting mode
python example_usage.py 4
```

## Basic Configuration

Edit `config.py` to set defaults:

```python
SCRAPER_CONFIG = {
    'headless': False,      # Set True for cloud/headless
    'scroll_loops': 20,     # More loops = more tweets
    'page_load_wait': 5,    # Wait time in seconds
}

SEARCH_PARAMS = {
    'keywords': 'your keywords here',
    'start_date': '2024-01-01',
    'end_date': '2024-01-31',
    'search_type': 'Latest',  # or 'Top'
}
```

## Common Use Cases

### 1. Brand Monitoring

```python
scraper.run(
    keywords="gensyn OR Gensyn OR @gensyn",
    start_date="2024-01-01",
    end_date="2024-01-31",
    min_likes=10,
    exclude_replies=True,
    max_tweets=1000
)
```

### 2. Trend Analysis

```python
scraper.run(
    keywords="#AI OR #MachineLearning",
    start_date="2024-01-01",
    end_date="2024-01-07",
    min_likes=100,
    search_type="Top",
    max_tweets=500
)
```

### 3. Competitor Research

```python
scraper.run(
    keywords="@competitor1 OR @competitor2",
    start_date="2024-01-01",
    end_date="2024-12-31",
    min_likes=50,
    exclude_replies=False,
    max_tweets=2000
)
```

### 4. Large Date Range (Time-Splitting)

```python
scraper.run(
    keywords="cryptocurrency",
    output_file="crypto_tweets.csv",
    use_time_splitting=True,
    start_date="2024-01-01",
    end_date="2024-12-31",
    split_mode="week",
    min_likes=20,
    max_tweets=5000
)
```

## Output

Results are saved as CSV files:

```csv
tweet_id,tweet_url,username,display_name,text,timestamp,likes,retweets,replies,views,media_urls
1234567890,https://twitter.com/user/status/1234567890,@user,Display Name,Tweet text here,2024-01-15T10:30:00.000Z,150,25,10,5000,https://...
```

Open with:
- Excel / Google Sheets
- Pandas: `pd.read_csv('tweets.csv')`
- Any CSV reader

## Authentication (Optional but Recommended)

For better results, use Twitter cookies:

1. **Export cookies** (see `COOKIE_GUIDE.md`)
2. **Save as** `twitter_cookies.json`
3. **Update config:**

```python
config = {
    'cookies_file': 'twitter_cookies.json',
    'scroll_loops': 20,
}
```

## Troubleshooting

### Chrome not found
```bash
# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

### No tweets found
- Check date range has tweets
- Remove engagement filters
- Verify keywords are correct
- Use cookies for authentication

### Slow performance
```python
config = {
    'headless': True,      # Enable headless mode
    'scroll_loops': 10,    # Reduce scroll loops
}
```

### Rate limiting
```python
config = {
    'request_delay': 5,    # Increase delay
    'scroll_loops': 5,     # Reduce loops
}
```

## Next Steps

1. **Read full documentation:** See `README.md`
2. **Export cookies:** See `COOKIE_GUIDE.md`
3. **Try examples:** Run `example_usage.py`
4. **Customize:** Edit `config.py`
5. **Deploy:** Use Docker for cloud deployment

## Quick Reference

### Keyword Syntax

```python
# OR operator
keywords = "bitcoin OR ethereum"

# Exact phrase
keywords = '"machine learning"'

# Exclude words
keywords = "crypto -scam -spam"

# Combine
keywords = '(AI OR "machine learning") python -tutorial'
```

### Date Formats

```python
start_date = "2024-01-01"  # YYYY-MM-DD
end_date = "2024-12-31"
```

### Search Types

```python
search_type = "Latest"  # Recent tweets
search_type = "Top"     # Popular tweets
```

### Engagement Filters

```python
min_likes = 100      # Minimum likes
min_retweets = 50    # Minimum retweets
min_replies = 10     # Minimum replies
```

### Languages

```python
lang = "en"    # English
lang = "es"    # Spanish
lang = "fr"    # French
```

## Support

- **Issues:** Check `README.md` troubleshooting section
- **Examples:** See `example_usage.py`
- **Cookies:** See `COOKIE_GUIDE.md`
- **Documentation:** See `README.md`

---

**Happy Scraping! 🚀**

Need help? Check the full `README.md` for detailed documentation.
