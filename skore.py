#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from konstanty import *

class Skore(pygame.sprite.Sprite):
    """Trieda Skore vykresľuje skóre na obrazovke."""

    def __init__(self, zivoty, uroven, pod_uroven, zivoty_zakladne, peniaze, skore):
        # Načítanie triedy Sprite
        pygame.sprite.Sprite.__init__(self)
        # Lokálne premenné v triede
        self.zivoty = zivoty
        self.uroven = uroven
        self.pod_uroven = pod_uroven        
        self.zivoty_zakladne = zivoty_zakladne        
        self.peniaze = peniaze
        self.skore = skore
        # Zadefinovanie fontu a textu
        self.farba = (0, 64, 255)
        self.font = pygame.font.SysFont("comicsansms", 19)
        # "u" pred úvodzovkami značí, že sa bude jednať o Unicode znaky (diakritika)
        self.text = u"      %d          ÚROVEŇ: %d - %d                                   %d                                  %d                    SKÓRE: %d" % (self.zivoty, self.uroven, self.pod_uroven, self.zivoty_zakladne, self.peniaze, self.skore)
        self.image = self.font.render(self.text, 1, self.farba)
        self.rect = self.image.get_rect()
        # Nastavenie súradnicu x,y objektu
        self.rect.topleft = [0, 2]


    def update(self, zivoty, uroven, pod_uroven, zivoty_zakladne, peniaze, skore):
        """Mení skóre na základe vstupných parametrov."""
        self.zivoty = zivoty
        self.uroven = uroven
        self.pod_uroven = pod_uroven        
        self.zivoty_zakladne = zivoty_zakladne        
        self.peniaze = peniaze
        self.skore = skore
        self.text = u"      %d          ÚROVEŇ: %d - %d                                   %d                                  %d                    SKÓRE: %d" % (self.zivoty, self.uroven, self.pod_uroven, self.zivoty_zakladne, self.peniaze, self.skore)
        # V prípade, ak sú peniaze veľmi veľké a posúvajú skóre mimo obrazovky,
        # tak sa položka skóre nastaví o niečo viac vľavo
        if self.peniaze > 999:
            self.text = u"      %d          ÚROVEŇ: %d - %d                                   %d                                  %d                 SKÓRE: %d" % (self.zivoty, self.uroven, self.pod_uroven, self.zivoty_zakladne, self.peniaze, self.skore)
        # Ak je hráč v 6. pod-úrovni - bonusovej pod-úrovni, tak sa nepíše 6. pod-úroveň ale x. bonus
        if self.pod_uroven == 6:
            self.text = u"      %d     ÚROVEŇ: %d. BONUS                                %d                                  %d                  SKÓRE: %d" % (self.zivoty, self.uroven, self.zivoty_zakladne, self.peniaze, self.skore)
        # Ak je hráč v 7. pod-úrovni - Boss pod-úrovni, tak sa nepíše 7. pod-úroveň ale x. Boss
        if self.pod_uroven == 7:
            self.text = u"      %d      ÚROVEŇ: %d. BOSS                                %d                                  %d                  SKÓRE: %d" % (self.zivoty, self.uroven, self.zivoty_zakladne, self.peniaze, self.skore)
        self.image = self.font.render(self.text, 1, self.farba)
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 2]
        
class Skore_bar(pygame.sprite.Sprite):
    
    def __init__(self):
        """Vykresľuje podklad(bar) pre skóre"""
        pygame.sprite.Sprite.__init__(self)
        # Načítanie obrázkov zo súboru
        self.bar_normal = pygame.image.load('obrazky/ui/bar.bmp').convert()
        # 2. obrázok v prípade boss pod-úrovne, sa zobrazia životy Boss-a a nie životy základne
        self.bar_boss = pygame.image.load('obrazky/ui/barBoss.bmp').convert()
        self.image = self.bar_normal
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]

    def update(self, bar):
        """Podľa vstupu určuje druh bar-u, ktorý sa vykreslí"""
        if bar == 0:
            self.image = self.bar_normal
        else:
            self.image = self.bar_boss

