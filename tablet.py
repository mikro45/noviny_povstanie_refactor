#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from konstanty import *

class Tablet(pygame.sprite.Sprite):
    """Trieda Tablet vykresľuje hráča na obrazovke."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Načítanie a vykreslenie obrázku tabletu
        self.image = pygame.image.load('obrazky/tablet.bmp').convert()
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [VELKOST_OKNA_X / 2 - self.rect.width, VELKOST_OKNA_Y - self.rect.height]

    def update(self, smer, rychlost):
        """Umožnuje pohyb hráča po obrazovke na základe vstupu."""
        if smer == 0 and self.rect.left > 0:
            self.rect.left -= rychlost
        elif smer == 1 and self.rect.left < VELKOST_OKNA_X - self.rect.width:
            self.rect.left += rychlost
