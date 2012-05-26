#!/usr/bin/python2.7
# -*- coding: utf-8 -*

#this is qrencode v.1.01 code
#sudo easy_install qrencode
import qrencode


(version, size, img) = qrencode.encode_scaled('https://shackspace.de/wiki/doku.php', 500, level=3, version=3)
img.save('qrcode.png')

