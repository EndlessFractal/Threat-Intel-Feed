# EndlessFractal's Threat Intel Feed

An automated pipeline that aggregates 30+ cybersecurity and threat-intel RSS feeds into a single combined feed (`feed.xml`), and optionally pushes new entries to webhooks.

**Subscribe directly in your RSS reader:**
> https://endlessfractal.github.io/Threat-Intel-Feed/feed.xml

## What it aggregates

Feeds are pulled from `list.txt` and merged, deduplicated by link, and sorted by publish date. The 60 most recent entries are kept. Sources include:

- AhnLab ASEC, Bitdefender Labs, Broadcom SED, CISA Alerts, Cloudflare Security
- CrowdStrike, EclecticIQ, Fortinet Threat Research, Google Project Zero
- GovTech Cybersecurity, Graham Cluley, Infosecurity Magazine, Kaspersky Securelist
- KrebsOnSecurity, Malwarebytes, Maryland MCAC, Microsoft Security, Nao-Sec
- NIST Cybersecurity Insights, Palo Alto Unit 42, Recorded Future, SANS ISC
- Schneier on Security, Security Affairs, SensePost, SentinelOne, SOC Prime
- Sophos News, Talos Intelligence, TechRepublic Security, The Guardian Security
- The Hacker News, The Record, Threatpost, Troy Hunt

Full list with links: see [`list.txt`](list.txt).

## Files

| File | Purpose |
|---|---|
| `FeedMerger.py` | Fetches all feeds in `list.txt` in parallel, dedupes by link, sorts by date, and writes the combined feed to `feed.xml`. |
| `RSSparser.py` | Reads `feed.xml`, finds entries not yet posted (tracked in `posted_links.txt`), and sends them as JSON payloads to one or more webhook URLs with a delay between posts. |
| `list.txt` | Plain list of source feed URLs, one per line. |
| `posted_links.txt` | History of links already sent by `RSSparser.py`, used to avoid duplicate posts. |

## Install & run

Requires Python 3.9+.

```bash
git clone https://github.com/EndlessFractal/Threat-Intel-Feed.git
cd Threat-Intel-Feed
pip install -r requirements.txt
```

**Merge feeds into `feed.xml`:**
```bash
python FeedMerger.py
```

**Parse `feed.xml` and post new entries to webhook(s):**
```bash
python RSSparser.py https://your-webhook-url-1 https://your-webhook-url-2
```

In production, both scripts are typically run on a schedule (e.g. a GitHub Actions cron job every couple of hours) so `feed.xml` stays fresh and new entries get posted automatically.

## Example

**Input** - one line in `list.txt`:
```
https://thehackernews.com/feeds/posts/default
```

**Output** - a merged entry in `feed.xml`:
```xml
<item>
  <title>AI Agent Exploits Langflow RCE to Automate Database Ransomware Attack</title>
  <link>https://thehackernews.com/2026/07/ai-agent-exploits-langflow-rce-to.html</link>
  <pubDate>Thu, 02 Jul 2026 09:13:13 +0000</pubDate>
</item>
```

If a webhook is configured, `RSSparser.py` sends that same entry as:
```json
{"content": "AI Agent Exploits Langflow RCE to Automate Database Ransomware Attack\nhttps://thehackernews.com/2026/07/ai-agent-exploits-langflow-rce-to.html\n\n"}
```

## Adding a new feed source

1. Add the feed's URL to `list.txt` (one URL per line, no trailing slash needed).
2. Re-run `FeedMerger.py` to confirm it fetches and parses correctly.
3. Optionally add it to the source list above for documentation purposes.

Feeds that fail to fetch (timeouts, HTTP errors, etc.) are retried automatically and skipped if they still fail - a broken source won't break the whole run.

## License & support

Licensed under [GPL-3.0](LICENSE). Issues and PRs are welcome via GitHub.