"""
Test script to verify Twitter scraper setup
"""

import sys


def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")

    try:
        import selenium
        print(f"✓ Selenium version: {selenium.__version__}")
    except ImportError as e:
        print(f"✗ Selenium import failed: {e}")
        return False

    try:
        from selenium import webdriver
        print("✓ Selenium WebDriver imported")
    except ImportError as e:
        print(f"✗ WebDriver import failed: {e}")
        return False

    try:
        from selenium.webdriver.chrome.options import Options
        print("✓ Chrome Options imported")
    except ImportError as e:
        print(f"✗ Chrome Options import failed: {e}")
        return False

    return True


def test_chromedriver():
    """Test if ChromeDriver can be initialized"""
    print("\nTesting ChromeDriver...")

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=chrome_options)
        driver.quit()

        print("✓ ChromeDriver initialized successfully")
        return True

    except Exception as e:
        print(f"✗ ChromeDriver initialization failed: {e}")
        print("\nPossible solutions:")
        print("1. Install Chrome: https://www.google.com/chrome/")
        print("2. ChromeDriver will be auto-downloaded by selenium")
        return False


def test_scraper_import():
    """Test if the scraper module can be imported"""
    print("\nTesting scraper module...")

    try:
        from twitter_scraper import TwitterAdvancedScraper
        print("✓ TwitterAdvancedScraper imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import TwitterAdvancedScraper: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_config_import():
    """Test if config module can be imported"""
    print("\nTesting config module...")

    try:
        import config
        print("✓ Config module imported successfully")
        print(f"  - Scraper config keys: {list(config.SCRAPER_CONFIG.keys())}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import config: {e}")
        return False


def test_scraper_initialization():
    """Test if scraper can be initialized"""
    print("\nTesting scraper initialization...")

    try:
        from twitter_scraper import TwitterAdvancedScraper

        config = {
            'headless': True,
            'scroll_loops': 1,
        }

        scraper = TwitterAdvancedScraper(config)
        print("✓ Scraper initialized successfully")
        print(f"  - Config: {scraper.config}")
        return True

    except Exception as e:
        print(f"✗ Scraper initialization failed: {e}")
        return False


def test_url_builder():
    """Test URL builder functionality"""
    print("\nTesting URL builder...")

    try:
        from twitter_scraper import TwitterAdvancedScraper

        config = {'headless': True}
        scraper = TwitterAdvancedScraper(config)

        url = scraper.build_search_url(
            keywords="test",
            start_date="2024-01-01",
            end_date="2024-01-31",
            min_likes=10,
            search_type="Latest"
        )

        print(f"✓ URL built successfully")
        print(f"  - URL: {url[:100]}...")

        # Verify URL contains expected parts
        assert "twitter.com/search" in url
        assert "test" in url
        assert "since:2024-01-01" in url
        assert "until:2024-01-31" in url
        assert "min_faves:10" in url

        print("✓ URL validation passed")
        return True

    except Exception as e:
        print(f"✗ URL builder test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Twitter Advanced Search Scraper - Setup Test")
    print("=" * 60)
    print()

    results = {
        "Imports": test_imports(),
        "ChromeDriver": test_chromedriver(),
        "Scraper Import": test_scraper_import(),
        "Config Import": test_config_import(),
        "Scraper Init": test_scraper_initialization(),
        "URL Builder": test_url_builder(),
    }

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:20} {status}")

    total_tests = len(results)
    passed_tests = sum(results.values())

    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Run an example: python example_usage.py 1")
        print("2. Or create your own script using the examples")
        return 0
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
