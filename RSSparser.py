import argparse
import json
import os
import time

import feedparser
import requests

MAX_LINKS_TO_KEEP = 500

# Read lines from a file into a set
def read_links(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

# Append link to file and update set
def record_link(path, link, links_set):
    if link not in links_set:
        with open(path, 'a') as f:
            f.write(link + '\n')
        links_set.add(link)

# Trim file to most recent MAX_LINKS_TO_KEEP links
def trim_links(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        if len(lines) > MAX_LINKS_TO_KEEP:
            lines = lines[-MAX_LINKS_TO_KEEP:]
            with open(path, 'w') as f:
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
    headers = {'Content-Type': 'application/json'}
    for url in webhook_urls:
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException:
            return False
    return True

def main():
    parser = argparse.ArgumentParser(description='Process RSS feed and post payloads.')
    parser.add_argument('webhook_urls', nargs='+', help='Webhook URLs for posting')
    args = parser.parse_args()

    rss_url = "https://raw.githubusercontent.com/EndlessFractal/Threat-Intel-Feed/main/feed.xml"
    links_path = "posted_links.txt"
    posted_links = read_links(links_path)
    payloads = parse_and_format_rss(rss_url, 2000, posted_links)
    if not payloads:
        print("No new payloads.")
        return
    for payload in payloads:
        if send_payload(args.webhook_urls, payload, 5):
            # Record every link found in the payload content
            for line in payload["content"].splitlines():
                if line.startswith("http"):
                    record_link(links_path, line, posted_links)
    trim_links(links_path)

if __name__ == "__main__":
    main()
