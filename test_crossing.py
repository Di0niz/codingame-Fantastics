# -*- coding: utf-8 -*- 

import sys
import math
import unittest

from app import Vec2
import matplotlib.pyplot as plt


class Vec2TestCase (unittest.TestCase):


    def line(self,a,b):

        m = (a.y - b.y)/(a.x - b.x)

        return m 
    
    def test_seek(self):

        p1 = Vec2(2,3)
        p2 = Vec2(15,15)

        print p2.lenght()
        print p1.distance(p2)

        gate1 = Vec2(10,8)
        gate2 = Vec2(10,12)

        angle = p1.angle_to(p2) 
        angle_min = p1.angle_to(gate1) 
        angle_max = p1.angle_to(gate2) 

        print "%f" % angle_min 
        print "%f" % angle
        print "%f" % angle_max

        print (angle_min <= angle <= angle_max or angle_min >= angle >= angle_max )


  

if __name__ == '__main__':
    unittest.main()
