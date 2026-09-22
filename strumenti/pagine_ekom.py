# -*- coding: utf-8 -*-
"""Gli indirizzi delle pagine del volantino Ekom, uno per uno.

Stessa faccenda di Mercatò, stessa fonte: ogni immagine è firmata con un
codice calcolato sull'indirizzo, quindi il numero di pagina da solo non basta
e la pagina 5 non si ricava dalla 4. Gli indirizzi si raccolgono tutti, in
ordine, e si tengono qui.

**Vanno rifatti a ogni volantino nuovo**, insieme alle date. Si prendono dalla
pagina del volantino sulla fonte cercando gli indirizzi che contengono
`/0x0/` (le pagine intere; quelli con `240x240` sono le miniature) e
ordinandoli per il numero prima di `.jpg`.

Il primo indirizzo è la pagina 1 (sulla fonte è numerata 0).

Qui non si pubblica niente: sono collegamenti al sito di chi il volantino lo
mette online, come per tutte le altre insegne.
"""

PAGINE_EKOM_08 = (
 'https://eu.kimbicdn.com/thumbor/BjFDpK1MPvzB5OqXqyJGSeBNwoQ=/0x0/filters:format(webp):quality(65)/it/data/162/167414/0.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/XxHuMOFTofD-omgjxi5SBsB9xSc=/0x0/filters:format(webp):quality(65)/it/data/162/167414/1.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/pWitoD10zlkXC881lHW1GO-_Fg8=/0x0/filters:format(webp):quality(65)/it/data/162/167414/2.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/C7vsINo28QOyhdDDBWkmvxHTB0s=/0x0/filters:format(webp):quality(65)/it/data/162/167414/3.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/BOLUNx54NumgA1GaIN0fow4xTDg=/0x0/filters:format(webp):quality(65)/it/data/162/167414/4.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/NPbaN4rliz77gmeMdWIGf_tqE4o=/0x0/filters:format(webp):quality(65)/it/data/162/167414/5.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/hMkhaFW69tP3EgViULDWqyujHkA=/0x0/filters:format(webp):quality(65)/it/data/162/167414/6.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/TnnODusoxxPBj7-OHHmSOqSp_LU=/0x0/filters:format(webp):quality(65)/it/data/162/167414/7.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/gCcwq-ICH6CY5pUDXcNLWEJ_DBw=/0x0/filters:format(webp):quality(65)/it/data/162/167414/8.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/Iaw3_iC38Dugr04g1yZkr70wbKo=/0x0/filters:format(webp):quality(65)/it/data/162/167414/9.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/MyXyjWwVdzBwVLyQRF9tBIp4IEs=/0x0/filters:format(webp):quality(65)/it/data/162/167414/10.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/5NSoiF1Hxoe9KNxZzgJcLNspQEQ=/0x0/filters:format(webp):quality(65)/it/data/162/167414/11.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/vgtZ21HqGbklj1qS_rfp9ujr7RQ=/0x0/filters:format(webp):quality(65)/it/data/162/167414/12.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/4Iq-_7H9HzqL3uc90lUkGIJ31PE=/0x0/filters:format(webp):quality(65)/it/data/162/167414/13.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/p4uhff2BGN5lWLHVzWhB9I8xLwU=/0x0/filters:format(webp):quality(65)/it/data/162/167414/14.jpg?t=1788922633',
 'https://eu.kimbicdn.com/thumbor/-DMsP8zF3xkHHgfSfI-iu9r5AF4=/0x0/filters:format(webp):quality(65)/it/data/162/167414/15.jpg?t=1788922633',
)

# «I più ekonomici», dal 22 settembre al 5 ottobre. Fonte diversa dall'8-21:
# non più kimbino ma il sito ufficiale ekomdiscount.it, che è un'app
# Javascript e non risponde niente a un fetch semplice. Le pagine vere
# arrivano dall'API che l'app chiama in pagina, non dalla pagina stessa:
# `https://www.ekomdiscount.it/ebsn/api/leaflet/search?parent_leaflet_type_id=1`
# torna la lista dei volantini con un `baseLocation` e le pagine sono
# `{baseLocation}{n}.png`, n da 0. In NOTE.md c'è per esteso.
PAGINE_EKOM_22 = (
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/0.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/1.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/2.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/3.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/4.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/5.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/6.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/7.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/8.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/9.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/10.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/11.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/12.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/13.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/14.png',
 'https://app.ekomdiscount.it/photo/leaflets/2026/09/15/73/15.png',
)
