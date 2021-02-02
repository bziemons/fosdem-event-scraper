# -*- coding: utf-8 -*-

# Scrapy settings for fosdem_event_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "fosdem_event_scraper"

SPIDER_MODULES = ["fosdem_event_scraper.spiders"]
NEWSPIDER_MODULE = "fosdem_event_scraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'fosdem_event_scraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'fosdem_event_scraper.middlewares.FosdemEventScraperSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'fosdem_event_scraper.middlewares.FosdemEventScraperDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "fosdem_event_scraper.pipelines.FosdemEventToCalenderPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


###
# FOSDEM event scraper specific settings
###

# a text file with one link to a FOSDEM event per line
INPUT_FILE = "fosdem_event_urls.txt"

# the output file to write
ICAL_OUTPUT_FILE = "fosdem_events.ical"

# the iCal event uid format string, where {uid} is replaced with the FOSDEM event uid
# depending on the calendar software this should make updates on existing events possible
ICAL_EVENT_UID = "{uid}@fosdem.org/2021"

# the format of the location text for the event
# {room} and {track} are replaced with what was found on the event page
ICAL_LOCATION_FORMAT = "{room} -- {track}"

# the format of the summary (title) for the event
# {title} is replaced with what was found on the event page
ICAL_SUMMARY_FORMAT = "{title}"

# the format of the description for the event
# {url} is replaced with the event page URL
ICAL_DESCRIPTION_FORMAT = "Event URL: {url}"

# ISO dates for the FOSDEM dates
FOSDEM_DAY_TO_ISODATE = {
    "saturday": "2021-02-06",
    "sunday": "2021-02-07",
}

# all replacements that needs to be done on a title to be safe to use as an uid
# underscores will be stripped from start/end and multiple underscores will be replaced with a single underscore
UID_REPLACEMENTS = [
    (":", ""),
    ("'", ""),
    ("’", ""),
    ("!", ""),
    ("?", ""),
    (",", ""),
    ("(", ""),
    (")", ""),
    ("+", "plus"),
    ("&", "_and_"),
    ("/", "_and_or_"),
    (" ", "_"),
    (".", "_"),
    ("-", "_"),
    ("—", "_"),
]
