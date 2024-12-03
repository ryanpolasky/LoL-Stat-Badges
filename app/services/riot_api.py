# Created by Ryan Polasky, 12/3/24
# All rights reserved
from typing import Any

import httpx
from app.config import settings

BASE_URL = "https://{region}.api.riotgames.com"


async def get_summoner_puuid(summoner_name: str, tag_line: str, region: str) -> Any | None:
    curr_region = BASE_URL.format(region=region)
    url = f"{curr_region}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"
    headers = {"X-Riot-Token": settings.RIOT_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["puuid"]
        return None


async def get_summoner_account_id(puuid: str, region: str) -> Any | None:
    curr_region = BASE_URL.format(region=region)
    url = f"{curr_region}/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": settings.RIOT_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["id"]
        return None

async def get_summoner_rank(summoner_name: str, tag_line: str, region: str) -> Any | None:
    # First, get the summoner PUUID
    summoner_puuid = await get_summoner_puuid(summoner_name, tag_line, region)
    if not summoner_puuid:
        return None

    # Next, get the summoner Account ID
    summoner_account_id = await get_summoner_account_id(summoner_puuid, region)

    # Finally, get the actual rank of the user
    curr_region = BASE_URL.format(region=region)
    url = f"{curr_region}/lol/league/v4/entries/by-summoner/{summoner_account_id}"
    headers = {"X-Riot-Token": settings.RIOT_API_KEY}

    # Return the tier & rank of the player
    # todo - handle unranked + multi-rank (i.e. solo/duo vs flex)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return {
                "rank": response.json()["tier"],
                "div": response.json()["rank"],
                "summoner_name": summoner_name,
                "tag_line": tag_line,
            }
        return None
