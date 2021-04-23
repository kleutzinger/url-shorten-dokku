#!/usr/bin/env python3
"""
https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful

soon i'll
"""

from flask import (
    Flask,
    jsonify,
    abort,
    make_response,
    redirect,
    render_template,
    send_from_directory,
)
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import database as db
import os
from dotenv import load_dotenv

load_dotenv()
PORT = os.getenv("PORT")

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == "miguel":
        return "python"
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({"message": "Unauthorized access"}), 403)


tasks = [
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
        "done": False,
    },
    {
        "id": 2,
        "title": "Learn Python",
        "description": "Need to find a good Python tutorial on the web",
        "done": False,
    },
]

task_fields = {
    "title": fields.String,
    "description": fields.String,
    "done": fields.Boolean,
    "uri": fields.Url("task"),
}


class ShortenerAPI(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "url", required=True, help="no url in POST", type=str
        )
        self.reqparse.add_argument("password", type=str)
        super(ShortenerAPI, self).__init__()

    def get(self):
        return {"short_link": "SHORT LINK", "long_link": "https://google.com"}
        task = [task for task in tasks if task["id"] == id]
        if len(task) == 0:
            abort(404)
        return {"task": marshal(task[0], task_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        long_url = args["url"]
        password = args["password"]
        ret = db.add_url_to_db(long_url, password)
        print(ret)
        return ret

    def delete(self):
        task = [task for task in tasks if task["id"] == id]
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return {"result": True}


api.add_resource(ShortenerAPI, "/api/url", endpoint="url")

# @app.route("/test", methods=["GET"])
# def test():
#    return redirect("https://google.com")


@app.route("/<short>", methods=["GET"])
def short(short):
    stored_long_url = db.check_short_url(short)
    if stored_long_url:
        return redirect(stored_long_url)
    else:
        return (f"<p>not found {short}</p>", 404)


HOME_HTML = """
 <form action="/api/url" method="post">
  <label for="url">Long Url</label>
  <input type="text" id="url" name="url"><br><br>
  <!-- <label for="password">Delete Password (optional)</label>
  <input type="text" id="password" name="password"><br><br> !-->
  <input type="submit" value="Submit">
</form> 
"""


@app.route("/", methods=["GET"])
def home():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
