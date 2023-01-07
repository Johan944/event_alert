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

import parser_shotgun


app = flask.Flask(__name__, instance_relative_config=True)
app.config["SECRET_KEY"] = "test!"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update_event")
def update_event():
    url = request.args.get("url")
    parser = parser_shotgun.ParserShotgun()
    infos = parser.get_infos(url)
    return infos

@app.route("/save_form", methods=["POST"])
def save_form():
    url = request.form["url"]
    mail = request.form["mail"]
    prices = request.form["prices"].split(",")
    prices.pop()

    flask.flash(f"WIP (non-fonctionnel) : Enregistrement des notifications pour l'évènement {url} pour les prix {', '.join(prices)} à l'adresse mail {mail}.")

    return flask.redirect(
        flask.url_for("index")
    )

if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)

    app.run(host="0.0.0.0", port=int(arguments["--port"]), debug=arguments["--debug"])