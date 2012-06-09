from flask import Flask,url_for,render_template,request,abort

app = Flask(__name__)
db = { "box" : [], "project": []}
@app.route("/")
def hello():
  return render_template("index.html")


@app.route("/publish",methods=["POST"])
def publish():
  """
  owner-email balls
  item-type item-type-project
  wiki-url khan
  owner-name aids
  freetext fuck
  """
  owner = request.form["owner-name"]
  owner_mail = request.form["owner-email"]
  t = request.form["item-type"]
  url = request.form["wiki-url"]
  text = request.form["freetext"]
  if t == "item-type-project":
    return "Owner %s (%s) added a project with url `%s` and freetext `%s`" % (owner,owner_mail,url,text)
  elif t == "item-type-box":
    return "Owner %s (%s)added a box" % (owner,owner_mail)
  else:
    return "WTF?"


if __name__ == "__main__":
  #url_for('static', filename='index.js')
  #url_for('static', filename='jquery-1.7.2.min.js')
  app.debug = True
  app.run(host= "0.0.0.0",port=8080)
