#!/bin/sh
#
# Finnish Meteorological Institute / Mikko Rauhala (2015-2017)
#
# SmartMet Data Ingestion Module for METAR Observations
#

TIMESTAMP=`date +%Y%m%d%H%M`

if [ -d /smartmet ]; then
    IN=/smartmet/data/incoming/metar
    OUT=/smartmet/data/gts/metar/world/querydata/
    TMP=/smartmet/tmp/data/metar_${TIMESTAMP}
    EDITOR=/smartmet/editor/in/
else
    IN=$HOME/data/incoming/metar
    OUT=$HOME/data/gts/metar/world/querydata/
    TMP=/tmp/data_metar_${TIMESTAMP}
    EDITOR=$HOME/editor/in/
fi
METARFILE=${TMP}/${TIMESTAMP}_gts_world_metar.sqd

# Log everything
#if [ ! -z "$ISCRON" ]; then
#    exec &> $LOGFILE
#fi

echo "Temporary directory: $TMP"
echo "Output directory: $OUT"
echo "Output file: $(basename $METARFILE)"

mkdir -p ${TMP}

for i in {0..23}
do
    wget --no-verbose --retry-connrefused --read-timeout=30 --tries=20 -N -P $IN http://tgftp.nws.noaa.gov/data/observations/metar/cycles/$(printf %02d $i)Z.TXT
done

# Do METAR stations
metar2qd -n "$IN/*.TXT" > $METARFILE
bzip2 -k $METARFILE

if [ -s $METARFILE ]; then
    mv -f $METARFILE $OUT/
    mv -f ${METARFILE}.bz2 $EDITOR/
fi
rmdir ${TMP}
