#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################################
#
#   Zdroje:
#   Pozadie1: http://worldartsme.com/landscape-clipart.html#gal_post_5381_landscape-clipart-1.jpg
#   Pozadie_menu: http://clipartfreefor.com/files/1/12063_landscape-clipart.html
#
#   noviny_povstanie.py
#   1/2016 - 4/2016
#   Vytvorené pomocou Python 2.7.11 a pygame 1.9.2a0
#
#   Miroslav Dzuriš
#   SPŠE-PO IV.SA
#   2015 / 2016
#
#   Nečakaj žiadne špeciálne pravidlá, no priprav sa
#   na hordu nepriateľských novín
#   pripravených na boj s tebou vlnu za vlnou.
#   Tak  nezabudaj chrániť svoju základňu.
#   Máš 5 bodov zdravia a možnosti ako sa vylepšovať.   
#   No to neznamená, že to budeš mať ľahké...
#   Veľa šťastia. ;)
#
#   Ovládanie: šípka doľava a doprava - pohyb, medzerník - streľba
#   ESC - pauza, ENTER - potvrdenie položky v menu
#
#
####################################################################

# Importovanie modulov
import random
import os
import sys
import math

# Ak nie je modul pygame nainštalovaný vopred, tak je možnosť použiť lokálnu zálohu
#sys.path.append("moduly") 

# Importovanie modulu pygame
import pygame
from pygame.locals import *

# Globálne premenné
VELKOST_OKNA_X = 1024
VELKOST_OKNA_Y = 720

# Definovanie tried
# Každá trieda osbsahuje povinné premenné self.image a self.rect
# kvôli tomu, aby metóda Sprite mala čo, self.image(obrázok), a kam, self.rect(súradnice), vykresľovať


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


class Noviny_1(pygame.sprite.Sprite):
    """Vykresľuje základného nepriateľa - noviny"""    
    def __init__(self, x, y, uroven = 1):
        pygame.sprite.Sprite.__init__(self)        
        # Výber vhodného obrázku na základe úrovne    
        if uroven == 1:
            self.image = pygame.image.load('obrazky/noviny/uroven_1/noviny_1.bmp').convert()
        elif uroven == 2:
            self.image = pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert()
        else:
            self.image = pygame.image.load('obrazky/noviny/uroven_3/noviny_%s.bmp' % str(random.randrange(1,42))).convert()
            
        # Určenie farby, ktorá bude slúžiť ako tzv. "alfa kanál"
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()

        # Určenie počiatočných súradníc novín na základne vstupných parametrov x a y
        # Noviny sú umiestnené mimo obrazovku a posupne sa posúvajú smerom na obrazvoku ku hráčovi
        self.x = (x * 210) + 55
        self.y = -(y * 210) - self.rect.height * 2
        self.rect.topleft = [self.x, self.y]
        
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
            self.cas_pohybu += 20
            

class Noviny_2(Noviny_1):
    """Trieda Noviny_2 dedí z Noviny_1 a preberá jej metódy a vlastnosti."""
    def __init__(self, x, y, uroven = 1):
        """Vďaka tomu, že trieda dedí z nadradenej triedy,
            nie je potreba písať všetky hodnoty,
            ale iba tie, ktoré sú potrebné"""
        # Narozdiel od dedených novín, tieto noviny strieľajú na hráča,
        # je to riešené v hlavnej funkcii.
        # Hlavný dôvod novej triedy, je nový obrázok,
        # no do budúcna sa môžu jej vlastnosti ľubovoľne upravovať.
        Noviny_1.__init__(self, x, y)
        if uroven == 1:
            self.image = pygame.image.load('obrazky/noviny/uroven_1/noviny_2.bmp').convert()
        elif uroven == 2:
            self.image = pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert()
        else:
            self.image = pygame.image.load('obrazky/noviny/uroven_3/noviny_%s.bmp' % str(random.randrange(1,42))).convert()
        self.rect.topleft = [self.x, self.y]
        self.smer = [2, 3]


class Noviny_3(Noviny_1):
    """Trieda Noviny_3 dedí z Noviny_1"""
    def __init__(self, x, y, uroven = 1):
        Noviny_1.__init__(self, x, y)
        # Trieda načítavá 2 obrázky do poľa, aby animácia bola možná.       
        self.obrazok_pole = []
        if uroven == 1:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_1/noviny_3.bmp').convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_1/noviny_3_5.bmp').convert())        
        elif uroven == 2:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert())
        else:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_3/noviny_%s.bmp' % str(random.randrange(1,42))).convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_3/noviny_%s.bmp' % str(random.randrange(1,42))).convert())
        self.rect.topleft = [self.x, self.y]
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
            if self.rect.left < self.x - self.draha or self.rect.left > self.x + self.draha:
                self.smer[0] = -self.smer[0]
                
            self.rect.left = self.rect.left + self.smer[0]
            self.rect.top = self.rect.top + self.smer[1]

            self.cas_pohybu += 20

            self.image = self.obrazok_pole[self.pocitadlo_animacie]
            if self.cas_animacie < casovac:
                self.cas_animacie = casovac
                self.pocitadlo_animacie -= 1
                if self.pocitadlo_animacie < 0:
                    self.pocitadlo_animacie = 1
                self.cas_animacie += 600

class Noviny_4(Noviny_1):
    """Trieda Noviny_4 dedí z Noviny_1"""
    def __init__(self, x, y, uroven = 1):
        """Trieda je veľmi podobná s triedou Noviny_3,
            pohyb je jemne upravený a obrázky zmenené"""
        Noviny_1.__init__(self, x, y)
        self.obrazok_pole = []
        if uroven == 1:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_1/noviny_4.bmp').convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_1/noviny_4_5.bmp').convert())        
        elif uroven == 2:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert())
        else:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_3/noviny_%s.bmp' % str(random.randrange(1,42))).convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_3/noviny_%s.bmp' % str(random.randrange(1,42))).convert())
        
        self.rect.topleft = [self.x, self.y]
        self.smer = [2, 3]
        self.draha = 50
                
        self.pocitadlo_animacie = random.randrange(0, 2)
        self.cas_animacie = 0

    def update(self, casovac):
      if self.cas_pohybu < casovac:
            self.cas_pohybu = casovac
            if self.rect.left < self.x - self.draha or self.rect.left > self.x + self.draha:
                self.smer[0] = -self.smer[0]
                
            self.rect.left = self.rect.left + self.smer[0]
            self.rect.top = self.rect.top + self.smer[1]

            self.cas_pohybu += 20

            self.image = self.obrazok_pole[self.pocitadlo_animacie]
            if self.cas_animacie < casovac:
                self.cas_animacie = casovac
                self.pocitadlo_animacie -= 1
                if self.pocitadlo_animacie < 0:
                    self.pocitadlo_animacie = 1
                self.cas_animacie += 300

class Noviny_5(Noviny_1):
    """Trieda Noviny_5 dedí z Noviny_1"""
    def __init__(self, x, y, uroven = 1):
        """Táto trieda má na možnosť z 2 obrázkov, ktoré náhodne vyberie pri spustení"""
        Noviny_1.__init__(self, x, y)
        self.obrazok_pole = []
        if uroven == 1:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_1/noviny_5.bmp').convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_1/noviny_5_5.bmp').convert())        
        elif uroven == 2:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert())
        else:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_3/noviny_%s.bmp' % str(random.randrange(1,42))).convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_3/noviny_%s.bmp' % str(random.randrange(1,42))).convert())
        self.image = self.obrazok_pole[random.randrange(0, 2)]
        
        self.rect.topleft = [self.x, self.y]
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
            
            self.cas_pohybu += 20

        if self.stop and self.stop_casovac < casovac:
          self.stop_casovac = casovac
          if self.rect.left > self.x - self.draha and self.rect.top < 100:
              self.rect.left = self.rect.left - self.smer[0]
          if self.rect.left < self.x + self.draha and self.rect.top > 100:
              self.rect.left = self.rect.left + self.smer[0]          
          self.stop_casovac += 5

class Noviny_6(Noviny_1):
    """Trieda Noviny_6 dedí z Noviny_1"""
    def __init__(self, x, y, uroven = 1):
        Noviny_1.__init__(self, x, y)
        self.obrazok_pole = []
        if uroven == 1:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_1/noviny_6.bmp').convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_1/noviny_6_5.bmp').convert())        
        elif uroven == 2:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert())
        else:
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_3/noviny_%s.bmp' % str(random.randrange(1,42))).convert())
            self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_3/noviny_%s.bmp' % str(random.randrange(1,42))).convert())
        self.image = self.obrazok_pole[random.randrange(0, 2)]
        
        self.rect.topleft = [self.x, self.y]
        self.smer = [3, 4]
        self.draha = 50
        self.stop = False
        # Vygeneruje na ktorých miestach sa má nepriateľ pozastaviť a vykonať určitý pohyb
        self.stop_opakovania = []
        self.stop_opakovania.append(random.randrange(100, 200))
        self.stop_opakovania.append(random.randrange(200, 400))
        self.stop_opakovania.append(random.randrange(400, 600))

    def update(self, casovac):
        """Pohyb je podobný ako u Noviny_5,
            lenže sa opakuje 3x ná náhodných miestach a taktiež je rýchlejší"""
        if self.cas_pohybu < casovac:
            self.cas_pohybu = casovac
            if (self.rect.top > self.stop_opakovania[0] and self.rect.top < self.stop_opakovania[0] + 4) or (self.rect.top > self.stop_opakovania[1] and self.rect.top < self.stop_opakovania[1] + 4) or (self.rect.top > self.stop_opakovania[2] and self.rect.top < self.stop_opakovania[2] + 4):
                self.cas_pohybu += 500
                self.stop = True                
            else:
                self.stop = False

            self.rect.top = self.rect.top + self.smer[1]

            self.cas_pohybu += 20            
      
        if self.stop:
          self.rect.left = self.rect.left + self.smer[0]
          if (self.rect.left < self.x - self.draha or self.rect.left > self.x + self.draha):
              self.smer[0] = -self.smer[0]

class Noviny_7(Noviny_1):
    """Trieda Noviny_7 dedí z Noviny_1"""
    def __init__(self, x, y, uroven = 1):
        Noviny_1.__init__(self, x, y)
        self.obrazok = pygame.image.load('obrazky/noviny/uroven_1/noviny_7.bmp').convert()
        self.obrazok_pole = []
        # Animácia skladajúca sa s 5 snímkov
        # Rozdelenie obrázku podľa parametrov a následné vloženie do poľa
        # 375 = šírka obrázku, 75 = šírka jedného snímku, 90 výška obrázku
        if uroven == 1:
            for i in range(0, 375, 75):
                self.obrazok_pole.append(self.obrazok.subsurface((i, 0, 75, 90)))
        elif uroven == 2:
            for i in range(1, 6):
                self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_2/noviny_%s.bmp' % str(random.randrange(1,27))).convert())
        else:
            for i in range(1, 6):
                self.obrazok_pole.append(pygame.image.load('obrazky/noviny/uroven_3/noviny_%s.bmp' % str(random.randrange(1,42))).convert())
        self.rect.topleft = [self.x, self.y]
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
            if self.rect.left < self.x - self.draha or self.rect.left > self.x + self.draha:
                    self.smer[0] = -self.smer[0]
                    # Pri každej otočke nepriateľ urobí menší skok smerom dole o 1O px
                    self.rect.top = self.rect.top + 10
                
            self.rect.left = self.rect.left + self.smer[0]
            self.rect.top = self.rect.top + self.smer[1]

            self.cas_pohybu += 20

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
                self.cas_animacie += 150
                
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


class Strela(pygame.sprite.Sprite):
    """Trieda Strela vykresľuje vystrelené strely hráča (Tabletu)."""

    def __init__(self, pozicia):
        pygame.sprite.Sprite.__init__(self)
        # Načítanie a vykreslenie obrázku strely
        self.image = pygame.image.load('obrazky/strela.bmp').convert()
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = pozicia

    def update(self):
        """Umožnuje pohyb (let) strely."""
        if self.rect.top > 31:
            self.rect.top -= 4
        # Ak je strela mimo obrazovky, tak sa strela odstráni (zabije)
        else:
            self.kill()


class strela_noviny(Strela):
    """Trieda Strela vykresľuje vystrelené strely nepriateľov a dedí z triedy Strela."""

    def __init__(self, pozicia):
        Strela.__init__(self, pozicia)
        # Načítanie a vykreslenie obrázku strely
        self.image = pygame.image.load('obrazky/strela_noviny.bmp').convert()
        self.image.set_colorkey((255, 0, 255))

    def update(self):
        """Umožnuje pohyb (let) strely."""
        if self.rect.top < VELKOST_OKNA_Y:
            self.rect.top += 6
        # Ak je strela mimo obrazovky, tak sa strela odstráni (zabije)
        else:
            self.kill()

class Explozia(pygame.sprite.Sprite):
    """Trieda Explozia vykresľuje explózie."""

    def __init__(self, pozicia):
        pygame.sprite.Sprite.__init__(self)
        # Animácia výbuchu skladajúca sa zo 4 snímkoch
        self.obrazky_pole = []
        self.obrazky = pygame.image.load('obrazky/explozia.bmp').convert()
        self.obrazky.set_colorkey((255, 0, 255))
        for i in range(0, 240, 60):
            self.obrazky_pole.append(self.obrazky.subsurface((i, 0, 60, 60)))
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
            self.cas_animacie += 50

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
    def strela_p(self, volume = 0.3):
        self.strela.play()
        self.strela.set_volume(volume)

    def explozia_p(self, volume = 0.2):
        self.explozia.play()
        self.explozia.set_volume(volume)

    def poskodenie_p(self, volume = 0.2):
        self.poskodenie.play()
        self.poskodenie.set_volume(volume)

    def boj_pokrik_p(self, volume = 1):
        self.boj_pokrik.play()
        self.boj_pokrik.set_volume(volume)
   

class Menu():
    """Trieda Menu vykresľuje menu v hre."""

    def __init__(self):
        # zoznam položiek menu
        self.polozky = []
        # index vybratej položky
        self.vybrata_polozka = 0
        # voliteľný text na zobrazenie
        self.riadky = []

        # Zadefinovanie veľkosti tlačidiel
        self.tlacidlo_sirka = 220
        self.tlacidlo_vyska = 36

        # Zadefinovanie rôznych druhov fontov
        self.font_polozky = pygame.font.SysFont("comicsansms", 24)
        self.font_riadky = pygame.font.SysFont("comicsansms", 24)
        self.font_velky = pygame.font.SysFont("comicsansms", 92)
        self.font_stredny = pygame.font.SysFont("comicsansms", 52)
        self.font_noviny_povstanie = pygame.font.SysFont("comicsansms", 64, bold = True)

        # Načítanie pozadia menu
        self.pozadie = pygame.image.load('obrazky/pozadia/pozadie_menu.bmp').convert()

        # Zadefinovanie farieb
        self.farba_biela = (255, 255, 224)
        self.farba_cierna = (0, 64, 64)
        self.farba_tlacidlo_neaktivne = (0, 192, 0)
        self.farba_tlacidlo_aktivne = (255, 0, 64)
        
    # Get-re a Set-re
    def riadok_pridaj(self, riadok):
        self.riadky.append(riadok)

    def polozka_pridaj(self, polozka):
        self.polozky.append(polozka)

    def polozka_nastav(self, cislo_polozky):
        self.vybrata_polozka = cislo_polozky

    def polozka_zisti(self):
        return self.vybrata_polozka
             
    # Pohyb medzi položkami menu
    def kurzor_hore(self):        
        self.vybrata_polozka = max(self.vybrata_polozka - 1, -1)
        if self.vybrata_polozka == -1:
            self.vybrata_polozka = len(self.polozky) - 1
            
    def kurzor_dolava(self):        
        self.vybrata_polozka = max(self.vybrata_polozka - 1, -1)
        if self.vybrata_polozka == -1:
            self.vybrata_polozka = 0          

    def kurzor_dole(self):
        self.vybrata_polozka = min(self.vybrata_polozka + 1, len(self.polozky))
        if self.vybrata_polozka == len(self.polozky):
            self.vybrata_polozka = 0
            
    def kurzor_doprava(self):
        self.vybrata_polozka = min(self.vybrata_polozka + 1, len(self.polozky))
        if self.vybrata_polozka == len(self.polozky):
            self.vybrata_polozka = len(self.polozky) - 1
        

    # Funkcie pre vykresľovanie rôznych menu
    def vykresli_menu(self):
        menu = pygame.Surface((VELKOST_OKNA_X, VELKOST_OKNA_Y))
        menu.blit(self.pozadie, (0, 0))
                
        i = 0
        # Vykreslenie vsetkch poloziek
        while i < len(self.polozky):
          x = VELKOST_OKNA_X / 11 
          y = VELKOST_OKNA_Y / 11 * i + VELKOST_OKNA_Y / 10
          text = self.font_polozky.render(self.polozky[i], 1, self.farba_biela)
          pygame.draw.rect(menu, self.farba_tlacidlo_neaktivne, (x - 10, y, self.tlacidlo_sirka, self.tlacidlo_vyska))
          menu.blit(text, (x, y))
          # Vykreslenie vybratej - aktivnej polozky
          if i == self.vybrata_polozka:
            pygame.draw.rect(menu, self.farba_tlacidlo_aktivne, (x - 10, y, self.tlacidlo_sirka, self.tlacidlo_vyska))
            menu.blit(text, (x, y))

          i += 1

        i = 0

        # Vykreslenie všetkých riadkov - textu
        while i < len(self.riadky):
          x = VELKOST_OKNA_X / 11 
          y = VELKOST_OKNA_Y / 16 * i + VELKOST_OKNA_Y / 5          
          text = self.font_riadky.render(self.riadky[i], 1, self.farba_cierna)
          menu.blit(text,(x, y))
          i += 1

        menu.blit(self.font_noviny_povstanie.render("Noviny - Povstanie", 1, self.farba_biela),(400, 50))
        pygame.display.update()
        return menu
    
    # Vykreslí menu, ktoré prekryje aktuálnu obrazovku s menu bez pozadia
    def vykresli_popup_menu(self, obrazovka):
        i = 0

        while i < len(self.polozky):
          x = VELKOST_OKNA_X / 3.5 * i + VELKOST_OKNA_X / 3.5
          y = VELKOST_OKNA_Y / 2

          text = self.font_polozky.render(self.polozky[i], 1, self.farba_biela)
          rect = pygame.draw.rect(obrazovka, self.farba_tlacidlo_neaktivne, (x - 10, y, self.tlacidlo_sirka, self.tlacidlo_vyska))
          obrazovka.blit(text, (x, y)) 

          if i == self.vybrata_polozka:
            rect = pygame.draw.rect(obrazovka, self.farba_tlacidlo_aktivne, (x - 10, y, self.tlacidlo_sirka, self.tlacidlo_vyska))
            obrazovka.blit(text, (x, y))  

          i += 1      

        pygame.display.update()
        return obrazovka

    # Vykreslí koniec hry - text
    def vykresli_koniec(self, obrazovka):
        i = 0

        while i < len(self.riadky):
          x = VELKOST_OKNA_X / 5
          y = VELKOST_OKNA_Y / 5 * i + 100
          text = self.font_velky.render(self.riadky[i], 1, self.farba_cierna)
          if i > 0:
            text = self.font_stredny.render(self.riadky[i], 1, self.farba_biela)
          rect = text.get_rect()
          rect.centerx = VELKOST_OKNA_X / 2
          rect.y = y
          obrazovka.blit(text, rect)
         
          i += 1
          
        pygame.display.update()
        return obrazovka

class Menu_Obchod(Menu):
    """Trieda Menu_Obchod vykresľuje obchod v hre"""

    def __init__(self):
        Menu.__init__(self)

        # Načítanie obrázkov šípiek pre pohyb v obchode
        self.sipka_l0 = pygame.image.load('obrazky/ui/sipka_l0.bmp').convert()
        self.sipka_l0.set_colorkey((255, 0, 255))
        self.sipka_p0 = pygame.image.load('obrazky/ui/sipka_p0.bmp').convert()
        self.sipka_p0.set_colorkey((255, 0, 255))
        self.sipka_l = pygame.image.load('obrazky/ui/sipka_l.bmp').convert()
        self.sipka_l.set_colorkey((255, 0, 255))
        self.sipka_p = pygame.image.load('obrazky/ui/sipka_p.bmp').convert()
        self.sipka_p.set_colorkey((255, 0, 255))

        # Načítanie obrázkov pre náhľad v obchode
        self.ob_tablet_zivot = pygame.image.load('obrazky/obchod_veci/ob_tablet_zivot.bmp').convert()
        self.ob_tablet_zivot.set_colorkey((255, 0, 255))
        self.ob_tablet_rychlost = pygame.image.load('obrazky/obchod_veci/ob_tablet_rychlost.bmp').convert()
        self.ob_tablet_rychlost.set_colorkey((255, 0, 255))
        self.ob_zakladna_zivot = pygame.image.load('obrazky/obchod_veci/ob_zakladna_zivot.bmp').convert()
        self.ob_zakladna_zivot.set_colorkey((255, 0, 255))
        self.ob_zbran_rychlost = pygame.image.load('obrazky/obchod_veci/ob_zbran_rychlost.bmp').convert()
        self.ob_zbran_rychlost.set_colorkey((255, 0, 255))
        self.ob_zbran_nova = pygame.image.load('obrazky/obchod_veci/ob_zbran_nova.bmp').convert()
        self.ob_zbran_nova.set_colorkey((255, 0, 255))

        # Boolean pre určenie či hráč bude pohybovať v náhľade alebo medzi tlačidlami
        self.obchod = False

    # Metódy pre pohyb v obchode
    def kurzor_obchod(self):
        self.obchod = True
        self.vybrata_polozka = 3

    def kurzor_obchod_lavo(self):
        self.vybrata_polozka = 101
        
    def kurzor_obchod_pravo(self):
        self.vybrata_polozka = 102

    def kurzor_obchod_dole(self):
        self.obchod = False
        self.vybrata_polozka = 0

    # Vykresleni obchodu
    def vykresli_obchod_menu(self, index, cena, meno, extra = ""):
        menu = pygame.Surface((VELKOST_OKNA_X, VELKOST_OKNA_Y))
        menu.blit(self.pozadie, (0, 0))

        i = 0

        # Zadefinovanie rozmerov a suradnic vsetkych objektov v obchode
        # pre pripadne buduce zmene a pre ropoznanie
        ramcek_12_hrubka = 4
        ramcek_1 = [387, 125, 250]
        ramcek_2 = [170, 404, 684, 244]
        ramcek_3 = [402, 43, 220, 60]

        sipka_1 = [ramcek_1[0] - 107, 205]
        sipka_2 = [ramcek_1[0] + ramcek_1[2] + 60, 205]

        ramcek_1_obrazok = [ramcek_1[0] + 3, ramcek_1[1] + 3]

        text_nadpisu = [418, 35]
        text_popisu = [195, 410]

        # Zadefinovanie pouzitych farieb
        farba_ramceka = (0, 64, 64)
        farba_ramceka_vnutri = (255, 255, 224)
        farba_ramceka_aktivna = (0, 192, 0)
        farba_popisu = (0, 192, 255)
        farba_nadpisu = (0, 128, 255)
               

        
        while i < len(self.polozky):
            x = VELKOST_OKNA_X / 3.3 * i + VELKOST_OKNA_X / 4
            y = 670

            text = self.font_polozky.render(self.polozky[i], 1, self.farba_biela)
            rect = pygame.draw.rect(menu, self.farba_tlacidlo_neaktivne, (x - 10, y, self.tlacidlo_sirka, self.tlacidlo_vyska))
            menu.blit(text, (x, y))        

            if i == self.vybrata_polozka:
                rect = pygame.draw.rect(menu, self.farba_tlacidlo_aktivne, (x - 10, y, self.tlacidlo_sirka, self.tlacidlo_vyska))
                menu.blit(text, (x, y))          

            i += 1
        
        # Vykreslenie ramcekov
        rect = pygame.draw.rect(menu, farba_ramceka, (ramcek_1[0], ramcek_1[1], ramcek_1[2], ramcek_1[2]), ramcek_12_hrubka)
        rect = pygame.draw.rect(menu, farba_ramceka_vnutri, (ramcek_1[0] + 3, ramcek_1[1] + 3, ramcek_1[2] - 5, ramcek_1[2] -5))        
            
        rect = pygame.draw.rect(menu, farba_ramceka, (ramcek_2[0], ramcek_2[1], ramcek_2[2], ramcek_2[3]), ramcek_12_hrubka)
        rect = pygame.draw.rect(menu, farba_ramceka_vnutri, (ramcek_2[0] + 3, ramcek_2[1] + 3, ramcek_2[2] - 5, ramcek_2[3] - 5))

        rect = pygame.draw.rect(menu, farba_ramceka, (ramcek_3[0], ramcek_3[1], ramcek_3[2], ramcek_3[3]), ramcek_12_hrubka)
        rect = pygame.draw.rect(menu, farba_ramceka_vnutri, (ramcek_3[0] + 3, ramcek_3[1] + 3, ramcek_3[2] - 5, ramcek_3[3] - 5))

        menu.blit(self.sipka_l0, (sipka_1[0], sipka_1[1]))
        menu.blit(self.sipka_p0, (sipka_2[0], sipka_2[1]))               
        

        if self.obchod:
            rect = pygame.draw.rect(menu, farba_ramceka_aktivna, (ramcek_1[0], ramcek_1[1], ramcek_1[2], ramcek_1[2]), ramcek_12_hrubka)
            if self.vybrata_polozka == 101:
                menu.blit(self.sipka_l, (sipka_1[0], sipka_1[1]))
            if self.vybrata_polozka == 102:
                menu.blit(self.sipka_p, (sipka_2[0], sipka_2[1]))

        # Vykreslenie objektov obchodu, podľa aktuálného výberu
        if index == 0:
            menu.blit(self.ob_tablet_zivot, (ramcek_1_obrazok[0], ramcek_1_obrazok[1]))
        elif index == 1:
            menu.blit(self.ob_tablet_rychlost, (ramcek_1_obrazok[0], ramcek_1_obrazok[1]))
        elif index == 2:
            menu.blit(self.ob_zakladna_zivot, (ramcek_1_obrazok[0], ramcek_1_obrazok[1]))
        elif index == 3:
            menu.blit(self.ob_zbran_rychlost, (ramcek_1_obrazok[0], ramcek_1_obrazok[1]))
        elif index == 4:
            menu.blit(self.ob_zbran_nova, (ramcek_1_obrazok[0], ramcek_1_obrazok[1]))

        menu.blit(self.font_stredny.render(u"Obchod", 1, farba_nadpisu), (text_nadpisu[0], text_nadpisu[1]))
        
        # Vykresľovanie popisu pre rôzne položky obchodu      
        menu.blit(self.font_stredny.render(meno, 1, farba_popisu), (text_popisu[0], text_popisu[1]))
        menu.blit(self.font_stredny.render("CENA = %d" % cena, 1, farba_popisu), (text_popisu[0], text_popisu[1] + 72))
        menu.blit(self.font_stredny.render(u"%s" % extra, 1, farba_popisu), (text_popisu[0], text_popisu[1] + 72 * 2))

        pygame.display.update()  
        return menu


class Hranica(pygame.sprite.Sprite):
    """Neviditeľná hranica, ktorá je vykresľovaná mimo obrazovky pre detekciu,
        kedy sú nepratelia mimo obrazovky."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('obrazky/ui/hranica.bmp').convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, VELKOST_OKNA_Y + 89]


# Hlavná funkcia
def main():
    """
    Hlavná funkcia, je funkcia ktorá je volaná pri spustení hry.

    Načíta všetko potrebné a potom spustí hlavnú slučku,
    ktorá sa opakuje až kým neskončí hra
    """

    # Lokálne konštanty
    STAV_MENU_HLAVNE = 0    
    STAV_VYHRA = 1
    STAV_PREHRA = 2
    STAV_MENU_AKO = 3
    STAV_V_HRE = 4
    STAV_MENU_OBCHOD = 5
    STAV_MENU_PAUSE = 6


    # Načítanie modulu pygame
    pygame.init()

    # Nastavenie pozicie okna na horny kraj obrazovky
    #os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    # Nastavenie pozicie okna na stred obrazovky
    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
    
    # Zadefinovanie lokálnych premenných
    # Základné hodnoty skóre
    skore_zivoty = 5
    skore_peniaze = 0
    skore_zivoty_zakladne = 15
    skore_uroven = 1
    skore_pod_uroven = 1
    skore_skore = 0

    # Boolean určujúci rozdielne vykresľovanie pre 1. úroveň
    uroven_1 = True

    # Premenné slúžiace na pohyb strel v hre
    cas_strely = 0
    cas_strely_noviny = 0
    # Premenné slúžiace na umiernený pohyb v menu medzi položkami
    oneskorenie_enter = 0
    oneskorenie_sipky = 0

    # Premenné určujúce základné hodnoty obchodu
    ob_tablet_rychlost = 9.0
    ob_tablet_rychlost_lvl = 1
    ob_strelba_rychlost = 300
    ob_strelba_rychlost_lvl = 1
    ob_strela_pocet = 1

    # Pomocné premenné pre bochod
    index_obchod = 0
    cena = 0
    meno = ""
    extra = ""
    obchod = False
    obchod_pokracuj = False

    # Premenná určujúca počiatočný počet životov Boss-ov
    boss_hp = 100

    # Načítanie skóra zo súbora
    try:
        HIGHSCORE = [line.rstrip('\n') for line in open('highscore.txt')]
    except IOError:
        highscore = file("highscore.txt", "w")
        highscore.write(str(0))
        highscore.close()
        HIGHSCORE = [line.rstrip('\n') for line in open('highscore.txt')]

    # Stav = čo sa aktuálne deje - čo je vykreslene na obrazovke
    stav = STAV_MENU_HLAVNE

    # Nastavenie základných parametrov pygame
    hodiny = pygame.time.Clock()
    obrazovka = pygame.display.set_mode((VELKOST_OKNA_X, VELKOST_OKNA_Y))#, pygame.FULLSCREEN
    pozadie = pygame.image.load('obrazky/pozadia/pozadie1.bmp').convert()

    # Prispôsobenie herného okna
    pygame.display.set_caption('Noviny - Povstanie')
    pygame.mouse.set_visible(0)
    ikona = pygame.image.load("ikona.ico")
    pygame.display.set_icon(ikona)

    # Vytvorenie skupín objektov a pridanie niektorých objektov do skupín
    noviny = pygame.sprite.RenderUpdates()
    noviny_ozbrojene = pygame.sprite.RenderUpdates()
    noviny_boss = pygame.sprite.RenderUpdates()
    noviny_bonus = pygame.sprite.RenderUpdates()

    skore = pygame.sprite.RenderUpdates()
    skore.add(Skore(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore))

    tablet = pygame.sprite.RenderUpdates()
    tablet.add(Tablet())
    
    strely = pygame.sprite.RenderUpdates()

    explozie = pygame.sprite.RenderUpdates()
    
    strely_noviny = pygame.sprite.RenderUpdates()

    hranica = pygame.sprite.RenderUpdates()
    hranica.add(Hranica())

    skore_bar = pygame.sprite.RenderUpdates()
    skore_bar.add(Skore_bar())
    
    # Načítanie triedy Zvuky
    zvuk = Zvuky()

    # Zadefinovanie všetkych položiek všetkých menu
    menu_hlavne = Menu()
    menu_hlavne.polozka_pridaj(u"Nová Hra")
    menu_hlavne.polozka_pridaj(u"Pokračovať v hre")
    menu_hlavne.polozka_pridaj(u"Ako Hrať")
    menu_hlavne.polozka_pridaj("Koniec")

    menu_ako = Menu()
    menu_ako.polozka_pridaj(u"Späť")
    menu_ako.riadok_pridaj(u"Ovládanie:")
    menu_ako.riadok_pridaj(u"pohyb: šípky doľava a doprava, streľba: medzerník")
    menu_ako.riadok_pridaj(u"pauza: ESCAPE, potvrdenie menu: ENTER")
    menu_ako.riadok_pridaj("")
    menu_ako.riadok_pridaj(u"Máš 5 životov tabletu a 15 životov základne.")
    menu_ako.riadok_pridaj(u"Môžeš sa vylepšovať, ak nato máš peniaze.")
    menu_ako.riadok_pridaj(u"V bonusových úrovniach čakaj nečakané ;).")
    menu_ako.riadok_pridaj("")
    menu_ako.riadok_pridaj(u"Cieľ hry:")
    menu_ako.riadok_pridaj(u"Zničiť všetky noviny!")
    menu_ako.riadok_pridaj("")
    menu_ako.riadok_pridaj(u"Najvyššie skóre: " + str(HIGHSCORE[0]))

    menu_obchod = Menu_Obchod()
    menu_obchod.polozka_pridaj(u"Kúpiť")
    menu_obchod.polozka_pridaj(u"Pokračovať v hre")

    menu_pause = Menu()
    menu_pause.polozka_pridaj(u"Pokračovať v hre")
    menu_pause.polozka_pridaj(u"Hlavné menu")

    menu_prehra = Menu()
    menu_prehra.riadok_pridaj("PREHRAL SI!")
    menu_prehra.riadok_pridaj("")
    menu_prehra.riadok_pridaj("")
    menu_prehra.riadok_pridaj(u"Stlač ESC pre návrat do menu.")

    menu_vyhra = Menu()
    menu_vyhra.riadok_pridaj("VYHRAL SI!")
    menu_vyhra.riadok_pridaj(u"Porazil si všetky noviny!")
    menu_vyhra.riadok_pridaj(u"Snáď už natrvalo!")
    menu_vyhra.riadok_pridaj(u"Stlač ESC pre návrat do menu.")

    # Hlavná slučka
    while 1:
        # Počíta čas od spustenia hry
        cas = pygame.time.get_ticks()

        stlacena_klavesa = pygame.key.get_pressed()

        # Načítanie vstupu
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()        

        if stav == STAV_V_HRE:
            
            if stlacena_klavesa[K_LEFT]:
                smer = 0
            elif stlacena_klavesa[K_RIGHT]:
                smer = 1
            else:
                smer = 3

            if stlacena_klavesa[K_SPACE]:
                vystrelene = 1
            else:
                vystrelene = 0

            if stlacena_klavesa[K_ESCAPE] and cas > oneskorenie_enter:
                stav = STAV_MENU_PAUSE
                oneskorenie_enter = cas + 250

            if stlacena_klavesa[K_m]:
                skore_peniaze += 100
                skore_zivoty_zakladne += 1
                skore_zivoty += 1
               

            # Vystrelenie strely
            if vystrelene == 1 and cas > cas_strely:
                cas_strely = cas + ob_strelba_rychlost
                for p in range(0, ob_strela_pocet):
                  a, b, c, d = tablet_zoznam[0]
                  if p == 2:
                    strely.add(Strela((a+25-(1*20), b-29)))
                    break                  
                  strely.add(Strela((a+25+(p*20), b-29)))

                zvuk.strela_p()


            # Odstránenie všetkých objektov z obrazovky,
            # aby nedošlo k efektu, kedy objekty pri pohybe nechávajú
            # za sebou svojú vlastnú stopu
            tablet.clear(obrazovka, pozadie)
            noviny.clear(obrazovka, pozadie)
            noviny_ozbrojene.clear(obrazovka, pozadie)
            noviny_boss.clear(obrazovka, pozadie)
            noviny_bonus.clear(obrazovka, pozadie) 
            strely.clear(obrazovka, pozadie)
            strely_noviny.clear(obrazovka, pozadie)
            explozie.clear(obrazovka, pozadie)
            hranica.clear(obrazovka, pozadie)
            skore_bar.clear(obrazovka, pozadie)
            skore.clear(obrazovka, pozadie)


            # Aktualizácia všetkých objektov - zavolanie metód update v triedach
            tablet.update(smer, ob_tablet_rychlost)
            noviny.update(cas)
            noviny_ozbrojene.update(cas)
            noviny_boss.update(cas)
            noviny_bonus.update(cas)
            strely.update()
            strely_noviny.update()
            explozie.update(cas)
           

            # Detekcia kolízie objektov
            for i in pygame.sprite.groupcollide(noviny, strely, True, True):
                # a,b = x,y súradnice objektu, c,d = šírka a výška objektu
                a, b, c, d = i.rect
                # vytvorenie explózie a pripísanie skóre a peňazí
                explozie.add(Explozia((a-20, b-20)))
                skore_peniaze += 10
                skore_skore += 15
                # Spustenie zvuku explózie
                zvuk.explozia_p()

            for i in pygame.sprite.groupcollide(tablet, noviny, False, True):
                a, b, c, d = i.rect
                explozie.add(Explozia((a-20, b-20)))
                skore_zivoty -= 1
                zvuk.poskodenie_p()

            for i in pygame.sprite.groupcollide(noviny_ozbrojene, strely, True, True):
                a, b, c, d = i.rect
                explozie.add(Explozia((a-20, b-20)))
                skore_peniaze += 15
                skore_skore += 20
                zvuk.explozia_p()

            for i in pygame.sprite.groupcollide(tablet, noviny_ozbrojene, False, True):
                a, b, c, d = i.rect
                explozie.add(Explozia((a-20, b-20)))
                skore_zivoty -= 1
                zvuk.poskodenie_p()

            for i in pygame.sprite.groupcollide(tablet, strely_noviny, False, True):
                a, b, c, d = i.rect
                explozie.add(Explozia((a-20, b-20)))
                skore_zivoty -= 1
                zvuk.poskodenie_p()


            for i in pygame.sprite.groupcollide(hranica, noviny, False, True):
                skore_zivoty_zakladne -= 1
                
            for i in pygame.sprite.groupcollide(hranica, noviny_ozbrojene, False, True):
                skore_zivoty_zakladne -= 1

            for i in pygame.sprite.groupcollide(hranica, noviny_bonus, False, True):
                pass

            # Detekcia kolízie pre Boss-ov
            for i in pygame.sprite.groupcollide(noviny_boss, strely, False, True):
                a, b, c, d = i.rect
                explozie.add(Explozia((a+random.randrange(0,384), b+250)))
                boss_hp -= 1
                if boss_hp == 0:
                    skore_peniaze += 500
                    skore_skore += 1000
                    noviny_boss.empty()
                    
            # Detekcia kolízie v bonusovej úrovni
            if skore_uroven == 1 and skore_pod_uroven == 6:
                for i in pygame.sprite.groupcollide(tablet, noviny_bonus, False, True):
                    a, b, c, d = i.rect
                    explozie.add(Explozia((a-20, b-20)))
                    skore_peniaze += 10
                    zvuk.explozia_p()
                    
            if skore_uroven == 3 and skore_pod_uroven == 6:
                for i in pygame.sprite.groupcollide(noviny_bonus, strely, True, True):
                    a, b, c, d = i.rect
                    explozie.add(Explozia((a-20, b-20)))
                    skore_peniaze += 25
                    skore_skore += 30
                    zvuk.explozia_p()

            # Priradnie všetkých aktuálnych objektov do zoznamov
            tablet_zoznam = tablet.draw(obrazovka)
            noviny_zoznam = noviny.draw(obrazovka)
            noviny_ozbrojene_zoznam = noviny_ozbrojene.draw(obrazovka)
            noviny_boss_zoznam = noviny_boss.draw(obrazovka)
            noviny_bonus_zoznam = noviny_bonus.draw(obrazovka)     
            strely_zoznam = strely.draw(obrazovka)
            strely_noviny_zoznam = strely_noviny.draw(obrazovka)
            explozie_zoznam = explozie.draw(obrazovka)
            hranica_zoznam = hranica.draw(obrazovka)
            skore_bar_zoznam = skore_bar.draw(obrazovka)
            skore_zoznam = skore.draw(obrazovka)

            # Nastavovanie bar-u a skóre pri Boss úrovni
            if len(noviny_boss_zoznam) != 0:    
                skore.update(skore_zivoty, skore_uroven, skore_pod_uroven, boss_hp, skore_peniaze, skore_skore)
                skore_bar.update(1)
            else:
                skore.update(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore)
                skore_bar.update(0)

            # Streľba nepriateľov
            if len(noviny_ozbrojene_zoznam) != 0 and cas > cas_strely_noviny and len(strely_noviny_zoznam) < len(noviny_ozbrojene_zoznam):
                cas_strely_noviny = cas + 250
                a, b, c, d = noviny_ozbrojene_zoznam[random.randrange(0, len(noviny_ozbrojene_zoznam))]
                if b > 0:
                    strely_noviny.add(strela_noviny((a+20, b+50)))

            if len(noviny_boss_zoznam) != 0 and cas > cas_strely_noviny:
                cas_strely_noviny = cas + 350
                a, b, c, d = noviny_boss_zoznam[0]
                if b > 0:
                    e = [90, 135, 180, 225, 270]
                    strely_noviny.add(strela_noviny((a+random.choice(e), b+150)))
                

            # Spustenie novej "vlny", ak na obrazovke už nie sú žiadne noviny
            if len(noviny_zoznam) == 0 and len(noviny_ozbrojene_zoznam) == 0 and len(noviny_boss_zoznam) == 0 and len(noviny_bonus_zoznam) == 0:

                #herne pole je 5 x 4 
                #1,3,6 nestrielaju
                #2,4,5,7 strielaju

                # Generovanie úrovni hry zo súborov
                # a jej následné vykresľovanie
                # Jeden znak značí jedného nepriateľa
                
                # Generovanie 1. úrovne je rozdielne,
                # pretože pred ňou nemôže byť žiadne menu obchod
                if uroven_1:
                    f = file("urovne/1/uroven_1_1.txt")
                    l=f.readline()
                    y=0
                    while l!="":
                      for x in xrange(len(l)):
                          if l[x]=="1":
                              noviny.add(Noviny_1(x,y))
                          elif l[x]=="2":
                              noviny_ozbrojene.add(Noviny_2(x,y))
                          elif l[x]=="3":
                              noviny.add(Noviny_3(x,y))
                          elif l[x]=="4":
                              noviny_ozbrojene.add(Noviny_4(x,y))
                          elif l[x]=="5":
                              noviny_ozbrojene.add(Noviny_5(x,y))
                          elif l[x]=="6":
                              noviny.add(Noviny_6(x,y))
                          elif l[x]=="7":
                              noviny_ozbrojene.add(Noviny_7(x,y))                          
                          elif l[x]=="8":
                              noviny_bonus.add(Noviny_bonus_1(x,y))
                          elif l[x]=="9":
                              noviny_boss.add(Noviny_boss_12())
                              
                      l=f.readline()
                      y+=1
                    f.close()
                    uroven_1 = False
                   
                else:
                    menu_obchod.polozka_nastav(0)
                    index_obchod = 0
                    stav = STAV_MENU_OBCHOD             
                    skore_pod_uroven += 1

                    if skore_pod_uroven == 6 and skore_uroven == 2:
                        skore_uroven += 1
                        skore_pod_uroven = 1

                    if skore_pod_uroven == 8 and skore_uroven != 2:
                        skore_uroven += 1
                        skore_pod_uroven = 1
                        
                    level_name = "urovne/" + str(skore_uroven) + "/uroven_" + str(skore_uroven) + "_" + str(skore_pod_uroven)  + ".txt"
               
                    try:
                        skore_peniaze += 150
                        skore_skore += 500
                        f = file(level_name)
                        l=f.readline()
                        y=0
                        while l!="":
                          for x in xrange(len(l)):
                              if l[x]=="1":
                                  noviny.add(Noviny_1(x,y, skore_uroven))
                              elif l[x]=="2":
                                  noviny_ozbrojene.add(Noviny_2(x,y, skore_uroven))
                              elif l[x]=="3":
                                  noviny.add(Noviny_3(x,y, skore_uroven))
                              elif l[x]=="4":
                                  noviny_ozbrojene.add(Noviny_4(x,y, skore_uroven))
                              elif l[x]=="5":
                                  noviny_ozbrojene.add(Noviny_5(x,y, skore_uroven))
                              elif l[x]=="6":
                                  noviny.add(Noviny_6(x,y, skore_uroven))
                              elif l[x]=="7":
                                  noviny_ozbrojene.add(Noviny_7(x,y, skore_uroven))                          
                              elif l[x]=="8":
                                  noviny_bonus.add(Noviny_bonus_1(x,y))
                              elif l[x]=="9":
                                  noviny_boss.add(Noviny_boss_12(skore_uroven))
                              elif l[x]=="a":
                                  for x in range(0,69):
                                      noviny_bonus.add(Noviny_bonus_2())
                              elif l[x]=="b":
                                  boss_hp = 150
                                  noviny_boss.add(Noviny_boss_12(skore_uroven))
                                                                    
                          l=f.readline()
                          y+=1
                        f.close()
                        
                    # Ak hráč prejde všetke úrovne, vyhráva
                    except IOError:
                        stav = STAV_VYHRA       
                
            # Aktualizácia, čiže prevednie akejkoľvek zmeny na objekte
            # a vykreslenie všetkých objektov
            pygame.display.update(tablet_zoznam)
            pygame.display.update(noviny_zoznam)
            pygame.display.update(noviny_ozbrojene_zoznam)
            pygame.display.update(noviny_boss_zoznam)
            pygame.display.update(noviny_bonus_zoznam)
            pygame.display.update(strely_zoznam)
            pygame.display.update(strely_noviny_zoznam)
            pygame.display.update(explozie_zoznam)
            pygame.display.update(hranica_zoznam)
            pygame.display.update(skore_bar_zoznam)
            pygame.display.update(skore_zoznam)

            # Koniec hry, ak hráčovi dojdú životy tabletu alebo základni
            if skore_zivoty < 1 or skore_zivoty_zakladne < 1:
              stav = STAV_PREHRA
              Zvuky().explozia_p(1)
                
            # Zadefinovanie počtu snímkov za sekundu (FPS)
            hodiny.tick(60)
          
            
        elif stav == STAV_MENU_OBCHOD:

            obchod_pokracuj = True
            # Zapísanie najvyššieho skóre do súboru
            try:
                highscore = file("highscore.txt", "r")
                HIGHSCORE = highscore.readlines()
                highscore.close()
                if float(HIGHSCORE[0]) < skore_skore:
                    highscore = file("highscore.txt", "w")
                    highscore.write(str(skore_skore))
                    highscore.close()
            except (IOError, IndexError):
                highscore = file("highscore.txt", "w")
                highscore.write(str(0))
                highscore.close()
                
            # Prekreslenie obrazovky s obchod menu
            obrazovka.blit(Menu_Obchod.vykresli_obchod_menu(menu_obchod, index_obchod, cena, meno, extra),(0,0))

            skore_bar_zoznam = skore_bar.draw(obrazovka)
            skore_zoznam = skore.draw(obrazovka)
            pygame.display.update(skore_zoznam)
            strely = pygame.sprite.RenderUpdates()
            tablet = pygame.sprite.RenderUpdates()
            strely_noviny = pygame.sprite.RenderUpdates()
            explozie = pygame.sprite.RenderUpdates()
            tablet.add(Tablet())            

            # Zadefinovanie rôznych položiek obchodu
            if index_obchod == 0:
              cena = 300
              meno = u"Život tabletu"
              extra = ""
              
            elif index_obchod == 1:
              cena = 450
              meno = u"Rýchlejší tablet"
              extra = u"Aktuálna úroveň: %d" % ob_tablet_rychlost_lvl
              if ob_tablet_rychlost_lvl == 5:
                extra = u"Aktuálna úroveň: %d" % ob_tablet_rychlost_lvl + "(MAX)"
              
            elif index_obchod == 2:
              cena = 200
              meno = u"Život základne"
              extra = ""

            elif index_obchod == 3:
              cena = 350
              meno = u"Rýchlejšia Zbraň"
              extra = u"Aktuálna úroveň: %d" % ob_strelba_rychlost_lvl
              if ob_strelba_rychlost_lvl == 10:
                extra = u"Aktuálna úroveň: %d" % ob_strelba_rychlost_lvl + "(MAX)"                

            elif index_obchod == 4:
              cena = 950
              meno = u"Nová Zbraň"
              extra = u"Aktuálna úroveň: %d" % ob_strela_pocet
              if ob_strela_pocet == 3:
                extra = u"Aktuálna úroveň: %d" % ob_strela_pocet + "(MAX)"

            # Interakcia v menu
            if stlacena_klavesa[K_UP]:
                menu_obchod.kurzor_obchod()
                obchod = True
               
            if stlacena_klavesa[K_DOWN]:
                menu_obchod.kurzor_obchod_dole()
                obchod = False

            if stlacena_klavesa[K_LEFT] and cas > oneskorenie_sipky:
                
                if obchod:
                    oneskorenie_sipky = cas + 200
                    menu_obchod.kurzor_obchod_lavo()
                    if index_obchod != 0:
                        index_obchod -= 1
                else:
                    menu_obchod.kurzor_dolava()
                

            if stlacena_klavesa[K_RIGHT] and cas > oneskorenie_sipky:
                
                if obchod:
                     oneskorenie_sipky = cas + 200
                     menu_obchod.kurzor_obchod_pravo()
                     if index_obchod != 4:
                         index_obchod += 1
                else:
                    menu_obchod.kurzor_doprava()               

            # Nakupovanie rôznych položiek podľa indexov
            if stlacena_klavesa[K_RETURN] and cas > oneskorenie_enter:
                if menu_obchod.polozka_zisti() == 0:
                    if skore_peniaze >= cena:
                        if index_obchod == 0:
                            skore_zivoty += 1
                            skore_peniaze -= cena
                        elif index_obchod == 1 and ob_tablet_rychlost_lvl < 5:
                            ob_tablet_rychlost += 0.5
                            skore_peniaze -= cena
                            ob_tablet_rychlost_lvl += 1
                        elif index_obchod == 2:
                            skore_zivoty_zakladne += 1
                            skore_peniaze -= cena
                        elif index_obchod == 3 and ob_strelba_rychlost_lvl < 10:
                            ob_strelba_rychlost -= 7
                            skore_peniaze -= cena
                            ob_strelba_rychlost_lvl += 1
                        elif index_obchod == 4 and ob_strela_pocet < 3:
                            ob_strela_pocet += 1
                            skore_peniaze -= cena
                elif menu_obchod.polozka_zisti() == 1:
                    stav = STAV_V_HRE
                    obchod_pokracuj = False
                    obrazovka.blit(pozadie, (0, 0))
                    pygame.display.update()
                    zvuk.boj_pokrik_p()
                oneskorenie_enter = cas + 200
            if stlacena_klavesa[K_ESCAPE] and cas > oneskorenie_enter:
                oneskorenie_enter = cas + 200
                stav = STAV_MENU_HLAVNE
            if stlacena_klavesa[K_m]:
                skore_peniaze += 100
                skore_zivoty_zakladne += 1
                skore_zivoty += 1
                
            skore.update(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore)

        # Hlavné menu hry, spúštané pri spustení hry    
        elif stav == STAV_MENU_HLAVNE:
            obrazovka.blit(Menu.vykresli_menu(menu_hlavne),(0,0))
            
            if stlacena_klavesa[K_UP] and cas > oneskorenie_sipky:
                menu_hlavne.kurzor_hore()
                oneskorenie_sipky = cas + 250
               
            if stlacena_klavesa[K_DOWN] and cas > oneskorenie_sipky:
                menu_hlavne.kurzor_dole()
                oneskorenie_sipky= cas + 250
                
            # Pri spúštaní novej hry, sú všetké dôležité premenné resetované
            if stlacena_klavesa[K_RETURN] and cas > oneskorenie_enter:
                if menu_hlavne.polozka_zisti() == 0:
                    stav = STAV_V_HRE
                    obchod_pokracuj = False

                    skore_zivoty = 5
                    skore_peniaze = 0
                    skore_zivoty_zakladne = 15
                    skore_uroven = 1
                    skore_pod_uroven = 1
                    skore_skore = 0
                    uroven_1 = True

                    ob_tablet_rychlost = 9.0
                    ob_tablet_rychlost_lvl = 1
                    ob_strelba_rychlost = 300
                    ob_strelba_rychlost_lvl = 1
                    ob_strela_pocet = 1
                    
                    noviny = pygame.sprite.RenderUpdates()
                    noviny_ozbrojene = pygame.sprite.RenderUpdates()
                    noviny_boss = pygame.sprite.RenderUpdates()
                    noviny_bonus = pygame.sprite.RenderUpdates()
                    skore = pygame.sprite.RenderUpdates()
                    skore.add(Skore(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore))
                    tablet = pygame.sprite.RenderUpdates()
                    tablet.add(Tablet())
                    strely = pygame.sprite.RenderUpdates()
                    explozie = pygame.sprite.RenderUpdates()                    
                    strely_noviny = pygame.sprite.RenderUpdates()
                    
                    obrazovka.blit(pozadie, (0, 0))
                    pygame.display.update()
                    zvuk.boj_pokrik_p()                    
                elif menu_hlavne.polozka_zisti() == 1:
                    if obchod_pokracuj:
                        stav = STAV_MENU_OBCHOD
                    else:
                        stav = STAV_V_HRE
                        obrazovka.blit(pozadie, (0, 0))
                        pygame.display.update()
                elif menu_hlavne.polozka_zisti() == 2:
                    stav = STAV_MENU_AKO
                elif menu_hlavne.polozka_zisti() == 3:
                    pygame.quit()
                    sys.exit()
                oneskorenie_enter = cas + 200
            
                
        # Rôzne menšie stavy hry ako je menu ako hrat, pozitívny alebo negatívny koniec hry a pauza        
        elif stav == STAV_MENU_AKO:
            if stlacena_klavesa[K_RETURN]  and cas > oneskorenie_enter:
              stav = STAV_MENU_HLAVNE
              oneskorenie_enter = cas + 200

            obrazovka.blit(Menu.vykresli_menu(menu_ako),(0,0))

        elif stav == STAV_MENU_PAUSE:

            obrazovka.blit(Menu.vykresli_popup_menu(menu_pause, obrazovka),(0,0))

            if stlacena_klavesa[K_LEFT]:
                menu_pause.kurzor_dolava()

            if stlacena_klavesa[K_RIGHT]:
                menu_pause.kurzor_doprava()

            if stlacena_klavesa[K_RETURN] and cas > oneskorenie_enter:
                if menu_pause.polozka_zisti() == 0:
                    stav = STAV_V_HRE
                    obchod_pokracuj = False
                    obrazovka.blit(pozadie, (0, 0))
                    pygame.display.update()
                elif menu_pause.polozka_zisti() == 1:
                    stav = STAV_MENU_HLAVNE
                oneskorenie_enter = cas + 200

            elif stlacena_klavesa[K_ESCAPE] and cas > oneskorenie_enter:
              stav = STAV_V_HRE
              obchod_pokracuj = False
              obrazovka.blit(pozadie, (0, 0))
              pygame.display.update()
              oneskorenie_enter = cas + 250
              
        elif stav == STAV_VYHRA:
            obrazovka.blit(Menu.vykresli_koniec(menu_vyhra, obrazovka),(0,0))
            pygame.display.update()

            if stlacena_klavesa[K_ESCAPE]  and cas > oneskorenie_enter:
              stav = STAV_MENU_HLAVNE
              oneskorenie_enter = cas + 200

        elif stav == STAV_PREHRA:            
            obrazovka.blit(Menu.vykresli_koniec(menu_prehra, obrazovka),(0,0))
            pygame.display.update()

            if stlacena_klavesa[K_ESCAPE]  and cas > oneskorenie_enter:
                stav = STAV_MENU_HLAVNE
                oneskorenie_enter = cas + 200              


# Zavolanie hlavnej funkcie ak je spustený tento skript
if __name__ == '__main__':
    main()
