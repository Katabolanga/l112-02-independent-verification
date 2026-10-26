#!/bin/bash
# lancer_v3.sh -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent 119) : tests de donnees manquantes puis execution COMPLETE des copies
# corrigees _v3 sur MACHINE_A (meme machine que le lot X1 : ce n'est PAS une replication), codes natifs captures.
# Ordre : (0) tests d'arret sur donnee manquante ; (1) verif_phi_L56_int64_v3.py (X1) ; (2) verif_independante_int16_v3.py J=1 (X1) ;
# (3) verif_independante_int16_v3.py J=4 (X4, controle positif). nice 19, 1 fil BLAS, ulimit 6 Gio, delais.
set -u
D=<LOT>/R112_X1_FICHE_CATALOGUE_20261026
X=<LOT>/R112_X1_EFFORT_MAX_20261025
R=$X/copie_execution/roiban_112
S=$D/chaine_admission/scripts_v3
O=$D/chaine_admission/execution_v3
PY=$HOME/miniforge3/envs/g6k/bin/python
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $O || exit 2
sha256sum $S/*.py > $O/scripts_v3.sha256
date '+debut %Y-%m-%d %H:%M:%S %z' > $O/horodatage.txt
# (0) tests d'arret
$PY -I $S/verif_phi_L56_int64_v3.py $R $X/sorties/structure_x1/structure_x1.npz $X/sorties/certificats_X1 > $O/test0a.log 2>&1; echo "test0a (3 arguments) code natif $?" >> $O/codes_natifs.txt
$PY -I $S/verif_phi_L56_int64_v3.py $R $X/sorties/structure_x1/structure_x1.npz $X/sorties/certificats_X1 /nonexistent/min_reps_L.npz > $O/test0b.log 2>&1; echo "test0b (source absente) code natif $?" >> $O/codes_natifs.txt
$PY -I $S/verif_independante_int16_v3.py $R $X/sorties/structure_x1/structure_x1.npz $X/sorties/donnees_L/donnees_L.npz $X/sorties/orbites8_L_v2/norm8_reps_L.npz $X/sorties/orbites_min_L/min_reps_L.npz /nonexistent_certificats $X/scripts/independant/formes_canoniques $O/test0c 1 > $O/test0c.log 2>&1; echo "test0c (certificats absents) code natif $?" >> $O/codes_natifs.txt
# (1) phi exact
( ulimit -v 6291456; timeout 3600 nice -n 19 $PY -I $S/verif_phi_L56_int64_v3.py $R $X/sorties/structure_x1/structure_x1.npz $X/sorties/certificats_X1 $X/sorties/orbites_min_L/min_reps_L.npz > $O/phi_v3_X1.log 2>&1 ); echo "phi_v3_X1 code natif $?" >> $O/codes_natifs.txt
date '+fin phi %Y-%m-%d %H:%M:%S %z' >> $O/horodatage.txt
# (2) seconde implementation, X1
( ulimit -v 6291456; timeout 7200 nice -n 19 $PY -I $S/verif_independante_int16_v3.py $R $X/sorties/structure_x1/structure_x1.npz $X/sorties/donnees_L/donnees_L.npz $X/sorties/orbites8_L_v2/norm8_reps_L.npz $X/sorties/orbites_min_L/min_reps_L.npz $X/sorties/certificats_X1 $X/scripts/independant/formes_canoniques $O/X1_v3 1 > $O/X1_v3.log 2>&1 ); echo "independante_v3_X1 code natif $?" >> $O/codes_natifs.txt
date '+fin X1 %Y-%m-%d %H:%M:%S %z' >> $O/horodatage.txt
# (3) seconde implementation, X4 (controle positif : code 0 seulement si des touches (8,8) sont trouvees)
( ulimit -v 6291456; timeout 7200 nice -n 19 $PY -I $S/verif_independante_int16_v3.py $R $X/sorties/structure_X4/structure_X4.npz $X/sorties/temoin_X4/donnees8/donnees_L4.npz $X/sorties/temoin_X4/donnees8/norm8_reps_L4.npz $X/sorties/temoin_X4/donnees8/min_reps_L4.npz $X/sorties/temoin_X4/certificats $X/scripts/independant/formes_canoniques $O/X4_v3 4 > $O/X4_v3.log 2>&1 ); echo "independante_v3_X4 code natif $?" >> $O/codes_natifs.txt
date '+fin X4 %Y-%m-%d %H:%M:%S %z' >> $O/horodatage.txt
echo FINI >> $O/codes_natifs.txt
