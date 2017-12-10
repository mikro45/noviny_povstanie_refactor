#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from konstanty import *

class Noviny_boss_12(pygame.sprite.Sprite):
    """Vykresľuje 1. a 2. Boss-a hry"""
    def __init__(self, uroven = 1):
        pygame.sprite.Sprite.__init__(self)

        if uroven == 1:
            self.image = pygame.image.load('obrazky/noviny/boss/noviny_boss_1.bmp').convert()
            self.smer = [3, 3]
        else:
            self.image = pygame.image.load('obrazky/noviny/boss/noviny_boss_2.bmp').convert()
            self.smer = [5, 5]
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()
        
        self.rect.centerx = VELKOST_OKNA_X / 2
        self.rect.centery = - 100       
        
        
        self.cas_pohybu = 0

    def update(self, casovac):
        """Vykresľuje pohyb Boss-a"""        
        if self.cas_pohybu < casovac:
            self.cas_pohybu = casovac
            # Boss dojde do vzdialenosti 79 px a zastaví sa
            if self.rect.top < 80:
                self.rect.top = self.rect.top + self.smer[1]
            # Boss sa hýbe zo strany na stranu a popri tom strieľa
            if self.rect.left < 0 or self.rect.left > VELKOST_OKNA_X - self.rect.width:
                self.smer[0] = -self.smer[0]
            if self.rect.top > 79:
                self.rect.left = self.rect.left + self.smer[0]        
            self.cas_pohybu += 20
