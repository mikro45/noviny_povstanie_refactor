#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

import konstanty as kon

class Strela(pygame.sprite.Sprite):
    """Trieda Strela vykresľuje vystrelené strely hráča (Tabletu)."""

    def __init__(self, pozicia):
        pygame.sprite.Sprite.__init__(self)
        self.DRAHA_STRELY = 31
        # Načítanie a vykreslenie obrázku strely
        self.image = pygame.image.load('obrazky/strela.bmp').convert()
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = pozicia

    def update(self):
        """Umožnuje pohyb (let) strely."""
        if self.rect.top > self.DRAHA_STRELY:
            self.rect.top -= 4
        # Ak je strela mimo obrazovky, tak sa strela odstráni (zabije)
        else:
            self.kill()


class StrelaNoviny(Strela):
    """Trieda Strela vykresľuje vystrelené strely nepriateľov a dedí z triedy Strela."""

    def __init__(self, pozicia):
        Strela.__init__(self, pozicia)
        # Načítanie a vykreslenie obrázku strely
        self.image = pygame.image.load('obrazky/strela_noviny.bmp').convert()
        self.image.set_colorkey((255, 0, 255))

    def update(self):
        """Umožnuje pohyb (let) strely."""
        if self.rect.top < kon.VELKOST_OKNA_Y:
            self.rect.top += 6
        # Ak je strela mimo obrazovky, tak sa strela odstráni (zabije)
        else:
            self.kill()
