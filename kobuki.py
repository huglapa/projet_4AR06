import numpy as np
from math import pi, sin, cos
from matplotlib import pyplot as plt
from random import random, randint, seed
from classes_meca import Vecteur3d as V3D

import pygame
import pygame.draw as pygDraw
from pygame.time import Clock as pygClock


class Kobuki(object):
    """Robot Mobile"""

    def __init__(self, rayon=0.075, distance=0.35, pos=V3D(), ori=0, nom='tortue', c='green'):

        self.pos = [pos]
        self.dist = distance    # dist entre les roues
        self.r = rayon  # rayon des roues
        self.vit_t = 0  # vitesse tout droit
        self.vit_r = 0
        self.ori = [ori]     # orientation

        self.nom = nom
        self.color = c

    def __str__(self):
        msg = 'Tortue(' + str(self.pos[-1]) + ',' + ')'
        return msg

    def __repr__(self):
        msg = 'Tortue(' + str(self.pos[-1]) + ',' + ')'
        return msg

    def getSpeed(self, dt, vg=0, vd=0):

        vit_rot = (self.r/self.dist)*(vd - vg)
        vit_trans = (self.r/2)*(vg + vd)
        # self.vit_r = vit_rot
        # self.vit_t = vit_trans

        self.ori.append(self.ori[-1]+dt*vit_rot)

        dx = self.pos[-1].x+dt*vit_trans*cos(self.ori[-1])
        dy = self.pos[-1].y+dt*vit_trans*sin(self.ori[-1])
        self.pos.append(V3D(dx,dy))

    # def getPos(self,dt):
    #     self.ori.append(self.ori[-1]+dt*self.vit_r)
    #     self.pos.append(self.pos[-1]+dt*self.vit_t)

    def deplacement(self, obj_x, obj_y):

        dep_x = obj_x - self.pos[-1].x
        dep_y = obj_y - self.pos[-1].y
        pos_x = self.pos[-1].x + dep_x
        pos_y = self.pos[-1].y + dep_y

        angle = self.ori[-1] - np.arctan2(dep_y, dep_x)
        angle = self.ori[-1] - angle
        self.ori.append(angle)
        self.pos.append(V3D(pos_x, pos_y))

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
        plt.plot(trajx, trajy)  # color=self.color)
        plt.show()


class Simulateur(object):
    robots = []

    def __init__(self, nom):
        self.nom = nom

    def addKobuki(self, K=Kobuki()):
        self.robots.append(K)

    def removeKobuki(self, name):
        for r in self.robots:
            if r.nom == name:
                self.robots.remove(r)
            else:
                print('No Kobuki named ' + name + ' in simulateur ' + self.nom + '.')

    def controlRoues(self, name, step, vg, vd):
        for r in self.robots:
            if r.nom == name:
                r.getSpeed(step, vg, vd)
            else:
                print('No Kobuki named ' + name + ' in simulateur ' + self.nom + '.')

    def trajSinus(self, step, duree, a=1, omega=1):
        """trajectoire de la forme A *sin(omega*t)"""
        t = [0]
        while t[-1] < duree:
            for r in self.robots:
                vg = a * abs(sin(omega * t[-1]))
                vd = a * abs(sin((pi/2*omega)+omega * t[-1]))
                r.getSpeed(step, vg, vd)
            t.append(t[-1]+step)

    def controlRouesRand(self, step, duree):
        t = [0]
        i=0
        while t[-1] < duree:
            print(i)
            i+=1
            for r in self.robots:

                seed(a=None, version=2)
                g = randint(-2, 3)
                d = randint(-2, 3)

                self.controlRoues(r.nom, step, g, d)
        t.append(t[-1] + step)
#        return t

    def trace(self):
        plt.figure('Plan de ' + self.nom)
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


rob1 = Kobuki(nom='rob1', c='blue')
rob2 = Kobuki(nom='rob2', c='red')
rob3 = Kobuki(nom='rob3', c='black')
rob4 = Kobuki(nom='rob4', c='green')

simu = Simulateur('simu')

simu.addKobuki(rob1)

dt = 0.01
time = 5

#simu.controlRouesRand(dt, time)
simu.trajSinus(dt, time)
simu.trace()
