""" Module for property detail. """

from __future__ import annotations

from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from structlog import get_logger

from .property_search import PropertySearch


@dataclass(init=True)
class PropertyDetail(PropertySearch):
    """Class for property detail."""

    # pylint: disable=too-many-instance-attributes
    # There is a requirement for many instance attributes.
    property_type: str = None
    rateable_value: str = None
    parking_type: str = None
    in_the_area: str = None
    property_id: str = None
    agency_reference: str = None
    broadband_options: str = None
    description: str = None


def property_detail_fetch(link, property_search=None) -> list[PropertySearch]:
    """Function to fetch property detailed search result."""
    logger = get_logger()
    logger.info(
        "Starting property detail fetch",
        link=link,
    )
    logger.debug("", property_search=property_search)

    logger.info("Starting web request", url=link)
    # make a web request for property detail
    response = requests.get(url=link)
    if response.status_code != 200:
        logger.error(
            "Completed web request",
            url=link,
            response_status_code=response.status_code,
        )
        raise Exception(
            f"Error: request failed with response status code: {response.status_code}"
        )
    logger.info(
        "Completed web request", url=link, response_status_code=response.status_code
    )

    # parse the web response
    logger.info(
        "Starting web response parse",
        url=link,
    )
    soup = BeautifulSoup(response.content, "html.parser")
    property_listing_attributes = soup.find("tm-property-listing-attributes")
    logger.debug(
        "Starting property listing attributes parse",
    )
    property_detail = PropertyDetail()
    if property_listing_attributes:
        logger.debug("", found_property_listing_attributes=True)
        _parse_property_listing_attributes(property_listing_attributes, property_detail)
    else:
        logger.debug("", found_property_listing_attributes=False)

    # extract description
    property_listing_description_text = soup.find(
        "tm-markdown", class_="tm-property-listing-description__text"
    )
    if property_listing_description_text:
        property_detail.description = property_listing_description_text.text

    # populate result
    property_detail.city = property_search.city if property_search else None
    property_detail.link = property_search.link if property_search else None
    property_detail.title = property_search.title if property_search else None
    property_detail.address = property_search.address if property_search else None
    property_detail.number_of_bedrooms = (
        property_search.number_of_bedrooms if property_search else None
    )
    property_detail.number_of_bathrooms = (
        property_search.number_of_bathrooms if property_search else None
    )
    property_detail.number_of_parking_lots = (
        property_search.number_of_parking_lots if property_search else None
    )
    property_detail.number_of_living_areas = (
        property_search.number_of_living_areas if property_search else None
    )
    property_detail.floor_area_sqm = (
        property_search.floor_area_sqm if property_search else None
    )
    property_detail.land_area_sqm = (
        property_search.land_area_sqm if property_search else None
    )
    property_detail.asking_price = (
        property_search.asking_price if property_search else None
    )
    logger.debug(
        "Completed property listing attributes parse",
        property_detail=property_detail,
    )
    logger.info(
        "Completed web response parse",
        url=link,
    )

    logger.info(
        "Completed property detail fetch",
        link=link,
    )

    return property_detail


def _parse_property_listing_attributes(property_listing_attributes, property_detail):
    if property_listing_attributes:
        # extract property type, rateable value, parking type, in the area, property id
        # agency reference and broadband options
        rows = property_listing_attributes.find_all("tr")
        for row in rows:
            row_data = row.find_all("td")
            if not row_data or len(row_data) < 2:
                continue
            if str.strip(row_data[0].text) == "Property type":
                property_detail.property_type = str.strip(row_data[1].text)
                continue
            if str.strip(row_data[0].text) == "Rateable value (RV)":
                property_detail.rateable_value = str.strip(row_data[1].text)
                continue
            if str.strip(row_data[0].text) == "Parking":
                property_detail.parking_type = str.strip(row_data[1].text)
                continue
            if str.strip(row_data[0].text) == "In the area":
                property_detail.in_the_area = str.strip(row_data[1].text)
                continue
            if str.strip(row_data[0].text) == "Property ID#":
                property_detail.property_id = str.strip(row_data[1].text)
                continue
            if str.strip(row_data[0].text) == "Agency reference":
                property_detail.agency_reference = str.strip(row_data[1].text)
                continue
            if str.strip(row_data[0].text) == "Broadband options":
                property_detail.broadband_options = str.strip(row_data[1].text)
                continue
