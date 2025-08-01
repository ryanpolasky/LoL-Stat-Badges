# Created by Ryan Polasky, 12/3/24
# All rights reserved

import uvicorn
import time
import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from app.routers import badge
import logging
from discord_webhook import DiscordWebhook
from app.config import Settings
import os
import requests
from requests.exceptions import RequestException

app = FastAPI()

logger = logging.getLogger(__name__)

# Include router(s)
app.include_router(badge.router, prefix="/badge", tags=["Badge"])

# Mount the assets folder
assets_path = os.path.join(os.path.dirname(__file__), "assets")
app.mount("/assets", StaticFiles(directory=assets_path), name="assets")


def send_discord_webhook_safe(content: str, max_retries: int = 3, base_delay: float = 1.0):
    """
    Safely send a Discord webhook with error handling and rate limiting protection.

    Args:
        content: Message content to send
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds for exponential backoff
    """
    if not Settings.DISCORD_WEBHOOK:
        logger.warning("Discord webhook URL not configured, skipping notification")
        return False

    for attempt in range(max_retries):
        try:
            webhook = DiscordWebhook(url=Settings.DISCORD_WEBHOOK, content=content)
            response = webhook.execute()

            # Check if the response indicates success
            if hasattr(response, 'status_code') and response.status_code == 200:
                logger.info("Discord webhook sent successfully")
                return True
            elif hasattr(response, 'status_code') and response.status_code == 429:
                # Rate limited - extract retry-after if available
                retry_after = 60  # Default fallback
                try:
                    if hasattr(response, 'headers') and 'retry-after' in response.headers:
                        retry_after = int(response.headers['retry-after'])
                    elif hasattr(response, 'json'):
                        json_data = response.json()
                        retry_after = json_data.get('retry_after', 60)
                except (ValueError, json.JSONDecodeError, AttributeError):
                    pass

                logger.warning(
                    f"Discord webhook rate limited. Retry after {retry_after} seconds. Attempt {attempt + 1}/{max_retries}")

                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    time.sleep(retry_after)
                continue
            else:
                logger.warning(
                    f"Discord webhook returned unexpected status: {getattr(response, 'status_code', 'unknown')}")

        except RequestException as e:
            logger.error(f"Network error sending Discord webhook (attempt {attempt + 1}/{max_retries}): {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending Discord webhook (attempt {attempt + 1}/{max_retries}): {e}")

        # Exponential backoff for retries (except rate limiting, which uses retry-after)
        if attempt < max_retries - 1:
            delay = base_delay * (2 ** attempt)
            logger.info(f"Retrying Discord webhook in {delay} seconds...")
            time.sleep(delay)

    logger.error(f"Failed to send Discord webhook after {max_retries} attempts")
    return False


try:
    send_discord_webhook_safe("**Service Restarted**")
except Exception as e:
    logger.error(f"Critical error in Discord webhook setup: {e}")


@app.get("/")
async def root():
    logger.info("Root GET route accessed.")
    html_content = """
    <html>
        <head>
            <meta http-equiv="refresh" content="3;url=https://github.com/ryanpolasky/LoL-Stat-Badges" />
        </head>
        <body>
            <h1>Thanks for using my API! :)</h1>
            <p>You will be redirected to the GitHub repository shortly...</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.head("/")
async def head_root():
    logger.info("Root HEAD route accessed.")
    return RedirectResponse(
        url="https://github.com/ryanpolasky/LoL-Stat-Badges", status_code=303
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")