import bezier.curve as bezier
import numpy as np

class Bezier:

    def __init__(self, control_points):
        self.control_points = control_points

        # check control points to see how many Bezier's to combine to create one Bezier

        _beziers = []  # list of list of Beziers

        last_point = None
        cur_bezier = []

        for point in control_points:
            if last_point and last_point == point:
                _beziers.append(cur_bezier)
                cur_bezier = [point]
            else:
                last_point = point
                cur_bezier.append(point)

        _beziers.append(cur_bezier)

        self.beziers = [self._approximate_bspline(bezier_points) for bezier_points in _beziers]


        # self.curve = self._approximate_bspline(control_points)  # here for legacy reasons so shit doesn't fuck up yet

        self.total_bezier_length = 0

        self.linear_points = [np.ndarray.flatten(self.beziers[0].evaluate(0.0))]  # list of points, denoting the piecewise linear approximation of the Bezier curve

        for bezier_curve in self.beziers:
            self.total_bezier_length += bezier_curve.length
            self.linear_points += Bezier.linearize(bezier_curve, threshold=0.1)[1::]


    def _approximate_bspline(self, control_points, p=0):

        nodes = np.zeros((2, len(control_points)))
        for i, point in enumerate(control_points):
            nodes[0][i] = point[0]
            nodes[1][i] = point[1]

        nodes = np.asfortranarray(nodes)

        curve = bezier.Curve.from_nodes(nodes)
        return curve

    def evaluate(self, s):
        """
        Bezier evaluate

        Parameter: s, percentage of bezier

        Returns: coordinate of bezier at s of bezier

        Will fail if s is too large
        """
        running_length = 0

        for bezier_curve in self.beziers:

            # how much does current curve contribute to the entire curve

            additive_ratio = running_length / self.total_bezier_length
            running_length += bezier_curve.length

            if running_length / self.total_bezier_length >= s:

                # required segment is current bezier curve, evaluate this curve

                cur_curve_ratio = bezier_curve.length / self.total_bezier_length
                cur_curve_s = (s - additive_ratio) / cur_curve_ratio
                return bezier_curve.evaluate(cur_curve_s)
        return [None]

    def segment(self, s_vals):
        """
        Evaluate the bezier on a list of s_vals

        Returns: a list of points (the result of evaluate)
        """
        points = []
        for s_val in s_vals:
            point = self.evaluate(s_val)
            if point[0]:
                points.append((point[0], point[1]))
            else:
                continue
        # points = self.curve.evaluate_multi(s_vals)
        # print(points)
        return points
        #return [(points[0][i], points[1][i]) for i in range(len(s_vals))]

    @staticmethod
    def flatness(curve, precision=0.1):
        """
        Evaluate how flat this Bézier curve is.
        Compare the area of the error between this Bezier and a straight line connecting its endpoints

        Returns: float, area of the error between a line and this Bezier
        """

        startx, starty = np.ndarray.flatten(curve.evaluate(0.0))
        endx, endy = np.ndarray.flatten(curve.evaluate(1.0))

        if endx - startx == 0:
            slope = 1000
        else:
            slope = (endy - starty) / (endx - startx)

        total_area_error = 0

        for x in np.arange(0,1,precision):
            curve_x, curve_y = np.ndarray.flatten(curve.evaluate(x))
            line_y = slope * (curve_x - startx) + starty
            error = curve_y - line_y
            total_area_error += np.abs(error) * precision

        return total_area_error

    @staticmethod
    def linearize(curve, threshold=0.001):
        """
        Turn the curve into a piecewise linear approximation for ease of rendering. Threshold value is the minimum
        flatness error

        Returns: list of points, where lines should be rendered connecting all points
        """
        start_point = np.ndarray.flatten(curve.evaluate(0.0))

        return [start_point] + Bezier._linearize_helper(curve, threshold=threshold)

    @staticmethod
    def _linearize_helper(curve, threshold=0.001):
        """
        Recursively subdivide curve and linearize subdivisions
        """

        if Bezier.flatness(curve) < threshold:
            return [np.ndarray.flatten(curve.evaluate(1.0))]
        else:
            l, r = curve.subdivide()
            return Bezier._linearize_helper(l, threshold=threshold) + Bezier._linearize_helper(r, threshold=threshold)
