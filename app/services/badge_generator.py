# Created by Ryan Polasky, 12/3/24
# All rights reserved

from io import StringIO

def generate_badge(rank_data: dict) -> str:
    """
    Generates an SVG badge based on the rank data.
    """
    rank = rank_data[0]["tier"]  # Assuming rank_data is a list and the first entry is ranked solo/duo
    color = "gold" if rank.lower() in ["gold", "platinum"] else "silver"

    svg_template = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="120" height="30">
        <rect width="120" height="30" fill="{color}" />
        <text x="10" y="20" font-family="Arial" font-size="14" fill="black">
            Rank: {rank.capitalize()}
        </text>
    </svg>
    """
    return svg_template
