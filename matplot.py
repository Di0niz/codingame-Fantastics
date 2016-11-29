# -*- coding: utf-8 -*- 

import sys
import math
import unittest

import app

import matplotlib.pyplot as plt




class WorldTestCaseBronze(unittest.TestCase):
    
    def setUp(self):
        self.w = app.World("0")
        self.w.entities.append(app.Entity("0 WIZARD 5753 6347 420 96 0"))
        self.w.entities.append(app.Entity("1 WIZARD 3131 3215 -15 -165 0"))
        self.w.entities.append(app.Entity("2 OPPONENT_WIZARD 10392 2099 -345 7 0"))
        self.w.entities.append(app.Entity("3 OPPONENT_WIZARD 12974 3951 -2 108 0"))
        self.w.entities.append(app.Entity("4 SNAFFLE 4677 5392 0 0 0"))
        self.w.entities.append(app.Entity("5 SNAFFLE 8808 2329 -791 72 0"))
        self.w.entities.append(app.Entity("6 SNAFFLE 6789 6585 0 0 0"))
        self.w.entities.append(app.Entity("7 SNAFFLE 9211 915 0 0 0"))
        self.w.entities.append(app.Entity("8 SNAFFLE 8000 3750 0 0 0"))
        self.w.entities.append(app.Entity("9 BLUDGER 2806 5889 -228 336 0"))
        self.w.entities.append(app.Entity("10 BLUDGER 12881 1490 121 -340 0"))


    def test_draw_world(self):
        self.w = app.World("0")
        self.w.entities.append(app.Entity("0 WIZARD 5193 6218 414 95 0"))
        self.w.entities.append(app.Entity("1 WIZARD 3151 3435 -112 -338 0"))
        self.w.entities.append(app.Entity("2 OPPONENT_WIZARD 10852 2089 -312 -12 0"))
        self.w.entities.append(app.Entity("3 OPPONENT_WIZARD 12977 3807 131 212 0"))
        self.w.entities.append(app.Entity("4 SNAFFLE 4677 5392 0 0 0"))
        self.w.entities.append(app.Entity("5 SNAFFLE 9862 2233 -1054 96 0"))
        self.w.entities.append(app.Entity("6 SNAFFLE 6789 6585 0 0 0"))
        self.w.entities.append(app.Entity("7 SNAFFLE 9211 915 0 0 0"))
        self.w.entities.append(app.Entity("8 SNAFFLE 8000 3750 0 0 0"))
        self.w.entities.append(app.Entity("9 BLUDGER 3059 5516 -372 334 0"))
        self.w.entities.append(app.Entity("10 BLUDGER 12746 1867 259 -392 0"))


        ax = plt.axes()

        for entity in self.w.wizards():
            ax.arrow(entity.x, entity.y, entity.vx, entity.vy, head_width=0.05, head_length=0.1, fc='k', ec='k')
            ax.add_patch(plt.Circle((entity.x, entity.y), 150,fill=False,edgecolor="blue"))

        for entity in self.w.snaffles():
            ax.arrow(entity.x, entity.y, entity.vx, entity.vy, head_width=0.05, head_length=0.1, fc='k', ec='k')
            ax.add_patch(plt.Circle((entity.x, entity.y), 60,fill=False,edgecolor="red"))
        
        ax.arrow(5193, 6218, 6789 - 5193, 6585 - 6218, head_width=0.05, head_length=0.1, fc='k', ec='k')
        ax.arrow(3151, 3435, 4677 - 3151, 5392 - 3435, head_width=0.05, head_length=0.1, fc='k', ec='k')


        self.w = app.World("0")
        self.w.entities.append(app.Entity("0 WIZARD 5753 6347 420 96 0"))
        self.w.entities.append(app.Entity("1 WIZARD 3131 3215 -15 -165 0"))
        self.w.entities.append(app.Entity("2 OPPONENT_WIZARD 10392 2099 -345 7 0"))
        self.w.entities.append(app.Entity("3 OPPONENT_WIZARD 12974 3951 -2 108 0"))
        self.w.entities.append(app.Entity("4 SNAFFLE 4677 5392 0 0 0"))
        self.w.entities.append(app.Entity("5 SNAFFLE 8808 2329 -791 72 0"))
        self.w.entities.append(app.Entity("6 SNAFFLE 6789 6585 0 0 0"))
        self.w.entities.append(app.Entity("7 SNAFFLE 9211 915 0 0 0"))
        self.w.entities.append(app.Entity("8 SNAFFLE 8000 3750 0 0 0"))
        self.w.entities.append(app.Entity("9 BLUDGER 2806 5889 -228 336 0"))
        self.w.entities.append(app.Entity("10 BLUDGER 12881 1490 121 -340 0"))

        for entity in self.w.wizards():
            ax.arrow(entity.x, entity.y, entity.vx, entity.vy, head_width=0.05, head_length=0.1, fc='k', ec='k')
            ax.add_patch(plt.Circle((entity.x, entity.y), 150,fill=False,edgecolor="blue",alpha=0.8))

        for entity in self.w.snaffles():
            ax.arrow(entity.x, entity.y, entity.vx, entity.vy, head_width=0.05, head_length=0.1, fc='k', ec='k')
            ax.add_patch(plt.Circle((entity.x, entity.y), 60,fill=False,edgecolor="red",alpha=0.8))


  
        plt.xlim(0,16000) 
        plt.ylim(0,7000) 


        plt.show()
    
        pass

    def test_define_strategy(self):
        pass


if __name__ == '__main__':
    unittest.main()
