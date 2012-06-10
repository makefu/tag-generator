from flask import Flask,url_for,render_template,request,abort,make_response,send_file,redirect
app = Flask(__name__) 
app.config["SERVER_NAME"] = "incept.krebsco.de:8080"

# in-memory database
db = { "box" : [], "project": []}
@app.route("/")
def hello():
  return render_template("index.html")


@app.route("/publish",methods=["POST"])
def publish():
  """
  """
  try:
    owner = request.form["owner-name"]
    email= request.form["owner-email"]
    twitter = request.form["owner-twitter"]
    t = request.form["item-type"]
    url = request.form["wiki-url"]
    text = request.form["freetext"]
  except:
    abort(500)
  if t == "item-type-project":
    t = "project"
  elif t == "item-type-box":
    t = "box"
  else:
    return "WTF?"
  ident = len(db[t])
  db[t].append({"owner": owner, "email": email,"ident": ident,"url":url,"text":text, "twitter" : twitter})
  return redirect("/%s/details/%d" % (t,ident))



@app.route("/<typ>/qr/<int:ident>")
def gen_qr(typ=None,ident=None):
  if ident is None: abort (500)
  if typ not in ["box","project"]: abort(404)
  data = {}
  try: data = db[typ][ident]
  except : abort(404)

  import qrcode
  import os.path
  qrpath= "qr/%s"%ident
  if not os.path.isfile(qrpath):  #skip if qrcode has already been written
    qr = qrcode.QRCode(version=5,error_correction=qrcode.constants.ERROR_CORRECT_Q,box_size=15,border=0)
    qr.add_data("%s/%s/details/%s"%(app.config["SERVER_NAME"],typ,ident))
    qr.make(fit=True)
    img = qr.make_image()
    img.save(qrpath)
    generate_cute_qr(qrpath,ident)

  assert (os.path.isfile(qrpath))
  f = open(qrpath)
  #response = make_response(f.read())
  #f.close()
  #response.headers["Content-Type"] = "image/png"
  return send_file(f,mimetype="image/png")

@app.route("/box/details/<int:ident>")
def handle_box(ident=None):
  if ident is None:
    abort (500)
  data = {}
  try: 
    data = db["box"][ident]
  except : print "Box %d not found" % ident
  return render_template("box.html",app=app,ident=ident,data=data)

@app.route("/project/details/<int:ident>")
def handle_project(ident=None):
  if ident is None:
    abort (500)
  data = {}
  try: 
    data = db["project"][ident]
  except : print "Project %d not found" % ident
  return render_template("project.html",app=app,ident=ident,data=data)

def generate_cute_qr(qrpath,data):
  from PIL import Image, ImageDraw, ImageFont

  heading = "A Hacker known as %s" % (data["owner"])
  emailtext = "Email: %s" %data["email"]
  twittertext= "Twitter: %s" %data["twitter"]
  urltext = "URL: %s" %data["url"]
  freitext = "%s"%data["text"]
  textOffset =0

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
  draw.text((((im.size[0]- offsetX)/2) - (headingWidth/2 - offsetX), im.size[1]/8), heading, font=headingFont, fill="#000000") 
  #Text
  textWidth, textHeight = draw.textsize(emailtext, font=textFont)
  draw.text((((im.size[0]- offsetX)/2) - (textWidth/2 - offsetX), im.size[1]/5), emailtext, font=textFont, fill="#000000") 
  textOffset += textHeight
  if data["twitter"]:
    draw.text((((im.size[0]- offsetX)/2) - (textWidth/2 - offsetX), (im.size[1]/5)+textOffset), twittertext, font=textFont, fill="#000000") 
    textOffset += textHeight
  if data["url"]:
    draw.text((((im.size[0]- offsetX)/2) - (textWidth/2 - offsetX), (im.size[1]/5)+textOffset), urltext, font=textFont, fill="#000000") 
    textOffset += textHeight
  if data["text"]: #add another line 
    draw.text((((im.size[0]- offsetX)/2) - (textWidth/2 - offsetX), (im.size[1]/5)+textOffset+textHeight), freitext, font=textFont, fill="#000000") 

  #QR-Code
  draw.bitmap(((im.size[0]-offsetX)/2 - (qr.size[0]/2 - offsetX), im.size[1]/2.2), qr, fill="#000000")
  del draw
  im.save(qrpath, "PNG")

if __name__ == "__main__":
  #url_for('static', filename='index.js')
  #url_for('static', filename='jquery-1.7.2.min.js')
  app.debug = True
  app.run(host= "0.0.0.0",port=8080)
