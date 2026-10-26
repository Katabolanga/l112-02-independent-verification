#!/usr/bin/env bash
# fetch_roiban_data.sh -- download the public files of roiban1344 listed in ROIBAN_FILES.tsv into data/frozen/ and check
# their SHA-256. Nothing is redistributed by this repository: the files come from roiban1344's repositories (data and texts
# under CC BY 4.0, code under MIT). A file already present with the expected hash is kept; otherwise it is downloaded to
# <file>.part, checked, and only then renamed (a file with a wrong hash is kept as <file>.mismatch). Needs bash, curl and sha256sum (or shasum -a 256).
# Usage (from the repository root):  bash data/roiban/fetch_roiban_data.sh
# The download locations can be replaced (mirror, local copy for testing) with the environment variables
#   ROIBAN_RAW_BASE      default https://raw.githubusercontent.com/roiban1344
#   ROIBAN_RELEASE_BASE  default https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice/releases/download
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HERE/../frozen"
RAW="${ROIBAN_RAW_BASE:-https://raw.githubusercontent.com/roiban1344}"
REL="${ROIBAN_RELEASE_BASE:-https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice/releases/download}"
if command -v sha256sum >/dev/null; then SHA=(sha256sum); else SHA=(shasum -a 256); fi
hash_of() { "${SHA[@]}" "$1" | awk '{print $1}'; }
n=0
while IFS=$'\t' read -r path want bytes src; do
  case "$path" in ''|'#'*) continue;; esac
  kind="${src%%:*}"; rest="${src#*:}"; repo="${rest%%@*}"; rest="${rest#*@}"; ref="${rest%%:*}"; file="${rest#*:}"
  case "$kind" in
    git) url="$RAW/$repo/$ref/$file";;
    release) url="$REL/$ref/$file";;
    *) echo "unknown source kind in ROIBAN_FILES.tsv: $src" >&2; exit 2;;
  esac
  out="$DEST/$path"; mkdir -p "$(dirname "$out")"
  if [ -f "$out" ] && [ "$(hash_of "$out")" = "$want" ]; then echo "present  $path"; n=$((n + 1)); continue; fi
  curl -fsSL --retry 3 -o "$out.part" "$url"          # -o overwrites a previous partial file
  got="$(hash_of "$out.part")"
  if [ "$got" != "$want" ]; then
    mv -f "$out.part" "$out.mismatch"; echo "SHA-256 MISMATCH for $path: got $got, expected $want ($url); kept as $out.mismatch" >&2; exit 1
  fi
  mv -f "$out.part" "$out"; echo "fetched  $path"; n=$((n + 1))
done < "$HERE/ROIBAN_FILES.tsv"
echo "OK: $n files of roiban1344 present in data/frozen/ with the expected SHA-256"
