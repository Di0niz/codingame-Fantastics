import sys
import math
import unittest

import app
from app import World, Strategy,Entity


class WorldTestCase (unittest.TestCase):
    
    def test_flipendo(self):
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','9802','1566','397','130','0',400,300,1,0))
#        w.wizards.append(Entity('1','WIZARD','12384','4952','-340','66','0',400,300,1,0))
        w.snaffles.append(Entity('4','SNAFFLE','11957','3265','2','2','0',150,800,0,0))
#        w.snaffles.append(Entity('6','SNAFFLE','12778','4928','-463','1126','0',150,800,0,0))
#        w.opponents.append(Entity('2','OPPONENT_WIZARD','11526','3317','54','187','0',400,300,1,0))
#        w.opponents.append(Entity('3','OPPONENT_WIZARD','14275','4284','466','104','0',400,300,1,0))
#        w.bludgers.append(Entity('9','BLUDGER','12895','3847','-207','238','0',200,600,8,0))
#        w.bludgers.append(Entity('10','BLUDGER','13077','5465','-340','72','0',200,600,8,0))


        s = Strategy(w)

        flipendo = s.find_flipendo_snaffle(w.wizards[0], None)
        print flipendo
        print w.wizards[0], w.snaffles[0]

        prev_snaffle = None

        for_wizard, snaffle = w.wizards[0], w.snaffles[0]


        cur_pos = for_wizard.position.add(for_wizard.velocity)
        print cur_pos

        gate = w.opponent_gate()
        print gate

        min_dist = 4000

        flipendo = None

        for snaffle in w.snaffles:
            t = snaffle.position.add(snaffle.velocity)
            print t


            if(gate.x > t.x > cur_pos.x or gate.x < t.x < cur_pos.x) :

                y = (((t.y - cur_pos.y)*1.0/(t.x - cur_pos.x)) * (gate.x - t.x)) + t.y

                dy = (t.y - cur_pos.y)
                dx = (t.x - cur_pos.x)
                gx = (gate.x - t.x)

                print dy/dx

                print (t.y - cur_pos.y), (t.x - cur_pos.x),  (gate.x - t.x),  t.y
                print y

                dist = for_wizard.get_distance_to_unit(snaffle)

                # if new_min < min_dist and
                if (2100 < y < 5400) and snaffle != prev_snaffle and (400 < dist <  3000):
                    flipendo = snaffle
                    #min_dist = new_min


if __name__ == '__main__':
    unittest.main()
