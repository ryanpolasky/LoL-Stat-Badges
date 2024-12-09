# Created by Ryan Polasky, 12/3/24
# All rights reserved

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response, PlainTextResponse
from typing import Optional
import re
import logging
from app.services.riot_api import get_summoner_rank
from app.services.badge_generator import generate_badge

router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.get("/{region}/{summoner}/{tagline}", response_class=PlainTextResponse)
async def get_badge(region: str, summoner: str, tagline: str, rank_name: bool = Query(False)):
    """
    Generates a badge for a summoner's rank.
    """
    # Handle spaces in usernames
    safe_summoner = summoner.replace("%20", " ")

    # Check for invalid summoner name
    if len(safe_summoner) > 16:
        raise HTTPException(status_code=400, detail="Summoner name exceeds 16 characters.")
    if not re.match(r"^[a-zA-Z0-9\s._-]*$", safe_summoner):
        raise HTTPException(status_code=400, detail="Summoner name contains invalid characters.")

    # Check for invalid tag line
    if len(tagline) > 5:
        raise HTTPException(status_code=400, detail="Tagline exceeds 5 characters.")
    if not tagline.isalnum():
        raise HTTPException(status_code=400, detail="Tagline contains invalid characters.")

    try:
        # Fetch rank data from Riot API
        logger.info(f"\nTrying to retrieve rank data for user {safe_summoner}#{tagline} in region {region}...")
        rank_data = await get_summoner_rank(safe_summoner, tagline, region)

        if not rank_data:
            logger.info("Rank data not found")
            raise HTTPException(status_code=404, detail="Summoner rank not found")
        else:
            logger.info(f"Rank data found:\n{rank_data}")

        # Generate the badge as an SVG
        logger.info(f"Trying to generate badge for user {safe_summoner}#{tagline} in region {region}...")
        badge_svg = generate_badge(rank_data, rank_name)
        logger.info(badge_svg)

        # Generate the response & return it
        response = Response(badge_svg, media_type="image/svg+xml")
        response.headers["Cache-Control"] = "no-cache"
        return Response(badge_svg, media_type="image/svg+xml", status_code=200)

    # If an actual HTTP exception is raised, allow it to raise
    except HTTPException as e:
        raise e

    # If some other Pythonic exception is raised, package it into an HTTP exception
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while generating the badge")
