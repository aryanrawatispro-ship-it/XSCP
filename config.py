"""
Configuration file for Twitter Advanced Search Scraper
"""

# Scraper Configuration
SCRAPER_CONFIG = {
    # Browser settings
    'headless': False,  # Set to True for cloud deployment
    'scroll_loops': 20,  # Number of scroll iterations to load more tweets
    'page_load_wait': 5,  # Wait time after page load (seconds)
    'request_delay': 2,  # Delay between requests to avoid rate limiting

    # Authentication
    'cookies_file': None,  # Path to cookies JSON file (e.g., 'twitter_cookies.json')

    # Optional: Chrome driver path (leave None to use system PATH)
    'chrome_driver_path': None,
}

# Search Parameters (Default values)
SEARCH_PARAMS = {
    # Keywords
    'keywords': 'gensyn OR Gensyn OR GENSYN',

    # Date range
    'start_date': '2024-01-01',  # Format: YYYY-MM-DD
    'end_date': '2024-01-31',    # Format: YYYY-MM-DD

    # Engagement filters
    'min_likes': None,      # Minimum number of likes (e.g., 10)
    'min_replies': None,    # Minimum number of replies
    'min_retweets': None,   # Minimum number of retweets

    # Other filters
    'lang': None,           # Language code (e.g., 'en' for English)
    'search_type': 'Latest',  # 'Latest' or 'Top'
    'exclude_replies': True,  # Exclude reply tweets

    # Limits
    'max_tweets': None,     # Maximum number of tweets to scrape (None = unlimited)
}

# Time-splitting configuration (for large date ranges)
TIME_SPLIT_CONFIG = {
    'enabled': False,       # Enable time-splitting mode
    'split_mode': 'day',    # 'day', 'week', or 'month'
}

# Output configuration
OUTPUT_CONFIG = {
    'output_file': 'tweets.csv',  # Output CSV filename
}

# Example configurations for different use cases

# Example 1: Scrape specific brand mentions
EXAMPLE_BRAND_SEARCH = {
    'keywords': 'gensyn OR Gensyn OR GENSYN',
    'start_date': '2024-01-01',
    'end_date': '2024-12-31',
    'min_likes': 10,
    'search_type': 'Latest',
    'exclude_replies': True,
    'max_tweets': 1000,
}

# Example 2: Scrape trending topics
EXAMPLE_TRENDING_SEARCH = {
    'keywords': '#AI OR #MachineLearning',
    'start_date': '2024-01-01',
    'end_date': '2024-01-07',
    'min_likes': 100,
    'search_type': 'Top',
    'exclude_replies': False,
    'max_tweets': 500,
}

# Example 3: Scrape specific keyword with exact phrase
EXAMPLE_EXACT_PHRASE_SEARCH = {
    'keywords': '"artificial intelligence" OR "machine learning"',
    'start_date': '2024-01-01',
    'end_date': '2024-01-31',
    'lang': 'en',
    'min_likes': 50,
    'search_type': 'Latest',
    'exclude_replies': True,
}

# Example 4: Advanced search with multiple filters
EXAMPLE_ADVANCED_SEARCH = {
    'keywords': '(crypto OR bitcoin OR ethereum) -scam',  # Exclude scam tweets
    'start_date': '2023-12-01',
    'end_date': '2023-12-31',
    'min_likes': 100,
    'min_retweets': 50,
    'lang': 'en',
    'search_type': 'Top',
    'exclude_replies': True,
    'max_tweets': 2000,
}
