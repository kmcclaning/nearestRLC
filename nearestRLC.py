# -*- coding: utf-8 -*-
"""
Finds the nearest standard component value for 20%, 10% 5%, 2% 1%, and 0.5%
tolerances
"""

__author__ = "K.J. McClaning"
__created__ = "2020-10-02"
__updated__ = "2022-08-04"
__version__ = "0.0.2"

# MIT License
#
# Copyright (c) 2022 K.J. McClaning
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import math
from bisect import bisect_left

# enumerated lists of normalized component values: 20%, 10%, 5%, 2%, 1%, and 0.5%
# list of 0.5% component values, E192 series
tol0p5L = [
    1.00, 1.01, 1.02, 1.04, 1.05, 1.06, 1.07, 1.09, 1.10, 1.11, 1.13, 1.14, 1.15, 1.17, 1.18, 1.20, 1.21, 1.23,
    1.24, 1.26, 1.27, 1.29, 1.30, 1.32, 1.33, 1.35, 1.37, 1.38, 1.40, 1.42, 1.43, 1.45, 1.47, 1.49, 1.50, 1.52,
    1.54, 1.56, 1.58, 1.60, 1.62, 1.64, 1.65, 1.67, 1.69, 1.72, 1.74, 1.76, 1.78, 1.80, 1.82, 1.84, 1.87, 1.89,
    1.91, 1.93, 1.96, 1.98, 2.00, 2.03, 2.05, 2.08, 2.10, 2.13, 2.15, 2.18, 2.21, 2.23, 2.26, 2.29, 2.32, 2.34,
    2.37, 2.40, 2.43, 2.46, 2.49, 2.52, 2.55, 2.58, 2.61, 2.64, 2.67, 2.71, 2.74, 2.77, 2.80, 2.84, 2.87, 2.91,
    2.94, 2.98, 3.01, 3.05, 3.09, 3.12, 3.16, 3.20, 3.24, 3.28, 3.32, 3.36, 3.40, 3.44, 3.48, 3.52, 3.57, 3.61,
    3.65, 3.70, 3.74, 3.79, 3.83, 3.88, 3.92, 3.97, 4.02, 4.07, 4.12, 4.17, 4.22, 4.27, 4.32, 4.37, 4.42, 4.48,
    4.53, 4.59, 4.64, 4.70, 4.75, 4.81, 4.87, 4.93, 4.99, 5.05, 5.11, 5.17, 5.23, 5.30, 5.36, 5.42, 5.49, 5.56,
    5.62, 5.69, 5.76, 5.83, 5.90, 5.97, 6.04, 6.12, 6.19, 6.26, 6.34, 6.42, 6.49, 6.57, 6.65, 6.73, 6.81, 6.90,
    6.98, 7.06, 7.15, 7.23, 7.32, 7.41, 7.50, 7.59, 7.68, 7.77, 7.87, 7.96, 8.06, 8.16, 8.25, 8.35, 8.45, 8.56,
    8.66, 8.76, 8.87, 8.98, 9.09, 9.20, 9.31, 9.42, 9.53, 9.65, 9.76, 9.88,
]

# 1% tolerance, E96 series
tol01L = [
    1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50,
    1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32,
    2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57,
    3.65, 3.74, 3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49,
    5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45,
    8.66, 8.87, 9.09, 9.31, 9.53, 9.76,
]

# 2% tolerance, E48 series
tol02L = [
    1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54, 1.62, 1.69, 1.78, 1.87, 1.96, 2.05, 2.15, 2.26,
    2.37, 2.49, 2.61, 2.74, 2.87, 3.01, 3.16, 3.32, 3.48, 3.65, 3.83, 4.02, 4.22, 4.42, 4.64, 4.87, 5.11, 5.36,
    5.62, 5.90, 6.19, 6.49, 6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53,
]

# 5% tolerance, E24 series
tol05L = [
    1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8,
    7.5, 8.2, 9.1,
]

# 10% tolerance, E12 series
tol10L = [
    1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2,
]

# 20% tolerance, E6 series
tol20L = [
    1.0, 1.5, 2.2, 3.3, 4.7, 6.8,
]


def findNearestNormalized(valueL, exactValue):
    """
    Given a list of normalized values in [1.0,10.0), search through the list
    for the value closest to normalizedExactValue.
    :param list of floats valueL: list of sorted normalized values in [1.0,10.0). Must
    be sorted in ascending order.
    :param float exactValue: the exact value we want to quantize, in [1.0,10.0).
    :return float: a value from normalizedValueL that is closest to normalizedExactValue.
    """
    # find insertion point into sorted list
    idx = bisect_left(valueL, exactValue)

    # # check for edges of list
    if idx == 0:
        return valueL[0]
    if idx == len(valueL):
        return valueL[-1]

    # see if lower or upper element is closer to cExact
    beforeVal = valueL[idx - 1]
    afterVal = valueL[idx]
    if (afterVal - exactValue) < (exactValue - beforeVal):
        return afterVal
    else:
        return beforeVal


def findNearest(theList, exactValue):
    """
    Normalizes exactValue to [1.0,10.0), finds the nearest value in theList, then
    un-normalizes the value returned from the list
    :param list of floats theList: list of sorted normalized values in [1.0,10.0). Must
    be sorted in ascending order.
    :param exactValue: the exact value we want to quantize
    :return float nearestValue: the value from the passed list that is nearest to the
    exact value, with the proper exponent i.e. non-normalized
    """
    # get exactValue mantissa in [1.0,10.0)
    log10Exact = math.log10(abs(exactValue))
    exactExp = math.floor(log10Exact)
    exactMantissa = math.pow(10, (log10Exact - exactExp))

    # find the nearest normalized value from the list, and non-normalize the result
    nearestMantissa = findNearestNormalized(theList, exactMantissa)
    nearestValue = nearestMantissa * pow(10, exactExp)

    # fix up for negative exactValue
    if exactValue < 0.0:
        nearestValue *= -1.0

    return nearestValue


def nearestRLC(rLCExact, tolS):
    """
    Quantifies the passed value to the tolerance passed in tolS
    :param float rLCExact: the exact value of the resistor, inductor or capacitor that we wish
    to quantize to 0.5%, 1.0%, 2.0%, 5.0%, 10.0% or 20.0%
    :param string tolS: string in 'exact', '0p5', '1p0', '2p0', '5p0', '10p0', '20p0'
    :return float rLCQuantized: the component value quantized to the passed tolerance
    """
    # check for 0.0, nan, inf
    if rLCExact == 0.0:
        return 0.0
    if math.isnan(rLCExact):
        return rLCExact
    if math.isinf(rLCExact):
        return rLCExact

    if 'exact' in tolS:
        rLCQuantized = rLCExact
    elif '0p5' in tolS:
        rLCQuantized = findNearest(tol0p5L, rLCExact)
    elif '1p0' in tolS:
        rLCQuantized = findNearest(tol01L, rLCExact)
    elif '2p0' in tolS:
        rLCQuantized = findNearest(tol02L, rLCExact)
    elif '5p0' in tolS:
        rLCQuantized = findNearest(tol05L, rLCExact)
    elif '10p0' in tolS:
        rLCQuantized = findNearest(tol10L, rLCExact)
    elif '20p0' in tolS:
        rLCQuantized = findNearest(tol20L, rLCExact)
    else:
        rLCQuantized = None

    return rLCQuantized

# ==========================================================================
