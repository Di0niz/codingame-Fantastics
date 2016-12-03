# -*- coding: utf-8 -*- 

import sys
import math
import unittest

from app import Vec2, Entity, World, Strategy
import matplotlib.pyplot as plt


class Vec2TestCase (unittest.TestCase):
    
    def test_steer(self):

        wizard = Entity('0','WIZARD','1109','5353','82','77','0',400,300,1,0.75)

        t = Entity('6','SNAFFLE','2650','6813','0','0','0',150,800,0,0.75)

        wizard.set_target_unit(t, 150)

        print wizard.get_direction()
        print wizard.get_force()

        print wizard.position
        print "v: %s" % wizard.desired_velocity
        print "s: %s - %f" % (wizard.steer, wizard.steer.length())

        sneer = Vec2(4703,3510).normalize().mult(150)
        print sneer




        print "Entity('0','WIZARD','1109','5353','82','77','0',400,300,1,0)"
        



if __name__ == '__main__':
    unittest.main()
