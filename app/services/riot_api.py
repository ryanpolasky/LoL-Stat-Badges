# Created by Ryan Polasky, 12/3/24
# All rights reserved

import httpx
from app.config import settings

BASE_URL = "https://{region}.api.riotgames.com"


async def get_summoner_info(summoner: str, region: str) -> dict:
    url = f"{BASE_URL}/lol/summoner/v4/summoners/by-name/{summoner}".format(region=region)
    headers = {"X-Riot-Token": settings.RIOT_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None


async def get_summoner_rank(summoner: str, region: str) -> dict:
    # First, get the summoner ID
    summoner_info = await get_summoner_info(summoner, region)
    if not summoner_info:
        return None

    summoner_id = summoner_info["id"]
    url = f"{BASE_URL}/lol/league/v4/entries/by-summoner/{summoner_id}".format(region=region)
    headers = {"X-Riot-Token": settings.RIOT_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
