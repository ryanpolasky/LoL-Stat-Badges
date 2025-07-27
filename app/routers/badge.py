# Created by Ryan Polasky, 12/3/24
# All rights reserved

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import Response, PlainTextResponse
import regex as re
import logging
from discord_webhook import DiscordWebhook
from app.config import Settings, InvalidRegionException
from app.services.riot_api import get_summoner_rank
from app.services.badge_generator import generate_badge  # Assuming this function exists and works

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/{region}/{summoner}/{tag_line}", response_class=PlainTextResponse)
async def get_badge(
        region: str, summoner: str, tag_line: str, rank_name: bool = Query(False)
):
    """
    Generates a badge for a summoner's rank.
    """
    # Init user validity bool
    valid_user = True
    error_message = ""

    # Handle spaces in usernames
    safe_summoner = summoner.replace("%20", " ")

    # Send a webhook to creator's Discord for sake of counting the API's users
    Settings.API_CALLS += 1
    webhook = DiscordWebhook(
        url=Settings.DISCORD_WEBHOOK,  # Use Settings.DISCORD_WEBHOOK
        content=f"Call #{Settings.API_CALLS}: {safe_summoner}#{tag_line} in region {region}",
    )
    # Execute webhook in a non-blocking way if possible, or consider a background task
    # For simplicity, keeping it as is, but for high traffic, this could block.
    _ = webhook.execute()

    # Check for summoner name being too long
    if len(safe_summoner) > 16:
        valid_user = False
        error_message = "Summoner name too long (max 16 characters)."

    # Disallow only control characters and symbols
    pattern = r"^[^\p{C}\p{So}]*$"
    if valid_user and not re.match(pattern, safe_summoner):
        valid_user = False
        error_message = "Summoner name contains invalid characters."

    # Check for tag line being too long
    if valid_user and len(tag_line) > 5:
        valid_user = False
        error_message = "Tag line too long (max 5 characters)."

    # Check for tag line being alphanumeric
    if valid_user and not tag_line.isalnum():
        valid_user = False
        error_message = "Tag line contains non-alphanumeric characters."

    # If the username passed the validity checks above,
    if valid_user:
        try:
            # Fetch rank data from Riot API
            logger.info(
                f"Trying to retrieve rank data for user {safe_summoner}#{tag_line} in region {region}..."
            )
            rank_data = await get_summoner_rank(safe_summoner, tag_line, region)

            # Check if get_summoner_rank returned an error dictionary
            if rank_data and rank_data.get("rank") == "error":
                # Propagate the error message from riot_api.py
                detail_message = rank_data.get("error_message", "Unknown error from Riot API.")
                logger.error(f"Failed to retrieve rank data: {detail_message}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An error occurred while fetching rank data: {detail_message}",
                )

            logger.info(f"Rank data found: {rank_data}")
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
            return Response(badge_svg, media_type="image/svg+xml", status_code=status.HTTP_200_OK)

        # If an actual HTTP exception is raised, allow it to raise
        except HTTPException as e:
            raise e

        # If some other Pythonic exception is raised, package it into an HTTP exception
        except Exception as e:
            logger.error(f"An unexpected error occurred in badge generation: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while generating the badge: {e}",
            )
    else:  # If the user's configuration is incorrect,
        logger.warning(
            f"Invalid user configuration for {safe_summoner}#{tag_line} in region {region}. Reason: {error_message}"
        )

        # Create mock data to call `generate_badge` with for an error badge
        rank_data = {
            "rank": "error",
            "div": "n/a",
            "summoner_name": safe_summoner,
            "tag_line": tag_line,
            "error_message": error_message  # Pass the specific error message for the badge
        }

        # Generate the error badge
        badge_svg = generate_badge(rank_data, True)

        # Generate the response & return it
        response = Response(badge_svg, media_type="image/svg+xml")
        response.headers["Cache-Control"] = "no-cache"
        return Response(badge_svg, media_type="image/svg+xml", status_code=status.HTTP_200_OK)
