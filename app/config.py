# Created by Ryan Polasky, 12/3/24
# All rights reserved

import os


class Settings:
    RIOT_API_KEY: str = os.getenv("RIOT_API_KEY")
    API_BASE_URL: str = "https://lol-stat-badges.onrender.com"
    DISCORD_WEBHOOK: str = os.getenv("DISCORD_WEBHOOK")

    # Call counter for debugging (Yes, I know this isn't persistent, don't worry)
    API_CALLS = 0


class Constants:
    RIOT_ENDPOINTS = {
        "AMERICAS": {
            "BR": "https://br1.api.riotgames.com",
            "BR1": "https://br1.api.riotgames.com",
            "LAN": "https://la1.api.riotgames.com",
            "LA1": "https://la1.api.riotgames.com",
            "LAS": "https://la2.api.riotgames.com",
            "LA2": "https://la2.api.riotgames.com",
            "NA": "https://na1.api.riotgames.com",
            "NA1": "https://na1.api.riotgames.com",
            "OC": "https://oc1.api.riotgames.com",
            "OCE": "https://oc1.api.riotgames.com",
            "REGION": "https://americas.api.riotgames.com",
        },
        "ASIA": {
            "KR": "https://kr.api.riotgames.com",
            "JP": "https://jp1.api.riotgames.com",
            "JP1": "https://jp1.api.riotgames.com",
            "REGION": "https://asia.api.riotgames.com",
        },
        "EUROPE": {
            "EUN": "https://eun1.api.riotgames.com",
            "EUN1": "https://eun1.api.riotgames.com",
            "EUNE": "https://eun1.api.riotgames.com",
            "EUW": "https://euw1.api.riotgames.com",
            "EUW1": "https://euw1.api.riotgames.com",
            "TR": "https://tr1.api.riotgames.com",
            "TR1": "https://tr1.api.riotgames.com",
            "RU": "https://ru.api.riotgames.com",
            "RU1": "https://ru.api.riotgames.com",
            "REGION": "https://europe.api.riotgames.com",
        },
        "SEA": {
            "VN": "https://vn2.api.riotgames.com",
            "VN2": "https://vn2.api.riotgames.com",
            "PH": "https://ph2.api.riotgames.com",
            "PH2": "https://ph2.api.riotgames.com",
            "SG": "https://sg2.api.riotgames.com",
            "SG2": "https://sg2.api.riotgames.com",
            "TH": "https://th2.api.riotgames.com",
            "TH2": "https://th2.api.riotgames.com",
            "TW": "https://tw2.api.riotgames.com",
            "TW2": "https://tw2.api.riotgames.com",
            "REGION": "https://sea.api.riotgames.com",
        },
    }

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
        "error": "#cc0000",
        "unranked": "#808080",
    }

    CACHE_TTL: int = 3600  # Cache time-to-live in seconds


class InvalidRegionException(ValueError):
    pass


settings = Settings()
constants = Constants()
