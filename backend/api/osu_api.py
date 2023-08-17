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

    def get_beatmap_page(self, pages, e=None, query=None, language=None, genre=None, c=None, mode=0, sort=None, status=None, nsfw=None):
        """
        Get the number of pages of beatmaps with search parameters.

        To combine multiple parameters, use a "."
        Ex: To combine "storyboard" maps and "video" maps, do "storyboard.video"

        Parameters:

            pages : int
                number of pages of beatmaps

            e : string
                Whether a map must have storyboard/video

            query : string
                Search query

            language : int
                Song language

            genre : int
                Song genre

            c : string
                General searches, like "spotlights" for spotlighted beatmaps or "featured_artists" for maps with songs
                by featured artists

            mode : int
                Gamemode from 0 to 3, with:
                * standard : 0
                * taiko : 1
                * catch : 2
                * mania : 3

            sort : string
                Sort by property; options are:
                * title
                * artist
                * difficulty
                * ranked
                * rating
                * plays
                * favourites

                All sorting properties are followed with "desc" or "asc"
                Ex: "plays_desc" gives the most played osu! beatmaps

            status : string
                Map status

            nsfw : string
                Either "true" or "false"

        Returns: list of beatmapset JSONs containing beatmapset information
        """

        sets = []
        cursor_string = None
        for i in range(pages):
            cur_page = requests.get(
                self.BASE_OSU_API_URL + "beatmapsets/search",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                params={"e": e, "q": query, "g": genre, "l": language, "c": c, "m": mode,
                        "nsfw": nsfw, "s": status, "sort": sort, "cursor_string": cursor_string},
            )
            cur_page = cur_page.json()
            cursor_string = cur_page["cursor_string"]
            for beatmapset in cur_page["beatmapsets"]:
                sets.append(beatmapset)
        return sets

    @staticmethod
    def get_beatmap(beatmap_id):
        """
        Get beatmap by id

        Returns beatmap .osu file as text
        """
        return requests.get(f"https://osu.ppy.sh/osu/{beatmap_id}").text

    @staticmethod
    def get_beatmaps_in_beatmapset(beatmapset_json, sort_by=None, reverse=False):
        """
        Get beatmaps in beatmapset in the order given by sort_by (or unsorted if None)

        Returns: list of beatmaps in beatmapset in given order
        """

        beatmaps = beatmapset_json["beatmaps"]

        if sort_by:
            beatmaps = sorted(beatmaps, key=lambda beatmap: beatmap[sort_by], reverse=reverse)

        return beatmaps
