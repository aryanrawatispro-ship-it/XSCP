#!/usr/bin/env python3
"""
Interactive Twitter Advanced Search Scraper
Easy-to-use CLI interface - just run and input what you need!
"""

from twitter_scraper import TwitterAdvancedScraper
import sys
import os


def print_banner():
    """Print welcome banner"""
    print("=" * 70)
    print(" " * 15 + "Twitter Advanced Search Scraper")
    print(" " * 20 + "Interactive Mode")
    print("=" * 70)
    print()


def get_input(prompt, default=None, required=False, input_type=str):
    """
    Get user input with validation

    Args:
        prompt: Question to ask
        default: Default value if user presses Enter
        required: Whether input is required
        input_type: Type to convert input to (str, int, bool)

    Returns:
        User input or default value
    """
    if default is not None:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "

    while True:
        value = input(prompt_text).strip()

        # Use default if provided and no input given
        if not value and default is not None:
            return default

        # Check if required
        if required and not value:
            print("⚠ This field is required. Please enter a value.")
            continue

        # Allow empty for non-required fields
        if not value:
            return None

        # Convert to appropriate type
        if input_type == bool:
            if value.lower() in ['y', 'yes', 'true', '1']:
                return True
            elif value.lower() in ['n', 'no', 'false', '0']:
                return False
            else:
                print("⚠ Please enter y/yes or n/no")
                continue
        elif input_type == int:
            try:
                return int(value)
            except ValueError:
                print("⚠ Please enter a valid number")
                continue
        else:
            return value


def configure_basic_settings():
    """Configure basic scraper settings"""
    print("\n" + "─" * 70)
    print("BASIC CONFIGURATION")
    print("─" * 70)

    config = {}

    # Headless mode
    config['headless'] = get_input(
        "Run in headless mode (no browser window)?",
        default='n',
        input_type=bool
    )

    # Scroll loops
    print("\nScroll loops: More loops = more tweets but slower")
    print("  Recommended: 10-20 for most cases")
    config['scroll_loops'] = get_input(
        "Number of scroll loops",
        default=15,
        input_type=int
    )

    # Cookies
    config['cookies_file'] = get_input(
        "Path to Twitter cookies file (optional, press Enter to skip)",
        default=None
    )

    if config['cookies_file'] and not os.path.exists(config['cookies_file']):
        print(f"⚠ Warning: Cookie file '{config['cookies_file']}' not found")
        use_anyway = get_input("Continue without cookies?", default='y', input_type=bool)
        if use_anyway:
            config['cookies_file'] = None

    return config


def configure_proxy():
    """Configure proxy settings"""
    print("\n" + "─" * 70)
    print("PROXY CONFIGURATION (Optional)")
    print("─" * 70)

    use_proxy = get_input("Do you want to use a proxy?", default='n', input_type=bool)

    if not use_proxy:
        return None

    print("\nProxy formats supported:")
    print("  1. host:port (e.g., 123.456.789.0:8080)")
    print("  2. username:password@host:port")
    print()

    proxy_type = get_input("Does your proxy require authentication?", default='n', input_type=bool)

    if proxy_type:
        # Authenticated proxy
        host = get_input("Proxy host/IP", required=True)
        port = get_input("Proxy port", required=True)
        username = get_input("Proxy username", required=True)
        password = get_input("Proxy password", required=True)

        return {
            'host': host,
            'port': port,
            'username': username,
            'password': password
        }
    else:
        # Simple proxy
        host = get_input("Proxy host/IP", required=True)
        port = get_input("Proxy port", required=True)

        return {
            'host': host,
            'port': port
        }


def configure_search_params():
    """Configure search parameters"""
    print("\n" + "─" * 70)
    print("SEARCH PARAMETERS")
    print("─" * 70)

    params = {}

    # Keywords
    print("\nKeyword examples:")
    print("  - Simple: bitcoin")
    print("  - OR operator: bitcoin OR ethereum OR crypto")
    print("  - Exact phrase: \"machine learning\"")
    print("  - Exclude: crypto -scam -spam")
    print("  - Complex: (AI OR \"machine learning\") python -tutorial")
    print()
    params['keywords'] = get_input("Enter your keywords", required=True)

    # Date range
    print("\nDate range (YYYY-MM-DD format)")
    params['start_date'] = get_input("Start date (e.g., 2024-01-01)", required=True)
    params['end_date'] = get_input("End date (e.g., 2024-01-31)", required=True)

    # Search type
    print("\nSearch type:")
    print("  1. Latest - Most recent tweets")
    print("  2. Top - Most popular tweets")
    search_choice = get_input("Choose search type [1/2]", default='1')
    params['search_type'] = 'Latest' if search_choice == '1' else 'Top'

    # Engagement filters
    print("\nEngagement filters (optional, press Enter to skip)")
    params['min_likes'] = get_input("Minimum likes", input_type=int)
    params['min_replies'] = get_input("Minimum replies", input_type=int)
    params['min_retweets'] = get_input("Minimum retweets", input_type=int)

    # Language
    print("\nLanguage filter (optional)")
    print("  Examples: en (English), es (Spanish), fr (French), ja (Japanese)")
    params['lang'] = get_input("Language code (press Enter to skip)")

    # Exclude replies
    params['exclude_replies'] = get_input(
        "Exclude reply tweets?",
        default='y',
        input_type=bool
    )

    # Max tweets
    print("\nMaximum tweets to scrape (0 = unlimited)")
    max_tweets = get_input("Max tweets", default=500, input_type=int)
    params['max_tweets'] = max_tweets if max_tweets > 0 else None

    return params


def configure_time_splitting():
    """Configure time-splitting mode"""
    print("\n" + "─" * 70)
    print("TIME-SPLITTING MODE (Optional)")
    print("─" * 70)
    print("For large date ranges, split into smaller chunks for better coverage")
    print()

    use_splitting = get_input("Enable time-splitting?", default='n', input_type=bool)

    if not use_splitting:
        return False, None

    print("\nSplit modes:")
    print("  1. Day - Best for very active keywords")
    print("  2. Week - Good for moderate activity")
    print("  3. Month - For low activity keywords")
    mode_choice = get_input("Choose split mode [1/2/3]", default='2')

    mode_map = {'1': 'day', '2': 'week', '3': 'month'}
    split_mode = mode_map.get(mode_choice, 'week')

    return True, split_mode


def configure_output():
    """Configure output settings"""
    print("\n" + "─" * 70)
    print("OUTPUT CONFIGURATION")
    print("─" * 70)

    output_file = get_input(
        "Output CSV filename",
        default="tweets.csv"
    )

    return output_file


def show_summary(config, params, output_file, use_splitting, split_mode):
    """Show configuration summary"""
    print("\n" + "=" * 70)
    print("CONFIGURATION SUMMARY")
    print("=" * 70)

    print("\n📋 Basic Settings:")
    print(f"  Headless mode: {'Yes' if config['headless'] else 'No'}")
    print(f"  Scroll loops: {config['scroll_loops']}")
    print(f"  Cookies: {config['cookies_file'] if config['cookies_file'] else 'Not using'}")
    print(f"  Proxy: {'Yes' if config.get('proxy') else 'No'}")

    print("\n🔍 Search Parameters:")
    print(f"  Keywords: {params['keywords']}")
    print(f"  Date range: {params['start_date']} to {params['end_date']}")
    print(f"  Search type: {params['search_type']}")
    print(f"  Min likes: {params['min_likes'] if params['min_likes'] else 'None'}")
    print(f"  Min replies: {params['min_replies'] if params['min_replies'] else 'None'}")
    print(f"  Min retweets: {params['min_retweets'] if params['min_retweets'] else 'None'}")
    print(f"  Language: {params['lang'] if params['lang'] else 'Any'}")
    print(f"  Exclude replies: {'Yes' if params['exclude_replies'] else 'No'}")
    print(f"  Max tweets: {params['max_tweets'] if params['max_tweets'] else 'Unlimited'}")

    if use_splitting:
        print(f"\n⏱ Time-Splitting: Enabled ({split_mode} mode)")

    print(f"\n💾 Output: {output_file}")
    print("=" * 70)


def main():
    """Main interactive CLI"""
    print_banner()

    print("Welcome! This interactive tool will help you scrape Twitter easily.")
    print("Just answer the questions below - defaults are shown in [brackets]")
    print()

    # Get all configurations
    config = configure_basic_settings()
    proxy = configure_proxy()
    if proxy:
        config['proxy'] = proxy

    params = configure_search_params()
    use_splitting, split_mode = configure_time_splitting()
    output_file = configure_output()

    # Show summary
    show_summary(config, params, output_file, use_splitting, split_mode)

    # Confirm
    print()
    confirm = get_input("Start scraping with these settings?", default='y', input_type=bool)

    if not confirm:
        print("\n❌ Scraping cancelled.")
        return

    # Run scraper
    print("\n" + "=" * 70)
    print("STARTING SCRAPER")
    print("=" * 70)
    print()

    try:
        scraper = TwitterAdvancedScraper(config)

        # Prepare parameters for run method
        run_params = {
            'keywords': params['keywords'],
            'output_file': output_file,
            'start_date': params['start_date'],
            'end_date': params['end_date'],
            'search_type': params['search_type'],
            'exclude_replies': params['exclude_replies'],
        }

        # Add optional parameters
        if params['min_likes']:
            run_params['min_likes'] = params['min_likes']
        if params['min_replies']:
            run_params['min_replies'] = params['min_replies']
        if params['min_retweets']:
            run_params['min_retweets'] = params['min_retweets']
        if params['lang']:
            run_params['lang'] = params['lang']
        if params['max_tweets']:
            run_params['max_tweets'] = params['max_tweets']

        # Add time-splitting
        if use_splitting:
            run_params['use_time_splitting'] = True
            run_params['split_mode'] = split_mode

        # Run!
        scraper.run(**run_params)

        print("\n" + "=" * 70)
        print("✅ SCRAPING COMPLETED!")
        print("=" * 70)
        print(f"\n💾 Results saved to: {output_file}")
        print(f"📊 Total tweets scraped: {len(scraper.tweets_data)}")
        print("\nThank you for using Twitter Advanced Search Scraper! 🚀")
        print()

    except KeyboardInterrupt:
        print("\n\n⚠ Scraping interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        print("\nCheck the error message above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)
