#!/bin/bash
# lancer_verif_independante.sh -- agent 116 : seconde implementation (verif_independante_int16.py) pour X1 (et, si demande, X4).
# usage : lancer_verif_independante.sh 1|4      (nice 19, ulimit 4 Go, 1 fil BLAS ; code de sortie ecrit par ce script)
set -u
J="$1"
D=<LOT>/R112_X1_EFFORT_MAX_20261025
R=$D/copie_execution/roiban_112
PY=$HOME/miniforge3/envs/g6k/bin/python
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $D/scripts/independant || exit 2
if [ "$J" = "1" ]; then
  ST=$D/sorties/structure_x1/structure_x1.npz; DON=$D/sorties/donnees_L/donnees_L.npz; N8=$D/sorties/orbites8_L_v2/norm8_reps_L.npz
  MIN=$D/sorties/orbites_min_L/min_reps_L.npz; CERT=$D/sorties/certificats_X1; OUT=$D/sorties/independant/X1_int16
else
  ST=$D/sorties/structure_X4/structure_X4.npz; DON=$D/sorties/temoin_X4/donnees8/donnees_L4.npz; N8=$D/sorties/temoin_X4/donnees8/norm8_reps_L4.npz
  MIN=$D/sorties/temoin_X4/donnees8/min_reps_L4.npz; CERT=$D/sorties/temoin_X4/certificats; OUT=$D/sorties/independant/X4_int16
fi
mkdir -p $OUT
date '+debut %Y-%m-%d %H:%M:%S' > $OUT/horodatage.txt
( ulimit -v 6291456; timeout 10800 nice -n 19 $PY -I verif_independante_int16.py $R $ST $DON $N8 $MIN $CERT $D/scripts/independant/formes_canoniques $OUT $J > $OUT/sortie.log 2>&1 )
echo "code $?" >> $OUT/horodatage.txt
date '+fin %Y-%m-%d %H:%M:%S' >> $OUT/horodatage.txt
