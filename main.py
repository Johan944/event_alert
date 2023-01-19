"""Launches online integration

Usage:
  main.py [-h | --help]  [options]

Options:
  -h --help                         Show this screen.
  --host HOST                       Set host address [default: 127.0.0.1].
  --port PORT                       Set host port [default: 5000]
  --debug                           Set debug mode
"""
import docopt
import flask

from flask import render_template, request
from datetime import datetime

import parser_shotgun
import models
from config import app, db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/update_event")
def update_event():
    url = request.args.get("url")
    parser = parser_shotgun.ParserShotgun()
    try:
        infos = parser.get_infos(url)
        infos["error"] = False
    except parser_shotgun.BadUrlError:
        infos = {"error": True}
    return infos


@app.route("/save_form", methods=["POST"])
def save_form():
    url = request.form["url"]
    mail = request.form["mail"]
    prices = request.form["prices"][:-1]
    event_date = request.form["event_date_input"]

    import send_notification

    s = send_notification.SendNotification()
    s.send(url, mail, prices, event_date)

    flask.flash(
        f"WIP (non-fonctionnel) : Enregistrement des notifications pour l'évènement {url} pour les prix {prices} à l'adresse mail {mail}. Date : {event_date}."
    )

    return flask.redirect(flask.url_for("index"))


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)

    app.run(host=arguments["--host"], port=int(arguments["--port"]), debug=arguments["--debug"])
