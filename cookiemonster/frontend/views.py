# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import datetime
import functools
import json
import os
import os.path
import random
import urlparse

from flask import request, session, render_template, redirect, url_for, jsonify, Response

from cookiemonster.frontend.persona import verify_assertion
from cookiemonster.frontend import app
from cookiemonster.frontend.mozillians import lookup_mozillian

from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId


client = MongoClient()
db = client.cookiemonster


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            session["next"] = request.url
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def random_message():
    messages = [
        "Cookie starts with C",
        "C is for cookie, that's good enough for me",
        "Oh, cookie, cookie, cookie starts with C"
    ]
    return random.choice(messages)

@app.route("/")
def index():
    if session.get("email") is None:
        return redirect(url_for("login"))
    report = db.reports.find_one({"state":"FINISHED"}, sort=[("created", DESCENDING)])
    return render_template("index.html", report=report, message=random_message())

@app.route("/login")
def login():
    if session.get("email") is not None:
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/heartbeat")
def heartbeat():
    return "OK"


@app.route("/persona/login", methods=["POST"])
def persona_login():
    receipt = verify_assertion(request.form["assertion"], request.host)
    if not receipt:
        return jsonify(success=False)
    email = receipt["email"]
    if not email.endswith("@mozilla.com") and not email.endswith("@mozillafoundation.org"):
        mozillian = lookup_mozillian(app.config["MOZILLIANS_APP_NAME"],
                                     app.config["MOZILLIANS_APP_KEY"], email)
        if not mozillian or not mozillian["is_vouched"]:
            return jsonify(success=False, error="only-mozilla")
    session["email"] = receipt["email"]
    return jsonify(success=True, email=receipt["email"], next=session.get("next"))

@app.template_filter()
def labelfor(v, t):
    if t == "state":
        if v == "SUCCESS":
            return "label label-success"
        else:
            return "label label-danger"
    if t in ("secure", "httponly"):
        if v == True:
            return "label label-success"
        else:
            return "label label-danger"

@app.template_filter()
def hostname(v):
    u = urlparse.urlparse(v)
    return u.hostname
