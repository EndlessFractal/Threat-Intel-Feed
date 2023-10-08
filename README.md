# EndlessFractal's Threat Intel Feed

Retrieves a list of domain names from various sources and filters them to create a consolidated list of unique domains. The filtered list is then saved to a file called `hosts.txt`.

## Description

The script performs the following steps:

1. The script starts by importing necessary libraries and modules.
2. It contains functions for handling date and time conversions, as well as parsing dates with time zones.
3. The main part of the script combines multiple RSS feeds from given URLs:
   - It fetches articles from these feeds concurrently.
   - Combines all the fetched articles into one list.
   - Sorts the list based on the publication dates of the articles, in ascending order.
4. After combining and sorting the articles, the script creates a new RSS feed with specific metadata:
   - It sets the title and description for the new feed.
   - Provides a link to the feed.
   - Adds the most recent 50 articles to the feed.
   - Generates an XML representation of the feed.
5. Finally, the script reads a list of RSS feed URLs from 'list.txt', combines the feeds, creates a new feed with the most recent articles, and saves it to 'feed.xml'.

## Usage

Just import the following link into your favorite RSS reader!

> https://raw.githubusercontent.com/EndlessFractal/Threat-Intel-Feed/main/feed.xml

## Sources

The script retrieves feeds from the following sources:

- [AT&T Cybersecurity Blog](https://cybersecurity.att.com/site/blog-all-rss)
- [Bitdefender Labs Blog](https://www.bitdefender.com/blog/api/rss/labs/)
- [Broadcom SED Blog](https://sed-cms.broadcom.com/rss/v1/blogs/rss.xml)
- [CIO Security Blog](https://www.cio.com/security/feed/)
- [CISA ICS Advisories](https://www.cisa.gov/cybersecurity-advisories/ics-advisories.xml)
- [CISA ICS Medical Advisories](https://www.cisa.gov/cybersecurity-advisories/ics-medical-advisories.xml)
- [Cloudflare Security Blog](https://blog.cloudflare.com/tag/security/rss)
- [CrowdStrike Blog](https://www.crowdstrike.com/blog/feed)
- [Darknet Blog](https://www.darknet.org.uk/feed/)
- [EclecticIQ Blog](https://blog.eclecticiq.com/rss.xml)
- [ESET Blog](https://blog.eset.com/feed)
- [Fortinet Threat Research Blog](https://feeds.fortinet.com/fortinet/blog/threat-research)
- [Google Project Zero Blog](https://googleprojectzero.blogspot.com/feeds/posts/default)
- [GovTech Cybersecurity Blog](https://www.govtech.com/blogs/lohrmann-on-cybersecurity.rss)
- [Graham Cluley's Blog](https://www.grahamcluley.com/feed/)
- [HackerOne Blog](https://www.hackerone.com/blog.rss)
- [Hackmageddon Blog](https://www.hackmageddon.com/feed/)
- [IBM Security Intelligence Blog](https://securityintelligence.com/feed/)
- [Infosecurity Magazine News](https://www.infosecurity-magazine.com/rss/news/)
- [Intezer Research Blog](https://intezer.com/blog/research/feed/)
- [Kaspersky Securelist Blog](https://securelist.com/feed/)
- [KrebsOnSecurity Blog](https://krebsonsecurity.com/feed/)
- [Malwarebytes Blog](https://blog.malwarebytes.com/feed/)
- [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/feed/)
- [Nao-Sec Blog](https://nao-sec.org/feed.xml)
- [NIST Cybersecurity Insights](https://www.nist.gov/blogs/cybersecurity-insights/rss.xml)
- [Palo Alto Networks Unit 42 Blog](https://unit42.paloaltonetworks.com//feed)
- [Proofpoint Blog](https://www.proofpoint.com/us/blog)
- [Recorded Future Blog](https://www.recordedfuture.com/feed)
- [SANS Internet Storm Center Blog](https://isc.sans.edu/rssfeed_full.xml)
- [Schneier on Security Blog](https://www.schneier.com/blog/atom.xml)
- [Sebdraven's Medium Blog](https://sebdraven.medium.com/feed)
- [Security Affairs Blog](https://securityaffairs.co//feed)
- [SensePost Blog](https://sensepost.com/rss.xml)
- [SentinelOne Blog](https://www.sentinelone.com/feed/)
- [SOC Prime Blog](https://socprime.com/feed/)
- [Sophos News Blog](https://news.sophos.com/feed/)
- [Talos Intelligence Blog](https://blog.talosintelligence.com/rss/)
- [TechRepublic Security News](https://www.techrepublic.com/rssfeeds/topic/security/)
- [The CyberWire Blog](https://thecyberwire.com/feeds/rss.xml)
- [The Guardian Technology Security](https://www.theguardian.com/technology/data-computer-security/rss)
- [The Hacker News Blog](https://thehackernews.com/feeds/posts/default)
- [The Record Media Blog](https://therecord.media//feed)
- [Threatpost Blog](https://threatpost.com/feed/)
- [Troy Hunt's Blog](https://www.troyhunt.com/rss/)
- [UpGuard Blog](https://www.upguard.com/blog/rss.xml)
- [US-CERT Alerts](https://us-cert.cisa.gov/ncas/alerts.xml)
- [US-CERT Analysis Reports](https://us-cert.cisa.gov/ncas/analysis-reports.xml)
- [US-CERT Current Activity](https://us-cert.cisa.gov/ncas/current-activity.xml)
