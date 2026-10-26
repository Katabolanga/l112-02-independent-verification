#!/usr/bin/env bash
# assemble_package.sh -- build, from this repository, a NEW replication package with the layout expected by
# lancer_x1_rep_v2.sh (the launcher that was run on machine B): lanceurs/, scripts/, verificateur/, DONNEES_FIGEES/,
# REFERENCE_MACHINE_A/ and SHA256SUMS.txt. Every input is first checked against SHA256SUMS.txt of the repository and,
# for the files of roiban1344, against data/roiban/ROIBAN_FILES.tsv. Nothing in the repository is modified.
#
# Usage, from the repository root (Linux or WSL; bash, coreutils, awk):
#   bash data/roiban/fetch_roiban_data.sh                  # downloads the public files of roiban1344 (about 14 MB)
#   bash code/replication/assemble_package.sh NEW_DIR      # NEW_DIR must not exist
#   cd NEW_DIR && PY=/usr/bin/python3 PYN=/path/to/python3-with-numpy GP=/path/to/gp CC=/usr/bin/gcc \
#       bash lanceurs/lancer_x1_rep_v2.sh RUN_1           # RUN_1: a new sub-directory, created by the launcher
# The launcher refuses to start if MemAvailable < 10 GiB (variable R96_MEM_ADMISSION_KIO, in KiB) and runs every step
# under ulimit -v 6 GiB (R96_ULIMIT_KIO), with one thread, in series. Its global time budget is 18 000 s (R96_BUDGET_GLOBAL).
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEST="${1:?usage: bash code/replication/assemble_package.sh NEW_DIR}"
if [ -e "$DEST" ]; then echo "ERROR: $DEST already exists (a new directory is required)"; exit 10; fi
cd "$REPO"
echo "checking the repository files used by the package against SHA256SUMS.txt ..."
grep -E '^[0-9a-f]{64}  (code/verification|code/replication|data/frozen|logs/machine_A/reference_for_replication)/' SHA256SUMS.txt \
  | sha256sum -c --quiet -
echo "checking the files of roiban1344 against data/roiban/ROIBAN_FILES.tsv ..."
awk -F'\t' '!/^#/ && NF >= 4 && $1 ~ /^roiban_112\// {print $2 "  data/frozen/" $1}' data/roiban/ROIBAN_FILES.tsv \
  | sha256sum -c --quiet - || { echo "ERROR: run bash data/roiban/fetch_roiban_data.sh first"; exit 12; }
mkdir -p "$DEST"/lanceurs "$DEST"/scripts "$DEST"/verificateur "$DEST"/REFERENCE_MACHINE_A \
         "$DEST"/DONNEES_FIGEES/roiban_112/data "$DEST"/DONNEES_FIGEES/roiban_112/certificates
cp -p code/replication/lancer_x1_rep_v2.sh "$DEST/lanceurs/"
cp -p code/replication/verdict_x1_rep_v2.py "$DEST/verificateur/"
for f in enum_interval.c formes_canoniques.c parite_x1_rep_v1.py raccord_entrees_f1_rep_v1.py theta_extremale_56.gp \
         verdict_x1_v3_POUR_MEMOIRE.py verif_independante_int16_v3.py verif_phi_L56_int64_v3.py; do
  cp -p "code/verification/$f" "$DEST/scripts/"
done
cp -Rp data/frozen/F1 data/frozen/X1 data/frozen/X4 "$DEST/DONNEES_FIGEES/"
for f in data/L56_gram.txt data/sl2_29_generators.txt certificates/reduction_L.txt certificates/centralizer.npz \
         certificates/min_reps.npz certificates/norm8_reps.npz; do
  cp -p "data/frozen/roiban_112/$f" "$DEST/DONNEES_FIGEES/roiban_112/$f"
done
cp -Rp logs/machine_A/reference_for_replication/. "$DEST/REFERENCE_MACHINE_A/"
(cd "$DEST" && find scripts verificateur DONNEES_FIGEES REFERENCE_MACHINE_A lanceurs -type f | LC_ALL=C sort \
   | while IFS= read -r f; do sha256sum "$f"; done) > "$DEST/SHA256SUMS.txt"
echo "package assembled in $DEST ($(grep -c . "$DEST/SHA256SUMS.txt") files)."
echo "next: cd $DEST && PY=... PYN=... GP=... CC=... bash lanceurs/lancer_x1_rep_v2.sh RUN_1"
