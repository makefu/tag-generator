from flask import Flask, url_for, render_template, request, abort, make_response, send_file, redirect
import json
app = Flask(__name__)

#app.config["SERVER_NAME"] = "127.0.0.1:8080"
DB_FILE="db/db.json"

# in-memory database

def save_db():
  with open(DB_FILE,"w+") as persistence:
    json.dump(db,persistence)
    print "db saved"
    return db

def load_db():
  try:
    persistence = open(DB_FILE)
    return json.load(persistence)
    print "db loaded"
  except:
    print "cannot read db, trying to create it first"
    return save_db()

@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/publish", methods=["POST"])
def publish():
    """
    """
    try:
        owner = request.form["owner-name"]
        email = request.form["owner-email"]
        twitter = request.form["owner-twitter"]
        item_type = request.form["item-type"]
        url = request.form["wiki-url"]
        text = request.form["freetext"]
        telephone = request.form["owner-telephone"]
    except:
        abort(500)

    if item_type == "item-type-project":
        item_type = "project"
        qr_data = url
    elif item_type == "item-type-box":
        item_type = "box"
        qr_data = "mailto:%s" % email
    else:
        return "WTF?"

    ident = len(db[item_type])
    db[item_type].append({"owner": owner, "email": email, "ident": ident, "url": url, "text": text, "twitter": twitter,
        "telephone": telephone, "qr_data": qr_data,})
    save_db()
    return redirect("/%s/details/%d" % (item_type, ident))


@app.route("/<typ>/qr/<int:ident>")
def gen_qr(typ=None, ident=None):
    if ident is None: abort(500)
    if typ not in ["box", "project"]: abort(404)
    data = {}
    try: data = db[typ][ident]
    except: abort(404)

    import qrcode
    import os.path

    qrpath = "qr/%s_%s" % (typ, ident)
    if not os.path.isfile(qrpath):  #skip if qrcode has already been written
        qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=15, border=0)
        qr.add_data("%s" % (data["qr_data"]))
        qr.make(fit=True)
        img = qr.make_image()
        img.save(qrpath)
        generate_cute_qr(qrpath, data)

    assert (os.path.isfile(qrpath))
    f = open(qrpath)
    #response = make_response(f.read())
    #f.close()
    #response.headers["Content-Type"] = "image/png"
    return send_file(f, mimetype="image/png")


@app.route("/<typ>/details/<int:ident>")
def details_for(typ, ident=None):
    """
    returns details for box or project
    """
    if typ not in ["box", "project"]: abort(404)
    if ident is None: abort(500)

    data = {}
    try: data = db[typ][ident]
    except: print "%s %d not found" % (typ, ident)
    return render_template("%s.html" % typ, app=app, ident=ident, data=data)


@app.route("/<typ>/details/<int:ident>/json")
def json_for(typ, ident=None):
    import json

    if typ not in ["box", "project"]: abort(404)
    if ident is None: abort(500)

    data = {}
    try: data = db[typ][ident]
    except: abort(404)
    return json.dumps(data)


def generate_cute_qr(qrpath, data):
    from PIL import Image, ImageDraw, ImageFont

    heading = "A Hacker known as %s" % (data["owner"])
    emailtext = "Email: %s" % data["email"]
    twittertext = "Twitter: %s" % data["twitter"]
    urltext = "URL: %s" % data["url"]
    freitext = "%s" % data["text"]
    telephonetext = "Telephone: %s" % data["telephone"]
    textOffset = 0

    im = Image.open("../resources/A6_300dpi.png")
    qr = Image.open(qrpath)
    qr.convert('RGB')
    im.convert('RGB')

    headingFontsize = 70
    headingFont = ImageFont.truetype("../resources/arialbd.ttf", headingFontsize)
    textFontsize = 40
    textFont = ImageFont.truetype("../resources/arial.ttf", textFontsize)
    offsetX = 340  #offset for the shackspace logo on the leftside
    draw = ImageDraw.Draw(im)

    #Heading
    headingWidth, headingHeight = draw.textsize(heading, font=headingFont)
    sizeX = im.size[0]
    sizeY = im.size[1]

    draw.text((((sizeX - offsetX) / 2) - (headingWidth / 2 - offsetX), sizeY / 8),
        heading, font=headingFont, fill="#000000")

    #Text
    textWidth, textHeight = draw.textsize(emailtext, font=textFont)
    text_offsetX = ((sizeX - offsetX) / 2) - (textWidth / 2 - offsetX)
    text_baseline = (sizeY / 5)

    draw.text((text_offsetX, sizeY / 5), emailtext, font=textFont, fill="#000000")
    textOffset += textHeight

    if data["twitter"]:
        draw.text((text_offsetX, text_baseline + textOffset), twittertext, font=textFont, fill="#000000")
        textOffset += textHeight

    if data["url"]:
        draw.text((text_offsetX, text_baseline + textOffset), urltext, font=textFont, fill="#000000")
        textOffset += textHeight

    if data["telephone"]:
        draw.text((text_offsetX, text_baseline + textOffset), telephonetext, font=textFont, fill="#000000")
        textOffset += textHeight

    if data["text"]: #add another line
        textOffset += textHeight
        draw.text((text_offsetX, text_baseline + textOffset), freitext, font=textFont, fill="#000000")

    #QR-Code
    im.paste(qr, (int((sizeX - offsetX) / 2 - (qr.size[0] / 2 - offsetX)), int(sizeY / 2.2)))
    del draw
    im.save(qrpath, "PNG")

if __name__ == "__main__":
    from os import system
    #url_for('static', filename='index.js')
    #url_for('static', filename='jquery-1.7.2.min.js')
    app.debug = True
    #system("rm qr/*")
    db = {"box": [], "project": []}
    db = load_db()
    app.run(host="0.0.0.0", port=8080)
