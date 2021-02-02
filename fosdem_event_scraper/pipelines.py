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
    FOSDEM_SATURDAY_ISODATE,
    FOSDEM_SUNDAY_ISODATE,
    UID_REPLACEMENTS,
)


def attach_event_time(event: icalendar.Event, item: typing.Dict):
    event.add("dtstamp", item["time"], encode=True)

    fosdem_tzinfo = pytz.timezone("Europe/Brussels")
    if item["day"].lower() == "saturday":
        day = datetime.fromisoformat(FOSDEM_SATURDAY_ISODATE)
    elif item["day"].lower() == "sunday":
        day = datetime.fromisoformat(FOSDEM_SUNDAY_ISODATE)
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

    def open_spider(self, spider):
        self.file = open(ICAL_OUTPUT_FILE, "w")
        self.cal = icalendar.Calendar()

    def close_spider(self, spider):
        self.file.write(self.cal.to_ical().decode("utf-8"))
        self.file.close()

    def process_item(self, item, spider):
        event = icalendar.Event()
        attach_event_time(event, item)
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
        self.cal.add_component(event)
        return item
