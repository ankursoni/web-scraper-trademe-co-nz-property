""" Module for property search. """

from __future__ import annotations

import urllib.parse
from dataclasses import dataclass
from time import sleep

import requests
from bs4 import BeautifulSoup
from structlog import get_logger

DEFAULT_DOMAIN_URL = "https://www.trademe.co.nz"
DEFAULT_CITY = "auckland"
DEFAULT_HIT_DELAY_SECONDS = 0.05


@dataclass(init=True)
class PropertySearch:
    """Class for property search."""

    # pylint: disable=too-many-instance-attributes
    # There is a requirement for many instance attributes.
    city: str = None
    link: str = None
    title: str = None
    address: str = None
    number_of_bedrooms: str = None
    number_of_bathrooms: str = None
    number_of_parking_lots: str = None
    number_of_living_areas: str = None
    floor_area_sqm: str = None
    land_area_sqm: str = None
    asking_price: str = None


def property_search_fetch(
    domain_url=DEFAULT_DOMAIN_URL, city=DEFAULT_CITY, total_pages=1
) -> list[PropertySearch]:
    """Function to fetch property search results."""
    logger = get_logger()
    logger.info(
        "Starting property search fetch",
        domain_url=domain_url,
        city=city,
        total_pages=total_pages,
    )
    result = []
    for page_number in range(1, total_pages + 1):
        # make a web request for property search in the city
        url = urllib.parse.urljoin(
            domain_url, f"/a/property/residential/sale/{city}?page={page_number}"
        )
        logger.info("Starting web request", url=url)
        response = requests.get(url=url)
        if response.status_code != 200:
            logger.error(
                "Completing web request",
                url=url,
                response_status_code=response.status_code,
            )
            raise Exception(
                f"Error: request failed with response status code: {response.status_code}"
            )
        logger.info(
            "Completed web request", url=url, response_status_code=response.status_code
        )

        # parse the web response
        logger.info(
            "Starting web response parse",
            url=url,
        )
        soup = BeautifulSoup(response.content, "html.parser")
        property_listing_cards = soup.find_all("tm-property-premium-listing-card")
        if len(property_listing_cards) == 0:
            logger.info(
                "Completed web response parse", url=url, total_property_listing_cards=0
            )
            return result

        # parse each property lising card
        for index, plc in enumerate(property_listing_cards):
            logger.debug(
                "Starting property listing card parse",
                property_listing_card_index=index,
            )
            property_search = PropertySearch()
            property_search.city = city
            # extract property search url
            tag = plc.find("a", class_="tm-property-premium-listing-card__link")
            if tag:
                property_search.link = urllib.parse.urljoin(
                    domain_url, urllib.parse.urlparse(str.strip(tag.attrs["href"])).path
                )

            # extract property search title
            tag = plc.find("tm-property-search-card-listing-title")
            if tag:
                property_search.title = str.strip(tag.text)

            # extract property search address
            tag = plc.find("tm-property-search-card-address-subtitle")
            if tag:
                property_search.address = str.strip(tag.text)

            # extract number of bedrooms, bathrooms, parking slots and living areas (lounges)
            plc_icons = plc.find("tm-property-search-card-attribute-icons")
            _parse_property_search_card_attribute(plc_icons, property_search)

            # extract property search asking price
            tag = plc.find("tm-property-search-card-price-attribute")
            if tag:
                property_search.asking_price = str.strip(tag.text)

            # populate result list
            result.append(property_search)
            logger.debug(
                "Completed property listing card parse",
                property_listing_card_index=index,
                property_search=property_search,
            )

            sleep(DEFAULT_HIT_DELAY_SECONDS)

        logger.info(
            "Completed web response parse",
            url=url,
            total_property_listing_cards=len(property_listing_cards),
        )

    logger.info(
        "Completed property search fetch",
        domain_url=domain_url,
        city=city,
        total_pages=total_pages,
    )

    return result


def _parse_property_search_card_attribute(plc_icons, property_search):
    if not plc_icons:
        return
    tag = plc_icons.find("tg-icon", attrs={"name": "bedroom"})
    if tag:
        property_search.number_of_bedrooms = str.strip(tag.nextSibling.text)

    tag = plc_icons.find("tg-icon", attrs={"name": "bathroom"})
    if tag:
        property_search.number_of_bathrooms = str.strip(tag.nextSibling.text)

    tag = plc_icons.find("tg-icon", attrs={"name": "vehicle-car-front"})
    if tag:
        property_search.number_of_parking_lots = str.strip(tag.nextSibling.text)

    tag = plc_icons.find("tg-icon", attrs={"name": "armchair"})
    if tag:
        property_search.number_of_living_areas = str.strip(tag.nextSibling.text)

    tag = plc_icons.find("tg-icon", attrs={"name": "house-blueprint"})
    if tag:
        property_search.floor_area_sqm = str.strip(tag.nextSibling.text)

    tag = plc_icons.find("tg-icon", attrs={"name": "house-land-area"})
    if tag:
        property_search.land_area_sqm = str.strip(tag.nextSibling.text)
