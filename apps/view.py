# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from .model import UrlState, read_file_from_gcs, parse

app = Blueprint('hello', __name__)


@app.route('/', methods=['GET'])
def hello():
    return 'hello, world', 200


@app.route('/push', methods=['GET', 'POST'])
def push():
    """ extract files from GCS """
    data = request.json
    filename = data['message']['bucketId'] + '/' + data['message']['objectId']
    data = read_file_from_gcs(filename)

    # transform /parse files
    path = parse(data)

    # load items
    for p in path:
        state = UrlState(**{'path': p})
        state.put()

    return 'success', 200


@app.route('/get_one', methods=['GET'])
def arg():
    key = request.args.get("p", type=str)
    path = UrlState.get_one(key)
    return path, 200
