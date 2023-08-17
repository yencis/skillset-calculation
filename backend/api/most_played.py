from dotenv import load_dotenv
import os
import requests
import util_io
import osu_api

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

pages = 1
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
        sets.append(beatmapset)

print(*[b["title"] for b in sets], sep="\n")
print(len(sets))

id_list = []
for mapset in sets:
    id_list.append(osu_api.OSUAPI.get_beatmaps_in_beatmapset(mapset, sort_by="difficulty_rating", reverse=True)[0]["id"])

util_io.write_list_to_file(id_list, filename="top5000byplaycount.txt")

selection = 94
# Grabs ID of the first map (index 0, not necessarily the lowest/highest star value) in the nth most played beatmap set (in this case, 51st)
selected_map = sets[selection]["beatmaps"][0]["id"]
selected_map_content = requests.get(f"https://osu.ppy.sh/osu/{selected_map}").text
#print(selected_map_content)

