## NAME ##

convert2mp4 - Convert video file to mp4 for AMS streaming.

## DESCRIPTION ##

Convert2mp4 is a tool to convert video files into mp4
files that can be streamed by the Flash Media Server.  It
uses libx264 and libfdk_aac via ffmpeg to transcode the content.

## SYNOPSIS ##

    convert2mp4 [options] input_file [output_prefix]

To get a list of options and their descriptions, run convert2mp4
with the --help option

## SETUP ##

Before running script, you will want to edit the main configuration
file to set paths of many of the utilities and that the script
uses.  Probably the most important variable you'll want to change
is the path to encoding profile.  It will look something like this:

    [profiles]
    path = profiles-hidvl.xml

This is an xml file that lists the attributes such as dimensions
and bitrate for your output files.  If this is not a full path,
convert2mp4 will look in the conf/ directory for this file.

Another notable variable is the preset variable:

    [video]
    preset = default

This is where you can set some advanced options for the x264
library like the keyframe rate interval or GOP.

## EXAMPLES ##

To convert a video and use the hidvl preset

    ./convert2mp4.pl --video_preset hidvl input.mkv ouput

To convert a video containing a set of videos and write the out
put files in the same directory.

    ./convert2mp4.pl --profiles_path profiles-talking-heads.xml \
        Interviews.mov

To convert a video and force keyframes at specified intervals,
first create a text file containing those timecodes and run
something like

    ./convert2mp4.pl -k timecodes.txt ~/Videos/Breaking.Bad.avi \
        ~/my/output/directory/out

To add a watermark to your videos, specify the path to the
watermark image (preferably a transparent png) via the '-w' or
'--watermark' option.  For example,

    ./convert2mp4.pl -w /data/copyright.png /media/broadcast.mp4

That will place the watermark in the lower-right corner and it
will be 40% as wide as the output video.  To customize the size
and placement of the watermark, specify '-w' option as

    -w filename:orientation:width_percentage

So, the following invokation

    ./convert2mp4.pl -w /home/rasan/watermark.png:C:50 input.mkv

will center the watermark and it will be 50% of the video's width.
Possible values for placement are TL (top-left), TR (top-right),
BL (bottom-left), BR (bottom-right), C (center).

For more options, run with the -h or --help switch.

## REQUIREMENTS ##

Perl with the following modules:

    AppConfig
    IO::CaptureOutput
    Log::Log4perl
    Time::Duration

FFmpeg (http://www.ffmpeg.org/) compiled with x264 and libfdk_aac.

## INSTALLATION ##

The easiest way is install using the rpm provided.

    sudo rpm -Uvh convert2mp4-<version>.noarch.rpm

## AUTHOR ##

    Rasan Rasch (rasan@nyu.edu)

## SEE ALSO ##

    http://flowplayer.org/forum/7/12671
    http://sites.google.com/site/linuxencoding/x264-ffmpeg-mapping
    http://rob.opendot.cl/index.php/useful-stuff/ffmpeg-x264-encoding-guide/
    http://rob.opendot.cl/index.php/useful-stuff/x264-to-ffmpeg-option-mapping/
    https://www.virag.si/2012/01/web-video-encoding-tutorial-with-ffmpeg-0-9/
    https://documentation.apple.com/en/finalcutpro/usermanual/index.html#chapter=106%26section=6%26tasks=true
    https://wiki.libav.org/Encoding/aac
    https://trac.ffmpeg.org/wiki/Encode/AAC

