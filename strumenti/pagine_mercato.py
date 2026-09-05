# -*- coding: utf-8 -*-
"""Gli indirizzi delle pagine del volantino Mercatò, uno per uno.

Tutti gli altri volantini hanno un indirizzo a schema: cambi il numero di
pagina e ottieni la pagina. Mercatò no. La fonte che lo pubblica firma ogni
immagine con un codice calcolato sull'indirizzo stesso, quindi il numero di
pagina da solo non basta e la pagina 12 non si ricava dalla 11: gli indirizzi
vanno raccolti tutti, in ordine, e tenuti qui.

**Vanno rifatti a ogni volantino nuovo**, insieme alle date. Si prendono dalla
pagina del volantino sulla fonte cercando gli indirizzi che contengono
`/0x0/` (le pagine intere; quelli con `240x240` sono le miniature) e
ordinandoli per il numero prima di `.jpg`.

Il primo indirizzo è la pagina 1. Sul volantino la numerazione stampata parte
da 1 sulla stessa pagina, quindi indice+1 = «pagina N» scritta in basso.

Qui non si pubblica niente: sono collegamenti al sito di chi il volantino lo
mette online, come per tutte le altre insegne.
"""

PAGINE_MERCATO = [
 'https://eu.kimbicdn.com/thumbor/8kj1pOo8Bfv4cwmfmEJMZCK85Eo=/0x0/filters:format(webp):quality(65)/it/data/152/166559/0.jpg?t=1788232665',
 'https://eu.kimbicdn.com/thumbor/IXdVZRr3CTlVV3WlEe_PLW8qdxg=/0x0/filters:format(webp):quality(65)/it/data/152/166556/1.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/Pco5zk4uc3XZmPOd533vj1_VW5c=/0x0/filters:format(webp):quality(65)/it/data/152/166556/2.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/7lGrv_DYuYVjHsHbnB-9yMdsy5U=/0x0/filters:format(webp):quality(65)/it/data/152/166556/3.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/RbdQASi_lHKyD9Obs5kBeloaQ7g=/0x0/filters:format(webp):quality(65)/it/data/152/166556/4.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/XNQHWhMgE51j4uaDYe9YNFD1Q20=/0x0/filters:format(webp):quality(65)/it/data/152/166556/5.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/PX34zTbvBpNPto1sAqBbhK5YqFg=/0x0/filters:format(webp):quality(65)/it/data/152/166556/6.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/cSHfZuZUALe7MEvYkpYDwKaWYg8=/0x0/filters:format(webp):quality(65)/it/data/152/166556/7.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/JCjuVpBWgiZX0Ox1gvNN3uQKWSs=/0x0/filters:format(webp):quality(65)/it/data/152/166556/8.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/h0B8Q2HuepWVafS8_gMrlvAOaD0=/0x0/filters:format(webp):quality(65)/it/data/152/166556/9.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/22hoStOwYVI3XyqcdDKDsv8QXxU=/0x0/filters:format(webp):quality(65)/it/data/152/166556/10.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/-GEQn_dncw8Axsn_U4wLfss6WeI=/0x0/filters:format(webp):quality(65)/it/data/152/166556/11.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/PDaIAbG7JIZ7xcYsja1HfAvobnc=/0x0/filters:format(webp):quality(65)/it/data/152/166556/12.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/9JsVgrIS6O7JaHrLVxzXKjsLjJ0=/0x0/filters:format(webp):quality(65)/it/data/152/166556/13.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/QaFRmvtF2m9EoVO-c13DspmI0Fk=/0x0/filters:format(webp):quality(65)/it/data/152/166556/14.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/SyKI_Ww5YCwztJEwiliw3mrXQOI=/0x0/filters:format(webp):quality(65)/it/data/152/166556/15.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/1FhWFC4ZVOz0nF1EFollQHZhEoE=/0x0/filters:format(webp):quality(65)/it/data/152/166556/16.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/AKafgIpdWHC1VICZgN-u-eMwxQs=/0x0/filters:format(webp):quality(65)/it/data/152/166556/17.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/yRppE7kA4PJUCnSW3apOjqN1gZg=/0x0/filters:format(webp):quality(65)/it/data/152/166556/18.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/1Q01aloCnlVwScS2vcL3JteAgVM=/0x0/filters:format(webp):quality(65)/it/data/152/166556/19.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/8i1YEQf_wIBnsnUj8kL-H-dkCn4=/0x0/filters:format(webp):quality(65)/it/data/152/166556/20.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/f6q0VHQdVNoW5FIGs73lXOYE_-U=/0x0/filters:format(webp):quality(65)/it/data/152/166556/21.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/4oxzFtAFZGmkPSRlxrP89pGUHJ0=/0x0/filters:format(webp):quality(65)/it/data/152/166556/22.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/_u4e0ZmMrb-lKhjO4gKRzmRLx7E=/0x0/filters:format(webp):quality(65)/it/data/152/166556/23.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/zwD8JpV7OxDDcZyWgn4ZeiNTIGs=/0x0/filters:format(webp):quality(65)/it/data/152/166556/24.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/Xmvrl_iW_ZJTWH3k1ICgxIH7alw=/0x0/filters:format(webp):quality(65)/it/data/152/166556/25.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/b_2Av5bqc9kZLCAcQlriYJ0wlwY=/0x0/filters:format(webp):quality(65)/it/data/152/166556/26.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/Tmrgs0I8v7pXN-1NqH0dC-oEC9U=/0x0/filters:format(webp):quality(65)/it/data/152/166556/27.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/25HlBjMXZ7fsZXXtoLSBUWNLBdM=/0x0/filters:format(webp):quality(65)/it/data/152/166556/28.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/cZaaDf5fzXaBRpLYI-_Cd-rBiA0=/0x0/filters:format(webp):quality(65)/it/data/152/166556/29.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/J1fsRzKWG10B-w-iBRxPkTQudlQ=/0x0/filters:format(webp):quality(65)/it/data/152/166556/30.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/gD82WwiMlEYCGbUqNweRhFsBLNY=/0x0/filters:format(webp):quality(65)/it/data/152/166556/31.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/4pAoCHCc64PibmwEJdcVPmmRrL0=/0x0/filters:format(webp):quality(65)/it/data/152/166556/32.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/ME0-kElriFwKXL0XfM8A6oL4DNU=/0x0/filters:format(webp):quality(65)/it/data/152/166556/33.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/04_rOGVYwU3frb1wV8M4XJdwF40=/0x0/filters:format(webp):quality(65)/it/data/152/166556/34.jpg?t=1788301035',
 'https://eu.kimbicdn.com/thumbor/S-WnpNaHdQ9DnmkKHS1YFtAYwWc=/0x0/filters:format(webp):quality(65)/it/data/152/166556/35.jpg?t=1788301035',
]
