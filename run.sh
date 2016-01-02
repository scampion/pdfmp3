#!/bin/bash
#export PYTHONPATH=/Users/scampion/src/pdfmp3/python-musicbrainzngs
#python app.py $1
rm -Rf tmp
mkdir tmp
cd tmp

find "$1" -name 'artcover*' -print0 | while IFS= read -r -d $'\0' line; do
    FILENAME=$(basename "${line/artcover_/}")
    FILENAME=$(basename "${FILENAME/.jpg/}")    
    FILENAME=$(echo $FILENAME | cut -c 1-45)
    echo $FILENAME
    cp "$line" "$FILENAME"
done

montage  -pointsize 10 -label '%f'   -tile x1 -page A4 * -tile 2x3   -geometry 220x220+5+5 -font "LatoB"  -gravity center ../catalog.pdf
