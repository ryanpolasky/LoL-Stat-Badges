# Created by Ryan Polasky, 12/3/24
# All rights reserved

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from app.routers import badge
import logging
import os

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Include router(s)
app.include_router(badge.router, prefix="/badge", tags=["Badge"])

# Mount the assets folder
assets_path = os.path.join(os.path.dirname(__file__), "assets")
app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

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
    return RedirectResponse(url="https://github.com/ryanpolasky/LoL-Stat-Badges", status_code=303)
