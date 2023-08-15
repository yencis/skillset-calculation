import Beatmap.Object.HitObject as HitObject
import Beatmap.Object.TimingPoint as TimingPoint
import bisect


class Beatmap:
    """
    Data defining a beatmap:
    Contains a list of hitobjects (hitcircles and sliders) as well as song timings
    """

    class Difficulty:
        """
        Attributes relating to beatmap difficulty settings
        """

        def __init__(self, hp, cs, od, ar, sm, tr):
            self.hp = hp
            self.cs = cs
            self.od = od
            self.ar = ar
            self.sm = sm
            self.tr = tr

    def __init__(self, hp, cs, od, ar, sm, tr):  # sm = slidermultiplier, tr = tick rate
        self.difficulty = self.Difficulty(hp, cs, od, ar, sm, tr)
        self.timingPoints = []
        self.hitObjects = []
        self.preempt = 1200  # ms
        self.fade_in = 800
        if ar > 5:
            self.preempt -= 750 * (self.difficulty.ar - 5) / 5
            self.fade_in -= 500 * (self.difficulty.ar - 5) / 5
        elif ar < 5:
            self.preempt += 600 * (5 - self.difficulty.ar) / 5
            self.fade_in += 400 * (5 - self.difficulty.ar) / 5

    def check_timings(self):
        return len(self.timingPoints) > 0

    def get_objects_at(self, time):
        """
        Objects currently present on the playfield
        """

        lb = bisect.bisect_left(self.hitObjects, HitObject.HitObject.key_time(time))
        ub = bisect.bisect(self.hitObjects,
                           HitObject.HitObject.key_time(time + self.preempt))  # right binsearch, subtract 1
        return [self.hitObjects[obj] for obj in range(lb, ub)]

    def get_opacity_of_hitobject(self, hitobject, time):
        hit_interval = hitobject.time - time

        full_opacity = self.preempt - self.fade_in

        if hit_interval < 0 or hit_interval > self.preempt:
            return 0

        if 0 < hit_interval < full_opacity:
            return 1

        return 1 - ((hit_interval - full_opacity) / self.fade_in)

    def get_sv_at(self, time):  # we want slider velocity in osu pixels per millisecond

        # check if there is at least 1 timing point

        assert self.check_timings()

        index = bisect.bisect(self.timingPoints, TimingPoint.TimingPoint.key_time(time)) - 1

        # check if timing point is inherited

        base_slider_velocity = self.difficulty.sm

        if self.timingPoints[index].is_inherited():
            timing_slider_multiplier = - (100 / self.timingPoints[index].beat_length)



        return self.timingPoints[index]



    def get_duration(self):
        return self.hitObjects[-1].time + 1000  # 1s end time
