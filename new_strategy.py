# -*- coding: utf-8 -*- 

import sys
import math
import unittest

from app import Vec2, World, Strategy, Entity, DummyOpponentStrategy, DummyBludgerStrategy





class StrategyTestCase (unittest.TestCase):
    
    def test_obtacles(self):
        """проверяем как расчитывается entity"""
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','7198','4005','303','-241','1',400,300,1,0))
        w.wizards.append(Entity('1','WIZARD','7444','1846','99','273','0',400,300,1,0))
        w.snaffles.append(Entity('4','SNAFFLE','7198','4005','303','-241','0',150,800,0,0))
        w.snaffles.append(Entity('5','SNAFFLE','6871','5526','-367','-95','0',150,800,0,0))
        w.snaffles.append(Entity('6','SNAFFLE','7783','3195','92','-65','0',150,800,0,0))
        w.snaffles.append(Entity('7','SNAFFLE','9933','1634','-537','116','0',150,800,0,0))
        w.snaffles.append(Entity('8','SNAFFLE','8000','3750','0','0','0',150,800,0,0))
        w.opponents.append(Entity('2','OPPONENT_WIZARD','11532','1683','-87','128','0',400,300,1,0))
        w.opponents.append(Entity('3','OPPONENT_WIZARD','8517','6617','-315','-70','0',400,300,1,0))
        w.bludgers.append(Entity('9','BLUDGER','3817','6548','359','-4','0',200,600,8,0))
        w.bludgers.append(Entity('10','BLUDGER','12835','5848','-299','369','0',200,600,8,0))

        fw = w.opponents[0]

        s = DummyOpponentStrategy(w)
        problem = s.find_problem()

        faction = s.find_action(problem, fw)
        print faction
        
        s = DummyBludgerStrategy(w)
        problem = s.find_problem()
        fw = w.bludgers[0]
        faction = s.find_action(problem, fw)
        print faction
        

 
if __name__ == '__main__':
    unittest.main()