# Created by Ryan Polasky, 12/3/24
# All rights reserved

from fastapi import APIRouter, Query, HTTPException
from app.services.riot_api import get_summoner_rank
from app.services.badge_generator import generate_badge

router = APIRouter()


@router.get("/", response_class="PlainTextResponse")
async def get_badge(summoner: str = Query(..., description="Summoner's name"),
                    region: str = Query(..., description="Region code, e.g., 'NA', 'EUW'")):
    """
    Generates a badge for a summoner's rank.
    """
    try:
        # Fetch rank data from Riot API
        rank_data = await get_summoner_rank(summoner, region)

        if not rank_data:
            raise HTTPException(status_code=404, detail="Summoner rank not found")

        # Generate the badge as an SVG
        badge_svg = generate_badge(rank_data)
        return badge_svg

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while generating the badge")
