import argparse
import feedparser
import json
import requests
import time
import os


MAX_LINKS_TO_KEEP = 100


def read_posted_links(file_path):
    # Read the file containing posted links
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            posted_links = file.read().splitlines()
        return set(posted_links)
    else:
        return set()


def write_posted_link(file_path, link):
    # Write the newly posted link to the file
    with open(file_path, 'a') as file:
        file.write(link + '\n')


def trim_posted_links(file_path):
    # Read the file containing posted links
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            posted_links = file.read().splitlines()

        # Keep only the most recent MAX_LINKS_TO_KEEP links
        if len(posted_links) > MAX_LINKS_TO_KEEP:
            posted_links = posted_links[-MAX_LINKS_TO_KEEP:]

        # Write the trimmed links back to the file
        with open(file_path, 'w') as file:
            file.write('\n'.join(posted_links) + '\n')


def parse_and_format_rss(url, max_char, posted_links):
    # Initialize the list to store payloads
    payloads = []
    # Initialize variables to track formatted content and its length
    formatted_content = ""
    current_length = 0

    # Parse the RSS feed
    feed = feedparser.parse(url)

    # Iterate through entries in the feed
    for entry in feed.entries:
        title = entry.title
        entry_url = entry.link

        # Check if the link has already been posted
        if entry_url in posted_links:
            continue

        entry_text = f"{title}\n{entry_url}\n\n"
        entry_length = len(entry_text)

        # Check if adding the entry exceeds the character limit
        if current_length + entry_length <= max_char:
            formatted_content += entry_text
            current_length += entry_length
            # Mark the link as posted
            write_posted_link("posted_links.txt", entry_url)
        else:
            # Add payload to the list and reset variables for a new payload
            payloads.append({"content": formatted_content})
            formatted_content = entry_text
            current_length = entry_length
            # Mark the link as posted
            write_posted_link("posted_links.txt", entry_url)

    # Add the last payload if there is any remaining content
    if formatted_content:
        payloads.append({"content": formatted_content})

    # Trim the posted links to keep only the most recent ones
    trim_posted_links("posted_links.txt")

    return payloads


def send_payload_with_delay(webhook_url, payload, delay):
    # Introduce a delay before sending each payload
    time.sleep(delay)
    # Set the headers for the HTTP request
    headers = {'Content-Type': 'application/json'}
    # Send the payload to the webhook URL using the requests library
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    # Raise an exception for any HTTP errors
    response.raise_for_status()


def main():
    # Create command-line argument parser
    parser = argparse.ArgumentParser(description='Process RSS feed and send GitHub Actions payload.')
    # Add a command-line argument for the webhook URL
    parser.add_argument('webhook_url', help='Webhook URL for posting messages')
    # Parse command-line arguments
    args = parser.parse_args()

    # RSS feed URL
    rss_url = "https://raw.githubusercontent.com/EndlessFractal/Threat-Intel-Feed/main/feed.xml"

    # File path to store posted links
    file_path = "posted_links.txt"

    # Read the already posted links
    posted_links = read_posted_links(file_path)

    # Parse and format the RSS feed, avoiding duplicate links
    payloads = parse_and_format_rss(rss_url, 2000, posted_links)

    # Check if there are any payloads
    if not payloads:
        print("No new payloads found.")
        return

    # Send payloads using the specified webhook URL with a 5-second delay
    for i, payload in enumerate(payloads, start=1):
        send_payload_with_delay(args.webhook_url, payload, 5)


# Run the main function if the script is executed
if __name__ == "__main__":
    main()
