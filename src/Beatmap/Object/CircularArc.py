import numpy as np

"""
Transpilation of osu-framework /utils/CircularArcProperties.cs
"""


class CircularArc:

    def __init__(self, control_points):
        """
        Requires: control_points contains only 3 points
        (Otherwise a circular arc should not be made)
        """

        assert len(control_points) == 3

        self.control_points = control_points

        a = control_points[0]
        b = control_points[1]
        c = control_points[2]

        # if degenerate triangle with one side-length almost equal zero, give up and fallback to more stable method

        if np.isclose(0, (b[1] - a[1]) * (c[0] - a[0]) - (b[0] - a[0]) * (c[1] - a[1])):
            self.isValid = False
            return

        d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))

        aSq = a.lengthSquared()
        bSq = b.lengthSquared()
        cSq = c.lengthSquared()

        center = np.array([aSq * (b[1] - c[1]) + bSq * (c[1] - a[1]) + cSq * (a[1] - b[1]),
                           aSq * (c[0] - b[0]) + bSq * (a[0] - c[0]) + cSq * (b[0] - a[0])]) / d

        dA = a.as_ndarray() - center
        dC = c.as_ndarray() - center

        self.radius = np.linalg.norm(dA)

        theta_start = np.arctan2(dA[1], dA[0])
        theta_end = np.arctan2(dC[1], dC[0])

        while theta_end < theta_start:
            theta_end += 2 * np.pi

        direction = 1
        theta_range = theta_end - theta_start

        # decide in which direction to draw the circle, depending on which side of AC B lies
        orthoAtoC = c.as_ndarray() - a.as_ndarray()

        temp = orthoAtoC[0]
        orthoAtoC[0] = orthoAtoC[1]
        orthoAtoC[1] = -temp

        if np.dot(orthoAtoC, b.as_ndarray() - a.as_ndarray()) < 0:
            direction = -direction
            theta_range = 2 * np.pi - theta_range

        self.isValid = True
        self.theta_start = theta_start
        self.theta_end = theta_end
        self.theta_range = theta_range
        self.direction = direction
        self.length = theta_range * self.radius
        self.center = center
        self.linear_points = self.linearize()

    def evaluate(self, s):
        """
        Parametize this arc and then evaluate it

        Parameter: s between 0 and 1 (percent of curve travel)
        """
        t = self.theta_range * s
        x = self.center[0] + self.radius * np.cos(self.theta_start + t)
        y = self.center[1] + self.radius * np.sin(self.theta_start + t)
        return np.array([x, y])

    def linearize(self):
        return [self.evaluate(i) for i in np.linspace(0, 1, int(self.length)+1)]
