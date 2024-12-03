# Created by Ryan Polasky, 12/3/24
# All rights reserved

from fastapi import APIRouter, Query, HTTPException
from app.services.riot_api import get_summoner_info

router = APIRouter()


@router.get("/", response_model=dict)
async def get_summoner(summoner: str = Query(..., description="Summoner's name"),
                       region: str = Query(..., description="Region code, e.g., 'NA', 'EUW'")):
    """
    Retrieves basic information about a summoner.
    """
    try:
        # Fetch summoner info from Riot API
        summoner_info = await get_summoner_info(summoner, region)

        if not summoner_info:
            raise HTTPException(status_code=404, detail="Summoner not found")

        return summoner_info

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving summoner data")
