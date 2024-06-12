import datetime
import requests
import OsuGamemode

class OsuScore:
    """
    Class representing how a user's score is described by the osu! API
    Attribute wrapper for osu! scores.
    """
    def __init__(self):
        self.accuracy = 0
        self.best_id = 0
        self.created_at = ""
        self.id = 0
        self.max_combo = 0
        self.mode = ""
        self.mode_int = 0
        self.mods = []
        self.passed = True
        self.perfect = False
        self.pp = 0
        self.rank = ""
        self.replay = False
        self.score = 0
        self.statistics = {}
        self.type = ""
        self.user_id = 0
        self.current_user_attributes = {}
        self.beatmap = None
        self.beatmapset = None
        self.user = None
        self.weight = {}