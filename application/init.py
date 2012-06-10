from flask import Flask,url_for,render_template,request,abort,make_response,send_file,redirect

app = Flask(__name__)
print app.config.keys()

# in-memory database
db = { "box" : [], "project": []}
@app.route("/")
def hello():
  return render_template("index.html")


@app.route("/publish",methods=["POST"])
def publish():
  """
  """
  owner = request.form["owner-name"]
  email= request.form["owner-email"]
  t = request.form["item-type"]
  url = request.form["wiki-url"]
  text = request.form["freetext"]
  if t == "item-type-project":
    ident = len(db["project"])
    db["project"].append({"owner": owner, "email": email,"ident": ident,"url":url,"text":text})
    print "Add a project for Owner %s (%s) with url `%s` and freetext `%s`" % (owner,email,url,text)
    return redirect("/project/details/%d" % ident)
  elif t == "item-type-box":
    ident = len(db["box"])
    db["box"].append({"owner": owner, "email": email,"ident": ident})
    print "Add box with id `%d` and owner %s(%s)" % (ident,owner,email)
    return redirect("/box/details/%d" % ident)
  else:
    return "WTF?"

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

@app.route("/qr/<typ>/<int:ident>")
def gen_qr(typ=None,ident=None):
  import qrcode
  import os.path
  if ident is None:
    abort (500)
  if typ not in ["box","project"]:
    abort(404)
  qrpath= "qr/%s"%ident
  if not os.path.isfile(qrpath):
    img = qrcode.make("%s/%s/%s"%(app.config["SERVER_NAME"],typ,ident))
    img.save(qrpath)

  assert (os.path.isfile(qrpath))
  f = open(qrpath)
  #response = make_response(f.read())
  #f.close()
  #response.headers["Content-Type"] = "image/png"
  return send_file(f,mimetype="image/png")


if __name__ == "__main__":
  #url_for('static', filename='index.js')
  #url_for('static', filename='jquery-1.7.2.min.js')
  app.debug = True
  app.config["SERVER_NAME"] = "incept.krebsco.de:8080"
  app.run(host= "0.0.0.0",port=8080)
