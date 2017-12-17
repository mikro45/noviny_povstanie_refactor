#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

class Skore(pygame.sprite.Sprite):
    """Trieda Skore vykresľuje skóre na obrazovke."""
    
    def __init__(self, zivoty, uroven, pod_uroven, zivoty_zakladne, peniaze, skore):
        # Načítanie triedy Sprite
        pygame.sprite.Sprite.__init__(self)
        # Zadefinovanie fontu a textu
        self.font = pygame.font.SysFont("comicsansms", 19)
        self.farba = (0, 64, 255)
        # Premenné meniace skóre
        self.zivoty = zivoty
        self.uroven = uroven
        self.pod_uroven = pod_uroven        
        self.zivoty_zakladne = zivoty_zakladne        
        self.peniaze = peniaze
        self.skore = skore
        # Načítanie rôzneho pozadia / podkladu (bar) pre skóre        
        self.bar_normal = pygame.image.load('obrazky/ui/bar.bmp').convert()
        self.bar_boss = pygame.image.load('obrazky/ui/barBoss.bmp').convert()
        self.image = self.bar_normal
        self.rect = self.image.get_rect()
        # Určenie x, y súradnice pre vykreslovanie textu
        self.text_y = 2
        self.text_zivoty_x = 28
        self.text_uroven_x = 83
        self.text_zivoty_zakladne_x = 448
        self.text_peniaze_x = 659
        self.text_skore_x = 796
        # Premenné určujúce či je úroveň bonus, boss alebo normal
        self.uroven_bonus = 6
        self.uroven_boss = 7

    def update(self, zivoty, uroven, pod_uroven, zivoty_zakladne, peniaze, skore, bar):
        """Mení skóre na základe vstupných parametrov."""
        # Zmena skóre
        self.zivoty = zivoty
        self.uroven = uroven
        self.pod_uroven = pod_uroven        
        self.zivoty_zakladne = zivoty_zakladne        
        self.peniaze = peniaze
        self.skore = skore
        
        # Vloženie rôznych položiek skóre do poľa
        self.text_pole = []
        for self.text in ('{}'.format(self.zivoty),
                    u'ÚROVEŇ: {} - {}'.format(self.uroven, self.pod_uroven),
                    '{}'.format(self.zivoty_zakladne),
                    '{}'.format(self.peniaze),
                    u'SKÓRE: {}'.format(self.skore)):
            self.text_pole.append(self.font.render(self.text, True, self.farba))
            
        # Ak je hráč v 6. pod-úrovni - bonusovej pod-úrovni, tak sa nepíše 6. pod-úroveň ale x. bonus
        if pod_uroven == self.uroven_bonus:
            self.text_pole[1] = self.font.render(('{}. BONUS'.format(self.uroven)), True, self.farba)
        # Ak je hráč v 7. pod-úrovni - Boss pod-úrovni, tak sa nepíše 7. pod-úroveň ale x. Boss    
        if pod_uroven == self.uroven_boss:
            self.text_pole[1] = self.font.render(('{}. BOSS'.format(self.uroven)), True, self.farba)

        # Vykreslenie transparentého pozadia pod pozadie pre lepší anti-aliasing textu - vyhladzovanie hrán textu
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        
        # Podľa vstupu určuje druh pozadia, ktorý sa vykreslí
        if bar:
            self.image.blit(self.bar_normal, (0, 0))
        else:
            self.image.blit(self.bar_boss, (0, 0))        

        # Vykreslovanie položiek skóre na vopred určené pozície
        self.image.blit(self.text_pole[0], (self.text_zivoty_x, self.text_y))
        self.image.blit(self.text_pole[1], (self.text_uroven_x, self.text_y))
        self.image.blit(self.text_pole[2], (self.text_zivoty_zakladne_x, self.text_y))
        self.image.blit(self.text_pole[3], (self.text_peniaze_x, self.text_y))
        self.image.blit(self.text_pole[4], (self.text_skore_x, self.text_y))
