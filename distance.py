# -*- coding: utf-8 -*- 

import sys
import math
import unittest

from app import Vec2, World, Strategy, Entity

class StrategyTestCase (unittest.TestCase):

    def test_find_next_position(self):
        """определение ближайшей цели"""
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','6991','5222','359','-136','0',400,300,1,0))
        w.snaffles.append(Entity('4','SNAFFLE','9090','2136','518','202','0',150,800,0,0))
        w.snaffles.append(Entity('5','SNAFFLE','7776','6334','-728','-3','0',150,800,0,0))
        w.snaffles.append(Entity('6','SNAFFLE','8518','4533','218','-53','0',150,800,0,0))
        w.snaffles.append(Entity('7','SNAFFLE','11603','1273','45','240','0',150,800,0,0))
        w.snaffles.append(Entity('8','SNAFFLE','8000','3750','0','0','0',150,800,0,0))

        fw = w.wizards[0]

        s = Strategy(w)

        problem = s.find_problem()

        faction = s.find_action(problem, fw)


        self.assertEqual(6, faction[1].entity_id) 
    
    


    def test_find_action(self):
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','4506','5505','340','180','1',400,300,1,0))
        w.snaffles.append(Entity('6','SNAFFLE','4506','5505','340','180','0',150,800,0,0))

        fw = w.wizards[0]

        s = Strategy(w)

        problem = s.find_problem()

        faction = s.find_action(problem, fw)
        fcommand = s.get_command(fw, faction)

        self.assertEqual(Strategy.THROW_SNAFFLE, faction[0]) 




    def test_find_avoidance(self):

        w = World(0)
        w.wizards.append(Entity('0','WIZARD','3487','5376','278','14','0',400,300,1,0))
    #    w.wizards.append(Entity('1','WIZARD','3194','1537','334','-171','0',400,300,1,0))
        w.snaffles.append(Entity('6','SNAFFLE','4475','5218','1018','-105','0',150,800,0,0))
    #    w.opponents.append(Entity('2','OPPONENT_WIZARD','12513','2125','-278','-14','0',400,300,1,0))
    #    w.opponents.append(Entity('3','OPPONENT_WIZARD','12536','6215','-364','142','0',400,300,1,0))
        w.bludgers.append(Entity('11','BLUDGER','4675','4511','-557','180','0',200,600,8,0))
    #    w.bludgers.append(Entity('12','BLUDGER','11325','2989','557','-180','0',200,600,8,0))


        s = Strategy(w)


        fw = w.wizards[0]
    
        steer_direction = fw.steer_to_unit(w.snaffles[0])
        avoid = w.find_most_avoidance(fw, steer_direction).normalize().mult(150)
        self.assertNotEqual(avoid, Vec2(0,0)) 
 
if __name__ == '__main__':
    unittest.main()