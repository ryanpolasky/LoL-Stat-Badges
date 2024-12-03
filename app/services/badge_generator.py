# Created by Ryan Polasky, 12/3/24
# All rights reserved

from io import StringIO
from app.config import settings

def generate_badge(rank_data: dict) -> str:
    """
    Generates an SVG badge based on the rank data.
    """
    rank = rank_data["rank"].lower()
    div = rank_data["div"].upper()
    summoner_name = rank_data["summoner_name"]
    tag_line = rank_data["tag_line"]

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
    <svg xmlns="http://www.w3.org/2000/svg" width="150" height="30">
        <!-- Rectangle background -->
        <rect width="150" height="30" fill="#b4fbfd" />
        
        <!-- Icon -->
        <image href="{settings.API_BASE_URL}/assets/{rank}.png" x="5" y="2" width="30" height="30" />
        
        <!-- Bold Text centered relative to the rectangle -->
        <text x="45" y="17" font-family="Verdana" font-size="11" font-weight="bold" fill="black" dominant-baseline="middle">
            {summoner_name}#{tag_line}
        </text>
    </svg>
    """
    return svg_template
