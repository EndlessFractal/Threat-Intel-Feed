import concurrent.futures
from datetime import datetime, timezone
from email.utils import format_datetime
import html
from pathlib import Path
import time
from xml.dom import minidom
import xml.etree.ElementTree as ET

import feedparser
import requests

FEED_TITLE = "EndlessFractal's Threat Intel Feed"
FEED_DESCRIPTION = "A combined RSS feed of the 60 most recent articles from various sources"
FEED_LINK = "https://raw.githubusercontent.com/EndlessFractal/hosts/main/feed.xml"
OUTPUT_FILE = Path("feed.xml")
URLS_FILE = Path("list.txt")

MAX_ENTRIES = 60
MAX_WORKERS = 10
REQUEST_TIMEOUT = 10
MAX_RETRIES = 2
RETRY_DELAY = 3

USER_AGENT = "EndlessFractalRSSBot/1.0 (Fetch every two hours; +https://github.com/EndlessFractal/Threat-Intel-Feed)"

# Get the best available parsed datetime (published_parsed preferred) or None
def _get_parsed_datetime(entry):
    for field in ('published_parsed', 'updated_parsed'):
        parsed = getattr(entry, field, None)
        if parsed:
            return datetime(*parsed[:6], tzinfo=timezone.utc)
    return None

# Return UTC datetime for sorting (published_parsed > updated_parsed > min date)
def get_sort_key(entry):
    dt = _get_parsed_datetime(entry)
    return dt if dt is not None else datetime.min.replace(tzinfo=timezone.utc)

 # Fetch a single RSS feed with retries.
def fetch_feed(url):
    headers = {'User-Agent': USER_AGENT}
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            content = resp.content
            feed = feedparser.parse(content)
            return feed.entries if hasattr(feed, 'entries') else []

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "unknown"
            reason = e.response.reason if e.response is not None else str(e)
            print(f"HTTP error fetching {url} (attempt {attempt}/{MAX_RETRIES}): {status} {reason}")
        except requests.exceptions.Timeout:
            print(f"Timeout fetching {url} (attempt {attempt}/{MAX_RETRIES})")
        except requests.exceptions.RequestException as e:
            print(f"Request error fetching {url} (attempt {attempt}/{MAX_RETRIES}): {e}")
        except Exception as e:
            print(f"Unexpected error fetching {url} (attempt {attempt}/{MAX_RETRIES}): {e}")

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)

    print(f"Failed to fetch feed after {MAX_RETRIES} attempts: {url}")
    return []

# Fetch all feeds in parallel and combine unique entries
def combine_rss_feeds(feed_urls):
    combined = []
    seen_links = set()

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(fetch_feed, url): url for url in feed_urls}

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                entries = future.result()
                for entry in entries:
                    link = getattr(entry, 'link', None)
                    if link and link not in seen_links:
                        seen_links.add(link)
                        combined.append(entry)
            except Exception as exc:
                print(f"Exception while processing feed {url}: {exc}")

    # Sort by date (newest at the end)
    combined.sort(key=get_sort_key)
    return combined

# Generate and save the combined RSS feed
def create_rss_feed(entries):
    rss = ET.Element('rss', {'version': '2.0'})
    channel = ET.SubElement(rss, 'channel')

    ET.SubElement(channel, 'title').text = FEED_TITLE
    ET.SubElement(channel, 'description').text = FEED_DESCRIPTION
    ET.SubElement(channel, 'link').text = FEED_LINK

    # Keep only the 60 most recent entries
    recent_entries = entries[-MAX_ENTRIES:]

    for entry in recent_entries:
        item = ET.SubElement(channel, 'item')

        # Title
        title = getattr(entry, 'title', 'No Title') or 'No Title'
        ET.SubElement(item, 'title').text = html.unescape(title)

        # Link
        ET.SubElement(item, 'link').text = getattr(entry, 'link', '')

        # pubDate (uses feedparser's parsed dates)
        dt = _get_parsed_datetime(entry)
        if dt:
            pubdate_str = format_datetime(dt)
            ET.SubElement(item, 'pubDate').text = pubdate_str

    # Pretty-print XML
    rough_string = ET.tostring(rss, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    rss_content = reparsed.toprettyxml(indent="  ")

    OUTPUT_FILE.write_text(rss_content, encoding='utf-8')
    print(f"Successfully wrote {len(recent_entries)} entries to {OUTPUT_FILE}")

# Load feed URLs from list.txt
def load_feed_urls():
    if not URLS_FILE.exists():
        print(f"Error: {URLS_FILE} not found!")
        return []

    with open(URLS_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    urls = load_feed_urls()
    if not urls:
        print("No feed URLs found. Exiting.")
        return

    print(f"Fetching {len(urls)} feeds...")
    combined_entries = combine_rss_feeds(urls)

    print(f"Combined {len(combined_entries)} unique entries. Generating feed...")
    create_rss_feed(combined_entries)

if __name__ == "__main__":
    main()