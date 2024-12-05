# Created by Ryan Polasky, 12/3/24
# All rights reserved

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import badge
import logging
import os

app = FastAPI()

# Configure CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {"message": "Thanks for using my API! :)"}

@app.head("/")
async def head_root():
    logger.info("Root HEAD route accessed.")
