from Beatmap.Object.HitObject import HitObject
from Beatmap.Object.ControlPoint import ControlPoint
from Beatmap.Object.Bezier import Bezier
from Beatmap.Object.CircularArc import CircularArc
import numpy as np


class Slider(HitObject):

    def __init__(self, x, y, time, type, curveType, curvePoints, sliders, length):
        super().__init__(x, y, time, type)
        self.curveType = curveType  # B = bezier C = catmull L = linear P = circle
        self.curvePoints = curvePoints  # list of control points
        self.sliders = sliders
        self.length = length
        self.slider_velocity = -1  # if sv hasnt been set, defaults to -1
        """
        Will probably refactor later with a ``Curve`` abstract class, sorry for spaghetti in the meantime
        """
        self.inner_curve_length = 0  #unfortunate workaround with an abstract curve class
        if self.curveType == "B" or self.curveType == "L":
            self.bezier = Bezier(curvePoints)
            self.linear_points = self.bezier.linear_points
            self.inner_curve_length = self.bezier.total_bezier_length
        elif self.curveType == "P":
            self.arc = CircularArc(curvePoints)

            if not self.arc.isValid:
                self.bezier = Bezier(curvePoints)
                self.linear_points = self.bezier.linear_points
                self.inner_curve_length = self.bezier.total_bezier_length
                self.curveType = "B"
            else:
                self.linear_points = self.arc.linear_points  # implement this
                self.inner_curve_length = self.arc.length

        else: # aint no way we got a catmull user chat
            self.bezier = Bezier(curvePoints)  # bezier placeholder, it'll probably look better anyways
            self.linear_points = self.bezier.linear_points
            self.inner_curve_length = self.bezier.total_bezier_length

    @classmethod
    def from_text(cls, text):
        csv = text.split(",")
        curve = csv[5]
        curve_points = [ControlPoint(x=int(csv[0]), y=int(csv[1]))]
        curve_psv = curve.split("|")

        curve_type = curve_psv[0]

        for i in range(1, len(curve_psv)):
            curve_points.append(ControlPoint.from_text(curve_psv[i]))

        # curve_type = "B"

        slide = int(csv[6])
        length = float(csv[7])
        return cls(int(csv[0]), int(csv[1]), int(csv[2]), int(csv[3]), curve_type, curve_points, slide, length)

    def travel_time(self):  # how long it takes to get from start of slider to end in ms
        return self.length / self.slider_velocity

    def get_sv(self):
        return self.slider_velocity

    def set_sv(self, sv):
        self.slider_velocity = sv

    def slider_at_time(self,time):
        """
        Slider coordinates at time ``time``.

        Returns: coordinate if ``time`` is between slider.time and slider.time + travel_time as ndarray
        Otherwise returns (None,None) (Point of Nones)
        """
        if time < self.time or time > self.time + self.travel_time():
            return (None, None)
        elif self.curveType=="B" or self.curveType=="L":
            relative_time = time - self.time
            time_percent = relative_time / self.travel_time()

            # scale time_percent to the actual length of the object

            time_percent *= np.clip(self.length / self.bezier.total_bezier_length,0,1)

            return np.ndarray.flatten(self.bezier.evaluate(time_percent))
        elif self.curveType=="P":
            relative_time = time - self.time
            time_percent = relative_time / self.travel_time()

            # scale time_percent to the actual length of the object

            time_percent *= np.clip(self.length / self.arc.length, 0, 1)

            return np.ndarray.flatten(self.arc.evaluate(time_percent))
        else:
            #catmull
            pass

    def evaluate_curve(self, s):
        #print(s, self.curveType)
        if self.curveType == "B" or self.curveType == "L":
            return self.bezier.evaluate(s)
        elif self.curveType == "P":
            return self.arc.evaluate(s)
        else:
            return self.bezier.evaluate(s)
