# -*- coding: utf-8 -*- 

import sys
import math
import unittest

from app import Vec2, World, Strategy, Entity, Behaviour




class StrategyTestCase (unittest.TestCase):
    
    def test_find_snaffle(self):
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','12520','598','413','-34','0',400,300,1.000000,0.750000))
        w.wizards.append(Entity('1','WIZARD','13389','2859','382','-112','0',400,300,1.000000,0.750000))
        w.snaffles.append(Entity('4','SNAFFLE','13293','1766','80','-4','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('5','SNAFFLE','6908','3616','-52','-28','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('6','SNAFFLE','6348','5991','-349','-220','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('7','SNAFFLE','13844','1239','177','-6','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('10','SNAFFLE','7115','6707','-59','95','0',150,800,0.500000,0.900000))
        w.opponents.append(Entity('2','OPPONENT_WIZARD','7918','6461','-267','-117','0',400,300,1.000000,0.750000))
        w.opponents.append(Entity('3','OPPONENT_WIZARD','12492','3105','257','-313','0',400,300,1.000000,0.750000))
        w.bludgers.append(Entity('11','BLUDGER','10049','729','843','-148','0',200,600,8.000000,0.750000))
        w.bludgers.append(Entity('12','BLUDGER','10364','6002','-282','-397','0',200,600,8.000000,0.750000))

    

    def test_avoid(self):
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','12520','598','413','-34','0',400,300,1.000000,0.750000))
        w.wizards.append(Entity('1','WIZARD','13389','2859','382','-112','0',400,300,1.000000,0.750000))
        w.snaffles.append(Entity('4','SNAFFLE','13293','1766','80','-4','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('5','SNAFFLE','6908','3616','-52','-28','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('6','SNAFFLE','6348','5991','-349','-220','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('7','SNAFFLE','13844','1239','177','-6','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('10','SNAFFLE','7115','6707','-59','95','0',150,800,0.500000,0.900000))
        w.opponents.append(Entity('2','OPPONENT_WIZARD','7918','6461','-267','-117','0',400,300,1.000000,0.750000))
        w.opponents.append(Entity('3','OPPONENT_WIZARD','12492','3105','257','-313','0',400,300,1.000000,0.750000))
        w.bludgers.append(Entity('11','BLUDGER','10049','729','843','-148','0',200,600,8.000000,0.750000))
        w.bludgers.append(Entity('12','BLUDGER','10364','6002','-282','-397','0',200,600,8.000000,0.750000))
  
        s = Strategy(w)

        fw = w.wizards[0]
        fb = w.bludgers[0]


        pass
 
if __name__ == '__main__':
    unittest.main()