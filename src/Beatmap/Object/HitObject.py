class HitObject:

    def __init__(self, x=0, y=0, time=0, obj_type=0):
        self.x = x
        self.y = y
        self.time = time
        self.type = obj_type

    @classmethod
    def from_text(cls, text):
        csv = text.split(",")
        return cls(int(csv[0]), int(csv[1]), int(csv[2]), int(csv[3]))

    @classmethod
    def key_time(cls, time):
        return cls(time=time)

    def is_slider(self):
        return self.type & 2 == 2

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

    def __str__(self, other):
        return "HitObject=(x:{x}, y:{y}, time:{time}, type:{type})".format(x=self.x, y=self.y, time=self.time,
                                                                           type=self.type)
