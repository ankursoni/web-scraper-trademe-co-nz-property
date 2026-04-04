"""Module for command line interface (cli)."""

from __future__ import annotations

import asyncio
import logging
import sys

import pandas as pd
import structlog
from structlog import get_logger

from .property_detail import PropertyDetail, property_detail_fetch
from .property_search import (
    DEFAULT_CITY,
    DEFAULT_DOMAIN_URL,
    DEFAULT_HIT_DELAY_SECONDS,
    PropertySearch,
    property_search_fetch,
)


async def search_without_detail(
    domain_url=DEFAULT_DOMAIN_URL, city=DEFAULT_CITY, total_pages=1
) -> list[PropertySearch]:
    """Function searching without property detail."""
    logger = get_logger()
    logger.info(
        "Starting search without detail",
        domain_url=domain_url,
        city=city,
        total_pages=total_pages,
    )

    result = await property_search_fetch(
        domain_url=domain_url, city=city, total_pages=total_pages
    )
    await asyncio.sleep(DEFAULT_HIT_DELAY_SECONDS)
    logger.info(
        "Completed search without detail",
        domain_url=domain_url,
        city=city,
        total_pages=total_pages,
    )

    return result


async def search_with_detail(
    domain_url=DEFAULT_DOMAIN_URL, city=DEFAULT_CITY, total_pages=1
) -> list[PropertyDetail]:
    """Function searching with property detail."""
    logger = get_logger()
    logger.info(
        "Starting search with detail",
        domain_url=domain_url,
        city=city,
        total_pages=total_pages,
    )

    search = await property_search_fetch(
        domain_url=domain_url, city=city, total_pages=total_pages
    )
    result = []
    for item in search:
        result.append(
            # fetch property detail for each property in search result
            await property_detail_fetch(link=item.link, property_search=item)
        )
        await asyncio.sleep(DEFAULT_HIT_DELAY_SECONDS)
    logger.info(
        "Completed search with detail",
        domain_url=domain_url,
        city=city,
        total_pages=total_pages,
    )

    return result


def format_psv(property_list) -> str:
    """Function formatting property list to psv string."""
    logger = get_logger()
    logger.info("Starting psv formatting", total_property_list=len(property_list))
    if not property_list or len(property_list) == 0:
        return None
    dataframe = pd.DataFrame([p.__dict__ for p in property_list])
    dataframe.index.name = "sno"
    dataframe.index += 1
    result = dataframe.to_csv(sep="|")
    logger.info("Completed psv formatting", total_property_list=len(property_list))

    return result


def _strtobool(val: str) -> bool:
    """Converts a string representation of truth to a boolean.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'.
    False values are 'n', 'no', 'f', 'false', 'off', '0'.

    Raises ValueError if 'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    if val in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"invalid truth value {val!r}")


async def _async_main() -> None:
    logger = get_logger()
    # parse cli arguments
    arg_city = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CITY
    arg_total_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    arg_do_search_with_detail = _strtobool(sys.argv[3]) if len(sys.argv) > 3 else False
    arg_output_file = sys.argv[4] if len(sys.argv) > 4 else "result.psv"
    debug_mode = _strtobool(sys.argv[5]) if len(sys.argv) > 5 else False
    print(
        f"Calling property search for city = {arg_city} and",
        f"total pages = {arg_total_pages}, searching",
        "'with detail'" if arg_do_search_with_detail else "'without detail',",
        f"resulting in the output file {arg_output_file}",
        "running in 'debug mode' ..." if debug_mode else "...",
    )

    # configure global logging level
    structlog.configure_once(
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if debug_mode else logging.INFO
        )
    )

    # execute search
    search_result = (
        await search_with_detail(city=arg_city, total_pages=arg_total_pages)
        if arg_do_search_with_detail
        else await search_without_detail(city=arg_city, total_pages=arg_total_pages)
    )

    # format into csv file
    psv = format_psv(search_result)
    if psv:
        with open(arg_output_file, "w+", encoding="utf-8") as psv_file:
            logger.info(
                "Starting psv file write",
                psv_file_name=arg_output_file,
                total_lines=psv.count("\n"),
            )
            psv_file.write(psv)
            logger.info(
                "Completed psv file write",
                psv_file_name=arg_output_file,
                total_lines=psv.count("\n"),
            )
    else:
        print("No result!")


def main() -> None:
    """Entry point if called as an executable."""
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
