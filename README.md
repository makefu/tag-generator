Zustand
===========

Bronsen hat fertig umgezogen, das Projekt wurde umgezogen und nun geht es weiter mit der Implementierung und Verbesserung.

tag-generator
=============

Die Projekte des [shacks](http://shackspace.de/) sollen getaggt werden

Environment
===========

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

