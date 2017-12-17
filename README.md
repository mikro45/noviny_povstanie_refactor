# git-refactoring-mip-2017-mikro45

by Miroslav Dzuris

Videohra programovana pre rocnikovy projekt na strednej skole.

Je to 2D akcna vertikalna strielacka, kde hrac musi chranit jeho zakladnu pred vlnami nepriatelov v niekolkych urovniach, s boss urovnami a bonusovymi urovnami.
Medzi urovnami moze hrac nakupovat vylepsenie v obchode za peniaze nazbierane pocas hry.

Hra bola programovana v Python.

Poznamka: Kedze som zacal pisat commity po Anglicky, tak som to dotiahol az do konca po Anglicky, inac je vsetko po Slovensky

Zoznam zmien:

Initial commit
	- prve nahranie suborov

Odstranenie nepotrebnych suborov a uprava readme
	- odstranenie suborov ako instalacia, build a pod.
	
Vratenie spat ikony hry
	- vratenie nechtiac odstranenej ikony hry
	
Pridanie .gitignore	
	- pridanie .gitignore, ktory ignoruje *.pyc subory, ktore Python pri kompilovani vytvara
	
Vytvorenie branch "splitting-to-classes";
	Rozdelenie do tried
		- Rozdelenie tried z jedneho suboru do viacerych + zakladna funkcnost
	Uprava z "from module import *" na "import module"
		- Zmena systemu importovania na prehladnejsi a praktickejsi
		Merge do Master

Premenovanie premennych podla konvencii v main
	- premenovanie ako napriklad; suvisiace premnne maju rovnaky prefix, pouzivanie CamelCase a lower_case_with_underscores na spravnych miestach
Premenovanie premennych podla konvencii v triedach
	- podobne ako v main, len v osobitnych triedach

Vytvorenie branch "new_score";
	Zmena render systemu pre skore na novy
		- uprava vykreslovania skore, kedy pred tym bolo skore vykreslovane ako jeden text, teraz su rozne polozky presne urcene
		- plus odstranenie triedy "SkoreBar", ktore povodne vykreslovalo pozadie pre skore. Teraz je to riesene vsetko v jednom
	Finalna verzia render systemu pre skore
		- finalne upravy v main + v triede
		Merge do Master
	
Odstranenie chyby pri konci hry po uprave premennych
	- chyba po automatickom premenovavani

Vytvorenie branch "new_enemy_generator";
	Zjednodusenie generovania nepriatelov v main metode
		- povodne bolo generovanie zbytocne rozdelene, teraz je to prehladnejsie, vdaka odstraneniu explicitneho generovania
		Merge do Master
	
Zjednodusenie nacitavanie obrazkov novin
	- pouzitie funkcie na nacitavanie a globalnych konstant

Odstranenie magickych premennych
	- odstranenie magickych premnnych vo vsetkych suboroch programu
	- plus finalne detaily a kometare
	
Update readme
	- upload tohto suboru