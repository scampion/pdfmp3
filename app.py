from __future__ import print_function
import os, sys, urllib
import traceback
import musicbrainzngs
from mutagen import File
import shutil
import identicon
import random
from PIL import ImageFont
from PIL import ImageDraw
import re

def sub_dir(path):
    return [os.path.join(path, sub) for sub in os.listdir(path) if os.path.isdir(os.path.join(path, sub))]


login = os.environ.get("MUSICBRAINZ_LOGIN")
pwd = os.environ.get("MUSICBRAINZ_PWD")
musicbrainzngs.auth(login, pwd)
musicbrainzngs.set_useragent("PdfMp3", "0.1", "http://pdfmp3.fr")
rootdir = sys.argv[1]



def search(release_path, ext=None):
    query = os.path.basename(release_path)
    odir = os.path.abspath(release_path)
    if ext:
        odir = os.path.abspath(ext)
        query += " " + os.path.basename(ext)

    print (query, odir)
    jpg_query = "artcover_%s.jpg" % query
    ofile = os.path.join(odir, jpg_query)
    if os.path.exists(ofile):
        return query, ofile

    return jpgindir(release_path, query, ofile)


def MusicBrainz(release_path, query, ofile):
    try:
        r = musicbrainzngs.search_releases(query.replace('-', ''))
        id = r['release-list'][0]['id']
        img = musicbrainzngs.get_image_list(id)
        url = img['images'][0]['image']
        urllib.urlretrieve(url, ofile)
        print("OK " + ofile)
        return query, ofile
    except Exception as e:
        print("Error for %s (%s)" % (release_path, e))
        traceback.print_exc()
        return genimage(release_path, query, ofile)


def APICFrame(release_path, query, ofile):
    try:
        for f in os.listdir(release_path):
            if f.endswith("mp3") and not f.startswith("."):
                mp3file = os.path.join(release_path, f)
                print ("APIC search for ", mp3file)
                file = File(mp3file)
                for k, v in file.tags.items():
                    if k.startswith("APIC:"):
                        artwork = v.data
                        with open(ofile, 'wb') as img:
                           img.write(artwork)
                        print ("APIC img found ", query, ofile)
                        return query, ofile
    except Exception as e:
        print ("Error for %s (%s)" % (release_path, e))
        traceback.print_exc()
    return MusicBrainz(release_path, query, ofile)

def jpgindir(release_path, query, ofile):
    for f in os.listdir(release_path):
        if (f.endswith("jpg") or f.endswith('jpeg') or f.endswith('JPEG') or f.endswith('JPG')) and not f.startswith("artcover") and not f.startswith("."):
            jpgfile = os.path.join(release_path, f)
            print ("Copy : ", jpgfile, ofile)
            shutil.copy(jpgfile, ofile)
            return query, ofile
    return APICFrame(release_path, query, ofile)

def genimage(release_path, query, ofile):
    font = ImageFont.truetype("YanoneKaffeesatz-Bold.otf", 80 )
    img = identicon.render_identicon(random.randint(0, 99999999), 300)
    draw = ImageDraw.Draw(img)
    text = ""
    for l in query.split('-'):
        text += re.sub("(.{30})", "\\1\n", l, 0, re.DOTALL)
        text += "\n"
    draw.multiline_text((100, 300),text,(44,44,44),font=font, align='center')
    img.save(ofile)
    return query, ofile


def search_art_cover():
    for letter in sub_dir(rootdir):
        if letter.endswith("_compilation"):
            continue
        for release_or_artist in sub_dir(letter):
            is_artist = True if sub_dir(release_or_artist) else False
            # print release_or_artist, " is artist ", is_artist, sub_dir(release_or_artist)
            if is_artist:
                for release in sub_dir(release_or_artist):
                    search(release_or_artist, release)
            else:
                search(release_or_artist)


# search_art_cover()

f1 = open('catalog.txt', 'w')
for letter in sub_dir(rootdir):
    if letter.endswith("_compilation"):
        continue
    for release_or_artist in sub_dir(letter):
        is_artist = True if sub_dir(release_or_artist) else False
        # print release_or_artist, " is artist ", is_artist, sub_dir(release_or_artist)
        if is_artist:
            for release in sub_dir(release_or_artist):
                name, jpgpath = search(release_or_artist, release)
                f1.write("%s ; %s\n" % (name, jpgpath))
        else:
            name, jpgpath = search(release_or_artist)
            f1.write("%s ; %s\n" % (name, jpgpath))