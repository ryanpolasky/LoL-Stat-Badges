# Created by Ryan Polasky, 12/3/24
# All rights reserved

from fastapi import FastAPI
from app.routers import badge, summoner

app = FastAPI()

# Include routers
app.include_router(badge.router, prefix="/badge", tags=["Badge"])
app.include_router(summoner.router, prefix="/summoner", tags=["Summoner"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
