# Simple Rename Context

## Co projekt je

Simple Rename je desktopova Tkinter aplikace pro hromadne prejmenovani souboru. Uzivatel vybere soubory, urci prefix a zvoli typ sekvence:

- cisla s doplnenim nul podle poctu souboru
- pismena ve stylu Excel sloupcu: A, B, ..., Z, AA, AB, ...

## Co tvrdi README a co je realita

README spravne rika, ze jde o jednoduchy bulk rename nastroj. Puvodni implementace ale mela nekolik rozporu proti popisu:

- anglicky preklad zpusobil, ze metoda prejmenovani prestala fungovat, protoze logika znala jen ceske hodnoty
- pismena nebyla ve stylu Excelu, po Z vznikaly jine ASCII znaky
- pri vyberu souboru z vice slozek se vsechny docasne i cilove nazvy pocitaly podle prvni slozky, takze aplikace mohla soubory nechtene presouvat mezi adresari
- GUI zobrazovalo jen basename, takze stejne nazvane soubory z ruznych slozek nesly odlisit
- README puvodne obsahovalo chybne instalacni kroky (`cd` a `pip install` na GitHub URL)

Aktualni stav kodu po oprave:

- rename probiha bezpecne v puvodni slozce kazdeho souboru
- kolize se soubory mimo vyber zastavi operaci pred prvni zmenou
- operace probiha ve dvou fazich pres docasne nazvy a pri chybe se pokusi vratit puvodni stav
- CZ i EN UI pouzivaji stejnou interní logiku metod
- seznam souboru se v GUI radi podle interniho poradi, ne podle textu v listboxu
- rename jadro je oddelene od Tkinteru a vraci vysledek nebo vyhazuje explicitni chyby

## Architektura

- `main.py`: spusteni aplikace a presmerovani vystupu do denniho logu
- `window.py`: GUI vrstva a orchestrace mezi UI a sluzbami
- `widget_logic.py`: controller pro listbox, prepinani jazyka a pomocne UI akce
- `rename_logic.py`: cista rename service s validaci, planem prejmenovani a explicitnimi vyjimkami
- `log.py`: denni log soubor a jednoduche log viewer okno
- `config.py`: runtime stav aplikace a lokalizacni konstanty

## Omezeni a predpoklady

- aplikace nepodporuje undo historii mezi behy; rollback resi jen chybu v ramci aktualni rename operace
- vyber souboru je manualni pres file dialog, ne pres celou slozku
- lokalizace se tyka hlavniho okna, ne vsech systemovych dialogu Tkinteru
- projekt nema automaticke testy; vhodna je aspon smoke sada pro rename scenare nad docasnymi soubory

## Doporucene dalsi kroky

- oddelit GUI od rename jadra tak, aby slo snadno psat testy
- pridat preview seznamu cilovych nazvu pred potvrzenim operace
- pridat explicitni undo historii zalozenou na rename journalu
- doplnit testy pro kolize, vice slozek, duplicitni basename a EN/CZ prepinani