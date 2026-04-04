from pathlib import Path

import pytest

import search.main

_DATA_DIR = Path(__file__).resolve().parent / "data"
AUCKLAND_SEARCH_HTML = _DATA_DIR / "property_search_001.html"
PROPERTY_DETAIL_001_HTML = _DATA_DIR / "property_detail_001.html.html"

DEFAULT_HIT_DELAY_SECONDS = 0


def _make_playwright_mock(html_content: str):
    """Build a mock async_playwright that returns a browser/page yielding the given HTML."""

    class MockPage:
        async def goto(self, url):  # noqa: ARG002
            pass

        async def wait_for_selector(self, selector, timeout=None):  # noqa: ARG002
            pass

        async def content(self):
            return html_content

    class MockBrowser:
        async def new_page(self):
            return MockPage()

        async def close(self):
            pass

    class MockChromium:
        async def launch(self, headless=True):  # noqa: ARG002
            return MockBrowser()

    class MockPlaywright:
        @property
        def chromium(self):
            return MockChromium()

    class PlaywrightContext:
        async def __aenter__(self):
            return MockPlaywright()

        async def __aexit__(self, *args):
            return False

    def async_playwright():
        return PlaywrightContext()

    return async_playwright


@pytest.mark.system
async def test_search_without_detail(mocker):
    """System test: search without detail parses Auckland HTML and returns 22 listings."""
    mocker.patch.object(
        search.main, "DEFAULT_HIT_DELAY_SECONDS", DEFAULT_HIT_DELAY_SECONDS
    )
    html = AUCKLAND_SEARCH_HTML.read_text(encoding="utf-8")
    mocker.patch("search.property_search.async_playwright", _make_playwright_mock(html))

    result = await search.main.search_without_detail(
        domain_url="https://www.trademe.co.nz", city="auckland", total_pages=1
    )

    assert result is not None
    assert result != []
    assert len(result) == 22

    assert result[0].city == "auckland"
    assert (
        result[0].link
        == "https://www.trademe.co.nz/a/property/residential/sale/auckland/auckland-city/glendowie/listing/5854081968"
    )
    assert result[0].title == "Boutique Living in Glendowie"
    assert result[0].address == "1, 3,4,5/9 Kesteven Avenue, Glendowie, Auckland City"
    assert result[0].number_of_bedrooms == "3"
    assert result[0].number_of_bathrooms == "2"
    assert result[0].number_of_parking_lots == "1"
    assert result[0].number_of_living_areas is None
    assert result[0].floor_area_sqm is None
    assert result[0].land_area_sqm == "109  m2"
    assert result[0].asking_price == "Asking price $1,395,000"

    assert result[-1].city == "auckland"
    assert (
        result[-1].link
        == "https://www.trademe.co.nz/a/property/residential/sale/auckland/waitakere-city/sunnyvale/listing/5438793156"
    )
    assert result[-1].title == "RC EPA ready. BC pending."
    assert result[-1].address == "96 Millbrook Road, Sunnyvale, Waitakere City"
    assert result[-1].number_of_bedrooms == "3"
    assert result[-1].number_of_bathrooms == "1"
    assert result[-1].number_of_parking_lots == "3"
    assert result[-1].number_of_living_areas is None
    assert result[-1].floor_area_sqm is None
    assert result[-1].land_area_sqm == "809  m2"
    assert result[-1].asking_price == "Price by negotiation"


@pytest.mark.system
async def test_search_with_detail(mocker):
    """System test: search with detail enriches listings with parsed detail HTML fields."""
    mocker.patch.object(
        search.main, "DEFAULT_HIT_DELAY_SECONDS", DEFAULT_HIT_DELAY_SECONDS
    )
    search_html = AUCKLAND_SEARCH_HTML.read_text(encoding="utf-8")
    detail_html = PROPERTY_DETAIL_001_HTML.read_text(encoding="utf-8")
    mocker.patch(
        "search.property_search.async_playwright", _make_playwright_mock(search_html)
    )
    mocker.patch(
        "search.property_detail.async_playwright", _make_playwright_mock(detail_html)
    )

    result = await search.main.search_with_detail(
        domain_url="https://www.trademe.co.nz", city="auckland", total_pages=1
    )

    assert result is not None
    assert len(result) == 22

    # Basic fields come from the search result (first Auckland listing: Glendowie)
    assert result[0].city == "auckland"
    assert (
        result[0].link
        == "https://www.trademe.co.nz/a/property/residential/sale/auckland/auckland-city/glendowie/listing/5854081968"
    )
    assert result[0].title == "Boutique Living in Glendowie"
    assert result[0].address == "1, 3,4,5/9 Kesteven Avenue, Glendowie, Auckland City"
    assert result[0].number_of_bedrooms == "3"
    assert result[0].number_of_bathrooms == "2"
    assert result[0].number_of_parking_lots == "1"
    assert result[0].number_of_living_areas is None
    assert result[0].floor_area_sqm is None
    assert result[0].land_area_sqm == "109  m2"
    assert result[0].asking_price == "Asking price $1,395,000"

    # Detail fields come from property_detail_001.html.html (9 Kesteven Ave, Glendowie)
    assert result[0].property_type == "House"
    assert result[0].rateable_value is None
    assert result[0].parking_type == "1 open spaces"
    assert result[0].in_the_area is None
    assert result[0].property_id == "JRR719"
    assert result[0].agency_reference == "ORK31963"
    assert result[0].broadband_options is None
    assert "Welcome to 9 Kesteven Avenue" in (result[0].description or "")


def test_format_psv():
    item = type(
        "Item",
        (object,),
        {
            "__dict__": {
                "test1": 1,
                "test2": 2,
            }
        },
    )
    item_list = [item()]

    result = search.main.format_psv(property_list=item_list)

    assert result == "sno|test1|test2\n1|1|2\n"
