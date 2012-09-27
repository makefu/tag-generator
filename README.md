Stillstand?
===========

Der Bronsen steckt mitten im Umzug und hat keine Zeit für die schönen Tickets. Nach dem Umzug geht's wieder weiter.

tag-generator
=============

Die Projekte des [shacks](http://shackspace.de/) sollen getaggt werden

Environment
===========

System Packages
---------------
```
${installer}python-pip python-virtualenv gcc python-dev
```
virtualenv
---------
```
virtualenv .
. bin/activate
pip install -r requirements.txt
```

Running the Server
=================

Flask
-----
0. ```cd application```
1. Set Server Name:
  ```sed -i 's/incept.krebsco.de/localhost/' init.py```
2. ```python init.py```

