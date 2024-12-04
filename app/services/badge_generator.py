# Created by Ryan Polasky, 12/3/24
# All rights reserved

import logging
from app.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_badge(rank_data: dict) -> str:
    """
    Generates an SVG badge based on the rank data.
    :param rank_data: The rank data of the player. Found by using `app.services.riot_api.get_summoner_rank`.
    :return: Returns the SVG badge in plain text.
    """
    rank = rank_data["rank"].lower()
    div = rank_data["div"].upper()
    summoner_name = rank_data["summoner_name"]
    tag_line = rank_data["tag_line"]

    logger.info(f"`generate_badge` started for player {summoner_name}#{tag_line}")

    # Determine badge color based on rank, defaulting to white
    colors = {
        "iron": "#3c2f2a",
        "bronze": "#ae6f5b",
        "silver": "#7c8892",
        "gold": "#ae8a5a",
        "platinum": "#97eaf0",
        "emerald": "#33b86f",
        "diamond": "#218dc6",
        "master": "#ba48e1",
        "grandmaster": "#e3653d",
        "challenger": "#b4fbfd",
    }
    color = colors.get(rank, "#ffffff")

    svg_template = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="150" height="25">
        <!-- Rectangle background -->
        <rect width="150" height="25" fill="{color}" />
        
        <!-- Icon -->
        <image href="{settings.API_BASE_URL}/assets/{rank}.png" x="5" y="2" width="25" height="25" />
        
        <!-- Bold Text centered relative to the rectangle -->
        <text x="45" y="14" font-family="Verdana" font-size="11" font-weight="bold" fill="black" dominant-baseline="middle">
            {summoner_name}#{tag_line}
        </text>
    </svg>
    """
    return svg_template
