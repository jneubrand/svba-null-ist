# /usr/bin/env python3
# -*- coding: utf8 -*-

try:
    import config
except ImportError as e:
    print('''-*- Looks like you forgot to add a config file. Try this one: -*-

import time

empty = 'There\'s nothing here.'
data_path = '[YOUR_DATA_PATH]/'
valediction = lambda: 'gen at {}'.format(round(time.time(), 2)).encode('utf-8')

-*-''')
    raise e
from flask import Flask, redirect, send_from_directory, render_template
import glob
import json
import os

app = Flask(__name__,
            static_url_path='/static')


@app.errorhandler(404)
def err(e):
    return config.empty, 404


@app.route("/data")
@app.route("/data/")
def data():
    query = '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].json'
    return json.dumps([os.path.basename(a) for a in glob.glob(
        config.data_path + query)])


@app.route("/data/<path:path>")
def data_item(path):
    return send_from_directory(os.path.abspath(config.data_path), path)


@app.route("/")
def main():
    return render_template(
        'index.html', genstr=config.valediction())


@app.route("/robots.txt")
def robots():
    return 'User-agent: *\nAllow: /$\nDisallow: /'


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'max-age=300'
    return response


if __name__ == "__main__":
    app.run(debug=True)
