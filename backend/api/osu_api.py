from dotenv import load_dotenv
import os
import requests


class OSUAPI:
    def __init__(self):
        self.BASE_OSU_API_URL = "https://osu.ppy.sh/api/v2/"
        OSU_TOKEN_URL = "https://osu.ppy.sh/oauth/token"

        load_dotenv()
        token_response = requests.post(
            OSU_TOKEN_URL,
            headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": str(os.environ.get("OSU_CLIENT_ID")),
                "client_secret": str(os.environ.get("OSU_CLIENT_SECRET")),
                "grant_type": "client_credentials",
                "scope": "public",
            },
        )
        token_response.raise_for_status()
        self.access_token = token_response.json()["access_token"]

    def get_beatmap(self, id):