# P1 Advanced Racewear – Mockup V5

Online: https://p1-racewear-mockup-v5.vercel.app
Base: la V1 così com'è pubblicata (https://p1-racewear-mockup.vercel.app). V1, V2 e V3 non sono state toccate.

## Cosa cambia rispetto alla V1 (solo questo)

### 1. Foto vere dei prodotti al posto delle illustrazioni
Foto ufficiali P1 (CDN del negozio online). Sostituite dove esiste una foto del prodotto:
- Homepage: categorie (tute, intimo, guanti e scarpe, kart e meccanici, vintage), 4 tute in evidenza,
  "Una tuta per ogni pilota" (LITE-STAR, MID-YOUNG GUN, LITE-EXTRA), PRO-PARABOLICA, guida "PRO, LITE o MID".
  Nell'hero resta in primo piano la foto dei piloti; la tuta PRO-R è sotto come riserva.
- Categoria: 11 tute su 12 (MID-GENT.EVO non ha foto: resta il disegno con la nota [FOTO]).
- Prodotto: galleria PRO-R (fronte per ogni abbinamento, retro, dettaglio spalle e gamba ingranditi dalla foto),
  "Completa il kit" (X-FLOW, AIR, SPEED, SUPERLIGHT), miniature nel carrello.
- Storia: fascia iniziale e foto di gruppo con file di tute vere.
Restano disegnati, perché non esiste una foto di prodotto: etichetta FIA, misure/cartamodello/cucitura,
mappa, anteprima del template nella colonna sinistra della richiesta.

### 2. Scheda di personalizzazione con selezione colori (pagina prodotto)
- Colonna sinistra invariata (spiegazione del processo in 4 passi).
- Sezione "Grafica": anteprima fronte/retro che si colora dal vivo + 25 colori reali della linea PRO
  per Colore principale, Spalle e fasce, Dettagli e profili. Si sceglie dal campione o dal menu a tendina, sincronizzati.
- Cambiare colore non ridisegna il modulo: i campi già compilati restano.
- I colori si possono passare nel link: /prodotto?c1=%23C10E18&c2=...&c3=...#personalizza
- Nuovi campi: Nome da ricamare, Bandiera, Gruppo sanguigno (facoltativo), Taglia abituale (nelle misure).
- Restano le funzioni della V1: tipo di richiesta (grafica / su misura / entrambe) con sezioni che compaiono, upload, misure, dati.

## Da verificare
- Diritti d'uso delle foto prese dal negozio online P1.
- X-FLOW: la foto è della Comfort Fit Top nera (la V1 cita la Slim Fit Top).
- Il retro esiste solo in argento: per gli altri abbinamenti la vista "Retro" mostra la tuta argento.

## File
transform.py applica le modifiche ai file della V1. Le foto hero/fuoco/team/enrico in formato avif/webp
sono solo sul sito pubblicato (come nella V1).
