"""
Test nearestRLC component tolerance quantizer
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


from unittest import TestCase

import math
from nearestRLC import nearestRLC


class TestEngNotation(TestCase):

    def test_nearest_rlc(self):
        """
        test the nearestRLC routine for various tolerances and orders of magnitude. Note that because of
        the way the E6 - E192 standards are defined, some resistors have a larger error than the spec
        indicates e.g. 2.015 at 0p5 => 2.03 (err: 0.744%) and 4.99 at 2p0 => 5.11 (err: 2.405%). Hence
        the use of the fudgeFactor variable.
        :return boolean: assertion results
        """
        # list of mantissas to check. Check from
        mantissaL = [
            2.015, 2.03334, 2.985, 5.1303, 5.1, 4.99, 1.0, 1.00001, 7404, 22, 2.0815, 4.4256, 2.7516,
            -3.3333, 0.0, 0, math.inf, -math.inf, math.nan,
        ]

        # fudge factor to handle the oddities of the tolerance standards
        fudgeFactor = 1.5

        # start the test
        testCount = 1
        for thisMantissa in mantissaL:

            # cover exponents from -15 to +15 to cover possible inductor, capacitor and resistor values
            thisExponent = -15
            while thisExponent <= 15:
                testVal = thisMantissa * pow(10.0, thisExponent)
                for tolS in ['exact', '0p5', '1p0', '2p0', '5p0', '10p0', '20p0']:

                    # find quantized representation of the exact value and inform the user
                    s = "%i: %e, %s" % (testCount, testVal, tolS)
                    quantizedVal = nearestRLC(testVal, tolS)
                    s += " => %e" % quantizedVal

                    # compare the test value with the quantized value. should be within thisTolerance percent.
                    # try/except is for 0.0, math.nan, math.inf
                    try:
                        errorPercent = 100.0 * abs(quantizedVal - testVal) / testVal
                        s += " (err: %.3f%%)" % errorPercent
                    except ZeroDivisionError:
                        errorPercent = 0.0
                        s += " (err: %.3f%%)" % math.nan
                    print(s)

                    # check for nan, inf, -inf first.
                    if math.isnan(testVal):
                        self.assertTrue(math.isnan(quantizedVal))
                    elif math.isinf(testVal):
                        self.assertTrue(testVal == quantizedVal)
                    elif 'exact' in tolS:
                        self.assertAlmostEqual(errorPercent, 0.0, 4)
                    elif '0p5' in tolS:
                        self.assertLessEqual(errorPercent, fudgeFactor * 0.5)
                    elif '1p0' in tolS:
                        self.assertLessEqual(errorPercent, fudgeFactor * 1.0)
                    elif '2p0' in tolS:
                        self.assertLessEqual(errorPercent, fudgeFactor * 2.0)
                    elif '5p0' in tolS:
                        self.assertLessEqual(errorPercent, fudgeFactor * 5.0)
                    elif '10p0' in tolS:
                        self.assertLessEqual(errorPercent, fudgeFactor * 10.0)
                    else:  # '20p0' in tolS:
                        self.assertLessEqual(errorPercent, fudgeFactor * 20.0)

                    testCount += 1
                thisExponent += 1

# ===========================================================================
