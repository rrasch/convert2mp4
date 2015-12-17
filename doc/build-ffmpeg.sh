#!/bin/bash
#
# Script to compile FFmpeg 2.1.6
#
# Author: Rasan Rasch <rasan@nyu.edu>

FFMPEG_HOME="/usr/local/ffmpeg-2.1.6"

sudo mkdir -p $FFMPEG_HOME/lib

make clean

./configure \
    --prefix=/usr/local/ffmpeg-2.1.6 \
    --arch=x86_64 \
    --optflags="-O2 -g" \
    --enable-runtime-cpudetect \
    --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-version3 \
    --enable-bzlib \
    --enable-frei0r \
    --enable-gnutls \
    --enable-libass \
    --enable-libcdio \
    --enable-libdc1394 \
    --enable-libfaac --enable-nonfree \
    --enable-libfdk_aac --enable-nonfree \
    --enable-libfreetype \
    --enable-libgsm \
    --enable-libmp3lame \
    --enable-openal \
    --enable-libopencv \
    --enable-libopenjpeg \
    --enable-libopus \
    --enable-libpulse \
    --enable-librtmp \
    --enable-libschroedinger \
    --enable-libsoxr \
    --enable-libspeex \
    --enable-libtheora \
    --enable-libvorbis \
    --enable-libv4l2 \
    --enable-libvpx \
    --enable-libx264 \
    --enable-libxvid \
    --enable-x11grab \
    --enable-avfilter \
    --enable-avresample \
    --enable-postproc \
    --enable-pthreads \
    --disable-static \
    --enable-shared \
    --enable-gpl \
    --disable-debug \
    --disable-stripping \
    --extra-ldflags="-Wl,-rpath $FFMPEG_HOME/lib"

make

sudo make install

