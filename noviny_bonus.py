#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import pygame
from pygame.locals import *
from konstanty import *

class Noviny_bonus_1(pygame.sprite.Sprite):
    """Vykresľuje prvý bonusový level"""
    def __init__(self, x, y):
        """Pointa bonusového levelu, je pre hráča chytiť čo najviac novín,
            s tým, že má nekonečný počet životov"""
        pygame.sprite.Sprite.__init__(self)

        # Načítanie všetkých obrázkov z 1. úrovne
        self.obrazok_pole = []
        for i in range(1, 7):
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_1/noviny_%s.bmp' % str(i)).convert())
        for i in range(3, 7):
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_1/noviny_%s_5.bmp' % str(i)).convert())
        self.image = self.obrazok_pole[random.randrange(0,9)]
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()

        self.x = (x * 150) + 25
        self.y = -(y * 150) - self.rect.height * 2
        self.rect.topleft = [self.x, self.y]
        
        self.smer = [2, 8]
        self.cas_pohybu = 0

    def update(self, casovac):
        if self.cas_pohybu < casovac:
            self.cas_pohybu = casovac
            self.rect.top = self.rect.top + self.smer[1]
            self.cas_pohybu += 20

class Noviny_bonus_2(pygame.sprite.Sprite):
    """Vykresľuje prvý bonusový level"""
    def __init__(self):
        """Pointa bonusového levelu, je pre hráča chytiť čo najviac novín,
            s tým, že má nekonečný počet životov"""
        pygame.sprite.Sprite.__init__(self)

        # Načítanie náhodného obrázku z 2. úrovne
        self.image = pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert()
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()

        self.rect.topleft = [random.randrange(0, VELKOST_OKNA_X - self.rect.width), random.randrange(0, VELKOST_OKNA_Y / 4)]
        self.smer = [random.randrange(1, 5), random.randrange(1, 5)]

        self.cas_pohybu = 0

    def update(self, casovac):
        if self.cas_pohybu < casovac:
            self.cas_pohybu = casovac
            if self.rect.left < 0 or self.rect.left > VELKOST_OKNA_X - self.rect.width:
                self.smer[0] = -self.smer[0]
            if self.rect.top < 0 or self.rect.top > VELKOST_OKNA_Y - self.rect.height:
                self.smer[1] = -self.smer[1]

            self.rect.left = self.rect.left + self.smer[0]
            self.rect.top = self.rect.top + self.smer[1]

            self.cas_pohybu += 20
