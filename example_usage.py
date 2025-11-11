"""
Example usage scripts for Twitter Advanced Search Scraper
"""

from twitter_scraper import TwitterAdvancedScraper
from config import SCRAPER_CONFIG


def example1_simple_search():
    """
    Example 1: Simple keyword search with date range
    """
    print("=" * 60)
    print("Example 1: Simple keyword search")
    print("=" * 60)

    config = SCRAPER_CONFIG.copy()
    config['headless'] = False  # Set to True for headless mode
    config['scroll_loops'] = 10

    scraper = TwitterAdvancedScraper(config)

    scraper.run(
        keywords="gensyn OR Gensyn OR GENSYN",
        output_file="example1_gensyn_tweets.csv",
        start_date="2024-01-01",
        end_date="2024-01-31",
        search_type="Latest",
        max_tweets=100
    )


def example2_with_engagement_filters():
    """
    Example 2: Search with minimum engagement filters
    """
    print("=" * 60)
    print("Example 2: Search with engagement filters")
    print("=" * 60)

    config = SCRAPER_CONFIG.copy()
    config['scroll_loops'] = 15

    scraper = TwitterAdvancedScraper(config)

    scraper.run(
        keywords="AI OR MachineLearning",
        output_file="example2_ai_tweets.csv",
        start_date="2024-01-01",
        end_date="2024-01-07",
        min_likes=50,
        min_retweets=10,
        search_type="Top",
        exclude_replies=True,
        max_tweets=200
    )


def example3_exclude_replies():
    """
    Example 3: Search excluding replies
    """
    print("=" * 60)
    print("Example 3: Search excluding replies")
    print("=" * 60)

    config = SCRAPER_CONFIG.copy()
    config['scroll_loops'] = 10

    scraper = TwitterAdvancedScraper(config)

    scraper.run(
        keywords="python programming",
        output_file="example3_python_tweets.csv",
        start_date="2024-01-01",
        end_date="2024-01-15",
        exclude_replies=True,
        lang="en",
        search_type="Latest",
        max_tweets=150
    )


def example4_time_splitting():
    """
    Example 4: Time-splitting mode for large date ranges
    """
    print("=" * 60)
    print("Example 4: Time-splitting mode")
    print("=" * 60)

    config = SCRAPER_CONFIG.copy()
    config['scroll_loops'] = 5  # Fewer loops per time period
    config['request_delay'] = 3  # More delay between requests

    scraper = TwitterAdvancedScraper(config)

    scraper.run(
        keywords="cryptocurrency",
        output_file="example4_crypto_tweets.csv",
        use_time_splitting=True,
        start_date="2024-01-01",
        end_date="2024-03-31",
        split_mode="week",  # Split by week
        min_likes=20,
        search_type="Latest",
        max_tweets=500
    )


def example5_with_cookies():
    """
    Example 5: Search with authentication cookies
    """
    print("=" * 60)
    print("Example 5: Search with authentication cookies")
    print("=" * 60)

    config = SCRAPER_CONFIG.copy()
    config['cookies_file'] = 'twitter_cookies.json'  # Make sure this file exists
    config['scroll_loops'] = 20

    scraper = TwitterAdvancedScraper(config)

    scraper.run(
        keywords="trending topic",
        output_file="example5_trending_tweets.csv",
        start_date="2024-01-01",
        end_date="2024-01-31",
        search_type="Top",
        max_tweets=300
    )


def example6_exact_phrase_search():
    """
    Example 6: Exact phrase search
    """
    print("=" * 60)
    print("Example 6: Exact phrase search")
    print("=" * 60)

    config = SCRAPER_CONFIG.copy()
    config['scroll_loops'] = 10

    scraper = TwitterAdvancedScraper(config)

    scraper.run(
        keywords='"artificial intelligence" "deep learning"',
        output_file="example6_exact_phrase_tweets.csv",
        start_date="2024-01-01",
        end_date="2024-01-31",
        min_likes=100,
        lang="en",
        search_type="Latest",
        max_tweets=200
    )


def example7_headless_mode():
    """
    Example 7: Headless mode for cloud deployment
    """
    print("=" * 60)
    print("Example 7: Headless mode (cloud deployment)")
    print("=" * 60)

    config = SCRAPER_CONFIG.copy()
    config['headless'] = True  # Run in headless mode
    config['scroll_loops'] = 10

    scraper = TwitterAdvancedScraper(config)

    scraper.run(
        keywords="technology news",
        output_file="example7_tech_news_tweets.csv",
        start_date="2024-01-01",
        end_date="2024-01-07",
        search_type="Latest",
        max_tweets=100
    )


def example8_multiple_keywords_advanced():
    """
    Example 8: Advanced keyword combinations
    """
    print("=" * 60)
    print("Example 8: Advanced keyword combinations")
    print("=" * 60)

    config = SCRAPER_CONFIG.copy()
    config['scroll_loops'] = 15

    scraper = TwitterAdvancedScraper(config)

    # Search for tweets mentioning either "bitcoin" or "ethereum", but exclude "scam"
    scraper.run(
        keywords="(bitcoin OR ethereum) -scam -spam",
        output_file="example8_crypto_filtered_tweets.csv",
        start_date="2024-01-01",
        end_date="2024-01-31",
        min_likes=50,
        min_retweets=10,
        lang="en",
        exclude_replies=True,
        search_type="Top",
        max_tweets=500
    )


if __name__ == "__main__":
    import sys

    examples = {
        '1': example1_simple_search,
        '2': example2_with_engagement_filters,
        '3': example3_exclude_replies,
        '4': example4_time_splitting,
        '5': example5_with_cookies,
        '6': example6_exact_phrase_search,
        '7': example7_headless_mode,
        '8': example8_multiple_keywords_advanced,
    }

    print("\nAvailable Examples:")
    print("1. Simple keyword search")
    print("2. Search with engagement filters")
    print("3. Search excluding replies")
    print("4. Time-splitting mode for large date ranges")
    print("5. Search with authentication cookies")
    print("6. Exact phrase search")
    print("7. Headless mode (cloud deployment)")
    print("8. Advanced keyword combinations")
    print()

    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        if example_num in examples:
            examples[example_num]()
        else:
            print(f"Invalid example number: {example_num}")
            print("Usage: python example_usage.py [1-8]")
    else:
        print("Usage: python example_usage.py [1-8]")
        print("Example: python example_usage.py 1")
