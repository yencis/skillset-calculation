from Beatmap.Object.HitObject import HitObject
from Beatmap.Object.ControlPoint import ControlPoint
from Beatmap.Object.Bezier import Bezier


class Slider(HitObject):

    def __init__(self, x, y, time, type, curveType, curvePoints, sliders, length):
        super().__init__(x, y, time, type)
        self.curveType = curveType  # B = bezier C = catmull L = linear P = circle
        self.curvePoints = curvePoints  # list of control points
        self.sliders = sliders
        self.length = length

        self.bezier = Bezier(curvePoints)

    @classmethod
    def from_text(cls, text):
        csv = text.split(",")
        curve = csv[5]
        curve_points = [ControlPoint(x=int(csv[0]), y=int(csv[1]))]
        curve_psv = curve.split("|")
        curve_type = curve_psv[0]

        for i in range(1, len(curve_psv)):
            curve_points.append(ControlPoint.from_text(curve_psv[i]))

        slide = int(csv[6])
        length = float(csv[7])
        return cls(int(csv[0]), int(csv[1]), int(csv[2]), int(csv[3]), curve_type, curve_points, slide, length)
