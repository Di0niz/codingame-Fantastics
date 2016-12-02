# -*- coding: utf-8 -*- 

import sys
import math
import unittest

from app import Vec2, World, Strategy, Entity


def find_avoidance():

    w = World(0)
    w.wizards.append(Entity('0','WIZARD','3487','5376','278','14','0',400,300,1,0))
#    w.wizards.append(Entity('1','WIZARD','3194','1537','334','-171','0',400,300,1,0))
    w.snaffles.append(Entity('6','SNAFFLE','4475','5218','1018','-105','0',150,800,0,0))
#    w.opponents.append(Entity('2','OPPONENT_WIZARD','12513','2125','-278','-14','0',400,300,1,0))
#    w.opponents.append(Entity('3','OPPONENT_WIZARD','12536','6215','-364','142','0',400,300,1,0))
    w.bludgers.append(Entity('11','BLUDGER','4675','4511','-557','180','0',200,600,8,0))
#    w.bludgers.append(Entity('12','BLUDGER','11325','2989','557','-180','0',200,600,8,0))


    b = Vec2(11325,2989)
    vb = Vec2(557,-180)

    print b.add(vb)

    s = Strategy(w)


    fw = w.wizards[0]


    obtacle = w.bludgers[0]
 
    steer_direction = fw.steer_to_unit(w.snaffles[0])
    print steer_direction

    avoid = w.find_most_avoidance(fw, steer_direction).normalize().mult(150)
    print avoid
    steer_direction = fw.steer_to_unit(w.snaffles[0],avoid)
    print steer_direction
    
    
    dv = fw.velocity.sub(fw.position.sub(steer_direction).normalize().mult(150))

    print fw.position,obtacle.position,fw.position.distance(obtacle.position)

    for k in [1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0]:

        head = fw.position.add(dv.mult(k))
        target = obtacle.position.add(obtacle.velocity.mult(k))
        print head,target,target.distance(head)

 

if __name__ == '__main__':
    find_avoidance()
