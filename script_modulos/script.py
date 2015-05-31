#!/usr/bin/python
import os

os.system("mkdir model")
os.system("mkdir view")
os.system("mkdir demo")
os.system("mkdir doc")
os.system("mkdir data")
os.system("mkdir report")
os.system("mkdir wizard")
os.system("mkdir test")
os.system("mkdir tests")
os.system("mkdir static")
os.system("mkdir static/src")
os.system("mkdir static/src/img")
os.system("mkdir static/src/js")
os.system("mkdir static/src/css")
os.system("mkdir static/src/xml")
os.system("mkdir static/description")

os.system("touch static/description/index.html")
os.system("touch __openerp__.py")
os.system("touch __init__.py")
os.system("touch model/__init__.py")

os.system("mv icon.png static/src/img/")
