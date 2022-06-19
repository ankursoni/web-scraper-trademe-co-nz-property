""" Module for command line interface (cli). """

from __future__ import annotations

import distutils
import sys
from time import sleep

import pandas as pd

from .property_detail import PropertyDetail, property_detail_fetch
from .property_search import (
    DEFAULT_CITY,
    DEFAULT_DOMAIN_URL,
    DEFAULT_HIT_DELAY_SECONDS,
    PropertySearch,
    property_search_fetch,
)


def search_without_detail(
    domain_url=DEFAULT_DOMAIN_URL, city=DEFAULT_CITY, total_pages=1
) -> list[PropertySearch]:
    """Function searching without property detail."""
    result = property_search_fetch(
        domain_url=domain_url, city=city, total_pages=total_pages
    )
    sleep(DEFAULT_HIT_DELAY_SECONDS)
    return result


def search_with_detail(
    domain_url=DEFAULT_DOMAIN_URL, city=DEFAULT_CITY, total_pages=1
) -> list[PropertyDetail]:
    """Function searching with property detail."""
    search = property_search_fetch(
        domain_url=domain_url, city=city, total_pages=total_pages
    )
    result = []
    for item in search:
        result.append(
            # fetch property detail for each property in search result
            property_detail_fetch(link=item.link, property_search=item)
        )
        sleep(DEFAULT_HIT_DELAY_SECONDS)
    return result


def format_csv(property_list) -> str:
    """Function formatting property list to csv string."""
    if not property_list or len(property_list) == 0:
        return None
    dataframe = pd.DataFrame([p.__dict__ for p in property_list])
    dataframe.index.name = "sno"
    dataframe.index += 1
    return dataframe.to_csv(sep="|")


def main():
    """Entry point if called as an executable."""
    arg_city = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CITY
    arg_total_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    arg_do_search_with_detail = (
        distutils.util.strtobool(sys.argv[3]) if len(sys.argv) > 3 else False
    )
    arg_output_file = sys.argv[4] if len(sys.argv) > 4 else "result.csv"
    print(
        f"Calling property search for city = {arg_city} and total pages = {arg_total_pages}, doing",
        "'with details'" if arg_do_search_with_detail else "'without detail',",
        f"resulting in the output file {arg_output_file} ...",
    )

    search_result = (
        search_with_detail(city=arg_city, total_pages=arg_total_pages)
        if arg_do_search_with_detail
        else search_without_detail(city=arg_city, total_pages=arg_total_pages)
    )
    csv = format_csv(search_result)
    with open(arg_output_file, "w+", encoding="utf-8") as csv_file:
        csv_file.write(csv)


if __name__ == "__main__":
    main()
