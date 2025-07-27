# Created by Ryan Polasky, 12/3/24
# All rights reserved

from typing import Any
import httpx
import logging
from app.config import settings, constants, InvalidRegionException

RIOT_ENDPOINTS = constants.RIOT_ENDPOINTS

logger = logging.getLogger(__name__)


async def get_summoner_puuid(
        summoner_name: str, tag_line: str, region: str
) -> str | None:
    """
    Function used to request the PUUID for a player using their Summoner Name, their tag, and their region.
    Example: Eggo#WFLE
    :param summoner_name: The first portion of your name. Example: 'Eggo'
    :param tag_line: The second portion of your name. Example: 'WFLE'
    :param region: The region of your account. Example: 'NA1'
    :return: Returns the PUUID of the player.
    """
    logger.info(f"Attempting to retrieve PUUID for {summoner_name}#{tag_line} in region {region}...")

    try:
        curr_region_base_url = calculate_region(region, True)
    except InvalidRegionException:
        logger.error(f"Invalid region provided for PUUID lookup: {region}")
        return None

    url = (
        f"{curr_region_base_url}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"
    )
    logger.info(f"Riot API PUUID URL: {url}")
    headers = {"X-Riot-Token": settings.RIOT_API_KEY}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            puuid = response.json().get("puuid")
            if puuid:
                logger.info(f"PUUID found for {summoner_name}#{tag_line}: {puuid}")
                return puuid
            else:
                logger.warning(f"PUUID not found in response for {summoner_name}#{tag_line}. Response: {response.text}")
                return None
        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error retrieving PUUID for {summoner_name}#{tag_line}: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Network error retrieving PUUID for {summoner_name}#{tag_line}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred while getting PUUID for {summoner_name}#{tag_line}: {e}")
            return None


async def get_summoner_rank(
        summoner_name: str, tag_line: str, region: str
) -> Any | None:
    """
    Function used to request the rank data for a player using their Summoner Name, their tag, and their region.
    Example: Eggo#WFLE
    :param summoner_name: The first portion of your name. Example: 'Eggo'
    :param tag_line: The second portion of your name. Example: 'WFLE'
    :param region: The region of your account. Example: 'NA1'
    :return: Returns the rank data of the player.
    """
    logger.info(f"Initiating rank data retrieval for {summoner_name}#{tag_line} in region {region}...")

    # First, get the summoner PUUID
    summoner_puuid = await get_summoner_puuid(summoner_name, tag_line, region)
    if not summoner_puuid:
        logger.warning(f"Failed to get PUUID for {summoner_name}#{tag_line}. Cannot proceed with rank lookup.")
        return {
            "rank": "error",
            "div": "n/a",
            "summoner_name": summoner_name,
            "tag_line": tag_line,
            "error_message": "PUUID not found or invalid."
        }

    # Next, get the actual rank of the user using their PUUID
    try:
        curr_region_base_url = calculate_region(region, False)
    except InvalidRegionException:
        logger.error(f"Invalid region provided for rank lookup: {region}")
        return {
            "rank": "error",
            "div": "n/a",
            "summoner_name": summoner_name,
            "tag_line": tag_line,
            "error_message": "Invalid region for rank lookup."
        }

    url = f"{curr_region_base_url}/lol/league/v4/entries/by-puuid/{summoner_puuid}"
    logger.info(f"Riot API League Entry URL: {url}")
    headers = {"X-Riot-Token": settings.RIOT_API_KEY}

    async with httpx.AsyncClient() as client:
        try:
            logger.info("Requesting rank data from League-v4 endpoint...")
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            logger.info("Rank data retrieved successfully from League-v4 endpoint.")
            data = response.json()

            relevant_details = {
                "rank": "unranked",
                "div": "n/a",
                "summoner_name": summoner_name,
                "tag_line": tag_line,
            }

            # Locate the proper queue type (Solo/Duo)
            for rank_info in data:
                if rank_info.get("queueType") == "RANKED_SOLO_5x5":
                    logger.info("Solo/Duo rank found.")
                    relevant_details["rank"] = rank_info["tier"]
                    relevant_details["div"] = rank_info["rank"]
                    logger.info(
                        f"Player {summoner_name}#{tag_line} is rank {relevant_details['rank']}, division {relevant_details['div']}"
                    )
                    break

            if relevant_details["rank"] == "unranked":
                logger.info(f"Player {summoner_name}#{tag_line} is unranked in Solo/Duo.")

            return relevant_details

        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error retrieving rank data for {summoner_name}#{tag_line}: {e.response.status_code} - {e.response.text}")
            return {
                "rank": "error",
                "div": "n/a",
                "summoner_name": summoner_name,
                "tag_line": tag_line,
                "error_message": f"Riot API HTTP Error: {e.response.status_code}"
            }
        except httpx.RequestError as e:
            logger.error(f"Network error retrieving rank data for {summoner_name}#{tag_line}: {e}")
            return {
                "rank": "error",
                "div": "n/a",
                "summoner_name": summoner_name,
                "tag_line": tag_line,
                "error_message": f"Network Error: {e}"
            }
        except Exception as e:
            logger.error(f"An unexpected error occurred while getting rank data for {summoner_name}#{tag_line}: {e}")
            return {
                "rank": "error",
                "div": "n/a",
                "summoner_name": summoner_name,
                "tag_line": tag_line,
                "error_message": f"Unexpected Error: {e}"
            }


def calculate_region(region: str, by_area: bool) -> str:
    """
    Calculates the proper base URL for usage dependent on the passed region & whether it's a modern route.
    :param region: The region provided by the user. E.g., 'NA1', 'EUW1'.
    :param by_area: Whether we want the general regional endpoint (e.g., 'AMERICAS') or a specific region's endpoint (e.g., 'NA1').
                    True for regional routing (e.g., account-v1), False for platform routing (e.g., summoner-v4, league-v4).
    :return: The proper base URL for the Riot API.
    """
    region_upper = region.upper()

    area = None
    for area_name, regions_map in RIOT_ENDPOINTS.items():
        if region_upper in regions_map and area_name != "DEFAULT_REGION_KEY":
            area = area_name
            break

    if not area:
        logger.error(f"Region '{region}' not found in defined endpoints.")
        raise InvalidRegionException(f"Invalid region: {region}")

    if by_area:
        response = RIOT_ENDPOINTS[area]["REGION"]
    else:
        response = RIOT_ENDPOINTS[area][region_upper]

    return response
