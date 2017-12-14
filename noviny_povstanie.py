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

# Globálne konštanty
import konstanty as kon

# Importovanie tried z modulov
import skore
import noviny
import noviny_bonus as n_bonus
import noviny_boss as n_boss
import tablet
import strela
import grafika
import zvuky
import menu

# Definovanie tried
# Každá trieda osbsahuje povinné premenné self.image a self.rect
# kvôli tomu, aby metóda Sprite mala čo, self.image(obrázok), a kam, self.rect(súradnice), vykresľovať


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
    STAV_MENU_PAUZA = 6


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
    cas_objekt_strela = 0
    cas_objekt_strela_noviny = 0
    # Premenné slúžiace na umiernený pohyb v menu medzi položkami
    oneskorenie_enter = 0
    oneskorenie_sipky = 0

    # Premenné určujúce základné hodnoty obchodu
    obchod_tablet_rychlost = 9.0
    obchod_tablet_rychlost_lvl = 1
    obchod_strelba_rychlost = 300
    obchod_strelba_rychlost_lvl = 1
    obchod_strela_pocet = 1

    # Pomocné premenné pre obchod
    obchod_index = 0
    obchod_cena = 0
    obchod_meno = ""
    obchod_extra = ""
    obchod = False
    obchod_pokracuj = False

    # Premenná určujúca počiatočný počet životov Boss-ov
    noviny_boss_hp = 100

    # Načítanie skóre zo súbora
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
    obrazovka = pygame.display.set_mode((kon.VELKOST_OKNA_X, kon.VELKOST_OKNA_Y))#, pygame.FULLSCREEN
    pozadie = pygame.image.load('obrazky/pozadia/pozadie1.bmp').convert()

    # Prispôsobenie herného okna
    pygame.display.set_caption('Noviny - Povstanie')
    pygame.mouse.set_visible(1)
    ikona = pygame.image.load("ikona.ico")
    pygame.display.set_icon(ikona)

    # Vytvorenie skupín objektov a pridanie niektorých objektov do skupín
    objekt_noviny = pygame.sprite.RenderUpdates()
    objekt_noviny_ozbrojene = pygame.sprite.RenderUpdates()
    objekt_noviny_boss = pygame.sprite.RenderUpdates()
    objekt_noviny_bonus = pygame.sprite.RenderUpdates()

    objekt_skore = pygame.sprite.RenderUpdates()
    objekt_skore.add(skore.Skore(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore))

    objekt_tablet = pygame.sprite.RenderUpdates()
    objekt_tablet.add(tablet.Tablet())
    
    objekt_strela = pygame.sprite.RenderUpdates()

    objekt_explozia = pygame.sprite.RenderUpdates()
    
    objekt_strela_noviny = pygame.sprite.RenderUpdates()

    objekt_hranica = pygame.sprite.RenderUpdates()
    objekt_hranica.add(grafika.Hranica())

    objekt_skore_bar = pygame.sprite.RenderUpdates()
    objekt_skore_bar.add(skore.SkoreBar())
    
    # Načítanie triedy Zvuky
    objekt_zvuky = zvuky.Zvuky()

    # Zadefinovanie všetkych položiek všetkých menu
    menu_hlavne = menu.Menu()
    menu_hlavne.polozka_pridaj(u"Nová Hra")
    menu_hlavne.polozka_pridaj(u"Pokračovať v hre")
    menu_hlavne.polozka_pridaj(u"Ako Hrať")
    menu_hlavne.polozka_pridaj("Koniec")

    menu_ako = menu.Menu()
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
    menu_ako.riadok_pridaj(u"Zničiť všetky objekt_noviny!")
    menu_ako.riadok_pridaj("")
    menu_ako.riadok_pridaj(u"Najvyššie skóre: " + str(HIGHSCORE[0]))

    menu_obchod = menu.MenuObchod()
    menu_obchod.polozka_pridaj(u"Kúpiť")
    menu_obchod.polozka_pridaj(u"Pokračovať v hre")

    menu_pauza = menu.Menu()
    menu_pauza.polozka_pridaj(u"Pokračovať v hre")
    menu_pauza.polozka_pridaj(u"Hlavné menu")

    menu_prehra = menu.Menu()
    menu_prehra.riadok_pridaj("PREHRAL SI!")
    menu_prehra.riadok_pridaj("")
    menu_prehra.riadok_pridaj("")
    menu_prehra.riadok_pridaj(u"Stlač ESC pre návrat do menu.")

    menu_vyhra = menu.Menu()
    menu_vyhra.riadok_pridaj("VYHRAL SI!")
    menu_vyhra.riadok_pridaj(u"Porazil si všetky objekt_noviny!")
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
                stav = STAV_MENU_PAUZA
                oneskorenie_enter = cas + 250

            if stlacena_klavesa[K_m]:
                skore_peniaze += 100
                skore_zivoty_zakladne += 1
                skore_zivoty += 1
               

            # Vystrelenie objekt_strela
            if vystrelene == 1 and cas > cas_objekt_strela:
                cas_objekt_strela = cas + obchod_strelba_rychlost
                for pocet_strel in range(0, obchod_strela_pocet):
                  suradnica_x, suradnica_y, rozmer_a, rozmer_b = zoznam_tablet[0]
                  if pocet_strel == 2:
                    objekt_strela.add(strela.Strela((suradnica_x + 25 - (1 * 20), suradnica_y - 29)))
                    break                  
                  objekt_strela.add(strela.Strela((suradnica_x + 25 + (pocet_strel * 20), suradnica_y - 29)))

                objekt_zvuky.strela_p()


            # Odstránenie všetkých objektov z obrazovky,
            # aby nedošlo k efektu, kedy objekty pri pohybe nechávajú
            # za sebou svojú vlastnú stopu
            objekt_tablet.clear(obrazovka, pozadie)
            objekt_noviny.clear(obrazovka, pozadie)
            objekt_noviny_ozbrojene.clear(obrazovka, pozadie)
            objekt_noviny_boss.clear(obrazovka, pozadie)
            objekt_noviny_bonus.clear(obrazovka, pozadie) 
            objekt_strela.clear(obrazovka, pozadie)
            objekt_strela_noviny.clear(obrazovka, pozadie)
            objekt_explozia.clear(obrazovka, pozadie)
            objekt_hranica.clear(obrazovka, pozadie)
            objekt_skore_bar.clear(obrazovka, pozadie)
            objekt_skore.clear(obrazovka, pozadie)


            # Aktualizácia všetkých objektov - zavolanie metód update v triedach
            objekt_tablet.update(smer, obchod_tablet_rychlost)
            objekt_noviny.update(cas)
            objekt_noviny_ozbrojene.update(cas)
            objekt_noviny_boss.update(cas)
            objekt_noviny_bonus.update(cas)
            objekt_strela.update()
            objekt_strela_noviny.update()
            objekt_explozia.update(cas)
           

            # Detekcia kolízie objektov
            for objekt in pygame.sprite.groupcollide(objekt_noviny, objekt_strela, True, True):
                # a,b = suradnica_x,suradnica_y súradnice objektu, c,d = šírka a výška objektu
                suradnica_x, suradnica_y, rozmer_a, rozmer_b = objekt.rect
                # vytvorenie explózie a pripísanie skóre a peňazí
                objekt_explozia.add(grafika.Explozia((suradnica_x - 20, suradnica_y - 20)))
                skore_peniaze += 10
                skore_skore += 15
                # Spustenie zvuku explózie
                objekt_zvuky.explozia_p()

            for objekt in pygame.sprite.groupcollide(objekt_tablet, objekt_noviny, False, True):
                suradnica_x, suradnica_y, rozmer_a, rozmer_b = objekt.rect
                objekt_explozia.add(grafika.Explozia((suradnica_x - 20, suradnica_y - 20)))
                skore_zivoty -= 1
                objekt_zvuky.poskodenie_p()

            for objekt in pygame.sprite.groupcollide(objekt_noviny_ozbrojene, objekt_strela, True, True):
                suradnica_x, suradnica_y, rozmer_a, rozmer_b = objekt.rect
                objekt_explozia.add(grafika.Explozia((suradnica_x - 20, suradnica_y - 20)))
                skore_peniaze += 15
                skore_skore += 20
                objekt_zvuky.explozia_p()

            for objekt in pygame.sprite.groupcollide(objekt_tablet, objekt_noviny_ozbrojene, False, True):
                suradnica_x, suradnica_y, rozmer_a, rozmer_b = objekt.rect
                objekt_explozia.add(grafika.Explozia((suradnica_x - 20, suradnica_y - 20)))
                skore_zivoty -= 1
                objekt_zvuky.poskodenie_p()

            for objekt in pygame.sprite.groupcollide(objekt_tablet, objekt_strela_noviny, False, True):
                suradnica_x, suradnica_y, rozmer_a, rozmer_b = objekt.rect
                objekt_explozia.add(grafika.Explozia((suradnica_x - 20, suradnica_y - 20)))
                skore_zivoty -= 1
                objekt_zvuky.poskodenie_p()


            for objekt in pygame.sprite.groupcollide(objekt_hranica, objekt_noviny, False, True):
                skore_zivoty_zakladne -= 1
                
            for objekt in pygame.sprite.groupcollide(objekt_hranica, objekt_noviny_ozbrojene, False, True):
                skore_zivoty_zakladne -= 1

            for objekt in pygame.sprite.groupcollide(objekt_hranica, objekt_noviny_bonus, False, True):
                pass

            # Detekcia kolízie pre Boss-ov
            for objekt in pygame.sprite.groupcollide(objekt_noviny_boss, objekt_strela, False, True):
                suradnica_x, suradnica_y, rozmer_a, rozmer_b = objekt.rect
                objekt_explozia.add(grafika.Explozia((suradnica_x + random.randrange(0, 384), suradnica_y + 250)))
                noviny_boss_hp -= 1
                if noviny_boss_hp == 0:
                    skore_peniaze += 500
                    skore_skore += 1000
                    objekt_noviny_boss.empty()
                    
            # Detekcia kolízie v bonusovej úrovni
            if skore_uroven == 1 and skore_pod_uroven == 6:
                for objekt in pygame.sprite.groupcollide(objekt_tablet, objekt_noviny_bonus, False, True):
                    suradnica_x, suradnica_y, rozmer_a, rozmer_b = objekt.rect
                    objekt_explozia.add(grafika.Explozia((suradnica_x - 20, suradnica_y - 20)))
                    skore_peniaze += 10
                    objekt_zvuky.explozia_p()
                    
            if skore_uroven == 3 and skore_pod_uroven == 6:
                for objekt in pygame.sprite.groupcollide(objekt_noviny_bonus, objekt_strela, True, True):
                    suradnica_x, suradnica_y, rozmer_a, rozmer_b = objekt.rect
                    objekt_explozia.add(grafika.Explozia((suradnica_x - 20, suradnica_y - 20)))
                    skore_peniaze += 25
                    skore_skore += 30
                    objekt_zvuky.explozia_p()

            # Priradnie všetkých aktuálnych objektov do zoznamov
            zoznam_tablet = objekt_tablet.draw(obrazovka)
            zoznam_noviny = objekt_noviny.draw(obrazovka)
            zoznam_noviny_ozbrojene = objekt_noviny_ozbrojene.draw(obrazovka)
            zoznam_noviny_boss = objekt_noviny_boss.draw(obrazovka)
            zoznam_noviny_bonus = objekt_noviny_bonus.draw(obrazovka)     
            zoznam_strela = objekt_strela.draw(obrazovka)
            zoznam_strela_noviny = objekt_strela_noviny.draw(obrazovka)
            zoznam_explozia = objekt_explozia.draw(obrazovka)
            zoznam_hranica = objekt_hranica.draw(obrazovka)
            zoznam_skore_bar = objekt_skore_bar.draw(obrazovka)
            zoznam_skore = objekt_skore.draw(obrazovka)

            # Nastavovanie bar-u a skóre pri Boss úrovni
            if len(zoznam_noviny_boss) != 0:    
                objekt_skore.update(skore_zivoty, skore_uroven, skore_pod_uroven, noviny_boss_hp, skore_peniaze, skore_skore)
                objekt_skore_bar.update(1)
            else:
                objekt_skore.update(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore)
                objekt_skore_bar.update(0)

            # Streľba nepriateľov
            if len(zoznam_noviny_ozbrojene) != 0 and cas > cas_objekt_strela_noviny and len(zoznam_strela_noviny) < len(zoznam_noviny_ozbrojene):
                cas_objekt_strela_noviny = cas + 250
                suradnica_x, suradnica_y, rozmer_a, rozmer_b = zoznam_noviny_ozbrojene[random.randrange(0, len(zoznam_noviny_ozbrojene))]
                if suradnica_y > 0:
                    objekt_strela_noviny.add(strela.StrelaNoviny((a+20, b+50)))

            if len(zoznam_noviny_boss) != 0 and cas > cas_objekt_strela_noviny:
                cas_objekt_strela_noviny = cas + 350
                suradnica_x, suradnica_y, rozmer_a, rozmer_b = zoznam_noviny_boss[0]
                if suradnica_y > 0:
                    pozicie_strelby = [90, 135, 180, 225, 270]
                    objekt_strela_noviny.add(strela.StrelaNoviny((suradnica_x + random.choice(pozicie_strelby), suradnica_y + 150)))
                

            # Spustenie novej "vlny", ak na obrazovke už nie sú žiadne objekt_noviny
            if len(zoznam_noviny) == 0 and len(zoznam_noviny_ozbrojene) == 0 and len(zoznam_noviny_boss) == 0 and len(zoznam_noviny_bonus) == 0:

                #herne pole je 5 suradnica_x 4 
                #1,3,6 nestrielaju
                #2,4,5,7 strielaju

                # Generovanie úrovni hry zo súborov
                # a jej následné vykresľovanie
                # Jeden znak značí jedného nepriateľa
                
                # Generovanie 1. úrovne je rozdielne,
                # pretože pred ňou nemôže byť žiadne menu obchod
                if uroven_1:
                    uroven_subor = file("urovne/1/uroven_1_1.txt")
                    pamat = uroven_subor.readline()
                    suradnica_y = 0
                    while pamat != "":
                      for suradnica_x in xrange(len(pamat)):
                          if pamat[suradnica_x] == "1":
                              objekt_noviny.add(noviny.Noviny1(suradnica_x, suradnica_y))
                          elif pamat[suradnica_x] == "2":
                              objekt_noviny_ozbrojene.add(noviny.Noviny2(suradnica_x, suradnica_y))
                          elif pamat[suradnica_x] == "3":
                              objekt_noviny.add(noviny.Noviny3(suradnica_x, suradnica_y))
                          elif pamat[suradnica_x] == "4":
                              objekt_noviny_ozbrojene.add(noviny.Noviny4(suradnica_x, suradnica_y))
                          elif pamat[suradnica_x] == "5":
                              objekt_noviny_ozbrojene.add(noviny.Noviny5(suradnica_x, suradnica_y))
                          elif pamat[suradnica_x] == "6":
                              objekt_noviny.add(noviny.Noviny6(suradnica_x, suradnica_y))
                          elif pamat[suradnica_x] == "7":
                              objekt_noviny_ozbrojene.add(noviny.Noviny7(suradnica_x, suradnica_y))                          
                          elif pamat[suradnica_x] == "8":
                              objekt_noviny_bonus.add(n_bonus.NovinyBonus1(suradnica_x, suradnica_y))
                          elif pamat[suradnica_x] == "9":
                              objekt_noviny_boss.add(n_boss.NovinyBoss12())
                              
                      pamat = uroven_subor.readline()
                      suradnica_y += 1
                    uroven_subor.close()
                    uroven_1 = False
                   
                else:
                    menu_obchod.polozka_nastav(0)
                    obchod_index = 0
                    stav = STAV_MENU_OBCHOD             
                    skore_pod_uroven += 1

                    if skore_pod_uroven == 6 and skore_uroven == 2:
                        skore_uroven += 1
                        skore_pod_uroven = 1

                    if skore_pod_uroven == 8 and skore_uroven != 2:
                        skore_uroven += 1
                        skore_pod_uroven = 1
                        
                    uroven_cesta = "urovne/" + str(skore_uroven) + "/uroven_" + str(skore_uroven) + "_" + str(skore_pod_uroven)  + ".txt"
               
                    try:
                        skore_peniaze += 150
                        skore_skore += 500
                        uroven_subor = file(uroven_cesta)
                        pamat = uroven_subor.readline()
                        suradnica_y = 0
                        while pamat!="":
                          for suradnica_x in xrange(len(pamat)):
                              if pamat[suradnica_x] == "1":
                                  objekt_noviny.add(noviny.Noviny1(suradnica_x, suradnica_y, skore_uroven))
                              elif pamat[suradnica_x] == "2":
                                  objekt_noviny_ozbrojene.add(noviny.Noviny2(suradnica_x, suradnica_y, skore_uroven))
                              elif pamat[suradnica_x] == "3":
                                  objekt_noviny.add(noviny.Noviny3(suradnica_x, suradnica_y, skore_uroven))
                              elif pamat[suradnica_x] == "4":
                                  objekt_noviny_ozbrojene.add(noviny.Noviny4(suradnica_x, suradnica_y, skore_uroven))
                              elif pamat[suradnica_x] == "5":
                                  objekt_noviny_ozbrojene.add(noviny.Noviny5(suradnica_x, suradnica_y, skore_uroven))
                              elif pamat[suradnica_x] == "6":
                                  objekt_noviny.add(noviny.Noviny6(suradnica_x, suradnica_y, skore_uroven))
                              elif pamat[suradnica_x] == "7":
                                  objekt_noviny_ozbrojene.add(noviny.Noviny7(suradnica_x, suradnica_y, skore_uroven))                          
                              elif pamat[suradnica_x] == "8":
                                  objekt_noviny_bonus.add(n_bonus.NovinyBonus1(suradnica_x, suradnica_y))
                              elif pamat[suradnica_x] == "9":
                                  objekt_noviny_boss.add(n_boss.NovinyBoss12(skore_uroven))
                              elif pamat[suradnica_x] == "a":
                                  for suradnica_x in range(0,69):
                                      objekt_noviny_bonus.add(n_bonus.NovinyBonus2())
                              elif pamat[suradnica_x] == "b":
                                  noviny_boss_hp = 150
                                  objekt_noviny_boss.add(n_boss.NovinyBoss12(skore_uroven))
                                                                    
                          pamat = uroven_subor.readline()
                          suradnica_y += 1
                        uroven_subor.close()
                        
                    # Ak hráč prejde všetke úrovne, vyhráva
                    except IOError:
                        stav = STAV_VYHRA       
                
            # Aktualizácia, čiže prevednie akejkoľvek zmeny na objekte
            # a vykreslenie všetkých objektov
            pygame.display.update(zoznam_tablet)
            pygame.display.update(zoznam_noviny)
            pygame.display.update(zoznam_noviny_ozbrojene)
            pygame.display.update(zoznam_noviny_boss)
            pygame.display.update(zoznam_noviny_bonus)
            pygame.display.update(zoznam_strela)
            pygame.display.update(zoznam_strela_noviny)
            pygame.display.update(zoznam_explozia)
            pygame.display.update(zoznam_hranica)
            pygame.display.update(zoznam_skore_bar)
            pygame.display.update(zoznam_skore)

            # Koniec hry, ak hráčovi dojdú životy tabletu alebo základni
            if skore_zivoty < 1 or skore_zivoty_zakladne < 1:
              stav = STAV_PREHRA
              zvuky.Zvuky().explozia_p(1)
                
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
            obrazovka.blit(menu.MenuObchod.vykresli_obchod_menu(menu_obchod, obchod_index, obchod_cena, obchod_meno, obchod_extra), (0, 0))

            zoznam_skore_bar = objekt_skore_bar.draw(obrazovka)
            zoznam_skore = objekt_skore.draw(obrazovka)
            
            pygame.display.update(zoznam_skore)
            
            objekt_strela = pygame.sprite.RenderUpdates()
            objekt_tablet = pygame.sprite.RenderUpdates()
            objekt_strela_noviny = pygame.sprite.RenderUpdates()
            objekt_explozia = pygame.sprite.RenderUpdates()
            
            objekt_tablet.add(tablet.Tablet())            

            # Zadefinovanie rôznych položiek obchodu
            if obchod_index == 0:
              obchod_cena = 300
              obchod_meno = u"Život tabletu"
              obchod_extra = ""
              
            elif obchod_index == 1:
              obchod_cena = 450
              obchod_meno = u"Rýchlejší tablet"
              obchod_extra = u"Aktuálna úroveň: %d" % obchod_tablet_rychlost_lvl
              if obchod_tablet_rychlost_lvl == 5:
                obchod_extra = u"Aktuálna úroveň: %d" % obchod_tablet_rychlost_lvl + "(MAX)"
              
            elif obchod_index == 2:
              obchod_cena = 200
              obchod_meno = u"Život základne"
              obchod_extra = ""

            elif obchod_index == 3:
              obchod_cena = 350
              obchod_meno = u"Rýchlejšia Zbraň"
              obchod_extra = u"Aktuálna úroveň: %d" % obchod_strelba_rychlost_lvl
              if obchod_strelba_rychlost_lvl == 10:
                obchod_extra = u"Aktuálna úroveň: %d" % obchod_strelba_rychlost_lvl + "(MAX)"                

            elif obchod_index == 4:
              obchod_cena = 950
              obchod_meno = u"Nová Zbraň"
              obchod_extra = u"Aktuálna úroveň: %d" % obchod_strela_pocet
              if obchod_strela_pocet == 3:
                obchod_extra = u"Aktuálna úroveň: %d" % obchod_strela_pocet + "(MAX)"

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
                    if obchod_index != 0:
                        obchod_index -= 1
                else:
                    menu_obchod.kurzor_dolava()
                

            if stlacena_klavesa[K_RIGHT] and cas > oneskorenie_sipky:
                
                if obchod:
                     oneskorenie_sipky = cas + 200
                     menu_obchod.kurzor_obchod_pravo()
                     if obchod_index != 4:
                         obchod_index += 1
                else:
                    menu_obchod.kurzor_doprava()               

            # Nakupovanie rôznych položiek podľa indexov
            if stlacena_klavesa[K_RETURN] and cas > oneskorenie_enter:
                if menu_obchod.polozka_zisti() == 0:
                    if skore_peniaze >= obchod_cena:
                        if obchod_index == 0:
                            skore_zivoty += 1
                            skore_peniaze -= obchod_cena
                        elif obchod_index == 1 and obchod_tablet_rychlost_lvl < 5:
                            obchod_tablet_rychlost += 0.5
                            skore_peniaze -= obchod_cena
                            obchod_tablet_rychlost_lvl += 1
                        elif obchod_index == 2:
                            skore_zivoty_zakladne += 1
                            skore_peniaze -= obchod_cena
                        elif obchod_index == 3 and obchod_strelba_rychlost_lvl < 10:
                            obchod_strelba_rychlost -= 7
                            skore_peniaze -= obchod_cena
                            obchod_strelba_rychlost_lvl += 1
                        elif obchod_index == 4 and obchod_strela_pocet < 3:
                            obchod_strela_pocet += 1
                            skore_peniaze -= obchod_cena
                elif menu_obchod.polozka_zisti() == 1:
                    stav = STAV_V_HRE
                    obchod_pokracuj = False
                    obrazovka.blit(pozadie, (0, 0))
                    pygame.display.update()
                    objekt_zvuky.boj_pokrik_p()
                oneskorenie_enter = cas + 200
            if stlacena_klavesa[K_ESCAPE] and cas > oneskorenie_enter:
                oneskorenie_enter = cas + 200
                stav = STAV_MENU_HLAVNE
            if stlacena_klavesa[K_m]:
                skore_peniaze += 100
                skore_zivoty_zakladne += 1
                skore_zivoty += 1
                
            objekt_skore.update(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore)

        # Hlavné menu hry, spúštané pri spustení hry    
        elif stav == STAV_MENU_HLAVNE:
            obrazovka.blit(menu.Menu.vykresli_menu(menu_hlavne),(0, 0))
            
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

                    obchod_tablet_rychlost = 9.0
                    obchod_tablet_rychlost_lvl = 1
                    obchod_strelba_rychlost = 300
                    obchod_strelba_rychlost_lvl = 1
                    obchod_strela_pocet = 1
                    
                    objekt_noviny = pygame.sprite.RenderUpdates()
                    objekt_noviny_ozbrojene = pygame.sprite.RenderUpdates()
                    objekt_noviny_boss = pygame.sprite.RenderUpdates()
                    objekt_noviny_bonus = pygame.sprite.RenderUpdates()
                    objekt_skore = pygame.sprite.RenderUpdates()
                    objekt_skore.add(skore.Skore(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore))
                    objekt_tablet = pygame.sprite.RenderUpdates()
                    objekt_tablet.add(tablet.Tablet())
                    objekt_strela = pygame.sprite.RenderUpdates()
                    objekt_explozia = pygame.sprite.RenderUpdates()                    
                    objekt_strela_noviny = pygame.sprite.RenderUpdates()
                    
                    obrazovka.blit(pozadie, (0, 0))
                    pygame.display.update()
                    objekt_zvuky.boj_pokrik_p()                    
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

            obrazovka.blit(menu.Menu.vykresli_menu(menu_ako),(0,0))

        elif stav == STAV_MENU_PAUZA:

            obrazovka.blit(menu.Menu.vykresli_popup_menu(menu_pauza, obrazovka),(0,0))

            if stlacena_klavesa[K_LEFT]:
                menu_pauza.kurzor_dolava()

            if stlacena_klavesa[K_RIGHT]:
                menu_pauza.kurzor_doprava()

            if stlacena_klavesa[K_RETURN] and cas > oneskorenie_enter:
                if menu_pauza.polozka_zisti() == 0:
                    stav = STAV_V_HRE
                    obchod_pokracuj = False
                    obrazovka.blit(pozadie, (0, 0))
                    pygame.display.update()
                elif menu_pauza.polozka_zisti() == 1:
                    stav = STAV_MENU_HLAVNE
                oneskorenie_enter = cas + 200

            elif stlacena_klavesa[K_ESCAPE] and cas > oneskorenie_enter:
              stav = STAV_V_HRE
              obchod_pokracuj = False
              obrazovka.blit(pozadie, (0, 0))
              pygame.display.update()
              oneskorenie_enter = cas + 250
              
        elif stav == STAV_VYHRA:
            obrazovka.blit(menu.Menu.vykresli_koniec(menu_vyhra, obrazovka),(0, 0))
            pygame.display.update()

            if stlacena_klavesa[K_ESCAPE]  and cas > oneskorenie_enter:
              stav = STAV_MENU_HLAVNE
              oneskorenie_enter = cas + 200

        elif stav == STAV_PREHRA:            
            obrazovka.blit(menu.Menu.vykresli_koniec(menu_prehra, obrazovka),(0, 0))
            pygame.display.update()

            if stlacena_klavesa[K_ESCAPE]  and cas > oneskorenie_enter:
                stav = STAV_MENU_HLAVNE
                oneskorenie_enter = cas + 200              


# Zavolanie hlavnej funkcie ak je spustený tento skript
if __name__ == '__main__':
    main()
