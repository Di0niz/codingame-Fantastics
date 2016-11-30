import sys
import math
import unittest

from app import Vec2


def seek(i,vi, t, vt):
    
    max_velocity = 30

    new_t = t.add(vt.mult(3))

    desired_velocity = new_t.sub(i).normalize().mult(max_velocity)
#    steering = desired_velocity.sub(vi)   

    return (i.add(desired_velocity), desired_velocity, t.add(vt), vt)


def main():
    

    a = Vec2(0,0)
    va = Vec2(25,0)

    t = Vec2(60,100)
    vt = Vec2(20,0)

    print "distance %s" % a.distance(t) 

    d = a.distance(t) 
    dd = 0
    while (d >= 30):
        pt = t
        (a,va,t,vt) = seek (a,va,t,vt)
        print "distance %s" % d 
        print "seek %s" % str((a,va,t,vt))
        print "" 

        dd = dd + va.lenght()
        d = a.distance(t) 

    print "True dist: %s" % dd



if __name__ == '__main__':
    main()
