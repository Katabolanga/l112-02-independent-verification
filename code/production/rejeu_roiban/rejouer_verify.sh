#!/bin/bash
# rejouer_verify.sh -- agent 116. Rejeu des etapes v0, v2, v3, v4, v5, v6 de roiban1344 (LUES en entier le 25 oct. 18:50-18:58 :
# numpy et bibliotheque standard seulement, ecritures dans RACINE/out uniquement, pas de reseau, pas de shell) sur la COPIE.
# usage : rejouer_verify.sh RACINE_COPIE JOURNAL  -- python -I de l'env g6k (numpy 2.4.6), nice 19, ulimit -v 3000000, 3 fils BLAS.
set -u
RACINE="$1"; J="$2"
PY="$HOME/miniforge3/envs/g6k/bin/python"
export OPENBLAS_NUM_THREADS=3 OMP_NUM_THREADS=3 MKL_NUM_THREADS=3
cd "$RACINE" || exit 2
for s in v0_inputs v2_theta v3_minimal_orbits v4_norm8_orbits v5_odd_bounding v6_canonical_lookup; do
  date "+debut $s %Y-%m-%d %H:%M:%S" >> "$J"
  ( ulimit -v 3000000; timeout 5400 nice -n 19 "$PY" -I "code/verify/$s.py" > "out_rejeu_$s.log" 2>&1 ); c=$?
  date "+fin $s %Y-%m-%d %H:%M:%S code $c" >> "$J"
  if [ "$c" != "0" ]; then echo "ARRET apres $s (code $c)" >> "$J"; exit 1; fi
done
echo "REJEU v0 v2-v6 TERMINE" >> "$J"
