#!/usr/bin/env python3
""" Calculates the bspline given control points and end points"""

__author__ = "Tejaswin Parthasarathy"
__license__ = "GPL"

import numpy as np


def snake_bspline(t_coeff, l_centerline=1.0, keep_pts=False):
    """ Generates a bspline object that plots the spline interpolant for
    any vector x. Optionally takes in a centerline length, set to 1.0 by
    default and keep_pts for keeping record of control points

    Parameters
    ----------
    t_coeff : np.array
        The spline coefficients, denoted by :math:`beta_i`. Note that the first
        and the last values are set to zero by default.
    l_centreline : float
        The length of the centerline in meters.
    keep_pts : boolean, optional
        If True, we keep record of control point and coefficients at those points
        by returned as a (3, ) tuple. If False, returns only the splibe object.
        Defaults to False.

    Returns
    -------
    spline : scipy.interpolate.Bspline class
        A spline class that can be called as spline(x), where x are the points at
        which the spline needs to be evaluated.
    """
    # Divide into n_control_pts numbrer of points (n_ctr_pts-1) regions
    control_pts = l_centerline * np.linspace(0.0, 1.0, t_coeff.shape[0])

    # Degree of b-spline required. Set to cubic
    degree = 3

    # Update coefficients at the head and tail
    # Setting it to 0.0 here
    beta_head = 0.0
    beta_tail = 0.0

    if keep_pts:
        # Keep record of control point and coefficient at those points
        return __bspline_impl__(control_pts, t_coeff, beta_head, beta_tail,
                                degree)
    else:
        return __bspline_impl__(control_pts, t_coeff, beta_head, beta_tail,
                                degree)[0]


def __bspline_impl__(x_pts, t_c, b_head, b_tail, t_k):
    """
        """
    from scipy.interpolate import BSpline

    # Update the coefficients
    #
    t_c = np.hstack((b_head, t_c, b_tail))

    # Update the knots
    # You need 2 additional knots for the head and tail control points
    # You need degree + 1 additional knots to sink into the head and tail for
    # controlling C^k smoothness. We set it to 0.0
    n_upd = x_pts.shape[0] + 2 + (t_k + 1)

    # The first and last points are always fixed
    x_first = x_pts[0]
    x_last = x_pts[-1]
    x_pts = np.hstack((x_first, x_pts, x_last))

    # Generate the knots
    knots_updated = np.zeros(n_upd, )
    # Sink first degree-1 knots into head
    knots_updated[:t_k - 1] = x_first
    # Middle knot locations correspond to x_locations
    knots_updated[t_k - 1:n_upd - (t_k - 1)] = x_pts
    # Sink first degree-1 knots into tail
    knots_updated[n_upd - (t_k - 1):] = x_last

    return BSpline(knots_updated, t_c, t_k, extrapolate=False), x_pts, t_c


def test_bspline():
    """ Test object for the bspline function"""
    l_centre = 1.0
    t_coeff = np.abs(np.random.randn(6, ))
    my_spline, ctr_pts, ctr_coeffs = snake_bspline(t_coeff, keep_pts=True)
    my_spline(2.0)

    from matplotlib import pyplot as plt
    s = np.linspace(0.0, l_centre, 200)
    plt.plot(s, my_spline(s))
    plt.plot(ctr_pts, ctr_coeffs, 'kx')
    plt.show()


if __name__ == "__main__":
    test_bspline()
