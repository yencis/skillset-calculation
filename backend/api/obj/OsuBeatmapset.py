import datetime
import requests
import OsuBeatmap

class OsuBeatmapset:
    """
    Class representing how a Beatmapset is described by the osu! API.
    Attribute wrapper for osu! beatmapsets.
    """

    def __init__(self):
        self.artist = ""
        self.artist_unicode = ""
        self.covers = {}
        self.creator = ""
        self.favourite_count = -1
        self.hype = None
        self.id = -1
        self.nsfw = False
        self.offset = 0
        self.play_count = -1
        self.preview_url = ""
        self.source = ""
        self.spotlight = False
        self.status = "ranked"
        self.title = ""
        self.title_unicode = ""
        self.track_id = None
        self.user_id = -1
        self.video = False
        self.bpm = -1
        self.can_be_hyped = False
        self.deleted_at = None
        self.discussion_enabled = True
        self.discussion_locked = False
        self.is_scoreable = True
        self.last_updated = None
        self.legacy_thread_url = ""
        self.nominations_summary = {}
        self.ranked = 1
        self.ranked_date = None
        self.storyboard = False
        self.submitted_date = None
        self.tags = ""
        self.availability = {}
        self.beatmaps = []
        self.pack_tags = []

    @classmethod
    def from_dict(cls, beatmapset):
        """
        Create a beatmapset object given a dictionary of attributes. Converts beatmaps to ``OsuBeatmap``
        objects

        **Params**

        * beatmapset : dict of string-value pairs

        **Returns**

        * ``OsuBeatmapset``

        """


        bmpset = cls()

        for attr in bmpset.__dict__:

            if attr == "beatmaps":
                beatmaps = []
                beatmaps_dict = beatmapset["beatmaps"]
                for bmpdict in beatmaps_dict:
                    beatmaps.append(OsuBeatmap.from_dict(bmpdict))
                bmpset.beatmaps = beatmaps
            else:
                bmpset.__setattr__(attr, beatmapset[attr])

        return bmpset