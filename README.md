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

## Sources

The script retrieves feeds from the following sources:

- [AT&T Cybersecurity Blog](https://cybersecurity.att.com/site/blog-all-rss)
- [Bitdefender Labs Blog](https://www.bitdefender.com/blog/api/rss/labs/)
- [Broadcom Security Blog](https://sed-cms.broadcom.com/rss/v1/blogs/rss.xml)
- [CIO Security News](https://www.cio.com/security/feed/)
- [CISA - ICS Medical Advisories](https://www.cisa.gov/cybersecurity-advisories/ics-medical-advisories.xml)
- [CISA - Industrial Control Systems Advisories](https://www.cisa.gov/cybersecurity-advisories/ics-advisories.xml)
- [CISA - National Cyber Awareness System Alerts](https://us-cert.cisa.gov/ncas/alerts.xml)
- [CISA - National Cyber Awareness System Analysis Reports](https://us-cert.cisa.gov/ncas/analysis-reports.xml)
- [CISA - National Cyber Awareness System Current Activity](https://us-cert.cisa.gov/ncas/current-activity.xml)
- [Cisco Talos Blog](https://feeds.feedburner.com/feedburner/Talos)
- [Cloudflare Blog - Security](https://blog.cloudflare.com/tag/security/rss)
- [CrowdStrike Blog - Threat Intel & Research](https://www.crowdstrike.com/blog/category/threat-intel-research/feed)
- [Darknet - Ethical Hacking & Cyber Security](https://www.darknet.org.uk/feed/)
- [EclecticIQ Blog](https://blog.eclecticiq.com/rss.xml)
- [ESET WeLiveSecurity Blog](https://www.welivesecurity.com/en/rss/feed/)
- [Fortinet Threat Research Blog](https://feeds.fortinet.com/fortinet/blog/threat-research&x=1)
- [Google Online Security Blog](https://feeds.feedburner.com/GoogleOnlineSecurityBlog)
- [Google Project Zero Blog](https://googleprojectzero.blogspot.com/feeds/posts/default)
- [GovTech Blog - Lohrmann on Infrastructure](https://feeds.feedburner.com/govtech/blogs/lohrmann_on_infrastructure)
- [Graham Cluley's Blog](https://www.grahamcluley.com/feed/)
- [HackerOne Blog](https://www.hackerone.com/blog.rss)
- [Hackmageddon Blog](https://www.hackmageddon.com/feed/)
- [IBM Security Intelligence Blog](https://securityintelligence.com/feed/)
- [Infosecurity Magazine News](https://www.infosecurity-magazine.com/rss/news/)
- [Intezer Research Blog](https://intezer.com/blog/research/feed/)
- [Kaspersky Securelist Blog](https://securelist.com/feed/)
- [Krebs on Security](https://krebsonsecurity.com/feed/)
- [Malwarebytes Blog](https://blog.malwarebytes.com/feed/)
- [Microsoft Security Blog](https://www.microsoft.com/security/blog/feed/)
- [NAO Security Blog](https://nao-sec.org/feed)
- [NIST Cybersecurity Insights Blog](https://www.nist.gov/blogs/cybersecurity-insights/rss.xml)
- [Palo Alto Networks Unit 42 Blog](https://feeds.feedburner.com/Unit42)
- [Proofpoint Blog](https://www.proofpoint.com/us/rss.xml)
- [Recorded Future Blog](https://www.recordedfuture.com/feed)
- [SANS Internet Storm Center](https://isc.sans.edu/rssfeed_full.xml)
- [Schneier on Security Blog](https://www.schneier.com/blog/atom.xml)
- [Sebdraven's Blog](https://sebdraven.medium.com/feed)
- [Secureworks Blog - Research & Intelligence](https://www.secureworks.com/rss?feed=blog&category=research-intelligence)
- [Security Affairs Blog](https://securityaffairs.co/feed)
- [SensePost Blog](https://sensepost.com/rss.xml)
- [SentinelOne Labs Blog](https://www.sentinelone.com/labs/feed/)
- [SOC Prime Blog](https://socprime.com/blog/feed/)
- [Sophos Naked Security Blog](https://nakedsecurity.sophos.com/feed/)
- [TechRepublic Security News](https://www.techrepublic.com/rssfeeds/topic/security/?feedType=rssfeeds)
- [The CyberWire Blog](https://thecyberwire.com/feeds/rss.xml)
- [The Guardian - Data & Computer Security News](https://www.theguardian.com/technology/data-computer-security/rss)
- [The Hackers News](https://feeds.feedburner.com/TheHackersNews)
- [The Record Media](https://therecord.media/feed/)
- [Threatpost Blog](https://threatpost.com/feed/)
- [Troy Hunt's Blog](https://www.troyhunt.com/rss/)
- [UpGuard Data Breaches](https://www.upguard.com/breaches/rss.xml)
- [UpGuard News](https://www.upguard.com/news/rss.xml)
