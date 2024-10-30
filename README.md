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

- [AhnLab ASEC Feed](https://asec.ahnlab.com/en/feed/)
- [AT&T Cybersecurity Blog](https://cybersecurity.att.com/site/blog-all-rss)
- [Bitdefender Labs Blog](https://www.bitdefender.com/blog/api/rss/labs/)
- [Broadcom SED Blog](https://sed-cms.broadcom.com/rss/v1/blogs/rss.xml)
- [CISA ICS Advisories](https://www.cisa.gov/cybersecurity-advisories/ics-advisories.xml)
- [CISA ICS Medical Advisories](https://www.cisa.gov/cybersecurity-advisories/ics-medical-advisories.xml)
- [Cloudflare Security Blog](https://blog.cloudflare.com/tag/security/rss)
- [CrowdStrike Blog](https://www.crowdstrike.com/blog/feed)
- [Darknet Blog](https://www.darknet.org.uk/feed/)
- [DataBreachToday](https://www.databreachtoday.com/rss-feeds)
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
- [Infostealers by Hudson Rock Blog](https://www.infostealers.com/learn-info-stealers/feed/)
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
- [US-CERT Alerts](https://us-cert.cisa.gov/ncas/alerts.xml)
- [US-CERT Analysis Reports](https://us-cert.cisa.gov/ncas/analysis-reports.xml)
- [US-CERT Current Activity](https://us-cert.cisa.gov/ncas/current-activity.xml)
- [US-DOJ Cybercrime News](https://www.justice.gov/news/rss?f[0]=facet_topics:3911)
