from backend.src.Beatmap.Object.HitObject import HitObject


class Spinner(HitObject):

    def __init__(self, x, y, time, obj_type, endTime):
        super().__init__(x, y, time, obj_type)
        self.endTime = endTime

    @classmethod
    def from_text(cls, text):
        csv = text.split(",")
        return cls(int(csv[0]), int(csv[1]), int(csv[2]), int(csv[3]), int(csv[5]))

