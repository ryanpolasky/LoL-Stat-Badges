# Created by Ryan Polasky, 12/3/24
# All rights reserved

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response
import logging
from app.services.riot_api import get_summoner_rank
from app.services.badge_generator import generate_badge

router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.get("/{region}/{summoner}/{tagline}", response_class=PlainTextResponse)
async def get_badge(region: str, summoner: str, tagline: str):
    """
    Generates a badge for a summoner's rank.
    """
    try:
        # Fetch rank data from Riot API
        logger.info(f"\nTrying to retrieve rank data for user {summoner}#{tagline} in region {region}...")
        rank_data = await get_summoner_rank(summoner, tagline, region)

        if not rank_data:
            logger.info("Rank data not found")
            raise HTTPException(status_code=404, detail="Summoner rank not found")
        else:
            logger.info(f"Rank data found:\n{rank_data}")

        # Generate the badge as an SVG
        logger.info(f"Trying to generate badge for user {summoner}#{tagline} in region {region}...")
        badge_svg = generate_badge(rank_data)
        logger.info(badge_svg)

        # Generate the response & return it
        response = Response(badge_svg, media_type="image/svg+xml")
        response.headers["Cache-Control"] = "no-cache"
        return Response(badge_svg, media_type="image/svg+xml")

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while generating the badge")
