from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class PittEthicsBoardSpider(CityScrapersSpider):
    name = "pitt_ethics_board"
    agency = "Pittsburgh Ethics Hearing Board"
    timezone = "America/New_York"
    allowed_domains = ["pittsburghpa.gov"]
    start_urls = ["http://pittsburghpa.gov/ehb/ehb-meetings"]

    def _get_address(self, response):
        address = (response.css('p::text').extract()[0])
        return address


    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        address = self._get_address(response)
        item = ""
        meeting = Meeting(
            title=self._parse_title(item),
                description=self._parse_description(item),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(address),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )


        yield meeting
        # for item in response.css(".meetings"):
        #     meeting = Meeting(
        #         title=self._parse_title(item),
        #         description=self._parse_description(item),
        #         classification=self._parse_classification(item),
        #         start=self._parse_start(item),
        #         end=self._parse_end(item),
        #         all_day=self._parse_all_day(item),
        #         time_notes=self._parse_time_notes(item),
        #         location=self._parse_location(address),
        #         links=self._parse_links(item),
        #         source=self._parse_source(response),
        #     )

        #     meeting["status"] = self._get_status(meeting)
        #     meeting["id"] = self._get_id(meeting)

        #     yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return ""

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        return None

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, address):
        """Parse or generate location."""
        room = "Room 646 of the City-County Building"
        street = "414 Grant Street"
        city = "Pittsburgh, PA 15219"

        if not (room in address):
            raise ValueError("The address for this meeting has changed")

        return {
            "address": ", ".join([room, street, city]),
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
