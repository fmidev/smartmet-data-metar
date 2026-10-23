#!/bin/bash
#
# Finnish Meteorological Institute / Mikko Rauhala (2015-2017)
#
# SmartMet Data Ingestion Module for METAR Observations
#

# No `set -e`: a failed download of one cycle file must not stop the rest,
# and the `-s` size check below gates distribution.
set -uo pipefail

# Prevent parallel runs; the lock is released automatically when we exit
exec 9> /tmp/smartmet-data-metar.lock
flock -n 9 || exit 1

URL=https://tgftp.nws.noaa.gov/data/observations/metar/cycles

if [ -d /smartmet ]; then
    BASE=/smartmet
else
    BASE=$HOME/smartmet
fi

IN=$BASE/data/incoming/metar
OUT=$BASE/data/gts/metar/world/querydata
EDITOR=$BASE/editor/in
TMP=$BASE/tmp/data/metar
LOGFILE=$BASE/logs/data/metar.log
TIMESTAMP=$(date -u +%Y%m%d%H%M)

METARFILE=$TMP/${TIMESTAMP}_gts_world_metar.sqd

# Use log file if not run interactively
if [ "${TERM:-}" = "dumb" ]; then
    exec &> "$LOGFILE"
fi

mkdir -p "$IN" "$TMP" "$OUT" "$EDITOR"
trap 'rm -f "$TMP"/*metar*' EXIT

echo "URL: $URL"
echo "IN:  $IN"
echo "OUT: $OUT"
echo "TMP: $TMP"
echo "METAR File: $METARFILE"

for i in {0..23}
do
    wget --no-verbose --retry-connrefused --read-timeout=30 --tries=20 -N -P "$IN" "$URL/$(printf %02d "$i")Z.TXT"
done

# Do METAR stations
metar2qd -n "$IN/*.TXT" > "$METARFILE"

if [ -s "$METARFILE" ]; then
    lbzip2 -k "$METARFILE"
    mv -f "$METARFILE" "$OUT"/
    mv -f "${METARFILE}.bz2" "$EDITOR"
fi
