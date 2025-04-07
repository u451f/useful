#!/bin/sh
# takes only ".jpg", not ".JPG", not ".jpeg"
#

OUTPUTFILE="outputvideo.mp4"

ffmpeg -framerate 1/10 -pattern_type glob -i '*.jpg' -c:v libx264 -filter_complex "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -pix_fmt yuv420p -r 30 $OUTPUT
