# -*- coding: utf-8 -*- 

import sys
import math
import unittest

from steer import Vec2


class Vec2TestCase (unittest.TestCase):
    
    def test_first_step(self):

        a = Vec2(1,2)
        b = Vec2(2,9)
        print a.normalize().dot(b.normalize())

        print a.angle_to(b)

        pass


if __name__ == '__main__':
    unittest.main()
