from datetime import datetime
from dateutil import parser as date_parser
from feedgen.feed import FeedGenerator
import concurrent.futures
import feedparser
import html
import pytz


# Function to convert datetime objects to UTC timezone
def convert_to_utc(dt):
    return dt.astimezone(pytz.utc) if dt else datetime.min.replace(tzinfo=pytz.utc)


# Function to parse dates with timezone information
def parse_date_with_timezone(date_str):
    try:
        tzinfos = {
            "EDT": pytz.timezone("America/New_York"),
            "EST": pytz.timezone("America/New_York")
        }
        return date_parser.parse(date_str, tzinfos=tzinfos)
    except Exception as e:
        print(f"Error parsing date: {date_str} - {e}")
        return None


# Function to define the sorting key for entries
def sort_key(entry):
    if 'published' in entry:
        pub_date = parse_date_with_timezone(entry.published)
        if pub_date:
            return convert_to_utc(pub_date)
    return datetime.min.replace(tzinfo=pytz.utc)


# Function to fetch and combine RSS feeds using multithreading
def combine_rss_feeds(feed_urls):
    combined_feed = []
    unique_urls = set()

    def fetch_feed(url):
        try:
            feed = feedparser.parse(url)
            if 'entries' in feed:
                return [entry for entry in feed.entries if entry.link not in unique_urls]
            else:
                print(f"No entries found for URL: {url}")
        except Exception as e:
            print(f"An error occurred for URL: {url} - {e}")
        return []

    # Use multithreading to fetch articles from all feeds concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_feed, feed_urls)

    # Combine all entries into a single list
    for entries in results:
        for entry in entries:
            if entry.link not in unique_urls:
                unique_urls.add(entry.link)
                combined_feed.append(entry)

    # Sort the combined feed by publication date in ascending order
    return sorted(combined_feed, key=sort_key)


# Function to create an RSS feed from combined entries and save it to a file
def create_rss_feed(combined_feed):
    fg = FeedGenerator()
    fg.title("EndlessFractal's Threat Intel Feed")
    fg.description("A combined RSS feed of the 60 most recent articles from various sources")
    fg.link(href="https://raw.githubusercontent.com/EndlessFractal/hosts/main/feed.xml", rel="alternate")

    for entry in combined_feed[-60:]:
        pub_date = convert_to_utc(parse_date_with_timezone(entry.published)) if 'published' in entry else None

        fe = fg.add_entry()
        fe.title(html.unescape(entry.title))
        fe.link(href=entry.link)
        if pub_date:
            fe.published(pub_date)

    # Generate the RSS feed XML and save it to a file
    rss_feed = fg.rss_str(pretty=True)
    with open('feed.xml', 'wb') as rss_file:
        rss_file.write(rss_feed)


def main():
    # Read RSS feed URLs from list.txt
    with open('list.txt', 'r') as file:
        feed_urls = [line.strip() for line in file]

    # Get the combined RSS feed with the most recent articles from all feeds
    combined_feed = combine_rss_feeds(feed_urls)

    # Create an RSS feed from the combined entries and save it to a file
    create_rss_feed(combined_feed)


if __name__ == "__main__":
    main()
