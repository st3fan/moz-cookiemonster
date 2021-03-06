# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

from flask import Flask

app = Flask(__name__)

from cookiemonster.frontend import views


def configure_app(web_app, filename):
    if not filename:
        web_app.config.from_object('cookiemonster.frontend.config.DefaultConfig')
    else:
        web_app.config.from_pyfile(filename)
    return web_app
