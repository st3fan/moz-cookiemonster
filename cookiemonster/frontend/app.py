# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/


from flask import Flask


app = Flask(__name__)


def configure_app(web_app, debug=False):
    web_app.debug = debug
    web_app.use_evalex = False
    return web_app
