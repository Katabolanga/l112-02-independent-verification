#!/bin/bash
# rejouer_v1.sh -- agent 116. Compilation MANUELLE de enum_interval.c (drapeaux de lib/enumerate.py) et execution sur les entrees
# ecrites par v1_entrees_manuel.py.  usage : rejouer_v1.sh RACINE_COPIE DOSSIER  (un seul fil, nice 19, timeout 7200 s par entree)
set -u
RACINE="$1"; D="$2"
cd "$D" || exit 2
gcc -O2 -std=c11 -fno-fast-math -ffp-contract=off -o enum_interval "$RACINE/code/verify/enum_interval.c" -lm || exit 3
sha256sum "$RACINE/code/verify/enum_interval.c" enum_interval > compilation.sha256
for nom in E8 leech leech2_e8 L56; do
  date "+debut $nom %Y-%m-%d %H:%M:%S" >> horodatage.txt
  ( ulimit -v 3000000; timeout 7200 nice -n 19 ./enum_interval 5 < "$nom.entree" > "$nom.sortie" 2> "$nom.err" ); echo "$nom code $?" >> codes.txt
  date "+fin $nom %Y-%m-%d %H:%M:%S" >> horodatage.txt
done
echo FINI >> codes.txt
