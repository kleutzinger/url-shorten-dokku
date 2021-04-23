#!/usr/bin/env python3
"""
run a local flask server to handle shortening urls

starting point was from here:
https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
"""

from flask import (
    Flask,
    jsonify,
    abort,
    make_response,
    redirect,
    render_template,
    send_from_directory,
    request,
)
from flask_restful import Api, Resource, reqparse, fields, marshal, inputs
import database as db
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()
PORT = os.getenv("PORT")

app = Flask(__name__, static_url_path="")
api = Api(app)


class ShortenerAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        help_text = "bad POST, please supply a fully qualified url in the `url` field"
        self.reqparse.add_argument(
            "url", required=True, help=help_text, type=inputs.url
        )
        self.reqparse.add_argument("password", type=str)
        super(ShortenerAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        long_url = args["url"]
        password = args["password"]
        db_resp = db.add_url_to_db(long_url, password)
        parsed_req_url = urlparse(request.url)
        homepage_loc = f"{parsed_req_url.scheme}://{parsed_req_url.netloc}/"
        db_resp["short_url_proper"] = homepage_loc + db_resp["short_hash"]
        for strip_field in ("pw_hash", "salt"):
            if strip_field in db_resp:
                del db_resp[strip_field]
        return db_resp


api.add_resource(ShortenerAPI, "/api/url", endpoint="url")


@app.route("/<short>", methods=["GET"])
def short(short):
    stored_long_url = db.check_short_url(short)
    if stored_long_url:
        return redirect(stored_long_url)
    else:
        return (f'<p>no short url found at <a href="/{short}">/{short}</a></p>', 404)


@app.route("/", methods=["GET"])
def home():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
