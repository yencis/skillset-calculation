import datetime
import requests
import OsuGamemode

class OsuBeatmap:
    """
    Class representing how a Beatmap is described by the osu! API.
    Attribute wrapper for osu! beatmaps.
    """
    def __init__(self):
        self.beatmapset_id = -1
        self.difficulty_rating = -1.0
        self.id = -1
        self.mode = 'osu'
        self.status = 'ranked'
        self.total_length = -1
        self.user_id = -1
        self.version = ''
        self.accuracy = -1.0
        self.ar = -1.0
        self.bpm = -1.0
        self.convert = False
        self.count_circles = -1
        self.count_sliders = -1
        self.count_spinners = -1
        self.cs = -1
        self.deleted_at = None
        self.drain = -1
        self.hit_length = -1
        self.is_scoreable = True
        self.last_updated = None
        self.mode_int = -1
        self.passcount = -1
        self.playcount = -1
        self.ranked = 1
        self.url = ""
        self.checksum = ""
        self.max_combo = 0

    @classmethod
    def from_dict(cls, beatmap):
        """
        Create a beatmap object given a dictionary of attributes.

        **Params**

        * beatmap : dict of string-value pairs

        **Returns**

        * ``OsuBeatmap``

        """

        bmp = cls()
        # Imagine releasing this code
        # bmp.__dict__ = beatmap
        for attribute in bmp.__dict__:
            bmp.__setattr__(attribute, beatmap[attribute])
        return bmp

    def get_attributes(self):
        """
        Get this beatmap's attributes as a dictionary of string-value pairs.

        **Returns**

        * dict

        """
        return self.__dict__

    def get_osu_file(self, beatmap_id):
        """
        Get this beatmap's ``.osu`` file

        **Returns**

        * string
            The ``.osu`` file as text.
        """
        return requests.get(f"https://osu.ppy.sh/osu/{beatmap_id}").text

    def get_gamemode(self):
        """
        Return this beatmap's original gamemode

        **Returns**

        * string
            Name of gamemode
        """
        return OsuGamemode.decode(self.mode_int)