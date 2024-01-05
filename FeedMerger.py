from datetime import datetime
from dateutil import parser as date_parser
from feedgen.feed import FeedGenerator
import concurrent.futures
import feedparser
import html
import pytz


# Function to convert datetime objects to UTC timezone
def convert_to_utc(dt):
    if dt:
        return dt.astimezone(pytz.utc)
    return datetime.min.replace(tzinfo=pytz.utc)  # Set a default UTC time


# Function to parse dates with timezone information
def parse_date_with_timezone(date_str):
    try:
        tzinfos = {
            "EDT": pytz.timezone("America/New_York"),
            "EST": pytz.timezone("America/New_York")
            }
        return date_parser.parse(date_str, tzinfos=tzinfos)
    except Exception as e:
        print(f"Error parsing date: {date_str}")
        print(e)
        return None


# Function to define the sorting key for entries
def sort_key(entry):
    if hasattr(entry, 'published'):
        pub_date = parse_date_with_timezone(entry.published)
        if pub_date:
            pub_date_utc = convert_to_utc(pub_date)
            return pub_date_utc
    return datetime.min.replace(tzinfo=pytz.utc)  # Set a default UTC time


# Function to fetch and combine RSS feeds using multithreading
def combine_rss_feeds(feed_urls):
    combined_feed = []

    def fetch_feed(url):
        try:
            feed = feedparser.parse(url)
            if 'entries' in feed:
                return feed.entries
            else:
                print(f"No entries found for URL: {url}")
                return []
        except Exception as e:
            print(f"An error occurred for URL: {url}")
            print(e)
            return []

    # Use multithreading to fetch articles from all feeds concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_feed, feed_urls)

    # Combine all entries into a single list
    for entries in results:
        combined_feed.extend(entries)

    # Sort the combined feed by publication date in ascending order
    combined_feed = sorted(combined_feed, key=sort_key, reverse=False)

    return combined_feed


def create_rss_feed(combined_feed):
    # Create an instance of FeedGenerator
    fg = FeedGenerator()
    fg.title("EndlessFractal's Threat Intel Feed")
    fg.description("A combined RSS feed of the 20 most recent articles from various sources")
    fg.link(href="https://raw.githubusercontent.com/EndlessFractal/hosts/main/feed.xml", rel="alternate")

    # Add the entries from the combined feed to the RSS feed
    for entry in combined_feed[-60:]:
        pub_date = convert_to_utc(parse_date_with_timezone(entry.published)) if hasattr(entry, 'published') else None

        fe = fg.add_entry()
        fe.title(html.unescape(entry.title))
        fe.link(href=entry.link)
        fe.published(pub_date) if pub_date else None

    # Generate the RSS feed XML and save it to a file
    rss_feed = fg.rss_str(pretty=True)
    with open('feed.xml', 'wb') as rss_file:
        rss_file.write(rss_feed)


def main():
    # Read RSS feed URLs from list.txt
    with open('list.txt', 'r') as file:
        feed_urls = [line.strip() for line in file]

    # Get the combined RSS feed with the 100 most recent articles from all feeds
    combined_feed = combine_rss_feeds(feed_urls)

    # Create an RSS feed from the combined entries and save it to a file
    create_rss_feed(combined_feed)


if __name__ == "__main__":
    main()
