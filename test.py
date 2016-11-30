import sys
import math
import unittest

import app
from app import World, Strategy


class WorldTestCase (unittest.TestCase):
    
    def setUp(self):
        self.w = app.World("1")

        self.w.add_raw_input("0 WIZARD 1269 5192 128 -28 1")
        self.w.add_raw_input("1 WIZARD 1269 2308 128 28 0")
        self.w.add_raw_input("2 OPPONENT_WIZARD 14733 2189 -128 -30 0")
        self.w.add_raw_input("3 OPPONENT_WIZARD 14727 5220 -131 -14 0")
        self.w.add_raw_input("4 SNAFFLE 5654 5192 0 0 0")
        self.w.add_raw_input("5 SNAFFLE 10346 2816 0 0 0")
        self.w.add_raw_input("6 SNAFFLE 2563 5610 0 0 0")
        self.w.add_raw_input("7 SNAFFLE 13437 1890 0 0 0")
        self.w.add_raw_input("8 SNAFFLE 3770 4797 0 0 0")
        self.w.add_raw_input("9 SNAFFLE 12230 2703 0 0 0")
        self.w.add_raw_input("10 SNAFFLE 8000 3750 0 0 0")      
        

    def test_steer(self):
        
        w  = self.w.wizards[0]

        snaffle = self.w.snaffles[0]
        print w
        print snaffle
        print w.steer_to_unit(snaffle)

        for sh in self.w.snaffles:
            print w.get_steer_dist_to_unit(sh)
            print w.steer_to_unit(sh)

    def test_strategy(self):
        w = self.w
        s = Strategy(w)

        wizards = w.wizards

        fw = w.wizards[0]
        print s.find_snaffle(fw,None)

        sw = w.wizards[1]
        print s.find_snaffle(sw,None)

        problem = s.find_problem()

        faction = s.find_action(problem, fw)
        saction = s.find_action(problem, sw)

        if faction[0] == saction[0] and faction[0] == Strategy.MOVE_SNAFFLE:
            if fw.get_distance_to_unit(faction[1]) > sw.get_distance_to_unit(saction[1]):
                faction = s.find_action(problem, fw, saction)
            else:
                saction = s.find_action(problem, sw, faction)

        fcommand = s.get_command(fw,faction)
        scommand = s.get_command(sw,saction)

        w.add_spell()

        print fcommand
        print scommand        





class EntityTestCase (unittest.TestCase):
    
    def test_init(self):
        pass



if __name__ == '__main__':
    unittest.main()
