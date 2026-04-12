import argparse
import json
from pathlib import Path
import time

import feedparser
import requests

MAX_LINKS_TO_KEEP = 200
MAX_PAYLOAD_CHARS = 2000
DELAY_BETWEEN_PAYLOADS = 5

RSS_URL = "https://raw.githubusercontent.com/EndlessFractal/Threat-Intel-Feed/main/feed.xml"
LINKS_PATH = Path("posted_links.txt")

# Read lines from a file into a set
def read_links(path):
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    return set()

# Append link to file and update set
def record_link(path, link, links_set):
    if link not in links_set:
        with path.open("a", encoding="utf-8") as f:
            f.write(link + "\n")
        links_set.add(link)

# Trim file to most recent MAX_LINKS_TO_KEEP links
def trim_links(path):
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        if len(lines) > MAX_LINKS_TO_KEEP:
            lines = lines[-MAX_LINKS_TO_KEEP:]
            with path.open("w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")

# Parse feed and format payloads with a char limit
def parse_and_format_rss(url, max_char, posted):
    payloads = []
    content = ""
    curr_len = 0
    used_urls = set()
    feed = feedparser.parse(url)
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        if link in posted or link in used_urls:
            continue
        text = f"{title}\n{link}\n\n"
        text_len = len(text)
        if curr_len + text_len <= max_char:
            content += text
            curr_len += text_len
            used_urls.add(link)
        else:
            payloads.append({"content": content})
            content = text
            curr_len = text_len
            used_urls.add(link)
    if content:
        payloads.append({"content": content})
    return payloads

# Send payloads to each webhook URL with delay
def send_payload(webhook_urls, payload, delay):
    time.sleep(delay)
    data = json.dumps(payload)

    headers = {"Content-Type": "application/json"}

    for url in webhook_urls:
        try:
            response = requests.post(
                url, data=data, headers=headers, timeout=10
            )
            if response.status_code >= 400:
                print(f"HTTP error posting to {url}: {response.status_code}")
                return False
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error posting to {url} (attempt 1/1): {e}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"Request error posting to {url} (attempt 1/1): {e}")
            return False
        except Exception as e:
            print(f"Unexpected error posting to {url} (attempt 1/1): {e}")
            return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Process RSS feed and post payloads.")
    parser.add_argument("webhook_urls", nargs="+", help="Webhook URLs for posting")
    args = parser.parse_args()

    posted_links = read_links(LINKS_PATH)
    payloads = parse_and_format_rss(RSS_URL, MAX_PAYLOAD_CHARS, posted_links)

    if not payloads:
        print("No new payloads.")
        return

    for payload in payloads:
        if send_payload(args.webhook_urls, payload, DELAY_BETWEEN_PAYLOADS):
            # Record every link found in the payload content
            for line in payload["content"].splitlines():
                if line.startswith("http"):
                    record_link(LINKS_PATH, line, posted_links)
            trim_links(LINKS_PATH)

if __name__ == "__main__":
    main()