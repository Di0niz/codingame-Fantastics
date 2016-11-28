import sys
import math
import unittest

import app


class WorldTestCase (unittest.TestCase):
    
    def setUp(self):
        self.w = app.World("1")

        self.w.entities.append(app.Entity("0 WIZARD 1269 5192 128 -28 0"))
        self.w.entities.append(app.Entity("1 WIZARD 1269 2308 128 28 0"))
        self.w.entities.append(app.Entity("2 OPPONENT_WIZARD 14733 2189 -128 -30 0"))
        self.w.entities.append(app.Entity("3 OPPONENT_WIZARD 14727 5220 -131 -14 0"))
        self.w.entities.append(app.Entity("4 SNAFFLE 5654 4684 0 0 0"))
        self.w.entities.append(app.Entity("5 SNAFFLE 10346 2816 0 0 0"))
        self.w.entities.append(app.Entity("6 SNAFFLE 2563 5610 0 0 0"))
        self.w.entities.append(app.Entity("7 SNAFFLE 13437 1890 0 0 0"))
        self.w.entities.append(app.Entity("8 SNAFFLE 3770 4797 0 0 0"))
        self.w.entities.append(app.Entity("9 SNAFFLE 12230 2703 0 0 0"))
        self.w.entities.append(app.Entity("10 SNAFFLE 8000 3750 0 0 0"))      
        

    def test_first_step(self):

        self.assertEqual(len(self.w.entities), 11)  
        self.assertEqual(len(self.w.wizards()), 2)  
        self.assertEqual(len(self.w.snaffles()), 7)  
       
        pass

    def test_define_strategy(self):
        s = app.Strategy(self.w)

        wizard = self.w.wizards()[0]
        action = s.find_action(app.StrategyState.MOVE, wizard)
        self.assertEqual(action[0], app.StrategyState.MOVE_SNAFFLE)  
        self.assertEqual(action[1].entity_id, 6)  

        self.assertEqual(s.get_command(action).split()[:3], ["MOVE","2563","5610"])  
       
        wizard = self.w.wizards()[1]
        action = s.find_action(app.StrategyState.MOVE, wizard)
        self.assertEqual(action[0], app.StrategyState.MOVE_SNAFFLE)  
        self.assertEqual(action[1].entity_id, 8)  

        self.assertEqual(s.get_command(action).split()[:3], ["MOVE","3770","4797"])  

class EntityTestCase (unittest.TestCase):
    
    def test_init(self):
        pass



if __name__ == '__main__':
    unittest.main()
