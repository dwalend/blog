#!/usr/bin/env bash
# Check every URL the local _site build produces against a live base URL.
#
#   npx @11ty/eleventy          # build _site first, so the list is current
#   bin/sweep.sh https://blog.walend.net
#
# Exits non-zero if any URL is not 200, or if the sanity check does not 404.
set -uo pipefail

BASE="${1:?usage: bin/sweep.sh BASE_URL}"
BASE="${BASE%/}"
SITE="${SITE:-$(cd "$(dirname "$0")/.." && pwd)/_site}"

if [ ! -d "$SITE" ]; then
  echo "no build at $SITE - run: npx @11ty/eleventy" >&2
  exit 2
fi

fail=0
n=0
while IFS= read -r path; do
  n=$((n + 1))
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$BASE$path")
  if [ "$code" != "200" ]; then
    echo "FAIL $code  $BASE$path"
    fail=$((fail + 1))
  fi
done < <(cd "$SITE" && find . -type f \
  \( -name '*.html' -o -name '*.xml' -o -name '*.txt' \
     -o -name '*.css' -o -name '*.png' -o -name '*.xsl' \) \
  | sed 's|^\.||; s|/index\.html$|/|' | sort)

echo "--- checked $n URLs, $fail failures ---"

# A checker that cannot fail is not a checker. This URL must 404.
sanity=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$BASE/definitely-not-a-page-$RANDOM/")
echo "sanity check (want 404): $sanity"

[ "$fail" -eq 0 ] && [ "$sanity" = "404" ]
