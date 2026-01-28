import concurrent.futures
from datetime import datetime
import html
import time

from dateutil import parser as date_parser
from feedgen.feed import FeedGenerator
import feedparser
import pytz
import requests

# Convert dt to UTC
def convert_to_utc(dt):
    return dt.astimezone(pytz.utc) if dt else datetime.min.replace(tzinfo=pytz.utc)

# Parse date with tz info
TZINFOS = {"EDT": pytz.timezone("America/New_York"),
           "EST": pytz.timezone("America/New_York")}

def parse_date(date_str):
    try:
        return date_parser.parse(date_str, tzinfos=TZINFOS)
    except Exception as e:
        print(f"Parse error: {date_str} - {e}")
        return None

# Key for sorting entries by published date
def sort_key(entry):
    date_str = getattr(entry, 'published', None) or getattr(entry, 'updated', None)
    if date_str:
        dt = parse_date(date_str)
        if dt:
            return convert_to_utc(dt)
    return datetime.min.replace(tzinfo=pytz.utc)

# Fetch feed entries with retries and timeout
def fetch_feed(url, max_retries=2, delay=3, timeout=5):
    headers = {
        'User-Agent': 'EndlessFractalRSSBot/1.0 (Fetch every two hours; +https://github.com/EndlessFractal/Threat-Intel-Feed'
    }
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            feed = feedparser.parse(resp.content)
            if hasattr(feed, 'entries'):
                return feed.entries
        except (requests.Timeout, concurrent.futures.TimeoutError):
            print(f"Timeout: {url} (attempt {attempt + 1})")
        except Exception as e:
            print(f"Error fetching {url} (attempt {attempt + 1}): {e}")
        time.sleep(delay)
    return []


# Combine feeds and remove duplicate links
def combine_rss_feeds(feed_urls):
    combined = []
    seen = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(10, len(feed_urls))) as executor:
        future_to_url = {executor.submit(fetch_feed, url): url for url in feed_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                entries = future.result()
                for entry in entries:
                    if entry.link not in seen:
                        seen.add(entry.link)
                        combined.append(entry)
            except Exception as exc:
                print(f"Feed {url} generated an exception: {exc}")

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
