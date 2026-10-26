#!/usr/bin/env bash
# lancer_f1l_natif.sh -- Claude, 26 oct. 2026. REJEU de F1 cote L (min L = 6) pour X1, a l'identique (meme binaire enum_interval
# compile depuis enum_interval.c de roiban, sha fdbb8617..., meme entree L_bkz40_rayon4.entree, sha 9c3ff453...), mais avec le CODE
# NATIF capture (reserve d'<REVIEWER> du 25 oct. 23:13 UTC : « done » ne remplace pas un code natif). Lance par setsid nohup.
cd "$(dirname "$0")" || exit 2
date '+debut %Y-%m-%d %H:%M:%S %z' > horodatage.txt
( ulimit -v 3000000; timeout --kill-after=10 5400 nice -n 19 ./enum_interval 5 < L_bkz40_rayon4.entree > L_bkz40_rayon4.sortie 2> L_bkz40_rayon4.err ); c=$?
echo "code natif $c" > code_natif.txt
date '+fin %Y-%m-%d %H:%M:%S %z' >> horodatage.txt
sha256sum L_bkz40_rayon4.sortie >> horodatage.txt
