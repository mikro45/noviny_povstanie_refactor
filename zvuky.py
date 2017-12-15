#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

# Zvuky sú stiahnuté z internetu od neznámeho zdroja, pri čom ale neplánujem tieto zvuky naďalej šíriť
class Zvuky():
    """Trieda Zvuky prehráva všetky zvuky v hre."""

    def __init__(self):
        # Načítanie prehrávača zvukov a jeho nastavenie
        pygame.mixer.pre_init(44000, 16, 2, 4096)
        # Načítanie všetkých zvukov
        self.strela = pygame.mixer.Sound('zvuky/strela.wav')
        self.explozia = pygame.mixer.Sound('zvuky/explozia.wav')
        self.poskodenie = pygame.mixer.Sound('zvuky/poskodenie.wav')
        self.boj_pokrik = pygame.mixer.Sound('zvuky/boj_pokrik.wav')

    # Jednotlive funkcie pre prehrávanie jednotlivých zvukov
    # a zadefinovnie úrovní hlasitostí
    def strela_prehraj(self, volume = 0.3):
        self.strela.play()
        self.strela.set_volume(volume)

    def explozia_prehraj(self, volume = 0.2):
        self.explozia.play()
        self.explozia.set_volume(volume)

    def poskodenie_prehraj(self, volume = 0.2):
        self.poskodenie.play()
        self.poskodenie.set_volume(volume)

    def boj_pokrik_prehraj(self, volume = 1):
        self.boj_pokrik.play()
        self.boj_pokrik.set_volume(volume)
   
