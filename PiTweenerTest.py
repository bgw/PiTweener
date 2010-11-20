from PiTweener import *
import unittest
import random

class TweenerTest(unittest.TestCase):
    pass
    
class FormulaTest(unittest.TestCase):
    def setUp(self):
        e = TweenerEquations()
        self.tweener_equations = e
        self.func_list = [e.OUT_EXPO, e.LINEAR, e.IN_QUAD, e.OUT_QUAD,
                          e.IN_OUT_QUAD, e.OUT_IN_QUAD, e.IN_CUBIC, e.OUT_CUBIC,
                          e.IN_OUT_CUBIC, e.OUT_IN_CUBIC, e.IN_QUART,
                          e.OUT_QUART, e.IN_OUT_QUART, e.OUT_ELASTIC]
        # funct_list[n](time_since_start, start_val, change_in_val,
        #               total_duration)
    
    def test_middle_values(self):
        # no equation should throw an exception when values in between the min
        # and max time are used
        for i in range(1000):
            t = random.random() * 100.
            st_val = random.random() * 100.
            ch_val = random.random() * 100.
            cur_t = t * random.random()
            for f in self.func_list:
                self.failIf(isinstance(f(cur_t, st_val, ch_val, t),
                                       complex),
                            "Incorrect middle value for easing equation: " +
                            f.__name__)
    
    def test_final_values(self):
        # all equations should end up at startval + changeinval, within a margin
        # of rounding error
        for i in range(1000):
            t = random.random() * 100. + .5 # we don't want a value so tiny that
                                            # it causes rounding issues
            st_val = random.random() * 100. + .5
            ch_val = random.random() * 100. + .5
            for f in self.func_list:
                # within 4 decimal places of accuracy
                self.assert_(math.fabs(
                                 f(t, st_val, ch_val, t) - st_val - ch_val)
                                 < .0001,
                             "Incorrect ending value for easing equation: " +
                             f.__name__)

if __name__ == "__main__":
    unittest.main()
else:
    raise Exception("PiTweenerTest is a program, not a library, and as such, " +
                    "should not be imported.")
