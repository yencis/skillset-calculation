from dotenv import load_dotenv
import os
import requests

BASE_OSU_API_URL = "https://osu.ppy.sh/api/v2/"
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
access_token = token_response.json()["access_token"]

pages = 4
sets = []
cursor_string = None
for i in range(pages):
    cur_page = requests.get(
        BASE_OSU_API_URL + "beatmapsets/search",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        params={"sort": "plays_desc", "cursor_string": cursor_string},
    )
    cur_page = cur_page.json()
    cursor_string = cur_page["cursor_string"]
    for beatmapset in cur_page["beatmapsets"]:
        sets.append(beatmapset["title"])

print(*sets, sep="\n")
