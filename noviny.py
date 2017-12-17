#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import pygame
from pygame.locals import *

import konstanty as kon

def nacitaj_1_noviny(NOVINY, uroven):
    """Výber 1 vhodného obrázku na základe úrovne"""
    if uroven == 1:
        image = pygame.image.load(kon.NOVINY_CESTA.format(uroven, NOVINY)).convert()
    elif uroven == 2:
        image = pygame.image.load(kon.NOVINY_CESTA.format(uroven, random.randrange(1,27))).convert()
    else:
        image = pygame.image.load(kon.NOVINY_CESTA.format(uroven, random.randrange(1,42))).convert()

    return image

def nacitaj_2_noviny(NOVINY, uroven):
    """Výber 2 vhodných obrázkov na základe úrovne"""
    noviny_animovane = str(NOVINY) + '_5'
    obrazok_pole = []
    if uroven == 1:
        obrazok_pole.append(pygame.image.load(kon.NOVINY_CESTA.format(uroven, NOVINY)).convert())
        obrazok_pole.append(pygame.image.load(kon.NOVINY_CESTA.format(uroven, noviny_animovane)).convert())        
    elif uroven == 2:
        obrazok_pole.append(pygame.image.load(kon.NOVINY_CESTA.format(uroven, random.randrange(1,27))).convert())
        obrazok_pole.append(pygame.image.load(kon.NOVINY_CESTA.format(uroven, random.randrange(1,27))).convert())
    else:
        obrazok_pole.append(pygame.image.load(kon.NOVINY_CESTA.format(uroven, random.randrange(1,42))).convert())
        obrazok_pole.append(pygame.image.load(kon.NOVINY_CESTA.format(uroven, random.randrange(1,42))).convert())
    return obrazok_pole

class Noviny1(pygame.sprite.Sprite):
    """Vykresľuje základného nepriateľa - noviny"""    
    def __init__(self, suradnica_x, suradnica_y, uroven = 1):
        pygame.sprite.Sprite.__init__(self)
        self.NOVINY_OFSET_1 = 210
        self.NOVINY_OFSET_2 = 55
        self.NOVINY = 1
        # Výber vhodného obrázku na základe úrovne    
        self.image = nacitaj_1_noviny(self.NOVINY, uroven)
            
        # Určenie farby, ktorá bude slúžiť ako tzv. "alfa kanál"
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()

        # Určenie počiatočných súradníc novín na základne vstupných parametrov suradnica_x a suradnica_y
        # Noviny sú umiestnené mimo obrazovku a posupne sa posúvajú smerom na obrazvoku ku hráčovi
        self.suradnica_x = (suradnica_x * self.NOVINY_OFSET_1) + self.NOVINY_OFSET_2
        self.suradnica_y = -(suradnica_y * self.NOVINY_OFSET_1) - self.rect.height * 2
        self.rect.topleft = [self.suradnica_x, self.suradnica_y]
        
        # Určenie rýchlosti pohybu novín po obrazovke
        # Prvé číslo je smer horizontálny a druhý je vertikálny
        self.smer = [2, 3]
        self.cas_pohybu = 0

    def update(self, casovac):
        """Vykresľuje pohyb novín po obrazovke smerom dole"""
        # Pohyb je založený na reálnom čase
        # V tomto prípade každých 20 ms prebehne podmienka
        # a nepriateľ sa pohne o "smer" hodnotu smerom dole obrazovky
        if self.cas_pohybu < casovac:
            self.cas_pohybu = casovac
            self.rect.top = self.rect.top + self.smer[1]
            self.cas_pohybu += kon.NOVINY_DLZKA_POHYBU
            

class Noviny2(Noviny1):
    """Trieda Noviny2 dedí z Noviny1 a preberá jej metódy a vlastnosti."""
    def __init__(self, suradnica_x, suradnica_y, uroven = 1):
        """Vďaka tomu, že trieda dedí z nadradenej triedy,
            nie je potreba písať všetky hodnoty,
            ale iba tie, ktoré sú potrebné"""
        # Narozdiel od dedených novín, tieto noviny strieľajú na hráča,
        # je to riešené v hlavnej funkcii.
        # Hlavný dôvod novej triedy, je nový obrázok,
        # no do budúcna sa môžu jej vlastnosti ľubovoľne upravovať.
        Noviny1.__init__(self, suradnica_x, suradnica_y)
        self.NOVINY = 2
        self.image = nacitaj_1_noviny(self.NOVINY, uroven)


class Noviny3(Noviny1):
    """Trieda Noviny3 dedí z Noviny1"""
    def __init__(self, suradnica_x, suradnica_y, uroven = 1):
        Noviny1.__init__(self, suradnica_x, suradnica_y)
        self.NOVINY = 3
        self.DZLKA_ANIMACIE = 600
        # Trieda načítavá 2 obrázky do poľa, aby animácia bola možná.       
        self.obrazok_pole = nacitaj_2_noviny(self.NOVINY, uroven)
        
        self.rect.topleft = [self.suradnica_x, self.suradnica_y]
        self.smer = [4, 3]
        # Náhodné číslo, ktoré určuje, akú veľkú dráhu objekt vykoná do strán
        self.draha = random.randrange(30, 51)

        # Náhodne určuje, ktorý obrázok bude ako prvý        
        self.pocitadlo_animacie = random.randrange(0, 2)
        # Určuje aký čas bude medzi jednotlivými snímkami animácie
        self.cas_animacie = 0

    def update(self, casovac):
        """Funkcia riadi pohyb smerom dole, ale aj do strán"""
        if self.cas_pohybu < casovac:
            self.cas_pohybu = casovac
            if self.rect.left < self.suradnica_x - self.draha or self.rect.left > self.suradnica_x + self.draha:
                self.smer[0] = -self.smer[0]
                
            self.rect.left = self.rect.left + self.smer[0]
            self.rect.top = self.rect.top + self.smer[1]

            self.cas_pohybu += kon.NOVINY_DLZKA_POHYBU

            self.image = self.obrazok_pole[self.pocitadlo_animacie]
            if self.cas_animacie < casovac:
                self.cas_animacie = casovac
                self.pocitadlo_animacie -= 1
                if self.pocitadlo_animacie < 0:
                    self.pocitadlo_animacie = 1
                self.cas_animacie += self.DZLKA_ANIMACIE

class Noviny4(Noviny1):
    """Trieda Noviny4 dedí z Noviny1"""
    def __init__(self, suradnica_x, suradnica_y, uroven = 1):
        """Trieda je veľmi podobná s triedou Noviny3,
            pohyb je jemne upravený a obrázky zmenené"""
        Noviny1.__init__(self, suradnica_x, suradnica_y)
        self.NOVINY = 4
        self.DZLKA_ANIMACIE = 300
        self.obrazok_pole = nacitaj_2_noviny(self.NOVINY, uroven)
        
        self.rect.topleft = [self.suradnica_x, self.suradnica_y]
        self.smer = [2, 3]
        self.draha = 50
                
        self.pocitadlo_animacie = random.randrange(0, 2)
        self.cas_animacie = 0

    def update(self, casovac):
      if self.cas_pohybu < casovac:
            self.cas_pohybu = casovac
            if self.rect.left < self.suradnica_x - self.draha or self.rect.left > self.suradnica_x + self.draha:
                self.smer[0] = -self.smer[0]
                
            self.rect.left = self.rect.left + self.smer[0]
            self.rect.top = self.rect.top + self.smer[1]

            self.cas_pohybu += kon.NOVINY_DLZKA_POHYBU

            self.image = self.obrazok_pole[self.pocitadlo_animacie]
            if self.cas_animacie < casovac:
                self.cas_animacie = casovac
                self.pocitadlo_animacie -= 1
                if self.pocitadlo_animacie < 0:
                    self.pocitadlo_animacie = 1
                self.cas_animacie += self.DZLKA_ANIMACIE

class Noviny5(Noviny1):
    """Trieda Noviny5 dedí z Noviny1"""
    def __init__(self, suradnica_x, suradnica_y, uroven = 1):
        """Táto trieda má na možnosť z 2 obrázkov, ktoré náhodne vyberie pri spustení"""
        Noviny1.__init__(self, suradnica_x, suradnica_y)
        self.NOVINY = 5
        self.obrazok_pole = nacitaj_2_noviny(self.NOVINY, uroven)
        
        self.image = self.obrazok_pole[random.randrange(0, 2)]
        
        self.rect.topleft = [self.suradnica_x, self.suradnica_y]
        self.smer = [3, 4]
        self.draha = 50
        self.stop = False
        self.stop_casovac = 0

    def update(self, casovac):
        """Pohyb je komplexnejší a nepriateľ sa počas pohybu zastaví,
            posunie o určitú vzdialenosť do strany,
            pokračuje ďalej a opakaje celé od znova ešte raz."""
        if self.cas_pohybu < casovac:
            self.cas_pohybu = casovac
            if (self.rect.top > 90 and self.rect.top < 94) or (self.rect.top > 350 and self.rect.top < 354):
                # Boolean self.stop určujé, či noviny zastavili a ak áno, tak stoja presne 500 ms.
                self.cas_pohybu += 500
                self.stop = True
            else:
                self.stop = False

            self.rect.top = self.rect.top + self.smer[1]
            
            self.cas_pohybu += kon.NOVINY_DLZKA_POHYBU

        if self.stop and self.stop_casovac < casovac:
          self.stop_casovac = casovac
          if self.rect.left > self.suradnica_x - self.draha and self.rect.top < 100:
              self.rect.left = self.rect.left - self.smer[0]
          if self.rect.left < self.suradnica_x + self.draha and self.rect.top > 100:
              self.rect.left = self.rect.left + self.smer[0]          
          self.stop_casovac += 5

class Noviny6(Noviny1):
    """Trieda Noviny6 dedí z Noviny1"""
    def __init__(self, suradnica_x, suradnica_y, uroven = 1):
        Noviny1.__init__(self, suradnica_x, suradnica_y)
        self.NOVINY = 6
        self.obrazok_pole = nacitaj_2_noviny(self.NOVINY, uroven)
        
        self.image = self.obrazok_pole[random.randrange(0, 2)]
        
        self.rect.topleft = [self.suradnica_x, self.suradnica_y]
        self.smer = [3, 4]
        self.draha = 50
        self.stop = False
        # Vygeneruje na ktorých miestach sa má nepriateľ pozastaviť a vykonať určitý pohyb
        self.stop_opakovania = []
        self.stop_opakovania.append(random.randrange(100, 200))
        self.stop_opakovania.append(random.randrange(200, 400))
        self.stop_opakovania.append(random.randrange(400, 600))

    def update(self, casovac):
        """Pohyb je podobný ako u Noviny5,
            lenže sa opakuje 3x ná náhodných miestach a taktiež je rýchlejší"""
        if self.cas_pohybu < casovac:
            self.cas_pohybu = casovac
            if (self.rect.top > self.stop_opakovania[0] and self.rect.top < self.stop_opakovania[0] + 4) or (self.rect.top > self.stop_opakovania[1] and self.rect.top < self.stop_opakovania[1] + 4) or (self.rect.top > self.stop_opakovania[2] and self.rect.top < self.stop_opakovania[2] + 4):
                self.cas_pohybu += 500
                self.stop = True                
            else:
                self.stop = False

            self.rect.top = self.rect.top + self.smer[1]

            self.cas_pohybu += kon.NOVINY_DLZKA_POHYBU            
      
        if self.stop:
          self.rect.left = self.rect.left + self.smer[0]
          if (self.rect.left < self.suradnica_x - self.draha or self.rect.left > self.suradnica_x + self.draha):
              self.smer[0] = -self.smer[0]

class Noviny7(Noviny1):
    """Trieda Noviny7 dedí z Noviny1"""
    def __init__(self, suradnica_x, suradnica_y, uroven = 1):
        Noviny1.__init__(self, suradnica_x, suradnica_y)
        self.NOVINY = 7
        self.DLZKA_ANIMACIE = 150
        self.obrazok = pygame.image.load(kon.NOVINY_CESTA.format(uroven, self.NOVINY)).convert()
        self.obrazok_pole = []
        # Animácia skladajúca sa s 5 snímkov
        # Rozdelenie obrázku podľa parametrov a následné vloženie do poľa
        # 375 = šírka obrázku, 75 = šírka jedného snímku, 90 výška obrázku
        if uroven == 1:
            for i in range(0, 375, 75):
                self.obrazok_pole.append(self.obrazok.subsurface((i, 0, 75, 90)))
        elif uroven == 2:
            for i in range(1, 6):
                self.obrazok_pole.append(pygame.image.load(kon.NOVINY_CESTA.format(uroven, random.randrange(1,27))).convert())
        else:
            for i in range(1, 6):
                self.obrazok_pole.append(pygame.image.load(kon.NOVINY_CESTA.format(uroven, random.randrange(1,42))).convert())

        self.rect.topleft = [self.suradnica_x, self.suradnica_y]
        self.smer = [4, 3]
        self.draha = 20

        self.pocitadlo_animacie = 0
        self.cas_animacie = 0
        # Určuje smer animácie
        self.smer_animacie = random.randrange(0, 2)
        # Podmienka určuje, aby animácia bola presne opačná
        if self.smer_animacie == 1:
           self.pocitadlo_animacie = 4 

    def update(self, casovac):
      if self.cas_pohybu < casovac:
            self.cas_pohybu = casovac
            if self.rect.left < self.suradnica_x - self.draha or self.rect.left > self.suradnica_x + self.draha:
                    self.smer[0] = -self.smer[0]
                    # Pri každej otočke nepriateľ urobí menší skok smerom dole o 1O px
                    self.rect.top = self.rect.top + 10
                
            self.rect.left = self.rect.left + self.smer[0]
            self.rect.top = self.rect.top + self.smer[1]

            self.cas_pohybu += kon.NOVINY_DLZKA_POHYBU

            self.image = self.obrazok_pole[self.pocitadlo_animacie]
            if self.cas_animacie < casovac:
                self.cas_animacie = casovac
                if self.smer_animacie == 0:
                    self.pocitadlo_animacie -= 1
                    if self.pocitadlo_animacie < 0:
                        self.pocitadlo_animacie = 4
                if self.smer_animacie == 1:
                    self.pocitadlo_animacie += 1
                    if self.pocitadlo_animacie > 4:
                        self.pocitadlo_animacie = 0
                self.cas_animacie += self.DLZKA_ANIMACIE
