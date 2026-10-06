# Senad Transporti, sito HTML classico

Cartella da pubblicare: tutto tranne `generatore/` e questo file.
- `el/ en/ de/ ru/`: pagine nelle 4 lingue. `index.html`: scelta lingua.
- `generatore/`: per cambiare testi o dati, modifica `L.json`, `legal.json` o `BUSINESS` in `build_html.py`, poi `python3 build_html.py` dalla cartella `generatore`.
- Il sito è bloccato ai motori di ricerca (`NOINDEX = True`). Al lancio: `NOINDEX = False`, `SITE_URL` con il dominio vero, poi rigenerare.
- Il modulo di prenotazione non invia ancora nulla.
- Dati ditta e testi legali: vuoti o in bozza.
