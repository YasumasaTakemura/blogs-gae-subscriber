# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from .model import Hash

app = Blueprint('hello', __name__)


@app.route('/', methods=['GET'])
def hello():
    return 'hello, world', 200


@app.route('/json', methods=['GET', 'POST'])
def json():
    data = request.json
    return jsonify(data=data), 200


@app.route('/arg', methods=['GET'])
def arg():
    key = request.args.get("key", type=str)
    hash_obj = Hash(key)
    val = hash_obj.get_hash()
    return val, 200


@app.route('/form', methods=['POST'])
def form():
    req = request.form
    val = req.get('key')
    return jsonify(data=val), 200
