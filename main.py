# -*- coding: utf-8 -*-
from flask import Flask
from apps.view import app as hello_app

app = Flask(__name__)

modules_define = [hello_app]
for _app in modules_define:
    app.register_blueprint(_app)