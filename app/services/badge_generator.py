# Created by Ryan Polasky, 12/3/24
# All rights reserved

import logging
import base64

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def calculate_width(badge_text: str) -> float:
    """
    Dynamically calculates the rectangle width based on the summoner name and tagline length.
    Ensures the text fits comfortably within the rectangle.
    :param badge_text: The text to be displayed on the badge.
    :return: The width of the rectangle.
    """
    char_width = 7.5  # Average width of a character in pixels
    padding = 25  # Extra padding for aesthetic spacing
    icon_size = 35  # Extra space for the icon

    total_length = len(badge_text)
    calculated_width = total_length * char_width + padding + icon_size

    return calculated_width


def encode_image_to_base64(image_path: str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def generate_badge(rank_data: dict, use_rank_name: bool) -> str:
    """
    Generates an SVG badge based on the rank data.
    :param rank_data: The rank data of the player. Found by using `app.services.riot_api.get_summoner_rank`.
    :param use_rank_name: Whether to display the rank name instead of username. False by default.
    :return: Returns the SVG badge in plain text.
    """
    rank = rank_data["rank"].lower()
    div = rank_data["div"].upper()
    summoner_name = rank_data["summoner_name"]
    tag_line = rank_data["tag_line"]

    if use_rank_name:
        badge_text = rank.upper()
    else:
        badge_text = f"{summoner_name}#{tag_line}"

    logger.info(f"`generate_badge` started for player {summoner_name}#{tag_line}")

    # Determine badge color based on rank, defaulting to light grey for unranked
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
        "challenger": "#43AFEC",
    }
    color = colors.get(rank, "#D3D3D3")

    # Calculate proper width for badge
    proper_width = calculate_width(badge_text)

    # Base64 encode the image (encode into the SVG for sake of GitHub embeds)
    base64_rank_img = encode_image_to_base64(f"app/assets/{rank}.png")

    # todo - polish this badge layout, maybe add modular styles
    svg_template = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{proper_width}" height="28">
        <!-- Rectangle background -->
        <rect width="{proper_width}" height="28" fill="{color}" />
        
        <!-- Icon -->
        <image href="data:image/png;base64,{base64_rank_img}" x="5" y="0" width="28" height="28" />
        
        <!-- Text -->
        <text x="38" y="15.5" font-family="Verdana" font-size="11" font-weight="bold" fill="white" dominant-baseline="middle" letter-spacing="1">
            {badge_text}
        </text>
    </svg>
    """
    return svg_template
