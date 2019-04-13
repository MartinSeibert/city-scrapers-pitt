from dateutil.parser import parse

from datetime import datetime
from os.path import dirname, join

import pytest
from freezegun import freeze_time
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response

from city_scrapers.spiders.pitt_ethics_board import PittEthicsBoardSpider

test_response = file_response(
    join(dirname(__file__), "files", "pitt_ethics_board.html"),
    url="http://pittsburghpa.gov/ehb/ehb-meetings",
)
spider = PittEthicsBoardSpider()

meetings = spider._build_datatable(test_response)

freezer = freeze_time("2019-03-29")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_meetings():
	
	assert len(meetings) > 0

def test_title():
	print("TITLE: " + parsed_items[0]["title"])
	assert parsed_items[0]["title"] == "Ethics Hearing Board Meeting"


# def test_description():
#     assert parsed_items[0]["description"] == "EXPECTED DESCRIPTION"


def test_start():
	assert parsed_items[0]["start"] == datetime(2019, 1, 10, 16, 0)
	

# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


# def test_time_notes():
#     assert parsed_items[0]["time_notes"] == "EXPECTED TIME NOTES"


# def test_id():
#     assert parsed_items[0]["id"] == "EXPECTED ID"


# def test_status():
#     assert parsed_items[0]["status"] == "EXPECTED STATUS"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "",
        "address": "Room 646 of the City-County Building, 414 Grant Street, Pittsburgh, PA 15219"
    }


def test_source():
    assert parsed_items[0]["source"] == "http://pittsburghpa.gov/ehb/ehb-meetings"


# def test_links():
#     assert parsed_items[0]["links"] == [{
#       "href": "EXPECTED HREF",
#       "title": "EXPECTED TITLE"
#     }]


# def test_classification():
#     assert parsed_items[0]["classification"] == NOT_CLASSIFIED


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
