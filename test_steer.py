# -*- coding: utf-8 -*- 

import sys
import math
import unittest

from steer import Vec2


class Vec2TestCase (unittest.TestCase):
    
    def test_first_step(self):

        a = Vec2(1,2)
        print a.sub(Vec2(2,7))

        print a
 
        pass


if __name__ == '__main__':
    unittest.main()
