import concurrent.futures
from datetime import datetime
import html
import time

from dateutil import parser as date_parser
from feedgen.feed import FeedGenerator
import feedparser
import pytz

# Convert dt to UTC
def convert_to_utc(dt):
    return dt.astimezone(pytz.utc) if dt else datetime.min.replace(tzinfo=pytz.utc)

# Parse date with tz info
def parse_date(date_str):
    try:
        tzinfos = {"EDT": pytz.timezone("America/New_York"),
                   "EST": pytz.timezone("America/New_York")}
        return date_parser.parse(date_str, tzinfos=tzinfos)
    except Exception as e:
        print(f"Parse error: {date_str} - {e}")
        return None

# Key for sorting entries by published date
def sort_key(entry):
    if hasattr(entry, 'published'):
        dt = parse_date(entry.published)
        if dt:
            return convert_to_utc(dt)
    return datetime.min.replace(tzinfo=pytz.utc)

# Fetch feed entries with retries
def fetch_feed(url, max_retries=3, delay=5):
    for attempt in range(max_retries):
        try:
            feed = feedparser.parse(url)
            if hasattr(feed, 'entries'):
                return feed.entries
        except Exception as e:
            print(f"Error fetching {url} (attempt {attempt + 1}): {e}")
        time.sleep(delay)
    return []


# Combine feeds and remove duplicate links
def combine_rss_feeds(feed_urls):
    combined = []
    seen = set()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for entries in executor.map(fetch_feed, feed_urls):
            for entry in entries:
                if entry.link not in seen:
                    seen.add(entry.link)
                    combined.append(entry)
    return sorted(combined, key=sort_key)

# Create and save RSS feed XML
def create_rss_feed(entries):
    fg = FeedGenerator()
    fg.title("EndlessFractal's Threat Intel Feed")
    fg.description("A combined RSS feed of the 60 most recent articles from various sources")
    fg.link(href="https://raw.githubusercontent.com/EndlessFractal/hosts/main/feed.xml", rel="alternate")
    # Use the 60 most recent entries
    for entry in entries[-60:]:
        fe = fg.add_entry()
        fe.title(html.unescape(entry.title))
        fe.link(href=entry.link)
        if hasattr(entry, 'published'):
            dt = parse_date(entry.published)
            if dt:
                fe.published(convert_to_utc(dt))
    rss = fg.rss_str(pretty=True)
    with open('feed.xml', 'wb') as f:
        f.write(rss)

def main():
    with open('list.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    combined = combine_rss_feeds(urls)
    create_rss_feed(combined)

if __name__ == "__main__":
    main()
