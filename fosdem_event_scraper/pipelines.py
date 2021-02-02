# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import typing
from datetime import date, time, datetime

import icalendar
import pytz


def attach_event_time(event: icalendar.Event, item: typing.Dict):
    event.add('dtstamp', item['time'], encode=True)

    fosdem_tzinfo = pytz.timezone('Europe/Brussels')
    if item['day'].lower() == "saturday":
        day = date(2019, 2, 2)
    elif item['day'].lower() == "sunday":
        day = date(2019, 2, 3)
    else:
        raise RuntimeError("unknown day: " + item['day'])

    startsplit = item['start'].split(":", maxsplit=1)
    starttime = time(int(startsplit[0]), int(startsplit[1]))

    endsplit = item['end'].split(":", maxsplit=1)
    endtime = time(int(endsplit[0]), int(endsplit[1]))

    event.add('dtstart', datetime.combine(day, starttime, tzinfo=fosdem_tzinfo), encode=True)
    event.add('dtend', datetime.combine(day, endtime, tzinfo=fosdem_tzinfo), encode=True)


class FosdemEventToCalenderPipeline:
    file = None
    cal = None

    def open_spider(self, spider):
        self.file = open('fosdem_events.ical', 'w')
        self.cal = icalendar.Calendar()

    def close_spider(self, spider):
        self.file.write(self.cal.to_ical().decode("utf-8"))
        self.file.close()

    def process_item(self, item, spider):
        event = icalendar.Event()
        attach_event_time(event, item)
        event.add("summary", item['title'])
        event.add("location", item['room'] + " -- " + item['track'])
        uid = item['title'].casefold() \
            .replace(":", "") \
            .replace("'", "") \
            .replace("!", "") \
            .replace("?", "") \
            .replace(",", "") \
            .replace("(", "") \
            .replace(")", "") \
            .replace("&", " and ") \
            .replace("/", " and or ") \
            .replace(" ", "_") \
            .replace(".", "_") \
            .replace("-", "_") \
            .replace("—", "_") \
            .strip("_")
        uid = "event_" + re.sub(r'__+', "_", uid)
        assert uid.isidentifier(), "uid [" + repr(uid) + "] must be an identifier string"
        event.add("uid", uid + "@fosdem.org/2019")
        event.add("sequence", 1)
        event.add("url", item['url'])
        self.cal.add_component(event)
        return item
