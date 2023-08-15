"""
Beatmap TimingPoint
"""


class TimingPoint:

    def __init__(self, time, beat_length=0, uninherited=0):
        self.time = time
        self.beat_length = beat_length  # bpm = 60000/beatLength
        # self.meter = meter
        self.uninherited = uninherited

    @classmethod
    def from_text(cls, text):
        csv = text.split(",")
        time = int(csv[0])
        beat_length = float(csv[1])
        return cls(time, beat_length, 1 if beat_length > 0 else 0)

    @classmethod
    def key_time(cls, time):
        return cls(time)

    def is_inherited(self):
        return self.uninherited == 0

    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time

    def __gt__(self, other):
        return self.time > other.time

    def __ge__(self, other):
        return self.time >= other.time

    def __eq__(self, other):
        return self.time == other.time