# Created by Ryan Polasky, 12/3/24
# All rights reserved

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response, PlainTextResponse
import regex as re
import logging
from discord_webhook import DiscordWebhook
from app.config import Settings
from app.services.riot_api import get_summoner_rank
from app.services.badge_generator import generate_badge

router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.get("/{region}/{summoner}/{tag_line}", response_class=PlainTextResponse)
async def get_badge(
    region: str, summoner: str, tag_line: str, rank_name: bool = Query(False)
):
    """
    Generates a badge for a summoner's rank.
    """
    # Init user validity bool
    valid_user = True

    # Handle spaces in usernames
    safe_summoner = summoner.replace("%20", " ")

    # Send a webhook to creator's Discord for sake of counting the API's users
    Settings.API_CALLS += 1
    webhook = DiscordWebhook(
        url=Settings.DISCORD_WEBHOOK,
        content=f"Call #{Settings.API_CALLS}: {safe_summoner}#{tag_line} in region {region}",
    )
    _ = webhook.execute()

    # Check for summoner name being too long
    if len(safe_summoner) > 16:
        valid_user = False

    # Disallow only control characters and symbols
    pattern = r"^[^\p{C}\p{So}]*$"
    if not re.match(pattern, safe_summoner):
        valid_user = False

    # Check for tag line being too long
    if len(tag_line) > 5:
        valid_user = False

    # Check for tag line being alphanumeric
    if not tag_line.isalnum():
        valid_user = False

    # If the username passed the validity checks above,
    if valid_user:
        try:
            # Fetch rank data from Riot API
            logger.info(
                f"\nTrying to retrieve rank data for user {safe_summoner}#{tag_line} in region {region}..."
            )
            rank_data = await get_summoner_rank(safe_summoner, tag_line, region)

            logger.info(f"Rank data found:\n{rank_data}")
            # Generate the badge as an SVG
            logger.info(
                f"Trying to generate badge for user {safe_summoner}#{tag_line} in region {region}..."
            )
            badge_svg = generate_badge(rank_data, rank_name)
            logger.info(
                f"Badge successfully generated for {safe_summoner}#{tag_line} in region {region}!"
            )

            # Generate the response & return it
            response = Response(badge_svg, media_type="image/svg+xml")
            response.headers["Cache-Control"] = "no-cache"
            return Response(badge_svg, media_type="image/svg+xml", status_code=200)

        # If an actual HTTP exception is raised, allow it to raise
        except HTTPException as e:
            raise e

        # If some other Pythonic exception is raised, package it into an HTTP exception
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while generating the badge: {e}",
            )
    else:  # If the user's configuration is incorrect,
        # todo - fix this, { "detail": "An error occurred while generating the badge: 'NoneType' object is not subscriptable" }
        logger.info(
            f"\nConfiguration {safe_summoner}#{tag_line} in region {region} invalid..."
        )

        # Create mock data to call `generate_badge` with
        rank_data = {
            "rank": "error",
            "div": "n/a",
            "summoner_name": safe_summoner,
            "tag_line": tag_line,
        }

        # Generate the error badge
        badge_svg = generate_badge(rank_data, True)

        # Generate the response & return it
        response = Response(badge_svg, media_type="image/svg+xml")
        response.headers["Cache-Control"] = "no-cache"
        return Response(badge_svg, media_type="image/svg+xml", status_code=200)
