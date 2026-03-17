# Simple Rename

Simple Rename je desktopová aplikace v Pythonu pro bezpečné hromadné přejmenování souborů. Je zaměřená na rychlé přejmenování epizod, videí nebo jiných sérií souborů bez zbytečné složitosti, ale zároveň s důrazem na bezpečnost operace a předvídatelné chování.

Aktuální release: `1.0.0`

Aktuální verze už není jen jednoduchý proof of concept. Umí bezpečné batch rename operace, přehledné řazení souborů v UI, drag-and-drop z Windows Exploreru, lokalizaci CZ/EN a vrácení posledního přejmenování.

## Hlavní vlastnosti

- Bezpečné hromadné přejmenování více souborů v jednom kroku.
- Číselná sekvence s automatickým doplněním nul podle počtu souborů.
- Písmenná sekvence ve stylu Excel sloupců: `A ... Z, AA, AB, AC ...`.
- Zachování původní přípony souboru.
- Zachování původní složky každého souboru, i když vybíráš soubory z více adresářů.
- Ochrana proti kolizi s cizími existujícími soubory ještě před první změnou.
- Dvoufázové přejmenování přes dočasné názvy, aby se minimalizovalo riziko rozbití batch operace.
- Pokus o bezpečný návrat původního stavu při selhání rename operace.
- Vrácení posledního úspěšného batch rename jedním klikem.
- Přehledné ruční řazení souborů v listu:
    - posun nahoru a dolů
    - přesun na začátek a konec
    - otočení pořadí
- Import souborů přes dialog i přetažením z Windows Exploreru do bílé oblasti seznamu.
- CZ a EN rozhraní se stejnou interní logikou rename metod.
- Vestavěný denní log a jednoduchý log viewer.
- Automatizované regresní testy pro rename logiku i UI chování.

## Jak funguje přejmenování

Uživatel zadá základ názvu a zvolí způsob sekvence.

- `Čísla` / `Numbers`:
    - přidají číselný suffix podle aktuálního pořadí v seznamu
    - šířka čísel se mění podle počtu vybraných souborů
    - příklady:
        - 9 souborů -> `1` až `9`
        - 12 souborů -> `01` až `12`
- `Písmena` / `Letters`:
    - přidají písmena podle aktuálního pořadí v seznamu
    - pokračují jako `A, B, C ... Z, AA, AB, AC ...`

Pořadí v levém seznamu přímo určuje výsledné názvy. Pokud tedy změníš pořadí před přejmenováním, změníš i finální sekvenci souborů.

## Bezpečnost a rollback

Projekt je postavený tak, aby rename operace byla co nejméně riskantní.

- Každý soubor se přejmenovává ve své původní složce.
- Pokud by výsledný název kolidoval s jiným existujícím souborem mimo aktuální výběr, operace se zastaví předem.
- Neplatné Windows znaky v cílovém názvu se zachytí ještě před rename.
- Rename běží ve dvou fázích přes dočasné názvy.
- Když rename selže v průběhu, aplikace se pokusí vrátit původní názvy.
- Po úspěšném rename lze vrátit zpět poslední batch přes tlačítko `Vrátit zpět`.
- Undo nepřepisuje cizí soubory. Pokud je původní název mezitím obsazený nebo renamed soubor zmizel, daná položka se přeskočí a uživatel dostane jasnou informaci.

## Uživatelské rozhraní

Rozhraní je rozdělené na dvě hlavní části.

- Levý panel:
    - seznam vybraných souborů
    - tlačítka pro změnu pořadí
    - výběr, odebrání vybraných a odebrání všech souborů
- Pravý panel:
    - nastavení názvu a metody přejmenování
    - informační tooltip k metodám číslování
    - hlavní akce `Přejmenuj soubory`
    - sekundární akce `Vrátit zpět`
    - stručný návod k použití

UI je laděné tak, aby drželo stabilní layout v češtině i angličtině a aby texty nerozbíjely rozložení hlavních prvků.

## Instalace

### Požadavky

- Windows
- Python 3.11+ nebo novější

### Postup

1. Naklonuj repository:

```bash
git clone https://github.com/Mitelin/Simple-Rename
```

2. Přejdi do složky projektu:

```bash
cd Simple-Rename
```

3. Vytvoř a aktivuj virtuální prostředí:

```bash
python -m venv .venv
.venv\Scripts\activate
```

4. Nainstaluj dependency:

```bash
pip install -r requirements.txt
```

5. Spusť aplikaci:

```bash
python main.py
```

## Použité technologie

- Python
- Tkinter
- tkinterdnd2
- unittest

## Spuštění testů

Automatizované testy spustíš takto:

```bash
python -m unittest discover -s tests -v
```

Aktuální testy pokrývají hlavně:

- validaci vstupů
- číselné i písmenné sekvence
- kolize názvů
- rename napříč více složkami
- rollback a částečný rollback
- drag-and-drop parsing
- základní UI layout a stav tlačítek

## Struktura projektu

- `main.py` - vstupní bod aplikace, inicializace logování a spuštění okna
- `window.py` - stavba UI a orchestrace mezi GUI a službami
- `widget_logic.py` - controller pro chování widgetů a pomocné UI akce
- `rename_logic.py` - rename service, validace, bezpečné přejmenování a rollback poslední operace
- `config.py` - stav aplikace a lokalizované texty
- `log.py` - denní log a log viewer
- `tests/` - automatizované testy

## Logování

Aplikace zapisuje běh do denního log souboru ve složce `log/`.

- log se vytváří automaticky při spuštění
- zapisují se do něj rename i rollback operace
- log lze otevřít z UI přes tlačítko `Open Log` / `Otevrit log`

## Aktuální omezení

- Undo vrací jen poslední úspěšný batch rename, ne celou historii operací.
- Drag-and-drop je zaměřený na soubory z Windows Exploreru, ne na kompletní import celé složky.
- Aplikace je navržená primárně pro Windows prostředí.
- Tooltipy, log viewer a systémové dialogy jsou stále relativně jednoduché.

## Důležité chování

- Přejmenování nikdy úmyslně nepřepisuje cizí existující soubory.
- Pokud nelze vrátit všechny soubory při undo, aplikace vrátí jen bezpečné položky a zbytek nahlásí.
- Seznam v UI používá reálné interní pořadí, ne jen text zobrazený v listboxu.
- Soubory se stejným basename z různých složek jsou v seznamu odlišené názvem rodičovské složky.

## Možné další rozšíření

- preview budoucích názvů před potvrzením rename
- podpora importu celé složky
- bohatší historie undo operací
- potvrzovací dialog před rollbackem
- detailnější log viewer a export logu
