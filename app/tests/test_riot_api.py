# Created by Ryan Polasky, 12/3/24
# All rights reserved

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app  # Import your FastAPI app
from app.services.riot_api import get_summoner_puuid  # Import the function to mock

client = TestClient(app)

# Mock data
mock_summoner_data = {
    "summoner_name": "Eggo",
    "tag_line": "WFLE",
    # I know this PUUID looks like a secret value that I messed up & put in plain code, but it's
    # actually plainly accessible to anyone w/ a Riot API key, so it's nothing to worry about obscuring
    "puuid": "m6VD_tt5-vRTs3zqXyjNbqddf8WuLUZp4rEpYvwj6fTf63L-_oOE2vLLl-imdVhrcNX1HPwgquIKUw"
}

@pytest.fixture
def mock_riot_api():
    with patch("app.services.riot_api.get_summoner_puuid", return_value=mock_summoner_data):
        yield


def test_get_summoner_puuid(mock_riot_api):
    """Test that a specific username returns the correct PUUID."""
    # Replace 'region' and 'username' with your test values
    response = client.get("/badge?summoner=MockSummoner&region=NA&tagline=1234")

    # Ensure the request was successful
    assert response.status_code == 200

    # Parse the returned badge data
    badge_svg = response.text

    # Check that the mocked PUUID or related info is embedded in the badge
    assert "mock-puuid" in badge_svg  # Adjust this based on how you display data
