''' Module for property detail. '''

from __future__ import annotations

from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from .property_search import PropertySearch


@dataclass(init=True)
class PropertyDetail(PropertySearch):
    ''' Class for property detail. '''
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
    ''' Function to fetch property detailed search result. '''
    # make a web request for property detail
    response = requests.get(url=link)
    if response.status_code != 200:
        raise Exception(
            f'Error: request failed with response status code: {response.status_code}')

    # parse the web response
    soup = BeautifulSoup(response.content, 'html.parser')
    property_listing_attributes = soup.find(
        'tm-property-listing-attributes')

    # extract property type, rateable value, parking type, in the area, property id
    # and agency reference
    property_detail = PropertyDetail()
    rows = property_listing_attributes.find_all('tr')
    for row in rows:
        row_data = row.find_all('td')
        if not row_data or len(row_data) < 2:
            continue
        if str.strip(row_data[0].text) == 'Property type':
            property_detail.property_type = str.strip(row_data[1].text)
            continue
        if str.strip(row_data[0].text) == 'Rateable value (RV)':
            property_detail.rateable_value = str.strip(row_data[1].text)
            continue
        if str.strip(row_data[0].text) == 'Parking':
            property_detail.parking_type = str.strip(row_data[1].text)
            continue
        if str.strip(row_data[0].text) == 'In the area':
            property_detail.in_the_area = str.strip(row_data[1].text)
            continue
        if str.strip(row_data[0].text) == 'Property ID#':
            property_detail.property_id = str.strip(row_data[1].text)
            continue
        if str.strip(row_data[0].text) == 'Agency reference':
            property_detail.agency_reference = str.strip(row_data[1].text)
            continue
        if str.strip(row_data[0].text) == 'Broadband options':
            property_detail.broadband_options = str.strip(row_data[1].text)
            continue

    # extract description
    property_listing_description_text = soup.find(
        'tm-markdown', class_='tm-property-listing-description__text')
    if property_listing_description_text:
        property_detail.description = property_listing_description_text.text

    # populate result
    property_detail.city = property_search.city if property_search else None
    property_detail.link = property_search.link if property_search else None
    property_detail.title = property_search.title if property_search else None
    property_detail.address = property_search.address if property_search else None
    property_detail.number_of_bedrooms = property_search.number_of_bedrooms \
        if property_search else None
    property_detail.number_of_bathrooms = property_search.number_of_bathrooms \
        if property_search else None
    property_detail.number_of_parking_lots = property_search.number_of_parking_lots \
        if property_search else None
    property_detail.number_of_living_areas = property_search.number_of_living_areas \
        if property_search else None
    property_detail.floor_area_sqm = property_search.floor_area_sqm if property_search else None
    property_detail.land_area_sqm = property_search.land_area_sqm if property_search else None
    property_detail.asking_price = property_search.asking_price if property_search else None

    return property_detail
