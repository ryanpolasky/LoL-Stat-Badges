# Created by Ryan Polasky, 12/3/24
# All rights reserved

import os
import html
import base64
import logging
from PIL import Image, ImageDraw, ImageFont
from app.config import constants

logger = logging.getLogger(__name__)

_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

try:
    _FONT = ImageFont.truetype(
        os.path.join(_ASSETS_DIR, "fonts", "Verdana.ttf"), size=11
    )
except IOError:
    _FONT = ImageFont.truetype(
        os.path.join(_ASSETS_DIR, "fonts", "NotoSansCJK.otf"), size=11
    )

_RANK_IMAGES: dict[str, str] = {}
for _rank_name in constants.colors:
    _img_path = os.path.join(_ASSETS_DIR, f"{_rank_name}.png")
    if os.path.exists(_img_path):
        with open(_img_path, "rb") as _f:
            _RANK_IMAGES[_rank_name] = base64.b64encode(_f.read()).decode("utf-8")

_DUMMY_IMAGE = Image.new("RGB", (1, 1))
_DUMMY_DRAW = ImageDraw.Draw(_DUMMY_IMAGE)


def calculate_width(badge_text: str) -> float:
    """
    Dynamically calculates the rectangle width based on the summoner name and tagline length.
    Ensures the text fits comfortably within the rectangle.
    :param badge_text: The text to be displayed on the badge.
    :return: The width of the rectangle.
    """
    padding = 22  # Extra padding for aesthetic spacing
    icon_size = 35  # Extra space for the icon

    letter_spacing = 1
    spacing_width = len(badge_text) * letter_spacing

    # Get the text width using the font and calculate the bounding box
    text_width = _DUMMY_DRAW.textbbox((0, 0), badge_text, font=_FONT)[2]

    # Calculate the total width, adding padding and icon space
    calculated_width = text_width + spacing_width + padding + icon_size

    return calculated_width


def generate_badge(rank_data: dict, use_rank_name: bool) -> str:
    """
    Generates an SVG badge based on the rank data.
    :param rank_data: The rank data of the player. Found by using `app.services.riot_api.get_summoner_rank`.
    :param use_rank_name: Whether to display the rank name instead of username. False by default.
    :return: Returns the SVG badge in plain text.
    """
    rank = rank_data["rank"].lower()
    summoner_name = rank_data["summoner_name"]
    tag_line = rank_data["tag_line"]

    if use_rank_name or rank == "error":
        badge_text = rank.upper()
    else:
        badge_text = f"{summoner_name}#{tag_line}"

    logger.info(f"`generate_badge` started for player {summoner_name}#{tag_line}")
    color = constants.colors.get(rank, "#FFFFFF")
    proper_width = calculate_width(badge_text)
    base64_rank_img = _RANK_IMAGES.get(rank, "")
    safe_text = html.escape(badge_text)

    # todo - polish this badge layout, maybe add modular styles
    svg_template = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{proper_width}" height="28">
        <!-- Rectangle background -->
        <rect width="{proper_width}" height="28" fill="{color}" />

        <!-- Icon -->
        <image href="data:image/png;base64,{base64_rank_img}" x="5" y="0" width="28" height="28" />

        <!-- Text -->
        <text x="38" y="15.5" font-family="Verdana" font-size="11" font-weight="bold" fill="white" dominant-baseline="middle" letter-spacing="1">
            {safe_text}
        </text>
    </svg>
    """
    return svg_template
