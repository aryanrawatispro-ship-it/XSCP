Build me a Twitter Advanced Search scraper in Python that replicates Octoparse's functionality. Requirements:

CORE FEATURES:
- Scrape tweets using Twitter's Advanced Search URL structure
- Support keyword filtering (any, all, none, exact phrase)
- Filter by date range (start date to end date)
- Filter by minimum engagement (likes, replies, retweets)
- Support language filtering
- Implement time-splitting modes (day/week/month) to handle large date ranges
- Auto-scroll infinite loading to capture all tweets
- Handle Twitter login cookies for full access

DATA TO EXTRACT:
- Tweet text/content
- Author username and display name
- Tweet URL and ID
- Timestamp/date posted
- Engagement metrics (likes, retweets, replies, views)
- Image/video URLs if present

TECHNICAL REQUIREMENTS:
- Use Selenium with Chrome WebDriver
- Implement proper wait times for AJAX loading (5 seconds)
- Auto-scroll with configurable loop count
- Export to CSV with all data fields
- Handle rate limiting and errors gracefully
- Support headless mode for cloud deployment

CONFIGURATION:
- Make it easy to set keywords (e.g., "gensyn OR Gensyn OR GENSYN")
- Configurable max tweets limit
- Toggle for "Latest" vs "Top" tweets
- Exclude replies option (-filter:replies)

Provide complete working code with comments and setup instructions.
