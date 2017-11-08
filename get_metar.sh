#!/bin/sh
#
# Finnish Meteorological Institute / Mikko Rauhala (2015-2017)
#
# SmartMet Data Ingestion Module for METAR Observations
#

URL=http://tgftp.nws.noaa.gov/data/observations/metar/cycles

if [ -d /smartmet ]; then
    BASE=/smartmet
else
    BASE=$HOME/smartmet
fi

IN=$BASE/data/incoming/metar
OUT=$BASE/data/gts/metar/world/querydata
EDITOR=$BASE/editor/in
TMP=$BASE/tmp/data/metar
TIMESTAMP=`date -u +%Y%m%d%H%M`

METARFILE=$TMP/${TIMESTAMP}_gts_world_metar.sqd

# Use log file if not run interactively
if [ $TERM = "dumb" ]; then
    exec &> $LOGFILE
fi
mkdir -p $TMP $OUT

echo "URL: $URL"
echo "IN:  $IN"
echo "OUT: $OUT"
echo "TMP: $TMP"
echo "METAR File: $METARFILE"

for i in {0..23}
do
    wget --no-verbose --retry-connrefused --read-timeout=30 --tries=20 -N -P $IN $URL/$(printf %02d $i)Z.TXT
done

# Do METAR stations
metar2qd -n "$IN/*.TXT" > $METARFILE

if [ -s $METARFILE ]; then
    lbzip2 -k $METARFILE
    mv -f $METARFILE $OUT
    mv -f ${METARFILE}.bz2 $EDITOR
fi

rm -f $TMP/*metar*
