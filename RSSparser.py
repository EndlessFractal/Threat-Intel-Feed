import argparse
import feedparser
import json
import requests
import time


def parse_and_format_rss(url, max_char):
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
        entry_text = f"{title}\n{entry_url}\n\n"
        entry_length = len(entry_text)

        # Check if adding the entry exceeds the character limit
        if current_length + entry_length <= max_char:
            formatted_content += entry_text
            current_length += entry_length
        else:
            # Add payload to the list and reset variables for a new payload
            payloads.append({"content": formatted_content})
            formatted_content = entry_text
            current_length = entry_length

    # Add the last payload if there is any remaining content
    if formatted_content:
        payloads.append({"content": formatted_content})

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

    # Parse and format the RSS feed
    payloads = parse_and_format_rss(rss_url, 2000)

    # Check if there are any payloads
    if not payloads:
        print("No payloads found.")
        return

    # Send payloads using the specified webhook URL with a 5-second delay
    for i, payload in enumerate(payloads, start=1):
        send_payload_with_delay(args.webhook_url, payload, 5)


# Run the main function if the script is executed
if __name__ == "__main__":
    main()
