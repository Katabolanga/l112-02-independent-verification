#!/bin/bash
# lancer_phase_finale.sh -- agent 116 : lance, detaches (setsid nohup), le test (8,8) de X1 puis de X4 (suite_apres_p3_v2.sh) et la
# seconde implementation pour X1 (lancer_verif_independante_v2.sh 1).
D=<LOT>/R112_X1_EFFORT_MAX_20261025/scripts
cd $D || exit 2
setsid nohup ./suite_apres_p3_v2.sh > $D/../sorties/suite_apres_p3_v2.lanceur.log 2>&1 < /dev/null &
echo "suite_apres_p3 : pid $!"
setsid nohup ./independant/lancer_verif_independante_v2.sh 1 > $D/../sorties/verif_independante_X1_v2.lanceur.log 2>&1 < /dev/null &
echo "verif_independante X1 : pid $!"
sleep 2
