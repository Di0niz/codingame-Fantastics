# -*- coding: utf-8 -*- 

import sys
import math
import unittest

from app import Vec2
import matplotlib.pyplot as plt


class Vec2TestCase (unittest.TestCase):
    
    def test_seek(self):


        max_velocity = 40
        max_force    = 30
        max_speed    = 40
        mass = 1.0

        t = Vec2(40,100)
        vt = Vec2(30,0)

        i = Vec2(0,0)
        vi = Vec2(10,30)

        
        position = i.add(vi).mult(3)

        futurePosition = i.add(vi).mult(3)



#        velocity = t.sub(position).normalize().mult(100)

#        new_t = t
#
#        new_t = t.add(vt.mult(3))
#
#        desired_velocity = new_t.sub(i).normalize().mult(max_velocity)
#        steering = desired_velocity.sub(vi)
#


#
#        steering = desired_velocity.sub(velocity)
#
#        steering = steering.truncate_lenght (max_force)
#        steering = steering.div(mass)
#
#
#        velocity = velocity.truncate_lenght(max_speed)
#        position = position.add(velocity)

        ax = plt.axes()

        new_i = i.add(desired_velocity)

        ax.arrow(i.x, i.y, vi.x, vi.y, head_width=0.05, head_length=0.1, fc='k', ec='k')
        ax.add_patch(plt.Circle((i.x, i.y), 40,fill=False, edgecolor="red",alpha=0.8))
        ax.add_patch(plt.Circle((new_i.x, new_i.y), 40,fill=False, edgecolor="red",alpha=0.3))

        ax.arrow(i.x, i.y, steering.x, steering.y, head_width=0.05, head_length=0.1, color="blue")
        ax.arrow(i.x, i.y, desired_velocity.x, desired_velocity.y, head_width=0.05, head_length=0.1, color="yellow")


        ax.arrow(t.x, t.y, vt.x, vt.y, head_width=0.05, head_length=0.1, fc='k', ec='k')
        ax.add_patch(plt.Circle((t.x, t.y), 10,fill=False, edgecolor="red",alpha=0.8))




        plt.xlim(-40,200) 
        plt.ylim(-40,200) 

        plt.show()




if __name__ == '__main__':
    unittest.main()
