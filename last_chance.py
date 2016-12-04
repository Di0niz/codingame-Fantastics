# -*- coding: utf-8 -*- 

import sys
import math
import unittest

from app import Vec2, World, Strategy, Entity, Behaviour

class StrategyTestCase (unittest.TestCase):
    
    def test_steer(self):
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','10440','660','325','-64','0',400,300,1.000000,0.750000))
        w.wizards.append(Entity('1','WIZARD','11138','3425','237','-219','0',400,300,1.000000,0.750000))
        w.snaffles.append(Entity('4','SNAFFLE','7369','5390','-646','-124','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('5','SNAFFLE','6432','5420','-233','33','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('6','SNAFFLE','6966','6380','0','0','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('8','SNAFFLE','920','1221','33','-17','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('9','SNAFFLE','3752','5898','-2130','-458','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('10','SNAFFLE','13020','4036','186','29','0',150,800,0.500000,0.900000))
        w.opponents.append(Entity('2','OPPONENT_WIZARD','8852','5989','-228','44','0',400,300,1.000000,0.750000))
        w.opponents.append(Entity('3','OPPONENT_WIZARD','12074','4590','402','3','0',400,300,1.000000,0.750000))
        w.bludgers.append(Entity('11','BLUDGER','7049','1137','698','-229','0',200,600,8.000000,0.750000))
        w.bludgers.append(Entity('12','BLUDGER','12236','6919','-458','-115','0',200,600,8.000000,0.750000))
                
        s = Strategy(w)

        fw = w.wizards[0]
        sw = w.wizards[1]

        problem = s.find_problem()

        faction = s.find_action(problem, fw)
        saction = s.find_action(problem, sw)

        if faction[0] == saction[0] and faction[0] == Strategy.MOVE_SNAFFLE:
            if fw.get_distance_to_unit(faction[1]) > sw.get_distance_to_unit(saction[1]):
                faction = s.find_action(problem, fw, saction)
            else:
                saction = s.find_action(problem, sw, faction)
        elif faction[0] == Strategy.CAST_FLIPENDO:
            saction = s.find_action(problem, sw, faction)
        elif saction[0] == Strategy.CAST_FLIPENDO:
            faction = s.find_action(problem, fw, saction)
        elif faction[0] == Strategy.CAST_ACCIO:
            saction = s.find_action(problem, sw, faction)
        elif saction[0] == Strategy.CAST_ACCIO:
            faction = s.find_action(problem, fw, saction)
        

        fcommand = s.get_command(fw, faction)
        
        target = faction[1].future_position()
        print fw.position, faction[1].future_position()

        max_velocity = fw.velocity.length() 
        desired_velocity = target.sub(fw.position).normalize().mult(max_velocity)
        steer = desired_velocity.sub(fw.velocity)

        print steer.normalize().mult(150*fw.friction)
        

        print fw.steer
        rz = Entity('0','WIZARD','10915','595','356','-48','0',400,300,1.000000,0.750000)
        print rz

        pass
    def test_find_snaffle(self):
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','14291','923','60','441','0',400,300,1.000000,0.750000))
        w.wizards.append(Entity('1','WIZARD','14271','4735','-198','390','0',400,300,1.000000,0.750000))
        w.snaffles.append(Entity('4','SNAFFLE','11399','1666','2','-2','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('5','SNAFFLE','7229','2712','-235','23','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('6','SNAFFLE','1891','3569','-23','-11','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('7','SNAFFLE','15873','2300','0','0','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('9','SNAFFLE','3239','5413','37','-43','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('10','SNAFFLE','5442','3700','-202','-2','0',150,800,0.500000,0.900000))
        w.opponents.append(Entity('2','OPPONENT_WIZARD','7229','2712','-235','23','1',400,300,1.000000,0.750000))
        w.opponents.append(Entity('3','OPPONENT_WIZARD','11778','2076','-468','90','0',400,300,1.000000,0.750000))
        w.bludgers.append(Entity('11','BLUDGER','13376','1717','-765','301','0',200,600,8.000000,0.750000))
        w.bludgers.append(Entity('12','BLUDGER','12074','817','510','-222','0',200,600,8.000000,0.750000))
   
        s = Strategy(w)

        #s.prepare_dummy()

        fw = w.wizards[0]
        sw = w.wizards[1]

        problem = s.find_problem()

        faction = s.find_action(problem, fw)
        saction = s.find_action(problem, sw)

        if faction[0] == saction[0] and faction[0] == Strategy.MOVE_SNAFFLE:
            if fw.get_distance_to_unit(faction[1]) > sw.get_distance_to_unit(saction[1]):
                faction = s.find_action(problem, fw, saction)
            else:
                saction = s.find_action(problem, sw, faction)
        elif faction[0] == Strategy.CAST_FLIPENDO:
            saction = s.find_action(problem, sw, faction)
        elif saction[0] == Strategy.CAST_FLIPENDO:
            faction = s.find_action(problem, fw, saction)
        elif faction[0] == Strategy.CAST_ACCIO:
            saction = s.find_action(problem, sw, faction)
        elif saction[0] == Strategy.CAST_ACCIO:
            faction = s.find_action(problem, fw, saction)

        fcommand = s.get_command(fw, faction)
        scommand = s.get_command(sw, saction)

        w.add_spell()

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