# Senad Transporti, sito classico (HTML, CSS, JS)

Copia identica del sito dinamico, senza server e senza database: si può pubblicare su qualunque hosting (anche GitHub Pages).

## Da dove viene
Queste pagine NON si modificano a mano. Si creano dal repo **senad_transporti_dinamico** con:

    npm run build:classic

Il risultato è nella cartella `dist-classic/` di quel repo: si copia qui al posto dei file vecchi (tranne questo file e il collegamento .lnk).

## Differenze rispetto al dinamico
- Moduli (Anfragen, Mietwagen, Angebot): aprono WhatsApp con il messaggio già scritto. Se manca il numero, usano l'email.
- Niente "Buchen" con pagamento online, niente admin, niente feedback dei clienti, niente traduttore.
- Chat: risposte automatiche nel browser + pulsante WhatsApp (niente "chat con il team").
- Mietwagen e Galerie: testo "in arrivo" finché non ci sono auto e foto.
- Privacy: il testo dice come funziona questa versione (niente database, moduli via WhatsApp). Bozza da far controllare.

## Stato
- 5 lingue: DE, EN, EL, RU, SR. Indirizzi nella lingua (es. /de/mietwagen). I vecchi (/de/book.html) portano ai nuovi.
- Nascosto a Google (noindex) finché nel dinamico `src/config.ts` ha `NOINDEX = true`.
- Non pubblicato: GitHub Pages è spento.
