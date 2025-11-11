# Twitter Advanced Search Scraper

A powerful Python-based Twitter scraper that replicates Octoparse functionality for scraping tweets using Twitter's Advanced Search. Built with Selenium for robust web automation and data extraction.

## Features

### Core Functionality
- ✅ **Advanced Search Support**: Full Twitter Advanced Search URL structure
- ✅ **Keyword Filtering**: Support for ANY, ALL, NONE, and exact phrase matching
- ✅ **Date Range Filtering**: Scrape tweets within specific date ranges
- ✅ **Engagement Filters**: Filter by minimum likes, replies, and retweets
- ✅ **Language Filtering**: Restrict results to specific languages
- ✅ **Time-Splitting Modes**: Split large date ranges by day/week/month for better coverage
- ✅ **Auto-Scroll**: Infinite scroll to capture all available tweets
- ✅ **Authentication Support**: Load Twitter cookies for full access

### Data Extraction
- Tweet text/content
- Author username and display name
- Tweet URL and unique ID
- Timestamp (posted date/time)
- Engagement metrics (likes, retweets, replies, views)
- Media URLs (images and videos)

### Technical Features
- Selenium WebDriver with Chrome
- Configurable wait times for AJAX loading
- Auto-scroll with customizable loop count
- CSV export with all data fields
- Error handling and rate limiting
- Headless mode for cloud deployment
- Duplicate tweet detection

## Installation

### Prerequisites
- Python 3.8 or higher
- Chrome browser installed
- ChromeDriver (automatically managed by webdriver-manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd XSCP
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python -c "from selenium import webdriver; print('Selenium installed successfully')"
   ```

## Quick Start

### Basic Usage

```python
from twitter_scraper import TwitterAdvancedScraper

# Configure the scraper
config = {
    'headless': False,        # Set to True for headless mode
    'scroll_loops': 10,       # Number of scroll iterations
    'page_load_wait': 5,      # Wait time after page load (seconds)
    'request_delay': 2,       # Delay between requests
}

# Initialize scraper
scraper = TwitterAdvancedScraper(config)

# Run a simple search
scraper.run(
    keywords="gensyn OR Gensyn OR GENSYN",
    output_file="gensyn_tweets.csv",
    start_date="2024-01-01",
    end_date="2024-01-31",
    min_likes=10,
    search_type="Latest",
    exclude_replies=True,
    max_tweets=500
)
```

### Running Examples

The project includes multiple example scripts demonstrating different use cases:

```bash
# Run example 1: Simple search
python example_usage.py 1

# Run example 2: Search with engagement filters
python example_usage.py 2

# Run example 4: Time-splitting mode
python example_usage.py 4
```

## Configuration

### Scraper Configuration

Edit `config.py` to customize scraper behavior:

```python
SCRAPER_CONFIG = {
    'headless': False,          # Run browser in headless mode
    'scroll_loops': 20,         # Number of scroll iterations
    'page_load_wait': 5,        # Wait after page load (seconds)
    'request_delay': 2,         # Delay between requests (seconds)
    'cookies_file': None,       # Path to Twitter cookies JSON
}
```

### Search Parameters

```python
# Keywords - supports Boolean operators
keywords = "gensyn OR Gensyn OR GENSYN"
keywords = '"exact phrase"'
keywords = "(bitcoin OR ethereum) -scam"

# Date range
start_date = "2024-01-01"    # Format: YYYY-MM-DD
end_date = "2024-01-31"

# Engagement filters
min_likes = 10               # Minimum likes
min_replies = 5              # Minimum replies
min_retweets = 3             # Minimum retweets

# Other filters
lang = "en"                  # Language code
search_type = "Latest"       # "Latest" or "Top"
exclude_replies = True       # Exclude reply tweets
max_tweets = 500             # Maximum tweets to scrape
```

## Advanced Features

### 1. Time-Splitting Mode

For large date ranges, use time-splitting to scrape data in smaller chunks:

```python
scraper.run(
    keywords="cryptocurrency",
    output_file="crypto_tweets.csv",
    use_time_splitting=True,
    start_date="2024-01-01",
    end_date="2024-03-31",
    split_mode="week",      # 'day', 'week', or 'month'
    min_likes=20,
    max_tweets=1000
)
```

**Benefits:**
- Better coverage for popular keywords
- Avoids Twitter's result limits
- More reliable for long date ranges

### 2. Authentication with Cookies

For full access to Twitter (recommended for better results):

1. **Export cookies from your browser:**
   - Install a cookie export extension (e.g., "Get cookies.txt LOCALLY")
   - Visit twitter.com and log in
   - Export cookies as JSON format
   - Save as `twitter_cookies.json`

2. **Use cookies in scraper:**
   ```python
   config = {
       'cookies_file': 'twitter_cookies.json',
       'scroll_loops': 20,
   }

   scraper = TwitterAdvancedScraper(config)
   scraper.run(...)
   ```

### 3. Headless Mode (Cloud Deployment)

Run the scraper without a visible browser window:

```python
config = {
    'headless': True,
    'scroll_loops': 10,
}

scraper = TwitterAdvancedScraper(config)
scraper.run(...)
```

**Use cases:**
- Cloud servers (AWS, GCP, Azure)
- Scheduled tasks/cron jobs
- Docker containers

### 4. Keyword Combinations

Twitter Advanced Search supports powerful keyword syntax:

```python
# OR operator - match any keyword
keywords = "bitcoin OR ethereum OR crypto"

# Exact phrase - use quotes
keywords = '"machine learning" "artificial intelligence"'

# Exclude keywords - use minus sign
keywords = "crypto -scam -spam"

# Complex combinations
keywords = '(python OR "machine learning") -tutorial'
```

## Output Format

The scraper exports data to CSV with the following columns:

| Column | Description |
|--------|-------------|
| `tweet_id` | Unique tweet identifier |
| `tweet_url` | Direct URL to the tweet |
| `username` | Author's username (@handle) |
| `display_name` | Author's display name |
| `text` | Full tweet text content |
| `timestamp` | ISO format timestamp |
| `likes` | Number of likes |
| `retweets` | Number of retweets |
| `replies` | Number of replies |
| `views` | Number of views (if available) |
| `media_urls` | Comma-separated media URLs |

Example CSV output:
```csv
tweet_id,tweet_url,username,display_name,text,timestamp,likes,retweets,replies,views,media_urls
1234567890,https://twitter.com/user/status/1234567890,@user,Display Name,Tweet text here,2024-01-15T10:30:00.000Z,150,25,10,5000,https://pbs.twimg.com/media/image.jpg
```

## Rate Limiting & Best Practices

### Avoid Rate Limiting

1. **Use appropriate delays:**
   ```python
   config = {
       'page_load_wait': 5,    # Wait for page to load
       'request_delay': 3,     # Delay between requests
       'scroll_loops': 10,     # Don't scroll too aggressively
   }
   ```

2. **Use time-splitting for large datasets:**
   - Split by day for very active keywords
   - Split by week for moderate activity
   - Split by month for low activity

3. **Use cookies for authentication:**
   - Better rate limits when logged in
   - Access to more results

### Best Practices

1. **Start small:** Test with small date ranges first
2. **Monitor output:** Check logs for errors or warnings
3. **Respect Twitter's ToS:** Don't abuse the scraper
4. **Use headless mode:** For production/cloud deployment
5. **Handle errors:** Implement retry logic for network issues

## Troubleshooting

### Common Issues

**1. ChromeDriver not found**
```bash
# Install webdriver-manager
pip install webdriver-manager

# Or manually download ChromeDriver
# https://chromedriver.chromium.org/downloads
```

**2. No tweets found**
- Check your search query is valid
- Verify date range contains tweets
- Try without engagement filters first
- Ensure cookies are loaded correctly (if using)

**3. Stale element errors**
- Increase `page_load_wait` in config
- Reduce `scroll_loops`
- Add more delays

**4. Rate limiting**
- Increase `request_delay`
- Use time-splitting mode
- Add authentication cookies
- Reduce `scroll_loops`

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Architecture

### Project Structure

```
XSCP/
├── twitter_scraper.py      # Main scraper class
├── config.py               # Configuration and examples
├── example_usage.py        # Usage examples
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── twitter_cookies.json   # Optional: Authentication cookies
```

### Class Structure

```
TwitterAdvancedScraper
├── setup_driver()          # Initialize Chrome WebDriver
├── load_cookies()          # Load authentication cookies
├── build_search_url()      # Construct Twitter search URL
├── auto_scroll()           # Scroll to load more tweets
├── extract_tweet_data()    # Extract data from tweet element
├── scrape_tweets()         # Main scraping logic
├── scrape_with_time_splitting()  # Time-split scraping
├── export_to_csv()         # Export to CSV file
└── run()                   # Main execution method
```

## API Reference

### TwitterAdvancedScraper

#### `__init__(config: Dict)`

Initialize the scraper with configuration.

**Parameters:**
- `config` (dict): Configuration dictionary

**Example:**
```python
config = {
    'headless': False,
    'scroll_loops': 10,
    'page_load_wait': 5,
}
scraper = TwitterAdvancedScraper(config)
```

#### `run(keywords, output_file, use_time_splitting=False, **kwargs)`

Main execution method.

**Parameters:**
- `keywords` (str): Search keywords
- `output_file` (str): Output CSV filename
- `use_time_splitting` (bool): Enable time-splitting mode
- `**kwargs`: Additional search parameters

**Search Parameters:**
- `start_date` (str): Start date (YYYY-MM-DD)
- `end_date` (str): End date (YYYY-MM-DD)
- `min_likes` (int): Minimum likes
- `min_replies` (int): Minimum replies
- `min_retweets` (int): Minimum retweets
- `lang` (str): Language code
- `search_type` (str): "Latest" or "Top"
- `exclude_replies` (bool): Exclude replies
- `max_tweets` (int): Maximum tweets to scrape

**Example:**
```python
scraper.run(
    keywords="AI",
    output_file="ai_tweets.csv",
    start_date="2024-01-01",
    end_date="2024-01-31",
    min_likes=50,
    search_type="Latest"
)
```

## Performance Tips

1. **Optimize scroll loops:**
   - Fewer loops = faster but less tweets
   - More loops = slower but more tweets
   - Recommended: 10-20 for most use cases

2. **Use headless mode:**
   - Faster execution
   - Lower memory usage
   - Better for automation

3. **Parallel execution:**
   - Run multiple scrapers for different keywords
   - Use threading/multiprocessing
   - Respect rate limits

4. **Time-splitting:**
   - Essential for date ranges > 1 month
   - Use appropriate split mode
   - Balance between coverage and speed

## Examples

See `example_usage.py` for complete examples:

1. **Simple keyword search**
2. **Search with engagement filters**
3. **Exclude replies**
4. **Time-splitting mode**
5. **With authentication cookies**
6. **Exact phrase search**
7. **Headless mode**
8. **Advanced keyword combinations**

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes only. Please respect Twitter's Terms of Service and robots.txt.

## Disclaimer

This scraper is intended for:
- Research purposes
- Data analysis
- Educational projects
- Personal use

**Important:**
- Do not use for spam or harassment
- Respect Twitter's rate limits
- Follow Twitter's Terms of Service
- Do not sell or distribute scraped data
- Use responsibly and ethically

## Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section
2. Review example usage scripts
3. Open an issue on GitHub

## Changelog

### v1.0.0 (2024-01-01)
- Initial release
- Core scraping functionality
- Advanced Search support
- Time-splitting mode
- CSV export
- Cookie authentication
- Headless mode support

## Roadmap

Future enhancements:
- [ ] JSON export option
- [ ] Database storage support
- [ ] Proxy rotation
- [ ] Multi-threading support
- [ ] Progress bar/UI
- [ ] Email notifications
- [ ] Scheduled scraping
- [ ] Tweet media download

---

**Happy Scraping! 🚀**
