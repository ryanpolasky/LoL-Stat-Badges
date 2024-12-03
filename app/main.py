# Created by Ryan Polasky, 12/3/24
# All rights reserved

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import badge
import os

app = FastAPI()

# Include router(s)
app.include_router(badge.router, prefix="/badge", tags=["Badge"])

# Mount the assets folder
assets_path = os.path.join(os.path.dirname(__file__), "assets")
app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

@app.get("/")
async def root():
    return {"message": "Thanks for using my API! :)"}
