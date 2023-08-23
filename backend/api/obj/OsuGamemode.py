class OsuGamemode:
    """
    Represents an osu! gamemode
    """
    # functionally this class is useless but it's really funny

    gamemodes = {0:"standard",1:"taiko",2:"ctb",3:"mania"}

    @staticmethod
    def decode(self, code):
        return self.gamemodes[code]