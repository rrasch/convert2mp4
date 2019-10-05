#!/bin/bash
#
# Script to compile FFmpeg 2.1
#
# Author: Rasan Rasch <rasan@nyu.edu>

X264_HOME="/usr/local/x264-0.152.2854+gite9a5903"
FFMPEG_HOME="/usr/local/ffmpeg-2.1.6"

export CFLAGS="-I$X264_HOME/include"
export CXXFLAGS="-I$X264_HOME/include"
export LDFLAGS="-L$X264_HOME/lib -Wl,-rpath,$X264_HOME/lib,-rpath,$FFMPEG_HOME/lib"

sudo mkdir -p $FFMPEG_HOME/lib

make clean

# Ubuntu 18.04: disable opencv, schroedinger, openjpeg, and docs
# https://ffmpeg.org/pipermail/ffmpeg-devel/2017-March/209128.html

./configure \
    --prefix=$FFMPEG_HOME \
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
    --disable-libopencv \
    --disable-libopenjpeg \
    --enable-libopus \
    --enable-libpulse \
    --enable-librtmp \
    --disable-libschroedinger \
    --enable-libsoxr \
    --enable-libspeex \
    --enable-libtheora \
    --enable-libvorbis \
    --enable-libv4l2 \
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
    --disable-doc

make

sudo make install

