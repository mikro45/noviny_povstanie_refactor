#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

import konstanty as kon

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
        menu = pygame.Surface((kon.VELKOST_OKNA_X, kon.VELKOST_OKNA_Y))
        menu.blit(self.pozadie, (0, 0))
                
        polozka_pocet = 0
        # Vykreslenie vsetkch poloziek
        while polozka_pocet < len(self.polozky):
          suradnica_x = kon.VELKOST_OKNA_X / 11 
          suradnica_y = kon.VELKOST_OKNA_Y / 11 * polozka_pocet + kon.VELKOST_OKNA_Y / 10
          text = self.font_polozky.render(self.polozky[polozka_pocet], 1, self.farba_biela)
          pygame.draw.rect(menu, self.farba_tlacidlo_neaktivne, (suradnica_x - 10, suradnica_y, self.tlacidlo_sirka, self.tlacidlo_vyska))
          menu.blit(text, (suradnica_x, suradnica_y))
          # Vykreslenie vybratej - aktivnej polozky
          if polozka_pocet == self.vybrata_polozka:
            pygame.draw.rect(menu, self.farba_tlacidlo_aktivne, (suradnica_x - 10, suradnica_y, self.tlacidlo_sirka, self.tlacidlo_vyska))
            menu.blit(text, (suradnica_x, suradnica_y))

          polozka_pocet += 1

        polozka_pocet = 0

        # Vykreslenie všetkých riadkov - textu
        while polozka_pocet < len(self.riadky):
          suradnica_x = kon.VELKOST_OKNA_X / 11 
          suradnica_y = kon.VELKOST_OKNA_Y / 16 * polozka_pocet + kon.VELKOST_OKNA_Y / 5          
          text = self.font_riadky.render(self.riadky[polozka_pocet], 1, self.farba_cierna)
          menu.blit(text,(suradnica_x, suradnica_y))
          polozka_pocet += 1

        menu.blit(self.font_noviny_povstanie.render("Noviny - Povstanie", 1, self.farba_biela),(400, 50))
        pygame.display.update()
        return menu
    
    # Vykreslí menu, ktoré prekryje aktuálnu obrazovku s menu bez pozadia
    def vykresli_popup_menu(self, obrazovka):
        polozka_pocet = 0

        while polozka_pocet < len(self.polozky):
          suradnica_x = kon.VELKOST_OKNA_X / 3.5 * polozka_pocet + kon.VELKOST_OKNA_X / 3.5
          suradnica_y = kon.VELKOST_OKNA_Y / 2

          text = self.font_polozky.render(self.polozky[polozka_pocet], 1, self.farba_biela)
          rect = pygame.draw.rect(obrazovka, self.farba_tlacidlo_neaktivne, (suradnica_x - 10, suradnica_y, self.tlacidlo_sirka, self.tlacidlo_vyska))
          obrazovka.blit(text, (suradnica_x, suradnica_y)) 

          if polozka_pocet == self.vybrata_polozka:
            rect = pygame.draw.rect(obrazovka, self.farba_tlacidlo_aktivne, (suradnica_x - 10, suradnica_y, self.tlacidlo_sirka, self.tlacidlo_vyska))
            obrazovka.blit(text, (suradnica_x, suradnica_y))  

          polozka_pocet += 1      

        pygame.display.update()
        return obrazovka

    # Vykreslí koniec hry - text
    def vykresli_koniec(self, obrazovka):
        polozka_pocet = 0

        while polozka_pocet < len(self.riadky):
          suradnica_x = kon.VELKOST_OKNA_X / 5
          suradnica_y = kon.VELKOST_OKNA_Y / 5 * polozka_pocet + 100
          text = self.font_velky.render(self.riadky[polozka_pocet], 1, self.farba_cierna)
          if polozka_pocet > 0:
            text = self.font_stredny.render(self.riadky[polozka_pocet], 1, self.farba_biela)
          rect = text.get_rect()
          rect.centerx = kon.VELKOST_OKNA_X / 2
          rect.suradnica_y = suradnica_y
          obrazovka.blit(text, rect)
         
          polozka_pocet += 1
          
        pygame.display.update()
        return obrazovka

class MenuObchod(Menu):
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

        # Boolean pre určenie čpolozka_pocet hráč bude pohybovať v náhľade alebo medzi tlačidlami
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
        menu = pygame.Surface((kon.VELKOST_OKNA_X, kon.VELKOST_OKNA_Y))
        menu.blit(self.pozadie, (0, 0))

        polozka_pocet = 0

        # Zadefinovanie rozmerov a suradnic vsetkych objektov v obchode
        # pre pripadne buduce zmene a pre ropoznanie
        ramcek_12_hrubka = 4
        ramcek_1 = [387, 125, 250]
        ramcek_2 = [170, 404, 684, 244]
        ramcek_3 = [402, 43, 220, 60]

        sipka_1 = [ramcek_1[0] - 107, 205]
        sipka_2 = [ramcek_1[0] + ramcek_1[2] + 60, 205]

        ramcek_1_obrazok = [ramcek_1[0] + 3, ramcek_1[1] + 3]

        text_nadpis = [418, 35]
        text_popis = [195, 410]

        # Zadefinovanie pouzitych farieb
        farba_ramcek = (0, 64, 64)
        farba_ramcek_vnutri = (255, 255, 224)
        farba_ramcek_aktivna = (0, 192, 0)
        farba_popis = (0, 192, 255)
        farba_nadpis = (0, 128, 255)
               

        
        while polozka_pocet < len(self.polozky):
            suradnica_x = kon.VELKOST_OKNA_X / 3.3 * polozka_pocet + kon.VELKOST_OKNA_X / 4
            suradnica_y = 670

            text = self.font_polozky.render(self.polozky[polozka_pocet], 1, self.farba_biela)
            rect = pygame.draw.rect(menu, self.farba_tlacidlo_neaktivne, (suradnica_x - 10, suradnica_y, self.tlacidlo_sirka, self.tlacidlo_vyska))
            menu.blit(text, (suradnica_x, suradnica_y))        

            if polozka_pocet == self.vybrata_polozka:
                rect = pygame.draw.rect(menu, self.farba_tlacidlo_aktivne, (suradnica_x - 10, suradnica_y, self.tlacidlo_sirka, self.tlacidlo_vyska))
                menu.blit(text, (suradnica_x, suradnica_y))          

            polozka_pocet += 1
        
        # Vykreslenie ramcekov
        rect = pygame.draw.rect(menu, farba_ramcek, (ramcek_1[0], ramcek_1[1], ramcek_1[2], ramcek_1[2]), ramcek_12_hrubka)
        rect = pygame.draw.rect(menu, farba_ramcek_vnutri, (ramcek_1[0] + 3, ramcek_1[1] + 3, ramcek_1[2] - 5, ramcek_1[2] -5))        
            
        rect = pygame.draw.rect(menu, farba_ramcek, (ramcek_2[0], ramcek_2[1], ramcek_2[2], ramcek_2[3]), ramcek_12_hrubka)
        rect = pygame.draw.rect(menu, farba_ramcek_vnutri, (ramcek_2[0] + 3, ramcek_2[1] + 3, ramcek_2[2] - 5, ramcek_2[3] - 5))

        rect = pygame.draw.rect(menu, farba_ramcek, (ramcek_3[0], ramcek_3[1], ramcek_3[2], ramcek_3[3]), ramcek_12_hrubka)
        rect = pygame.draw.rect(menu, farba_ramcek_vnutri, (ramcek_3[0] + 3, ramcek_3[1] + 3, ramcek_3[2] - 5, ramcek_3[3] - 5))

        menu.blit(self.sipka_l0, (sipka_1[0], sipka_1[1]))
        menu.blit(self.sipka_p0, (sipka_2[0], sipka_2[1]))               
        

        if self.obchod:
            rect = pygame.draw.rect(menu, farba_ramcek_aktivna, (ramcek_1[0], ramcek_1[1], ramcek_1[2], ramcek_1[2]), ramcek_12_hrubka)
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

        menu.blit(self.font_stredny.render(u"Obchod", 1, farba_nadpis), (text_nadpis[0], text_nadpis[1]))
        
        # Vykresľovanie popisu pre rôzne položky obchodu      
        menu.blit(self.font_stredny.render(meno, 1, farba_popis), (text_popis[0], text_popis[1]))
        menu.blit(self.font_stredny.render("CENA = %d" % cena, 1, farba_popis), (text_popis[0], text_popis[1] + 72))
        menu.blit(self.font_stredny.render(u"%s" % extra, 1, farba_popis), (text_popis[0], text_popis[1] + 72 * 2))

        pygame.display.update()  
        return menu

