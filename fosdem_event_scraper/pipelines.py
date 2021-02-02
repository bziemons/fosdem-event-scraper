# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import typing
from datetime import time, datetime

import icalendar
import pytz

from fosdem_event_scraper.settings import (
    ICAL_EVENT_UID,
    ICAL_LOCATION_FORMAT,
    ICAL_SUMMARY_FORMAT,
    ICAL_OUTPUT_FILE,
    UID_REPLACEMENTS,
    FOSDEM_DAY_TO_ISODATE,
    ICAL_DESCRIPTION_FORMAT,
)


def attach_event_time(
    event: icalendar.Event, item: typing.Dict, day_mapping: typing.Dict
):
    event.add("dtstamp", item["time"], encode=True)

    fosdem_tzinfo = pytz.timezone("Europe/Brussels")
    day = item["day"].casefold()
    if day in day_mapping:
        day = day_mapping[day]
    else:
        raise RuntimeError("unknown day: " + item["day"])

    startsplit = item["start"].split(":", maxsplit=1)
    starttime = time(int(startsplit[0]), int(startsplit[1]))

    endsplit = item["end"].split(":", maxsplit=1)
    endtime = time(int(endsplit[0]), int(endsplit[1]))

    event.add(
        "dtstart", datetime.combine(day, starttime, tzinfo=fosdem_tzinfo), encode=True
    )
    event.add(
        "dtend", datetime.combine(day, endtime, tzinfo=fosdem_tzinfo), encode=True
    )


class FosdemEventToCalenderPipeline:
    file = None
    cal = None
    day_to_isodate = {}

    def get_day_mapping(self):
        if not self.day_to_isodate:
            self.day_to_isodate = {
                day.casefold(): datetime.fromisoformat(isostr)
                for day, isostr in FOSDEM_DAY_TO_ISODATE.items()
            }
        return self.day_to_isodate

    def open_spider(self, spider):
        self.file = open(ICAL_OUTPUT_FILE, "w")
        self.cal = icalendar.Calendar()

    def close_spider(self, spider):
        self.file.write(self.cal.to_ical().decode("utf-8"))
        self.file.close()

    def process_item(self, item, spider):
        event = icalendar.Event()
        attach_event_time(event, item, self.get_day_mapping())
        event.add("summary", ICAL_SUMMARY_FORMAT.format(title=item["title"]))
        event.add(
            "location",
            ICAL_LOCATION_FORMAT.format(room=item["room"], track=item["track"]),
        )
        uid = item["title"].casefold()
        for replacement_tuple in UID_REPLACEMENTS:
            uid = uid.replace(*replacement_tuple)
        uid = uid.strip("_")
        uid = "event_" + re.sub(r"__+", "_", uid)
        assert uid.isidentifier(), f"uid [{repr(uid)}] must be an identifier string"
        event.add("uid", ICAL_EVENT_UID.format(uid=uid))
        event.add("sequence", 1)
        event.add("url", item["url"])
        event.add("description", ICAL_DESCRIPTION_FORMAT.format(url=item["url"]))
        self.cal.add_component(event)
        return item
