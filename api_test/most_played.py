from dotenv import load_dotenv
from ossapi import Ossapi, BeatmapsetSearchSort
import os

load_dotenv()
api = Ossapi(
    client_id=os.environ.get("OSU_CLIENT_ID"), client_secret=os.environ.get("OSU_CLIENT_SECRET")
)

most_played = api.search_beatmapsets(sort=BeatmapsetSearchSort.PLAYS_DESCENDING)
print([bp.title for bp in most_played.beatmapsets])
