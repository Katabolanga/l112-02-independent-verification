#!/bin/bash
# compiler_lean.sh -- agent 116 : compile un fichier .lean contre Mathlib v4.32.0 locale (~/lean_mathlib_4_32), sans reseau,
# sans lake update (lake env lean seulement). usage : compiler_lean.sh FICHIER.lean SORTIE.log
export PATH="$HOME/.elan/bin:$PATH"
F="$1"; OUT="$2"
cd "$HOME/lean_mathlib_4_32" || exit 2
( date '+debut %Y-%m-%d %H:%M:%S'; timeout 3600 nice -n 19 lake env lean "$F"; echo "code $?"; date '+fin %Y-%m-%d %H:%M:%S' ) > "$OUT" 2>&1
