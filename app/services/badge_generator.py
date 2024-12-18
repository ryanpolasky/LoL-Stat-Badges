# Created by Ryan Polasky, 12/3/24
# All rights reserved

from PIL import Image, ImageDraw, ImageFont
import logging
import base64
from app.config import constants

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def calculate_width(badge_text: str) -> float:
    """
    Dynamically calculates the rectangle width based on the summoner name and tagline length.
    Ensures the text fits comfortably within the rectangle.
    :param badge_text: The text to be displayed on the badge.
    :return: The width of the rectangle.
    """
    verdana_path = "app/assets/fonts/Verdana.ttf"
    noto_path = "app/assets/fonts/NotoSansCJK.otf"

    padding = 22  # Extra padding for aesthetic spacing
    icon_size = 35  # Extra space for the icon
    spacing_width = 0  # Init empty var to account for font differences

    try:
        font = ImageFont.truetype(verdana_path, size=11)  # Match SVG font-size

        # Account for letter spacing by adding extra space for each character (if needed)
        letter_spacing = (
            1  # You can adjust this value based on the desired letter spacing
        )
        spacing_width = len(badge_text) * letter_spacing

    except IOError:
        font = ImageFont.truetype(
            noto_path, size=11
        )  # Use NotoSansCJK if Verdana fails

    # Create a dummy image and drawing context to calculate text size
    dummy_image = Image.new("RGB", (1, 1))  # Small image for text sizing
    draw = ImageDraw.Draw(dummy_image)

    # Get the text width using the font and calculate the bounding box
    text_width = draw.textbbox((0, 0), badge_text, font=font)[2]  # Width of the text

    # Calculate the total width, adding padding and icon space
    calculated_width = text_width + spacing_width + padding + icon_size

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
    div = rank_data["div"].upper()  # Not used as of now
    summoner_name = rank_data["summoner_name"]
    tag_line = rank_data["tag_line"]

    if use_rank_name or rank == "error":
        badge_text = rank.upper()
    else:
        badge_text = f"{summoner_name}#{tag_line}"

    logger.info(f"`generate_badge` started for player {summoner_name}#{tag_line}")

    # Determine badge color based on rank, defaulting to light grey for unranked
    color = constants.colors.get(rank, "#FFFFFF")

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
