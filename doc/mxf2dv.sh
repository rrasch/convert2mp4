#!/bin/bash
#
# mxf2dv.sh

set -ex

OUTPUT_DIR="/mnt/easystore"

#        -max_muxing_queue_size 1024 \
for f in `cat input.txt`; do
    outfile="$OUTPUT_DIR/`basename $f .mxf`.dv"
    echo ffmpeg -y -i $f \
		-t 10 \
        -s 720x480 \
		-vcodec dvvideo
		-pix_fmt yuv422p \
        $outfile
done

