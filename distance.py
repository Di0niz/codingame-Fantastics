# -*- coding: utf-8 -*- 

import sys
import math
import unittest

from app import Vec2, World, Strategy, Entity

class StrategyTestCase (unittest.TestCase):
    

    def test_error1(self):
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','12020','4732','-392','44','0',400,300,1.000000,0.750000))
        w.wizards.append(Entity('1','WIZARD','4254','6880','-46','-101','0',400,300,1.000000,0.750000))
        w.snaffles.append(Entity('5','SNAFFLE','5051','6452','-28','145','0',150,800,0.500000,0.900000))
        w.opponents.append(Entity('2','OPPONENT_WIZARD','5051','6452','-28','145','1',400,300,1.000000,0.750000))
        w.opponents.append(Entity('3','OPPONENT_WIZARD','12128','6420','-639','-541','0',400,300,1.000000,0.750000))
        w.bludgers.append(Entity('9','BLUDGER','5038','5437','223','495','0',200,600,8.000000,0.750000))
        w.bludgers.append(Entity('10','BLUDGER','14473','4728','-248','239','0',200,600,8.000000,0.750000))
        s = Strategy(w)

        #s.prepare_dummy()

        wizards = w.wizards

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
        print faction
        print saction


    def test_can_cast_flipendo(self):
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','7273','3325','217','-272','1',400,300,1.000000,0.750000))
        w.wizards.append(Entity('1','WIZARD','8659','4217','123','172','0',400,300,1.000000,0.750000))
        w.snaffles.append(Entity('4','SNAFFLE','7478','7061','89','194','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('5','SNAFFLE','5133','2412','-546','236','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('6','SNAFFLE','7273','3325','217','-272','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('7','SNAFFLE','7889','2959','-396','-9','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('8','SNAFFLE','10041','2516','33','11','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('9','SNAFFLE','8058','4739','29','-11','0',150,800,0.500000,0.900000))
        w.snaffles.append(Entity('10','SNAFFLE','10386','3437','728','-119','0',150,800,0.500000,0.900000))
        w.opponents.append(Entity('2','OPPONENT_WIZARD','6972','1521','-205','170','0',400,300,1.000000,0.750000))
        w.opponents.append(Entity('3','OPPONENT_WIZARD','10041','2516','33','11','1',400,300,1.000000,0.750000))
        w.bludgers.append(Entity('11','BLUDGER','4933','1911','461','139','0',200,600,8.000000,0.750000))
        w.bludgers.append(Entity('12','BLUDGER','11268','5281','-366','-300','0',200,600,8.000000,0.750000))

    
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

        fw = w.wizards[0]

        s = Strategy(w)
        problem = s.find_problem()

        faction = s.find_action(problem, fw)
        print faction
        
        obj = fw.steer_to_unit(faction[1])
        avoid = w.find_most_avoidance(fw, obj)

        print obj
        print avoid
        fcommand = s.get_command(fw, faction)


    def test_throw_gate(self):
        """бросаем только в те шары, который находятся в стороне ворот"""
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','8054','3696','193','140','0',400,300,1,0))
        w.wizards.append(Entity('1','WIZARD','7955','2326','155','-242','0',400,300,1,0))
        w.snaffles.append(Entity('4','SNAFFLE','8179','4643','98','165','0',150,800,0,0))
        w.snaffles.append(Entity('5','SNAFFLE','6023','5307','-155','-40','0',150,800,0,0))
        w.snaffles.append(Entity('6','SNAFFLE','7996','3044','39','-28','0',150,800,0,0))
        w.snaffles.append(Entity('7','SNAFFLE','8691','1902','-227','49','0',150,800,0,0))
        w.snaffles.append(Entity('8','SNAFFLE','10032','2547','452','-268','0',150,800,0,0))
        w.opponents.append(Entity('2','OPPONENT_WIZARD','10661','2196','-256','167','0',400,300,1,0))
        w.opponents.append(Entity('3','OPPONENT_WIZARD','7956','5717','-63','-279','0',400,300,1,0))
        w.bludgers.append(Entity('9','BLUDGER','5422','6318','548','-70','0',200,600,8,0))
        w.bludgers.append(Entity('10','BLUDGER','11330','6901','-520','274','0',200,600,8,0))
        
        fw = w.wizards[0]

        s = Strategy(w)
        problem = s.find_problem()

        faction = s.find_action(problem, fw)
        #print faction
        fcommand = s.get_command(fw, faction)
       
        #self.assertEqual(True, isinstance(faction[1],Vec2)) 


    def test_kick_to_snaffle_gate(self):
        """Определяем стратегию, когда можем попасть в ворота"""

        w = World(0)
        w.wizards.append(Entity('0','WIZARD','4506','5505','340','180','1',400,300,1,0))
        w.wizards.append(Entity('1','WIZARD','4641','1403','406','-95','0',400,300,1,0))
        w.snaffles.append(Entity('4','SNAFFLE','6316','1013','0','0','0',150,800,0,0))
        w.snaffles.append(Entity('5','SNAFFLE','9684','6487','0','0','0',150,800,0,0))
        w.snaffles.append(Entity('6','SNAFFLE','4506','5505','340','180','0',150,800,0,0))
        w.snaffles.append(Entity('7','SNAFFLE','11240','1905','96','-84','0',150,800,0,0))
        w.snaffles.append(Entity('8','SNAFFLE','8000','3750','0','0','0',150,800,0,0))
        w.opponents.append(Entity('2','OPPONENT_WIZARD','11901','1411','-103','-649','0',400,300,1,0))
        w.opponents.append(Entity('3','OPPONENT_WIZARD','11763','5080','-326','162','0',400,300,1,0))
        w.bludgers.append(Entity('9','BLUDGER','3511','4847','-535','275','0',200,600,8,0))
        w.bludgers.append(Entity('10','BLUDGER','12460','3104','504','63','0',200,600,8,0))


        fw = w.wizards[0]

        s = Strategy(w)
        problem = s.find_problem()

        faction = s.find_action(problem, fw)
        fcommand = s.get_command(fw, faction)
       
        self.assertEqual(8, faction[1].entity_id) 

        
    def test_throw_to_snaffle(self):
        """Расчитываем траекторию броска в ворота"""
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','4506','5505','340','180','1',400,300,1,0))
        w.wizards.append(Entity('1','WIZARD','4641','1403','406','-95','0',400,300,1,0))
        w.snaffles.append(Entity('4','SNAFFLE','6316','1013','0','0','0',150,800,0,0))
        w.snaffles.append(Entity('5','SNAFFLE','9684','6487','0','0','0',150,800,0,0))
        w.snaffles.append(Entity('6','SNAFFLE','4506','5505','340','180','0',150,800,0,0))
        w.snaffles.append(Entity('7','SNAFFLE','11240','1905','96','-84','0',150,800,0,0))
        w.snaffles.append(Entity('8','SNAFFLE','8000','3750','0','0','0',150,800,0,0))
        w.opponents.append(Entity('2','OPPONENT_WIZARD','11901','1411','-103','-649','0',400,300,1,0))
        w.opponents.append(Entity('3','OPPONENT_WIZARD','11763','5080','-326','162','0',400,300,1,0))
        w.bludgers.append(Entity('9','BLUDGER','3511','4847','-535','275','0',200,600,8,0))
        w.bludgers.append(Entity('10','BLUDGER','12460','3104','504','63','0',200,600,8,0))
        
        fw = w.wizards[0]

        s = Strategy(w)
        problem = s.find_problem()
        faction = s.find_action(problem, fw)
        print faction
        fcommand = s.get_command(fw, faction)
       
        print fcommand

    def test_freeze_opponent(self):
        """Определяем, что в это время надо делать магию и морозить противника"""
        
        w = World(0)
        w.wizards.append(Entity('0','WIZARD','6726','5977','-436','65','0',400,300,1,0))
        w.snaffles.append(Entity('5','SNAFFLE','4825','6261','-2','-2','0',150,800,0,0))
        w.opponents.append(Entity('2','OPPONENT_WIZARD','11845','3745','-304','215','0',400,300,1,0))
        w.opponents.append(Entity('3','OPPONENT_WIZARD','3634','5957','405','107','0',400,300,1,0))
        w.bludgers.append(Entity('9','BLUDGER','10495','3227','-148','464','0',200,600,8,0))
        w.bludgers.append(Entity('10','BLUDGER','2890','6869','532','451','0',200,600,8,0))
        w.spell = 13

        fw = w.wizards[0]

        s = Strategy(w)
        problem = s.find_problem()
        faction = s.find_action(problem, fw)
        #print faction

        self.assertEqual(Strategy.CAST_PETRIFICUS, faction[0]) 


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
        """Определяем, что необходмо сделать"""
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
        w.opponents.append(Entity('2','OPPONENT_WIZARD','12513','2125','-278','-14','0',400,300,1,0))
    #    w.opponents.append(Entity('3','OPPONENT_WIZARD','12536','6215','-364','142','0',400,300,1,0))
        w.bludgers.append(Entity('11','BLUDGER','4675','4511','-557','180','0',200,600,8,0))
    #    w.bludgers.append(Entity('12','BLUDGER','11325','2989','557','-180','0',200,600,8,0))


        s = Strategy(w)
        s.prepare_dummy()


        fw = w.wizards[0]
        fw.set_target_unit(w.snaffles[0])
    
        steer_direction = fw.steer_to_unit(w.snaffles[0])
        avoid = w.find_most_avoidance(fw, steer_direction).normalize().mult(150)
        self.assertNotEqual(avoid, Vec2(0,0)) 
 
if __name__ == '__main__':
    unittest.main()