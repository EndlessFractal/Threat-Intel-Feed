import argparse
import feedparser
import json
import requests
import time
import os


MAX_LINKS_TO_KEEP = 200


def read_posted_links(file_path):
    # Read the file containing posted links
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            posted_links = set(file.read().splitlines())
        return posted_links
    else:
        return set()


def write_posted_link(file_path, link):
    # Check if the link is already in the set
    if link not in read_posted_links(file_path):
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

    # Set to track URLs that are already in the payload (to avoid duplicates)
    formatted_urls = set()

    # Parse the RSS feed
    feed = feedparser.parse(url)

    # Iterate through entries in the feed
    for entry in feed.entries:
        title = entry.title
        entry_url = entry.link

        # Skip if the URL has already been posted or included in a previous payload
        if entry_url in posted_links or entry_url in formatted_urls:
            continue

        entry_text = f"{title}\n{entry_url}\n\n"
        entry_length = len(entry_text)

        # Check if adding the entry exceeds the character limit
        if current_length + entry_length <= max_char:
            formatted_content += entry_text
            current_length += entry_length
            formatted_urls.add(entry_url)
        else:
            # Add payload to the list and reset variables for a new payload
            payloads.append({"content": formatted_content})
            formatted_content = entry_text
            current_length = entry_length
            formatted_urls.add(entry_url)

    # Add the last payload if there is any remaining content
    if formatted_content:
        payloads.append({"content": formatted_content})

    return payloads


def send_payload_with_delay(webhook_urls, payload, delay):
    # Introduce a delay before sending each payload
    time.sleep(delay)
    # Set the headers for the HTTP request
    headers = {'Content-Type': 'application/json'}

    # Iterate over each webhook URL and send the payload
    for webhook_url in webhook_urls:
        # Send the POST request, raising an exception for any HTTP errors
        try:
            response = requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            # Return False if any request fails
            return False 
    
    # Return True if all requests were successful
    return True

def main():
    # Create command-line argument parser
    parser = argparse.ArgumentParser(description='Process RSS feed and send GitHub Actions payload.')
    # Add a command-line argument for the webhook URLs (space-separated)
    parser.add_argument('webhook_urls', nargs='+', help='Space-separated list of webhook URLs for posting messages')

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

    # Send payloads using the specified webhook URLs with a 5-second delay
    for payload in payloads:
        if send_payload_with_delay(args.webhook_urls, payload, 5):
            # If sent successfully, write the links from the payload to posted_links.txt
            for entry in payload["content"].split("\n"):
                if entry.startswith("http"):
                    write_posted_link(file_path, entry)

    trim_posted_links(file_path)


# Run the main function if the script is executed
if __name__ == "__main__":
    main()
