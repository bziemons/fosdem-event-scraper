from datetime import datetime

import pytz as pytz
import scrapy


class FosdemEventSpider(scrapy.Spider):
    name = "fosdem-event"

    def start_requests(self):
        with open("/home/ben/Sync/FOSDEM_talks.txt", "r") as fhandle:
            for url in map(str.rstrip, fhandle.readlines()):
                yield scrapy.Request(url=url)

    def parse(self, response):
        ret = dict()
        for info_element in response.css("ul.side-box > li"):
            infoid = info_element.css("strong::text").extract_first().lower()
            ret[infoid] = info_element.css("a::text").extract_first()

        ret['title'] = response.css("#pagetitles h1::text").extract_first()
        ret['url'] = response.url
        ret['time'] = datetime.now(pytz.UTC)
        yield ret
