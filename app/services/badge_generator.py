# Created by Ryan Polasky, 12/3/24
# All rights reserved

import logging
from app.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def calculate_width(summoner_name: str, tag_line: str) -> int:
    """
    Dynamically calculates the rectangle width based on the summoner name and tagline length.
    Ensures the text fits comfortably within the rectangle.
    :param summoner_name: The name of the summoner.
    :param tag_line: The tag line of the summoner.
    :return: The width of the rectangle.
    """
    base_width = 150  # Minimum width for short names
    char_width = 7    # Average width of a character in pixels
    padding = 20      # Extra padding for aesthetic spacing

    total_length = len(f"{summoner_name}#{tag_line}")
    calculated_width = base_width + total_length * char_width + padding

    return max(calculated_width, base_width)

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

    # todo - polish this badge layout, maybe add modular styles
    svg_template = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{calculate_width(summoner_name, tag_line)}" height="28">
        <!-- Rectangle background -->
        <rect width="{calculate_width(summoner_name, tag_line)}" height="28" fill="{color}" />
        
        <!-- Icon -->
        <image href="{settings.API_BASE_URL}/assets/{rank}.png" x="3" y="3" width="21" height="21" />
        
        <!-- Text -->
        <text x="35" y="15" font-family="Verdana" font-size="11" font-weight="bold" fill="white" dominant-baseline="middle">
            {summoner_name}#{tag_line}
        </text>
    </svg>
    """
    return svg_template
