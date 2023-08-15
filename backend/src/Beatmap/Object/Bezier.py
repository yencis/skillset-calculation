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


        self.curve = self._approximate_bspline(control_points)  # here for legacy reasons so shit doesn't fuck up yet

        self.total_bezier_length = 0

        for bezier_curve in self.beziers:
            self.total_bezier_length += bezier_curve.length

    def _approximate_bspline(self, control_points, p=0):

        nodes = np.zeros((2, len(control_points)))
        for i, point in enumerate(control_points):
            nodes[0][i] = point[0]
            nodes[1][i] = point[1]

        nodes = np.asfortranarray(nodes)

        curve = bezier.Curve.from_nodes(nodes)
        return curve

    def evaluate(self, s):

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



# TODO: fix code, make it safer and prettier and maybe faster

    def segment(self, s_vals):
        points = []
        for s_val in s_vals:
            point = self.evaluate(s_val)
            try:
                points.append((point[0], point[1]))
            except:
                continue
        # points = self.curve.evaluate_multi(s_vals)
        # print(points)
        return points
        #return [(points[0][i], points[1][i]) for i in range(len(s_vals))]
