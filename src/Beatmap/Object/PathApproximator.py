"""
Code transpiled from osu-framework: PathApproximator.cs

Link: https://github.com/ppy/osu-framework/blob/master/osu.Framework/Utils/PathApproximator.cs

"""

import numpy as np


"""
class PathApproximator:

    def __init__(self):
        self.bezier_tolerance = 0.25
        self.catmull_detail = 50
        self.circular_arc_tolerance = 0.1

    def ApproximateBezier(self, control_points):
        return self.ApproximateBSpline(control_points)

    def ApproximateBSpline(self, control_points, p=0):

        output = []
        n = len(control_points) - 1

        if n < 0:
            return output

        toFlatten = []
        freeBuffers = []

        points = control_points

        if p > 0 and p < n:

            # subdivide b-spline into bezier control points at knots

            for i in range(n - p):
                subBezier = [None] * (p+1)
                subBezier[0] = points[i]

                # destructively insert the knot p - 1 times via Boehm's algorithm

                for j in range(p - 1):
                    subBezier[j + 1] = points[i + 1]

                    for k in range(1, p - j):
                        l = min(k, n - p - i)
                        points[i + k] = (l * points[i + k] + points[i + k + 1]) / (l + 1)

                subBezier[p] = points[i + 1]
                toFlatten.append(subBezier)

            toFlatten.append(points[(n-p)::])
            # reverse the stack so elements can be accessed in order
            toFlatten = toFlatten[::-1]
        else:
            # B-spline subdivision unnecessary, degenerate to single bezier
            p = n
            toFlatten.append(points)

        # ``toFlatten`` contains all the curves which are not yet approximated well enough.
        # We use a stack to emulate recursion without the risk of running into stack overflow.
        # (More specifically, we iteratively and adaptively refine our curve with a
        # DFS
        # over the tree resulting from the subdivisions we make.

        subdivisionBuffer1 = [None] * (p + 1)
        subdivisionBuffer2 = [None] * (p * 2 + 1)

        leftChild = subdivisionBuffer2

        while len(toFlatten) > 0:
"""