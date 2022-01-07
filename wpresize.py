#! /usr/bin/env python
# ブログ(wordpress)アップロード用に画像サイズを調整する

import argparse
import re, os
from PIL import Image
import piexif
from logging import getLogger, StreamHandler, DEBUG, INFO

# ログ設定
loggerLevel = DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(loggerLevel)
logger.setLevel(loggerLevel)
logger.addHandler(handler)
logger.propagate = False

# 引数解釈
parser = argparse.ArgumentParser(description='wpresize.py resize imagefile for wordpress')
parser.add_argument('infile', nargs='+', help='input image file(jpg etc.)')
parser.add_argument('-f', '--force', action='store_true', help='overwrite origin file.')
parser.add_argument('-q', '--quality', metavar='QUALITY', help='output jpeg quality. default: 90', type=int, choices=range(0,101), default=90)
parser.add_argument('-l', '--length', metavar='MAXLEN', help='max length of image (width or height)', type=int, default=1800)
args = parser.parse_args()

maxl = args.length

def main():
    for fn in args.infile:
        pn = os.path.dirname(fn)
        bn = os.path.basename(fn)
        bn1 = os.path.splitext(bn)[0]
        ext = os.path.splitext(bn)[1]
        if re.match('^\.(jpg|jpeg)$', ext.lower()):
            if args.force:
                outfile = fn
            else:
                outfile = os.path.join(pn, bn1 + '_f' + ext)
            im = Image.open(fn)
            w, h = im.size
            exif = im.info['exif']
            exif_dict = piexif.load(exif)
            logger.debug('name: %s, ext: %s (%d x %d)' % (bn, ext, w, h))
            del exif_dict['GPS']
            exif = piexif.dump(exif_dict)
            if w > h and w > maxl:
                w1 = maxl
                h1 = int(maxl * h / w)
            elif h > w and h > maxl:
                h1 = maxl
                w1 = int(maxl * w / h)
            logger.debug('resize to (%d x %d)' % (w1, h1))
            rim = im.resize([w1, h1], Image.BICUBIC)
            logger.debug(outfile)
            rim.save(outfile, quality=args.quality, exif=exif)

if __name__ == '__main__':
    main()
