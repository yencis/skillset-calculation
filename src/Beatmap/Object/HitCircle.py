from Beatmap.Object.HitObject import HitObject


class HitCircle(HitObject):

    def __init__(self, x, y, time, obj_type):
        super().__init__(x, y, time, obj_type)
