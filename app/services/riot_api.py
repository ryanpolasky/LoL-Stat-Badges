# Created by Ryan Polasky, 12/3/24
# All rights reserved
from typing import Any

import httpx
import logging
from app.config import settings, constants, InvalidRegionException

endpoints = constants.RIOT_ENDPOINTS

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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
    logger.info(f"Getting PUUID for {summoner_name}#{tag_line} in {region}...")

    curr_region = calculate_region(region, True)

    url = (
        f"{curr_region}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"
    )
    logger.info(url)
    headers = {"X-Riot-Token": settings.RIOT_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            puuid = response.json()["puuid"]
            logger.info(f"PUUID found: {puuid}")
            return puuid
        else:
            logger.info("PUUID not found")
            return None


async def get_summoner_account_id(puuid: str, region: str) -> str | None:
    """
    Function used to request the Account ID for a player using their PUUID and their region.
    :param puuid: The PUUID of the account obtained from `get_summoner_puuid`.
    :param region: The region of your account. Example: 'NA1'
    :return: Returns the Account ID of the player.
    """
    logger.info(f"Getting Account ID for PUUID {puuid} in {region}...")

    curr_region = calculate_region(region, False)
    url = f"{curr_region}/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": settings.RIOT_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["id"]
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
    logger.info("`get_summoner_rank` called...")

    # First, get the summoner PUUID
    summoner_puuid = await get_summoner_puuid(summoner_name, tag_line, region)
    if not summoner_puuid:
        return None

    # Next, get the summoner Account ID
    summoner_account_id = await get_summoner_account_id(summoner_puuid, region)
    if not summoner_account_id:
        return None

    # Finally, get the actual rank of the user
    curr_region = calculate_region(region, False)
    url = f"{curr_region}/lol/league/v4/entries/by-summoner/{summoner_account_id}"
    headers = {"X-Riot-Token": settings.RIOT_API_KEY}

    # Return the tier & rank of the player
    async with httpx.AsyncClient() as client:
        # Make the request
        logger.info("Requesting rank data...")
        response = await client.get(url, headers=headers)

        if response.status_code == 200:  # If the request is successful,
            logger.info("Rank data retrieved successfully")

            # Parse the data into Pythonic format
            data = response.json()

            # Locate the proper queue type
            for rank_info in data:
                if rank_info.get("queueType") == "RANKED_SOLO_5x5":
                    logger.info("Solo/Duo rank found")
                    data = rank_info  # Assign the solo/duo rank data to 'data'
                    break

            # Check to see if data is empty after trying to find the queue
            if not data:
                # Return the relevant details
                relevant_details = {
                    "rank": "unranked",
                    "div": "n/a",
                    "summoner_name": summoner_name,
                    "tag_line": tag_line,
                }
                logger.info(f"Player {summoner_name}#{tag_line} is unranked")

            else:
                # Return the relevant details
                relevant_details = {
                    "rank": data["tier"],
                    "div": data["rank"],
                    "summoner_name": summoner_name,
                    "tag_line": tag_line,
                }
                logger.info(
                    f"Player {summoner_name}#{tag_line} is rank {data['tier']}, division {data['rank']}"
                )

            # Return the important information
            return relevant_details

        else:  # If the request is not successful,
            logger.info("Request for rank data unsuccessful")
            return None


def calculate_region(region: str, by_area: bool) -> str:
    """
    Calculates the proper endpoint for usage dependent on the passed region & whether it's a modern route.
    :param region: The region provided by the user.
    :param by_area: Whether we want the general regional endpoint or a specific region's endpoint.
    :return: The proper endpoint.
    """
    if region in endpoints["AMERICAS"]:
        if by_area:
            response = endpoints["AMERICAS"]["REGION"]
        else:
            response = endpoints["AMERICAS"][region]
    elif region in endpoints["ASIA"]:
        if by_area:
            response = endpoints["ASIA"]["REGION"]
        else:
            response = endpoints["ASIA"][region]
    elif region in endpoints["EUROPE"]:
        if by_area:
            response = endpoints["EUROPE"]["REGION"]
        else:
            response = endpoints["EUROPE"][region]
    elif region in endpoints["SEA"]:
        if by_area:
            response = endpoints["SEA"]["REGION"]
        else:
            response = endpoints["SEA"][region]
    else:
        logger.info("Region not found")
        raise InvalidRegionException
    return response
