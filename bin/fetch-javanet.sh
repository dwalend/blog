#!/usr/bin/env bash
# Recover the 2003-2009 weblogs.java.net/blog/dwalend posts from the wayback
# machine into _archive-src/javanet/ as raw HTML, one file per article.
#
#   bin/fetch-javanet.sh          # fetch what is missing
#   bin/fetch-javanet.sh --list   # just show what would be fetched
#
# Resumable: files already present are skipped, so re-running after an
# interruption costs nothing. Nothing here touches src/ or the built site.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/_archive-src/javanet"
CDX="$OUT/cdx.txt"
mkdir -p "$OUT"

CDX_URL="https://web.archive.org/cdx/search/cdx?url=weblogs.java.net%2Fblog%2Fdwalend*&fl=original,timestamp,statuscode&collapse=urlkey&filter=statuscode:200"

if [ ! -s "$CDX" ]; then
  echo "querying CDX (this endpoint is often slow; be patient)..."
  curl -sS --max-time 600 --retry 3 --retry-delay 15 "$CDX_URL" -o "$CDX" || {
    echo "CDX query failed. Re-run; a timeout here means try again, not that anything is lost." >&2
    exit 1
  }
fi
echo "CDX rows: $(wc -l < "$CDX")"

# Article pages look like .../YYYY/MM/slug.html - note Movable Type puts them
# under /archive/, so do NOT filter that out; requiring the YYYY/MM/ date path
# already excludes the category listings like /archive/web_services_and_xml/.
# Drop index pages and the %23comments artifacts.
articles=$(awk '{print $1" "$2}' "$CDX" \
  | grep -E '/(19|20)[0-9]{2}/[0-9]{2}/[^/]+\.html' \
  | grep -v -i -E 'index\.html|%23|#comments' \
  | sort -u)

count=$(printf '%s\n' "$articles" | grep -c . || true)
echo "article snapshots: $count"

if [ "${1:-}" = "--list" ]; then
  printf '%s\n' "$articles"
  exit 0
fi

got=0; skipped=0; failed=0
while read -r url ts; do
  [ -z "${url:-}" ] && continue
  # _archive-src/javanet/2003-09-defending_autob.html
  slug=$(printf '%s' "$url" | sed -E 's#.*/((19|20)[0-9]{2})/([0-9]{2})/([^/]+)\.html.*#\1-\3-\4#')
  dest="$OUT/$slug.html"
  if [ -s "$dest" ]; then skipped=$((skipped+1)); continue; fi
  # id_ returns the original bytes with no wayback toolbar injection.
  if curl -sS --max-time 120 --retry 2 --retry-delay 5 \
       "https://web.archive.org/web/${ts}id_/${url}" -o "$dest"; then
    if [ -s "$dest" ]; then
      got=$((got+1)); echo "  $slug"
    else
      rm -f "$dest"; failed=$((failed+1)); echo "  EMPTY $slug" >&2
    fi
  else
    rm -f "$dest"; failed=$((failed+1)); echo "  FAIL  $slug" >&2
  fi
  sleep 1   # be polite to the archive
done <<< "$articles"

echo "--- fetched $got, skipped $skipped already present, $failed failed ---"
echo "raw HTML in $OUT"
