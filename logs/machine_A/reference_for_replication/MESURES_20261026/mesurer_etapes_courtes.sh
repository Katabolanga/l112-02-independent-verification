#!/usr/bin/env bash
# mesurer_etapes_courtes.sh -- agent 121, 26 oct. 2026. MESURES sur MACHINE_A (WSL) des etapes COURTES du paquet X1 (duree,
# pic de memoire par /usr/bin/time -v, code natif), depuis le paquet (lecture seule) vers ce dossier. Etapes longues NON
# relancees (deja mesurees le 26 oct.). V02 seulement en PARTIEL (420 s, coupe par timeout) pour le pic de memoire initial.
set -u
K=<LOT>/R112_X1_REPLICATION_MACHINE_B_PAQUET_20261026/PAQUET_X1_REP_V1
M=<LOT>/R112_X1_REPLICATION_MACHINE_B_PAQUET_20261026/MESURES_MACHINE_A_20261026
DF=$K/DONNEES_FIGEES
PYN=$HOME/miniforge3/envs/g6k/bin/python
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$M" || exit 2
W=$HOME/x1rep_mesures_20261026; mkdir -p "$W/bin"   # binaires sur ext4 (WSL), pas sur /mnt/c
mes() { local n="$1"; shift; date '+%H:%M:%S debut '"$n" >> horodatage.txt
  if /usr/bin/time -v -o "$n.time" "$@" > "$n.log" 2>&1; then c=0; else c=$?; fi
  echo "$n code natif $c" >> codes_natifs.txt; date '+%H:%M:%S fin '"$n" >> horodatage.txt; }
mes B01_compil_enum gcc -O2 -std=c11 -fno-fast-math -ffp-contract=off -o "$W/bin/enum_interval" "$K/scripts/enum_interval.c" -lm
mes B02_compil_formes gcc -O2 -o "$W/bin/formes_canoniques" "$K/scripts/formes_canoniques.c"
sha256sum "$K/scripts/enum_interval.c" "$K/scripts/formes_canoniques.c" "$W/bin/enum_interval" "$W/bin/formes_canoniques" > binaires.sha256
for e in E8 leech leech2_e8; do mes "B03_$e" bash -c "'$W/bin/enum_interval' 5 < '$DF/F1/$e.entree' > '$M/B03_$e.sortie'"; cmp "$M/B03_$e.sortie" "$K/REFERENCE_MACHINE_A/F1_$e.sortie" && echo "B03_$e identique a la reference" >> codes_natifs.txt; done
mes R01_raccords python3 -I "$K/scripts/raccord_entrees_f1_rep_v1.py" "$DF"
mes R02_parite python3 -I "$K/scripts/parite_x1_rep_v1.py" "$DF/X1/structure_x1.npz" "$DF/roiban_112/data/L56_gram.txt"
mes V01_phi_X1 bash -c "ulimit -v 6291456; exec nice -n 19 '$PYN' -I '$K/scripts/verif_phi_L56_int64_v3.py' '$DF/roiban_112' '$DF/X1/structure_x1.npz' '$DF/X1/certificats_X1' '$DF/X1/min_reps_L.npz'"
mes V02_partiel_420s bash -c "ulimit -v 6291456; exec timeout 420 nice -n 19 '$PYN' -I '$K/scripts/verif_independante_int16_v3.py' '$DF/roiban_112' '$DF/X1/structure_x1.npz' '$DF/X1/donnees_L.npz' '$DF/X1/norm8_reps_L.npz' '$DF/X1/min_reps_L.npz' '$DF/X1/certificats_X1' '$W/bin/formes_canoniques' '$W/V02_partiel' 1"
echo FINI >> codes_natifs.txt
