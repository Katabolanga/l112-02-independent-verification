#!/bin/bash
# suite_apres_p3_v2.sh -- agent 116 : enchaine, apres la fin de p3 sur L (orbites8_L), le test du type (8,8) pour X1, puis le
# transport des orbites de norme 8 vers L4 et le meme test pour le temoin positif X4. nice 19, ulimit 3 Go, 1 fil BLAS.
set -u
D=<LOT>/R112_X1_EFFORT_MAX_20261025
R=$D/copie_execution/roiban_112
PY=$HOME/miniforge3/envs/g6k/bin/python
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $D/scripts || exit 2
mkdir -p $D/sorties/collisions8_X1
( ulimit -v 6291456; timeout 10800 nice -n 19 $PY -I collisions8_x1.py $R $D/sorties/structure_x1/structure_x1.npz $D/sorties/donnees_L/donnees_L.npz $D/sorties/orbites8_L_v2/norm8_reps_L.npz $D/sorties/collisions8_X1 1 > $D/sorties/collisions8_X1/sortie.log 2>&1 ); echo "code $?" >> $D/sorties/collisions8_X1/sortie.log
( ulimit -v 6291456; timeout 1800 nice -n 19 $PY -I transporter_L4.py $R $D/sorties/structure_X4/structure_X4.npz $D/sorties/temoin_X4/isometrie_L4_L1.npz $D/sorties/donnees_L/donnees_L.npz $D/sorties/orbites_min_L/min_reps_L.npz $D/sorties/orbites8_L_v2/norm8_reps_L.npz $D/sorties/temoin_X4/donnees8 > $D/sorties/temoin_X4/transport8.log 2>&1 ); echo "code $?" >> $D/sorties/temoin_X4/transport8.log
mkdir -p $D/sorties/temoin_X4/collisions8
( ulimit -v 6291456; timeout 10800 nice -n 19 $PY -I collisions8_x1.py $R $D/sorties/structure_X4/structure_X4.npz $D/sorties/temoin_X4/donnees8/donnees_L4.npz $D/sorties/temoin_X4/donnees8/norm8_reps_L4.npz $D/sorties/temoin_X4/collisions8 4 > $D/sorties/temoin_X4/collisions8/sortie.log 2>&1 ); echo "code $?" >> $D/sorties/temoin_X4/collisions8/sortie.log
echo SUITE_TERMINEE >> $D/sorties/collisions8_X1/sortie.log
