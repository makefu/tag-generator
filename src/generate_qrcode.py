#!/usr/bin/python2.7
# -*- coding: utf-8 -*

#this is qrencode v.1.01 code
#sudo easy_install qrencode
import qrencode
import sys

width = 500
content = sys.argv[1]
(version, size, img) = qrencode.encode_scaled(content, width,  level=3, version=5)
img.save('qrcode.png', "PNG")

