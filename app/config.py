# Created by Ryan Polasky, 12/3/24
# All rights reserved

import os

class Settings:
    RIOT_API_KEY: str = os.getenv("RIOT_API_KEY")
    CACHE_TTL: int = 3600  # Cache time-to-live in seconds

settings = Settings()
