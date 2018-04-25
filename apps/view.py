# -*- coding: utf-8 -*-

from flask import Blueprint, request
from .model import UrlState, read_file_from_gcs, parse

app = Blueprint('sub', __name__)


@app.route('/', methods=['GET'])
def hello():
    return 'hello, world', 200


@app.route('/push', methods=['POST', 'GET'])
def push():
    """ extract files from GCS """
    data = request.json
    msg = data['message']['attributes']
    filename = '/' + msg['bucketId'] + '/' + msg['objectId']
    data = read_file_from_gcs(filename)

    # transform /parse files
    path = parse(data)

    if not path:
        return 'no path existed', 200

    # load items
    for p in path:
        key = UrlState.gen_key(p)
        state = UrlState(**{'path': p, 'key': key})
        state.put()

    return 'success', 200


@app.route('/get_one', methods=['GET'])
def get_one():
    key = request.args.get("p", type=str)
    path = UrlState.get_one(key)
    return path['path'] + '\n', 200
