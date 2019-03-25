#class Robot:


import numpy as np
from math import pi
from matplotlib import pyplot as plt
from random import random, randint, seed
from classes_meca import Vecteur3d as V3D




class Kobuki(object):
    """Robot Mobile"""

    def __init__(self, rayon=0.075, distance=0.35, pos=V3D(),vit=V3D(), ori=0, nom='tortue',c='green'):

        self.pos = [pos]
        self.dist = distance    # dist entre les roues
        self.r = rayon  # rayon des roues
        self.vit = [vit]  # vitesse tout droit
        self.ori = [ori]     # orientation

        self.nom = nom
        self.color = c
        #self.vit_droite = v_r
        #self.vit_gauche = v_g

    def __str__(self):
        msg = 'Tortue(' + str(self.pos[-1]) + ',' + ')'
        return msg

    def __repr__(self):
        msg = 'Tortue(' + str(self.pos[-1]) + ',' + ')'
        return msg

    #def mgd(self):
        #vit_rot = (self.r/self.dist)*(self.vit_droite-self.vit_gauche)
        #vit_trans = (self.r/2)*(self.vit_gauche+self.vit_droite)

    def deplacement(self, obj_x, obj_y):

        dep_x = obj_x - self.pos[-1].x
        dep_y = obj_y - self.pos[-1].y
        pos_x = self.pos[-1].x + dep_x
        pos_y = self.pos[-1].y + dep_y

        angle = self.ori[-1] - np.arctan2(dep_y, dep_x)
        angle = self.ori[-1] - angle
        self.ori.append(angle)
        self.pos.append(V3D(pos_x,pos_y))

    def deplacement_random(self):
        seed(a=None, version=2)
        x = random()
        y = random()
        self.deplacement(5*x, 5*y)

    def trajectoire(self):
        trajx=[]
        trajy=[]
        for i in range(0,len(self.pos)):
            trajx.append(self.pos[i].x)
            trajy.append(self.pos[i].y)
        plt.plot(trajx, trajy,)#color=self.color)
        plt.show()


class Simulateur(object):
    robots=[]

    def __init__(self, nom):
        self.nom = nom

    def addKobuki(self,K=Kobuki()):
        self.robots.append(K)

    def removeKobuki(self,name):
        for r in self.robots:
            if r.nom == nom:
                self.robots.remove(r)
            else:
                print('No Kobuki named ' + name + ' in simulateur ' + self.nom + '.')


    def trace(self):
        plt.figure('La plage de ' + self.nom)
        for t in self.robots:
            X = []
            Y = []
            for i in t.pos:
                X.append(i.x)
                Y.append(i.y)
            plt.plot(X, Y, color=t.color, label=t.nom)
            plt.legend()
        plt.show()

    # def createNkobuki(self,n):
    #     for i in range (1,n):



ahah = Kobuki(nom='ahah', c='blue')
baba = Kobuki(nom='baba', c='red')
coco = Kobuki(nom='coco', c='black')
kyky = Kobuki(nom='kyky')

plage = Simulateur('playa')

plage.addKobuki(ahah)
plage.addKobuki(baba)
plage.addKobuki(coco)
plage.addKobuki(kyky)

for i in range(1,5):
    for t in plage.robots:
        t.deplacement_random()



plage.trace()
