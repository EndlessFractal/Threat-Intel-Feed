# EndlessFractal's Threat Intel Feed

This automated feed retrieves a list of feeds from various sources, consolidates them and saves to a file called `feed.xml`.

## Files

- `FeedMerger.py` - Combines multiple RSS feeds into a single feed and saves it as an XML file.
- `RSSparser.py` - Parses an RSS feed, formats new entries as payloads, and sends them to specified webhook URLs with a delay between each post.

## Usage

Just import the following link into your favorite RSS reader!

> https://raw.githubusercontent.com/EndlessFractal/Threat-Intel-Feed/main/feed.xml

## Sources

The script retrieves feeds from the following sources:

- [AhnLab ASEC Feed](https://asec.ahnlab.com/en/feed)
- [AT&T Cybersecurity Blog](https://cybersecurity.att.com/site/blog-all-rss)
- [Bitdefender Labs Blog](https://bitdefender.com/blog/api/rss/labs)
- [Broadcom SED Blog](https://sed-cms.broadcom.com/rss/v1/blogs/rss.xml)
- [CISA Cybersecurity Alerts](https://cisa.gov/cybersecurity-advisories/all.xml)
- [Cloudflare Security Blog](https://blog.cloudflare.com/tag/security/rss)
- [CrowdStrike Blog](https://crowdstrike.com/blog/feed)
- [Darknet Blog](https://www.darknet.org.uk/feed)
- [EclecticIQ Blog](https://blog.eclecticiq.com/rss.xml)
- [Fortinet Threat Research Blog](https://feeds.fortinet.com/fortinet/blog/threat-research)
- [Google Project Zero Blog](https://googleprojectzero.blogspot.com/feeds/posts/default)
- [GovTech Cybersecurity Blog](https://govtech.com/blogs/lohrmann-on-cybersecurity.rss)
- [Graham Cluley's Blog](https://grahamcluley.com/feed)
- [Infosecurity Magazine News](https://infosecurity-magazine.com/rss/news)
- [Kaspersky Securelist Blog](https://securelist.com/feed)
- [KrebsOnSecurity Blog](https://krebsonsecurity.com/feed)
- [Malwarebytes Blog](https://blog.malwarebytes.com/feed)
- [Microsoft Security Blog](https://microsoft.com/en-us/security/blog/feed)
- [Nao-Sec Blog](https://nao-sec.org/feed.xml)
- [NIST Cybersecurity Insights](https://nist.gov/blogs/cybersecurity-insights/rss.xml)
- [Palo Alto Networks Unit 42 Blog](https://unit42.paloaltonetworks.com/feed)
- [Recorded Future Blog](https://www.recordedfuture.com/feed)
- [SANS Internet Storm Center Blog](https://isc.sans.edu/rssfeed_full.xml)
- [Schneier on Security Blog](https://schneier.com/blog/atom.xml)
- [Security Affairs Blog](https://securityaffairs.co/feed)
- [SensePost Blog](https://sensepost.com/rss.xml)
- [SentinelOne Blog](https://sentinelone.com/feed)
- [SOC Prime Blog](https://socprime.com/feed)
- [Sophos News Blog](https://news.sophos.com/feed)
- [Talos Intelligence Blog](https://blog.talosintelligence.com/rss)
- [TechRepublic Security News](https://techrepublic.com/rssfeeds/topic/security)
- [The Guardian Technology Security](https://theguardian.com/technology/data-computer-security/rss)
- [The Hacker News Blog](https://thehackernews.com/feeds/posts/default)
- [The Record Media Blog](https://therecord.media/feed)
- [Threatpost Blog](https://threatpost.com/feed)
- [Troy Hunt's Blog](https://troyhunt.com/rss)
- [US-DOJ Press Releases](https://www.justice.gov/news/rss?type[1]=press_release&field_component=39901)
