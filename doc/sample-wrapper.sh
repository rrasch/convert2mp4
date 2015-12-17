#!/bin/bash
#
# Sample wrapper script for convert2mp4
#
# Author: Rasan Rasch <rasan@nyu.edu>

trap "" HUP

XFER_DIR=/my/path/to/content/prod/xfer/rosie

if [ "`hostname -s`" = "myhost" ]; then
# 	OUTPUT_DIR=/data/vidproc/encode/rosie
	OUTPUT_DIR=/my/path/to/content/prod/rosie
	LINE_FILTER=1
else
	OUTPUT_DIR=/my/path/to/content/dev/rosie
	LINE_FILTER=0
fi

# Process odd numbered files on myhost and even numbered
# files dev-myhost
FILES=`find $XFER_DIR -name '*.mov' \
	| sort | awk "NR % 2 == $LINE_FILTER"`

# current date/time, e.g. 2010-07-13-20-14-59
NOW=$(date +"%Y-%m-%d-%H-%M-%S")

# log both stdout/stderr to this file
LOGFILE=../logs/convert2mp4-$NOW.log

LOGDIR=`dirname $LOGFILE`
[ ! -d "$LOGDIR" ] && mkdir -p $LOGDIR
# exec 1> >(tee -a $LOGFILE) 2>&1
exec > $LOGFILE 2>&1

for mov in $FILES
do
	short_name=`basename $mov`
	if grep -q $short_name results.txt; then
		echo "Skipping $short_name, already processed."
		continue
	fi
	echo Processing $short_name
	mp4_prefix=$OUTPUT_DIR/`echo $short_name | sed 's/.mov$//'`
	./convert2mp4.pl $mov $mp4_prefix
	RETVAL=$?
	if [ $RETVAL -eq 0 ]; then
		STATUS=PASS
	else
		STATUS=FAIL
	fi
	echo "$short_name: $STATUS" >> results.txt
done

