"""
Twitter Advanced Search Scraper
Replicates Octoparse functionality for scraping Twitter using Advanced Search
"""

import time
import csv
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urlencode, quote
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException


class TwitterAdvancedScraper:
    """
    Twitter Advanced Search Scraper with Octoparse-like functionality
    """

    def __init__(self, config: Dict):
        """
        Initialize the scraper with configuration

        Args:
            config: Dictionary containing scraper configuration
        """
        self.config = config
        self.driver = None
        self.tweets_data = []
        self.tweet_ids_seen = set()

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()

        if self.config.get('headless', False):
            chrome_options.add_argument('--headless=new')

        # Additional options for stability
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # User agent to avoid detection
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        # Proxy support
        proxy_config = self.config.get('proxy')
        if proxy_config:
            if isinstance(proxy_config, dict):
                # Handle dict format: {'host': 'ip', 'port': 'port', 'username': 'user', 'password': 'pass'}
                host = proxy_config.get('host')
                port = proxy_config.get('port')
                username = proxy_config.get('username')
                password = proxy_config.get('password')

                if username and password:
                    proxy_str = f"{username}:{password}@{host}:{port}"
                else:
                    proxy_str = f"{host}:{port}"
            else:
                # Handle string format: "host:port" or "username:password@host:port"
                proxy_str = proxy_config

            chrome_options.add_argument(f'--proxy-server={proxy_str}')
            self.logger.info(f"Using proxy: {proxy_str.split('@')[-1]}")  # Log without credentials

        # Initialize driver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

        self.logger.info("Chrome WebDriver initialized successfully")

    def load_cookies(self, cookies_file: str):
        """
        Load Twitter login cookies from file

        Args:
            cookies_file: Path to cookies JSON file
        """
        try:
            # First navigate to Twitter
            self.driver.get("https://twitter.com")
            time.sleep(2)

            # Load cookies
            with open(cookies_file, 'r') as f:
                cookies = json.load(f)

            for cookie in cookies:
                # Selenium requires certain fields
                if 'sameSite' in cookie and cookie['sameSite'] not in ['Strict', 'Lax', 'None']:
                    cookie['sameSite'] = 'None'
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    self.logger.warning(f"Could not add cookie: {e}")

            self.logger.info(f"Loaded cookies from {cookies_file}")

            # Refresh to apply cookies
            self.driver.refresh()
            time.sleep(3)

        except FileNotFoundError:
            self.logger.warning(f"Cookie file {cookies_file} not found. Proceeding without authentication.")
        except Exception as e:
            self.logger.error(f"Error loading cookies: {e}")

    def build_search_url(self, keywords: str, start_date: Optional[str] = None,
                        end_date: Optional[str] = None, min_likes: Optional[int] = None,
                        min_replies: Optional[int] = None, min_retweets: Optional[int] = None,
                        lang: Optional[str] = None, search_type: str = 'Latest',
                        exclude_replies: bool = False) -> str:
        """
        Build Twitter Advanced Search URL

        Args:
            keywords: Search keywords (supports OR, AND, quotes for exact match)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            min_likes: Minimum number of likes
            min_replies: Minimum number of replies
            min_retweets: Minimum number of retweets
            lang: Language code (e.g., 'en')
            search_type: 'Latest' or 'Top'
            exclude_replies: Whether to exclude replies

        Returns:
            Complete Twitter search URL
        """
        # Build the query string
        query_parts = [keywords]

        if start_date:
            query_parts.append(f"since:{start_date}")
        if end_date:
            query_parts.append(f"until:{end_date}")
        if min_likes:
            query_parts.append(f"min_faves:{min_likes}")
        if min_replies:
            query_parts.append(f"min_replies:{min_replies}")
        if min_retweets:
            query_parts.append(f"min_retweets:{min_retweets}")
        if lang:
            query_parts.append(f"lang:{lang}")
        if exclude_replies:
            query_parts.append("-filter:replies")

        query = " ".join(query_parts)

        # Determine the search endpoint
        if search_type.lower() == 'latest':
            base_url = "https://twitter.com/search?q="
            url = base_url + quote(query) + "&src=typed_query&f=live"
        else:  # Top
            base_url = "https://twitter.com/search?q="
            url = base_url + quote(query) + "&src=typed_query"

        return url

    def auto_scroll(self, scroll_loops: int, wait_time: int = 5):
        """
        Auto-scroll to load more tweets

        Args:
            scroll_loops: Number of scroll iterations
            wait_time: Wait time between scrolls in seconds
        """
        self.logger.info(f"Starting auto-scroll for {scroll_loops} loops")

        for i in range(scroll_loops):
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for content to load
            time.sleep(wait_time)

            # Check if we've reached the end (no new tweets loaded)
            current_height = self.driver.execute_script("return document.body.scrollHeight")

            if i % 5 == 0:
                self.logger.info(f"Scroll loop {i+1}/{scroll_loops} completed")

    def extract_tweet_data(self, tweet_element) -> Optional[Dict]:
        """
        Extract data from a single tweet element

        Args:
            tweet_element: Selenium WebElement representing a tweet

        Returns:
            Dictionary containing tweet data or None if extraction fails
        """
        try:
            tweet_data = {}

            # Extract tweet ID from data-testid or article element
            try:
                tweet_link = tweet_element.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
                tweet_url = tweet_link.get_attribute('href')
                tweet_data['tweet_url'] = tweet_url
                tweet_data['tweet_id'] = tweet_url.split('/status/')[-1].split('?')[0] if '/status/' in tweet_url else None
            except:
                tweet_data['tweet_url'] = None
                tweet_data['tweet_id'] = None

            # Skip if we've already seen this tweet
            if tweet_data['tweet_id'] and tweet_data['tweet_id'] in self.tweet_ids_seen:
                return None

            # Extract username and display name
            try:
                user_element = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]')
                tweet_data['display_name'] = user_element.find_element(By.CSS_SELECTOR, 'span').text

                # Username is in the format @username
                username_elements = user_element.find_elements(By.CSS_SELECTOR, 'span')
                for elem in username_elements:
                    text = elem.text
                    if text.startswith('@'):
                        tweet_data['username'] = text
                        break
                else:
                    tweet_data['username'] = None
            except:
                tweet_data['display_name'] = None
                tweet_data['username'] = None

            # Extract tweet text
            try:
                tweet_text_element = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                tweet_data['text'] = tweet_text_element.text
            except:
                tweet_data['text'] = None

            # Extract timestamp
            try:
                time_element = tweet_element.find_element(By.CSS_SELECTOR, 'time')
                tweet_data['timestamp'] = time_element.get_attribute('datetime')
            except:
                tweet_data['timestamp'] = None

            # Extract engagement metrics (likes, retweets, replies, views)
            try:
                # Reply count
                reply_element = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="reply"]')
                reply_text = reply_element.get_attribute('aria-label') or reply_element.text
                tweet_data['replies'] = self._parse_metric(reply_text)
            except:
                tweet_data['replies'] = 0

            try:
                # Retweet count
                retweet_element = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="retweet"]')
                retweet_text = retweet_element.get_attribute('aria-label') or retweet_element.text
                tweet_data['retweets'] = self._parse_metric(retweet_text)
            except:
                tweet_data['retweets'] = 0

            try:
                # Like count
                like_element = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="like"]')
                like_text = like_element.get_attribute('aria-label') or like_element.text
                tweet_data['likes'] = self._parse_metric(like_text)
            except:
                tweet_data['likes'] = 0

            try:
                # View count (if available)
                view_elements = tweet_element.find_elements(By.CSS_SELECTOR, 'a[href*="/analytics"]')
                if view_elements:
                    view_text = view_elements[0].get_attribute('aria-label') or view_elements[0].text
                    tweet_data['views'] = self._parse_metric(view_text)
                else:
                    tweet_data['views'] = 0
            except:
                tweet_data['views'] = 0

            # Extract media URLs (images/videos)
            tweet_data['media_urls'] = []
            try:
                # Images
                image_elements = tweet_element.find_elements(By.CSS_SELECTOR, 'img[src*="pbs.twimg.com/media"]')
                for img in image_elements:
                    img_url = img.get_attribute('src')
                    if img_url:
                        tweet_data['media_urls'].append(img_url)

                # Videos
                video_elements = tweet_element.find_elements(By.CSS_SELECTOR, 'video')
                for video in video_elements:
                    video_url = video.get_attribute('src')
                    if video_url:
                        tweet_data['media_urls'].append(video_url)
            except:
                pass

            tweet_data['media_urls'] = ', '.join(tweet_data['media_urls']) if tweet_data['media_urls'] else None

            # Mark this tweet as seen
            if tweet_data['tweet_id']:
                self.tweet_ids_seen.add(tweet_data['tweet_id'])

            return tweet_data

        except StaleElementReferenceException:
            return None
        except Exception as e:
            self.logger.warning(f"Error extracting tweet data: {e}")
            return None

    def _parse_metric(self, text: str) -> int:
        """
        Parse engagement metric from text (handles K, M suffixes)

        Args:
            text: Text containing the metric (e.g., "1.2K", "500")

        Returns:
            Integer value of the metric
        """
        if not text:
            return 0

        # Extract numbers from text
        import re
        match = re.search(r'([\d.]+)([KMB]?)', text)
        if not match:
            return 0

        number = float(match.group(1))
        suffix = match.group(2)

        multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}

        return int(number * multipliers.get(suffix, 1))

    def scrape_tweets(self, max_tweets: Optional[int] = None) -> List[Dict]:
        """
        Scrape tweets from the current page

        Args:
            max_tweets: Maximum number of tweets to scrape

        Returns:
            List of tweet dictionaries
        """
        self.logger.info("Starting tweet extraction")

        # Wait for tweets to load
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
            )
        except TimeoutException:
            self.logger.warning("No tweets found or page took too long to load")
            return []

        # Perform auto-scroll
        scroll_loops = self.config.get('scroll_loops', 10)
        self.auto_scroll(scroll_loops)

        # Extract all tweet elements
        tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
        self.logger.info(f"Found {len(tweet_elements)} tweet elements")

        for i, tweet_element in enumerate(tweet_elements):
            if max_tweets and len(self.tweets_data) >= max_tweets:
                self.logger.info(f"Reached max tweets limit: {max_tweets}")
                break

            tweet_data = self.extract_tweet_data(tweet_element)

            if tweet_data:
                self.tweets_data.append(tweet_data)

            if (i + 1) % 50 == 0:
                self.logger.info(f"Processed {i + 1} tweet elements, extracted {len(self.tweets_data)} tweets")

        self.logger.info(f"Total tweets extracted: {len(self.tweets_data)}")
        return self.tweets_data

    def scrape_with_time_splitting(self, keywords: str, start_date: str, end_date: str,
                                   split_mode: str = 'day', **kwargs) -> List[Dict]:
        """
        Scrape tweets by splitting the date range into smaller chunks

        Args:
            keywords: Search keywords
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            split_mode: 'day', 'week', or 'month'
            **kwargs: Additional search parameters

        Returns:
            List of all scraped tweets
        """
        self.logger.info(f"Starting time-split scraping with mode: {split_mode}")

        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        # Determine time delta based on split mode
        if split_mode == 'day':
            delta = timedelta(days=1)
        elif split_mode == 'week':
            delta = timedelta(weeks=1)
        elif split_mode == 'month':
            delta = timedelta(days=30)
        else:
            raise ValueError(f"Invalid split_mode: {split_mode}")

        current_start = start
        max_tweets = kwargs.get('max_tweets')

        while current_start < end:
            current_end = min(current_start + delta, end)

            self.logger.info(f"Scraping from {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}")

            # Build URL for this time range
            url = self.build_search_url(
                keywords=keywords,
                start_date=current_start.strftime('%Y-%m-%d'),
                end_date=current_end.strftime('%Y-%m-%d'),
                **{k: v for k, v in kwargs.items() if k != 'max_tweets'}
            )

            # Navigate to URL
            self.driver.get(url)
            time.sleep(self.config.get('page_load_wait', 5))

            # Scrape tweets for this time period
            remaining_tweets = None
            if max_tweets:
                remaining_tweets = max_tweets - len(self.tweets_data)
                if remaining_tweets <= 0:
                    break

            self.scrape_tweets(max_tweets=remaining_tweets)

            # Move to next time period
            current_start = current_end

            # Rate limiting between requests
            time.sleep(self.config.get('request_delay', 2))

        return self.tweets_data

    def export_to_csv(self, filename: str):
        """
        Export scraped tweets to CSV file

        Args:
            filename: Output CSV filename
        """
        if not self.tweets_data:
            self.logger.warning("No tweets to export")
            return

        fieldnames = [
            'tweet_id', 'tweet_url', 'username', 'display_name', 'text',
            'timestamp', 'likes', 'retweets', 'replies', 'views', 'media_urls'
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for tweet in self.tweets_data:
                writer.writerow(tweet)

        self.logger.info(f"Exported {len(self.tweets_data)} tweets to {filename}")

    def run(self, keywords: str, output_file: str = 'tweets.csv',
            use_time_splitting: bool = False, **kwargs):
        """
        Main execution method

        Args:
            keywords: Search keywords
            output_file: Output CSV filename
            use_time_splitting: Whether to use time-splitting mode
            **kwargs: Additional search parameters
        """
        try:
            # Setup driver
            self.setup_driver()

            # Load cookies if provided
            if self.config.get('cookies_file'):
                self.load_cookies(self.config['cookies_file'])

            if use_time_splitting:
                # Time-splitting mode
                start_date = kwargs.get('start_date')
                end_date = kwargs.get('end_date')
                split_mode = kwargs.get('split_mode', 'day')

                if not start_date or not end_date:
                    raise ValueError("start_date and end_date are required for time-splitting mode")

                self.scrape_with_time_splitting(keywords, start_date, end_date, split_mode, **kwargs)
            else:
                # Single search mode
                url = self.build_search_url(keywords, **kwargs)
                self.logger.info(f"Navigating to: {url}")

                self.driver.get(url)
                time.sleep(self.config.get('page_load_wait', 5))

                # Scrape tweets
                max_tweets = kwargs.get('max_tweets')
                self.scrape_tweets(max_tweets=max_tweets)

            # Export to CSV
            self.export_to_csv(output_file)

        except Exception as e:
            self.logger.error(f"Error during scraping: {e}", exc_info=True)
            raise
        finally:
            # Cleanup
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed")


if __name__ == "__main__":
    # Example usage
    config = {
        'headless': False,
        'scroll_loops': 10,
        'page_load_wait': 5,
        'request_delay': 2,
        'cookies_file': 'twitter_cookies.json'  # Optional
    }

    scraper = TwitterAdvancedScraper(config)

    # Example: Simple search
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
