#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

import konstanty as kon

class Explozia(pygame.sprite.Sprite):
    """Trieda Explozia vykresľuje explózie."""

    def __init__(self, pozicia):
        pygame.sprite.Sprite.__init__(self)
        # Animácia výbuchu skladajúca sa zo 4 snímkoch
        self.DLZKA_ANIMACIE = 50
        self.obrazky_pole = []
        self.obrazky = pygame.image.load('obrazky/explozia.bmp').convert()
        self.obrazky.set_colorkey((255, 0, 255))
        for snimok_cislo in range(0, 240, 60):
            self.obrazky_pole.append(self.obrazky.subsurface((snimok_cislo, 0, 60, 60)))
        self.image = self.obrazky_pole[0]
        self.rect = self.obrazky_pole[0].get_rect()
        self.cas_animacie = 0
        self.pocitadlo_animacie = 0
        # Výbuch prebehne na presnej zadanej pozície zo vstupuz
        self.rect.topleft = pozicia

    def update(self, casovac):
        """Vykresľuje animáciu výbuchu"""
        if self.cas_animacie < casovac:
            self.cas_animacie = casovac
            self.image = self.obrazky_pole[self.pocitadlo_animacie]
            self.pocitadlo_animacie += 1
            # Keď animácia skončí, objekt sa odstráni
            if self.pocitadlo_animacie > 3:
                self.kill()
            self.cas_animacie += self.DLZKA_ANIMACIE

class Hranica(pygame.sprite.Sprite):
    """Neviditeľná hranica, ktorá je vykresľovaná mimo obrazovky pre detekciu,
        kedy sú nepratelia mimo obrazovky."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.HRANICA_OFSET = 89
        self.image = pygame.image.load('obrazky/ui/hranica.bmp').convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, kon.VELKOST_OKNA_Y + self.HRANICA_OFSET]
