PDFMP3
------

Create a PDF art covert from an mp3 dir


Usage:
-------

Optional a musicbrainz account could be useful, set the following env variables:

- MUSICBRAINZ_LOGIN
- MUSICBRAINZ_PWD

Shell:

	# create art cover
	python app.py ~/Music/sandisk
	# build pdf
	./run.sh ~/Music/sandisk
	#optional convert flac and m4a to mp3
	./flac2mp3 ~/Music/sandisk


Dependencies:
-------------
Python : musizbrainz and identicon
Shell : montage from ImageMagick and ffmpeg for flac2mp3
Font : LatoB

Author:
-------
Sébastien Campion

Licence:
---------
AGPLv3

