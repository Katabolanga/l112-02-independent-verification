#!/usr/bin/env bash
# lancer_x1_rep_v2.sh -- lot R112_X1_REPLICATION (agent Claude n° 121, 26 oct. 2026 ; V2 : agent n° 122). REPLICATION DES VERIFICATEURS de la chaine
# « min X1 = 10 » (rang 112) sur MACHINE_B, selon <INTERNAL_NOTE>
# (§ 4 : « repliquer les verificateurs necessaires, pas la decouverte ») : donnees FIGEES, verifications F1 / F2-F3 / certificats /
# collisions / parite / raccords, codes natifs partout, AUCUNE recherche de classes, aucun G6K.
# VERSION V2 (26 oct. 2026, correction 1 d'<REVIEWER>, <INTERNAL_NOTE>, § 3 a
# et piece 2, point 1) : PY, PYN, GP et CC ont pour DEFAUT les chemins absolus releves sur MACHINE_B le 26 oct. a 12:18:43 UTC
# (<INTERNAL_NOTE>) ; une variable VIDE (par ex. « $(command -v gp-local) », qui
# ne resout rien chez MACHINE_B) retombe sur ce chemin, jamais sur un nom nu (« gp ») ; les quatre chemins sont ecrits dans le BILAN.
# Gardes de delai, controles de parametres, memoire, copie figee et etapes : INCHANGES par rapport a la V1.
# GARDES DE DELAI : celles de lancer_111_v3.sh (relu par <REVIEWER>, GO du 26 oct. 08:12 UTC), reprises A L'IDENTIQUE (memes variables
# R96_*, memes lignes ; un diff contre lancer_111_v3.sh ne montre que l'en-tete, la memoire, la copie figee, les etapes et le
# verdict) : horloge MONOTONE ; ECHEANCE = T0 + BUDGET - COLLECTE - MARGE (MARGE = R96_MARGE_SYSTEMD, defaut 120 s) ; FIN des
# etapes = ECHEANCE - RESERVE_VERDICT ; chaque etape recoit t = min(plafond, FIN - maintenant) et tourne sous
# « timeout --kill-after=KA (t - KA) » : SIGTERM a t - KA, SIGKILL du GROUPE au plus tard a t (KA = R96_KILL_AFTER, defaut 5 s) ;
# si t - KA < 1, l'etape NE PART PAS (code 124) ; le VERDICT est borne par ECHEANCE - maintenant (arret force compris) et n'est
# PAS lance s'il reste moins de R96_VERDICT_MIN (defaut 60 s) ; verdict interrompu ou acheve apres l'echeance = code 124, jamais
# un PASS ; un seul verdict. Crochets de TEST (mode factice seulement) : R96_TEST_ENFANT_TETU=<etape>, R96_TEST_VERDICT_DORT=<s>.
# ETAPES, EN SERIE, TOUTES BLOQUANTES (ordre : controles courts d'abord, puis F1, puis certificats et collisions) :
#   E00 numpy present dans PYN (sinon BLOCAGE avant tout calcul ; aucune installation n'est faite ni promise)
#   B01 compilation NATIVE de enum_interval.c (roiban) avec les drapeaux de lib/enumerate.py : gcc -O2 -std=c11 -fno-fast-math
#       -ffp-contract=off ... -lm ; B02 compilation native de formes_canoniques.c (gcc -O2) ;
#   B03 controles du binaire recompile sur E8, Leech, Leech2_E8 (sorties IDENTIQUES a celles de MACHINE_A) ;
#   R01 raccords des entrees F1 (Gram de l'entree = U G U^t, U unimodulaire, intervalles contenant les rationnels exacts) ;
#   R02 parite du recollement (1 596 congruences) ; R01 et R02 en BIBLIOTHEQUE STANDARD (PY, sans numpy) ;
#   R03 serie theta extremale de dimension 56 en PARI exact (GP) : |L_6| = 15 590 400 et |L_8| = 36 957 286 800, les nombres
#       theta contre lesquels V02 compte la couverture (valables pour L et L56, extremaux de minimum 6 par F01/F02) ;
#   F01 F1 cote L (enum_interval 5 < L_bkz40_rayon4.entree) ; F02 F1 cote L56 (enum_interval 5 < L56.entree) ;
#   V01 certificats impairs cote phi, exact int64 (verif_phi_L56_int64_v3.py, 7 controles dont la classe) ;
#   V02 seconde implementation X1 (verif_independante_int16_v3.py, J = 1) : groupes, recouvrement norme 6 (F2) et norme 8 (F3)
#       de L56 et de L, collisions (8,8) = 0, certificats phi ET psi ;
#   V03 controle POSITIF X4 (meme script, J = 4) : des collisions (8,8) doivent etre trouvees (20 sur MACHINE_A).
#   VERDICT : verificateur/verdict_x1_rep_v2.py (bibliotheque standard, lecture seule des sorties de CETTE execution) ; il fixe le
#   code de sortie global : 0 seulement si 0 touche (8,8), les deux cotes impairs, F1 des deux cotes, couverture, parite, raccords,
#   binaire controle et X4 positif sont lus PASS.
# CONTRAT DU LANCEUR (meme schema que lancer_111_v3.sh)
#   - Toute etape est BLOQUANTE : code natif capture par « if cmd; then c=0; else c=$?; fi » dans <etape>.native.exit ; reussite =
#     code 0 ET motif present dans la sortie designee ; sinon ARRET IMMEDIAT (aucune etape suivante), verdict terminal borne pour
#     trace, code global NON NUL (code de l'etape, ou 2 si code 0 sans motif, ou 124 si budget).
#   - PLAFOND GLOBAL DUR : R96_BUDGET_GLOBAL (defaut 18000 s = 5 h, voir le contrat X1) dont R96_COLLECTE (900 s) reserve a la
#     collecte, R96_MARGE_SYSTEMD (120 s) et R96_RESERVE_VERDICT (600 s) pour le verdict.
#   - Memoire : ulimit -v R96_ULIMIT_KIO (defaut 6291456 kio = 6 Gio, valeur sous laquelle V02 et V03 ont reussi sur MACHINE_A) ;
#     un seul processus de calcul a la fois (serie) ; nice -n 19 ; 1 fil (OPENBLAS/OMP/MKL_NUM_THREADS=1) ; admission si
#     MemAvailable >= R96_MEM_ADMISSION_KIO (defaut 10485760 kio = 10 Gio : 6 Gio + reserve 4 Gio).
#   - Copie source FIGEE : scripts/, verificateur/, DONNEES_FIGEES/ et REFERENCE_MACHINE_A/ sont copies dans le dossier d'execution
#     NEUF puis controles par SHA-256 contre SHA256SUMS.txt du paquet ; tout est execute depuis cette copie.
#   - Tests de controle de flux sans calcul : R96_FACTICE=1 (chaque etape = « sleep ; echo motif ») et R96_INJECTION=<etape>.
#     Ces modes ne produisent JAMAIS de verdict conforme (le verdict relit les sorties, absentes). INTERDITS en execution reelle.
# usage : PY=/usr/bin/python3 PYN=<MACHINE_B>/software/envs/sage/bin/python3 GP=<MACHINE_B>/software/envs/sage/bin/gp
#         CC=/usr/bin/gcc bash lanceurs/lancer_x1_rep_v2.sh NOM_EXEC   (dossier NEUF a la racine ; ces quatre chemins sont aussi les defauts)
set -u
RACINE="$(cd "$(dirname "$0")/.." && pwd)"
NOM="${1:?nom du dossier d execution}"
EX="$RACINE/$NOM"
PY="${PY:-/usr/bin/python3}"; PYN="${PYN:-<MACHINE_B>/software/envs/sage/bin/python3}"; CC="${CC:-/usr/bin/gcc}"; GP="${GP:-<MACHINE_B>/software/envs/sage/bin/gp}"
BUDGET="${R96_BUDGET_GLOBAL:-18000}"; COLLECTE="${R96_COLLECTE:-900}"; RESV="${R96_RESERVE_VERDICT:-600}"
MARGE="${R96_MARGE_SYSTEMD:-120}"; KA="${R96_KILL_AFTER:-5}"; VMIN="${R96_VERDICT_MIN:-60}"
FACTICE="${R96_FACTICE:-0}"; FDUREE="${R96_FACTICE_DUREE:-1}"; INJ="${R96_INJECTION:-}"
ULIM="${R96_ULIMIT_KIO:-6291456}"; MEMADM="${R96_MEM_ADMISSION_KIO:-10485760}"
mono() { "$PY" -c 'import time; print(int(time.monotonic()))'; }
for v in "$BUDGET" "$COLLECTE" "$RESV" "$MARGE" "$KA" "$VMIN"; do case "$v" in ""|*[!0-9]*) echo "ERREUR : parametre de delai non entier : « $v » ; rien n'est lance"; exit 9;; esac; done
for v in "$ULIM" "$MEMADM"; do case "$v" in ""|*[!0-9]*) echo "ERREUR : parametre de memoire non entier : « $v » ; rien n'est lance"; exit 9;; esac; done
if [ "$KA" -lt 1 ] || [ "$VMIN" -le "$KA" ]; then echo "ERREUR : R96_KILL_AFTER ($KA) doit etre >= 1 et < R96_VERDICT_MIN ($VMIN) ; rien n'est lance"; exit 9; fi
T0=$(mono); ECHEANCE=$((T0 + BUDGET - COLLECTE - MARGE)); FIN=$((ECHEANCE - RESV))
if [ "$FIN" -le "$T0" ]; then echo "ERREUR : budget trop court (FIN des etapes $FIN <= T0 $T0) ; rien n'est lance"; exit 124; fi
if [ -e "$EX" ]; then echo "ERREUR : $EX existe deja (dossier neuf exige)"; exit 10; fi
if [ "$FACTICE" != "1" ]; then
  if [ -n "${R96_TEST_ENFANT_TETU:-}" ] || [ -n "${R96_TEST_VERDICT_DORT:-}" ] || [ -n "$INJ" ]; then echo "ERREUR : crochets de test interdits en execution reelle ; rien n'est lance"; exit 9; fi
  MEMKB=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
  if [ "${MEMKB:-0}" -lt "$MEMADM" ]; then echo "ADMISSION REFUSEE : MemAvailable = ${MEMKB} kio < $MEMADM kio ($ULIM kio de plafond + reserve 4 Gio)"; exit 20; fi
else MEMKB="(mode factice)"; fi
ulimit -v "$ULIM"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
# integrite du paquet, puis copie figee
if (cd "$RACINE" && sha256sum -c --quiet SHA256SUMS.txt) > /dev/null 2>&1; then :; else echo "ERREUR : paquet non conforme a SHA256SUMS.txt"; exit 12; fi
mkdir "$EX" || exit 11
cp -a "$RACINE/scripts" "$RACINE/verificateur" "$RACINE/DONNEES_FIGEES" "$RACINE/REFERENCE_MACHINE_A" "$EX/" || exit 11
grep -E '^[0-9a-f]{64} [ *](scripts|verificateur|DONNEES_FIGEES|REFERENCE_MACHINE_A)/' "$RACINE/SHA256SUMS.txt" > "$EX/MANIFESTE_COPIE_FIGEE.sha256"
NMAN=$(grep -c . "$EX/MANIFESTE_COPIE_FIGEE.sha256")
if [ "$NMAN" -gt 0 ] && (cd "$EX" && sha256sum -c --quiet MANIFESTE_COPIE_FIGEE.sha256) > /dev/null 2>&1; then :; else echo "ERREUR : copie figee non conforme ($NMAN entrees)"; exit 13; fi
mkdir -p "$EX/sorties" "$EX/bin" || exit 11
BILAN="$EX/BILAN_X1_REP_V2.txt"
note() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" | tee -a "$BILAN"; }
verdict_terminal() {   # V3 : BORNE par ECHEANCE (arret force compris) ; NON lance s'il reste moins de VMIN s ; 124 si interrompu ou tardif
  local rv cv
  rv=$((ECHEANCE - $(mono)))
  if [ "$rv" -lt "$VMIN" ]; then echo 124 > "$EX/VERDICT.native.exit"; note "VERDICT NON LANCE : il reste $rv s avant l'echeance (minimum $VMIN s) ; sorties conservees ; code 124"; return 124; fi
  if [ "$FACTICE" = "1" ] && [ "${R96_TEST_VERDICT_DORT:-0}" -gt 0 ]; then   # TEST seulement : verdict lent qui ignore SIGTERM
    if timeout --kill-after="$KA" "$((rv - KA))" bash -c "trap '' TERM; exec -a R96_VERDICT_LENT sleep $R96_TEST_VERDICT_DORT" > "$EX/VERDICT.log" 2>&1; then cv=0; else cv=$?; fi
  else
    if (cd "$EX" && timeout --kill-after="$KA" "$((rv - KA))" "$PY" -I verificateur/verdict_x1_rep_v2.py "$EX") > "$EX/VERDICT.log" 2>&1; then cv=0; else cv=$?; fi
  fi
  if [ "$cv" = "124" ] || [ "$cv" = "137" ]; then cv=124; note "VERDICT INTERROMPU a l'echeance (delai $((rv - KA)) s + arret force $KA s) ; sorties conservees ; aucun PASS"; fi
  if [ "$(mono)" -gt "$ECHEANCE" ]; then cv=124; note "VERDICT ACHEVE APRES L'ECHEANCE : code 124, aucun PASS"; fi
  echo "$cv" > "$EX/VERDICT.native.exit"
  note "VERDICT : code natif $cv ; $(tail -1 "$EX/VERDICT.log" 2>/dev/null)"
  return "$cv"
}
terminer() {   # terminer CODE RAISON : arret immediat, verdict BORNE pour trace (ou aucun si le temps manque), code global non nul
  local code="$1"; note "ARRET : $2 (code $code) ; aucune etape suivante n'est lancee"
  verdict_terminal || true
  echo "$code" > "$EX/GLOBAL.native.exit"; mono > "$EX/FIN_MONO.txt"; note "CODE GLOBAL $code"; exit "$code"
}
# run_step NOM PLAFOND_S MOTIF FICHIER_DU_MOTIF commande...   (FICHIER_DU_MOTIF = "LOG" pour le journal de l'etape ; chemins
# relatifs a $EX ; toutes les commandes tournent dans $EX, entree standard fermee, nice -n 19, timeout exterieur)
run_step() {
  local n="$1" cap="$2" motif="$3" fm="$4"; shift 4
  local reste=$((FIN - $(mono)))
  if [ "$reste" -le 0 ]; then echo 124 > "$EX/$n.native.exit"; terminer 124 "budget global epuise avant $n"; fi
  local t="$cap"; [ "$reste" -lt "$t" ] && t="$reste"
  local tt=$((t - KA))   # V3 : SIGTERM a t - KA, SIGKILL du groupe au plus tard a t, donc avant FIN
  if [ "$tt" -lt 1 ]; then echo 124 > "$EX/$n.native.exit"; terminer 124 "etape $n NON lancee : il reste $t s, pas assez pour l'arret force de $KA s"; fi
  if [ "$fm" = "LOG" ]; then fm="$EX/$n.log"; else fm="$EX/$fm"; fi
  local t1 c
  t1=$(mono)
  if [ "$INJ" = "$n" ]; then
    if (exit 1) > "$EX/$n.log" 2>&1; then c=0; else c=$?; fi; echo "ECHEC INJECTE (test)" >> "$EX/$n.log"
  elif [ "$FACTICE" = "1" ] && [ "${R96_TEST_ENFANT_TETU:-}" = "$n" ]; then   # TEST seulement : enfant et petit-enfant sourds a SIGTERM
    if timeout --kill-after="$KA" "$tt" bash -c "trap '' TERM; (trap '' TERM; exec -a R96_TETU_PETIT_ENFANT sleep 100000) & exec -a R96_TETU_ENFANT sleep 100000" > "$EX/$n.log" 2>&1; then c=0; else c=$?; fi
    fm="$EX/$n.log"
  elif [ "$FACTICE" = "1" ]; then
    if timeout --kill-after="$KA" "$tt" bash -c "sleep $FDUREE; echo '$motif'" > "$EX/$n.log" 2>&1; then c=0; else c=$?; fi
    fm="$EX/$n.log"
  else
    if (cd "$EX" && timeout --kill-after="$KA" "$tt" nice -n 19 "$@" < /dev/null) > "$EX/$n.log" 2>&1; then c=0; else c=$?; fi
  fi
  echo "$c" > "$EX/$n.native.exit"
  echo "$(( $(mono) - t1 )) $tt $KA" > "$EX/$n.duree"
  if [ "$c" = "0" ] && grep -q -F -- "$motif" "$fm" 2>/dev/null; then
    touch "$EX/$n.ok"; note "$n : REUSSITE (code natif 0, motif « $motif » present) ; $(( $(mono) - t1 )) s (delai $tt s + arret force $KA s <= $t s)"; return 0
  fi
  [ "$c" = "137" ] && note "$n : ARRET FORCE (SIGKILL du groupe, code 137) au plus tard a la borne ($t s)"
  local cg="$c"; [ "$cg" = "0" ] && cg=2
  note "$n : ECHEC (code natif $c ; motif « $motif » $(grep -q -F -- "$motif" "$fm" 2>/dev/null && echo present || echo ABSENT))"
  terminer "$cg" "etape bloquante $n en echec"
}
DF=DONNEES_FIGEES
echo "T0 $T0 ; FIN $FIN ; ECHEANCE $ECHEANCE ; BUDGET $BUDGET ; COLLECTE $COLLECTE ; MARGE $MARGE ; RESV $RESV ; KA $KA ; VMIN $VMIN" > "$EX/ECHEANCES_MONO.txt"
note "debut lot X1 REP V2 dans $EX ; MemAvailable = $MEMKB kio ; ulimit -v $ULIM kio ; horloge monotone T0 $T0 ; etapes jusqu'a FIN = T0 + $((FIN - T0)) s ; verdict jusqu'a ECHEANCE = T0 + $((ECHEANCE - T0)) s ; collecte reservee $COLLECTE s + marge systemd $MARGE s ; arret force $KA s ; factice $FACTICE ; injection « $INJ »"
note "versions : $("$CC" --version 2>/dev/null | head -1 || echo 'cc ?') ; gp $("$GP" --version-short 2>/dev/null || echo ?) ; PY $("$PY" --version 2>&1) ; PYN $PYN ; $(uname -sr)"
note "chemins : PY=$PY PYN=$PYN GP=$GP CC=$CC"
# ---------------- E : environnement ----------------
run_step E00_numpy 120 "NUMPY DISPONIBLE" LOG "$PYN" -I -c 'import sys, numpy; print("python", sys.version.split()[0], "numpy", numpy.__version__, sys.executable); print("NUMPY DISPONIBLE")'
# ---------------- B : binaires natifs ----------------
run_step B01_compil_enum 300 "COMPILATION OK" LOG bash -c '"$0" --version | head -1 && "$0" -O2 -std=c11 -fno-fast-math -ffp-contract=off -o bin/enum_interval scripts/enum_interval.c -lm && sha256sum scripts/enum_interval.c bin/enum_interval && echo "COMPILATION OK"' "$CC"
run_step B02_compil_formes 300 "COMPILATION OK" LOG bash -c '"$0" -O2 -o bin/formes_canoniques scripts/formes_canoniques.c && sha256sum scripts/formes_canoniques.c bin/formes_canoniques && echo "COMPILATION OK"' "$CC"
run_step B03_controles_enum 300 "CONTROLES ENUM OK" LOG bash -c 'for e in E8 leech leech2_e8; do ./bin/enum_interval 5 < DONNEES_FIGEES/F1/$e.entree > sorties/B03_$e.sortie 2> sorties/B03_$e.err || exit 3; cmp sorties/B03_$e.sortie REFERENCE_MACHINE_A/F1_$e.sortie || exit 4; echo "$e : sortie identique a MACHINE_A"; done; echo "CONTROLES ENUM OK"'
# ---------------- R : raccords et parite (bibliotheque standard) ----------------
run_step R01_raccords 900 "BILAN : OK" LOG "$PY" -I scripts/raccord_entrees_f1_rep_v1.py $DF
run_step R02_parite 600 "PARITE : 56 + 1540 congruences vraies sur 1596" LOG "$PY" -I scripts/parite_x1_rep_v1.py $DF/X1/structure_x1.npz $DF/roiban_112/data/L56_gram.txt
run_step R03_theta56 300 "[ok]    norme 8 : 36 957 286 800 (somme des orbites de F3)" LOG "$GP" -q -D nbthreads=1 -f scripts/theta_extremale_56.gp
# ---------------- F : F1 des deux cotes (enum_interval natif) ----------------
run_step F01_F1_L 3600 "leaves 1" sorties/F1_L.sortie bash -c './bin/enum_interval 5 < DONNEES_FIGEES/F1/L_bkz40_rayon4.entree > sorties/F1_L.sortie 2> sorties/F1_L.err'
run_step F02_F1_L56 4200 "leaves 1" sorties/F1_L56.sortie bash -c './bin/enum_interval 5 < DONNEES_FIGEES/F1/L56.entree > sorties/F1_L56.sortie 2> sorties/F1_L56.err'
# ---------------- V : certificats, recouvrements, collisions ----------------
run_step V01_phi_X1 1200 "BILAN : OK" LOG "$PYN" -I scripts/verif_phi_L56_int64_v3.py $DF/roiban_112 $DF/X1/structure_x1.npz $DF/X1/certificats_X1 $DF/X1/min_reps_L.npz
run_step V02_indep_X1 7200 "VERDICT X1 (regle propre a X1) : nb_touches88 = 0 ; deux cotes impairs : True ; controles : OK -> CONFORME" LOG "$PYN" -I scripts/verif_independante_int16_v3.py $DF/roiban_112 $DF/X1/structure_x1.npz $DF/X1/donnees_L.npz $DF/X1/norm8_reps_L.npz $DF/X1/min_reps_L.npz $DF/X1/certificats_X1 bin/formes_canoniques sorties/X1_int16 1
run_step V03_indep_X4 7200 "-> CONFORME (touches trouvees)" LOG "$PYN" -I scripts/verif_independante_int16_v3.py $DF/roiban_112 $DF/X4/structure_X4.npz $DF/X4/donnees_L4.npz $DF/X4/norm8_reps_L4.npz $DF/X4/min_reps_L4.npz $DF/X4/certificats bin/formes_canoniques sorties/X4_int16 4
# ---------------- VERDICT TERMINAL ----------------
if verdict_terminal; then cg=0; else cg=$?; fi   # V3 : borne par ECHEANCE ; non lance (124) si le temps manque ; jamais de second verdict
echo "$cg" > "$EX/GLOBAL.native.exit"; mono > "$EX/FIN_MONO.txt"; note "CODE GLOBAL $cg (0 = replication X1 conforme selon le verdict ; sinon aucune conclusion)"
exit "$cg"
