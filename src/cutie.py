#!/usr/bin/python
import Image, ImageDraw, ImageFont, PIL


heading = "A Hacker known as Karl Koch"
text = "Es ist verboten toten Kojoten die Hoden zu verknoten!"


#----------------------------------------
im = Image.open("resources/A6_300dpi.png")
qr = Image.open("qrcode.png")
qr.convert('RGB')
im.convert('RGB')
headingFontsize = 70
headingFont = ImageFont.truetype("resources/arialbd.ttf", headingFontsize)

textFontsize = 40
textFont = ImageFont.truetype("resources/arial.ttf", textFontsize)

offsetX = 340  #offset for the shackspace logo on the leftside




draw = ImageDraw.Draw(im)
#Heading
headingWidth, headingHeight = draw.textsize(heading, font=headingFont)
draw.text((((im.size[0]- offsetX)/2) - (headingWidth/2 - offsetX), im.size[1]/8), heading, font=headingFont, fill="#000000") 

#Text
textWidth, textHeight = draw.textsize(text, font=textFont)
draw.text((((im.size[0]- offsetX)/2) - (textWidth/2 - offsetX), im.size[1]/4), text, font=textFont, fill="#000000") 

#QR-Code
draw.bitmap(((im.size[0]-offsetX)/2 - (qr.size[0]/2 - offsetX), im.size[1]/2.5), qr, fill="#000000")


del draw
# twrite to stdout
im.save("eselpenis.png", "PNG")

