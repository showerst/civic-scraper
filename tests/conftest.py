import datetime
from pathlib import Path

import pytest

# NOTE: To check if vcrpy/pytest-vcr
# is using cassettes as opposed to making
# live web requests, uncomment below
# and pass pytest caplog fixture to
# a test function. More details here:
#  https://vcrpy.readthedocs.io/en/latest/debugging.html
# import vcr
# import logging
# logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from vcrpy
# vcr_log = logging.getLogger("vcr")
# vcr_log.setLevel(logging.INFO)


@pytest.fixture
def civic_scraper_dir(tmp_path):
    return str(tmp_path.joinpath(".civic-scraper"))


def read_fixture(file_name):
    path = str(Path(__file__).parent.joinpath("fixtures").joinpath(file_name))
    return file_contents(path)


def file_contents(pth):
    with open(pth, "r") as f:
        return f.read()


def file_lines(pth):
    with open(pth, "r") as f:
        return f.readlines()


@pytest.fixture(scope="session")
def search_results_html():
    return read_fixture("civplus_agenda_search_results_page.html")


@pytest.fixture
def asset_inputs():
    return [
        {
            "asset_name": "May 4, 2020 Regular Meeting Agenda",
            "asset_type": "minutes",
            "committee_name": "Board of Commissioners",
            "content_length": "33319158",
            "content_type": "application/pdf",
            "meeting_date": datetime.datetime(2020, 5, 4, 0, 0),
            "meeting_id": "civicplus_nc-nashcounty_05042020-381",
            "meeting_time": None,
            "place": "nashcounty",
            "scraped_by": "civic-scraper_0.1.0",
            "state_or_province": "nc",
            "url": "http://nc-nashcounty.civicplus.com/AgendaCenter/ViewFile/Minutes/_05042020-381",
        },
        {
            "asset_name": "May 4, 2020 Regular Meeting Agenda",
            "asset_type": "agenda",
            "committee_name": "Board of Commissioners",
            "content_length": "4682030",
            "content_type": "application/pdf",
            "meeting_date": datetime.datetime(2020, 5, 4, 0, 0),
            "meeting_id": "civicplus_nc-nashcounty_05042020-381",
            "meeting_time": None,
            "place": "nashcounty",
            "scraped_by": "civic-scraper_0.1.0",
            "state_or_province": "nc",
            "url": "http://nc-nashcounty.civicplus.com/AgendaCenter/ViewFile/Agenda/_05042020-381",
        },
    ]
