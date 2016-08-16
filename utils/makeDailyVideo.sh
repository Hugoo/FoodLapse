#!/bin/sh
cd /
cd home/pi/prog/raw
#Rename pictures so the numbers are ok
ls *.jpg| awk 'BEGIN{ a=0 }{ printf "mv %s imgr%04d.JPG\n", $0, a++ }' | bash
DATE=$(date +%Y-%m-%d -d "yesterday")
avconv -r 20 -start_number 0001 -i imgr%4d.JPG -q:v 0 -vcodec libx264 -crf 25 ../html/videos/foodcam${DATE}.mp4
rm *.JPG
cd /
