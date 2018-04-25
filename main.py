# -*- coding: utf-8 -*-
from flask import Flask
from apps.view import app as subscriber

app = Flask(__name__)

modules_define = [subscriber]
for _app in modules_define:
    app.register_blueprint(_app)