#!/usr/bin/env python3
"""
https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
"""

from flask import Flask, jsonify, abort, make_response, redirect
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


class TaskListAPI(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "title",
            type=str,
            required=True,
            help="no tasktitle",
            location="json",
        )
        self.reqparse.add_argument("description", type=str, default="", location="json")
        super(TaskListAPI, self).__init__()

    def get(self):
        return {"tasks": [marshal(task, task_fields) for task in tasks]}

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            "id": tasks[-1]["id"] + 1 if len(tasks) > 0 else 1,
            "title": args["title"],
            "description": args["description"],
            "done": False,
        }
        tasks.append(task)
        return {"task": marshal(task, task_fields)}, 201


class TaskAPI(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("title", type=str, location="json")
        self.reqparse.add_argument("description", type=str, location="json")
        self.reqparse.add_argument("done", type=bool, location="json")
        super(TaskAPI, self).__init__()

    def get(self, id):
        return "aa"
        task = [task for task in tasks if task["id"] == id]
        if len(task) == 0:
            abort(404)
        return {"task": marshal(task[0], task_fields)}

    def put(self, id):
        task = [task for task in tasks if task["id"] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {"task": marshal(task, task_fields)}

    def delete(self, id):
        task = [task for task in tasks if task["id"] == id]
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return {"result": True}


api.add_resource(TaskListAPI, "/todo/api/v1.0/tasks", endpoint="tasks")
api.add_resource(TaskAPI, "/todo/api/v1.0/tasks/<int:id>", endpoint="task")


class ShortenerAPI(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "url", required=True, help="no url provided", type=str, location="json"
        )
        self.reqparse.add_argument("password", type=str, location="json")
        super(ShortenerAPI, self).__init__()

    def get(self):
        return {"short_link": "SHORT LINK", "long_link": "https://google.com"}
        task = [task for task in tasks if task["id"] == id]
        if len(task) == 0:
            abort(404)
        return {"task": marshal(task[0], task_fields)}

    def put(self):
        args = self.reqparse.parse_args()
        for k, v in args.items():
            print(k, v)
        return args

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
    print(short)
    return f'<a href="/api/url">url</a><br><p>{short}</p>'


HOME_HTML = """
 <form action="/api/url" method="put">
  <label for="url">Long Url</label>
  <input type="text" id="url" name="url"><br><br>
  <label for="password">Delete Password (optional)</label>
  <input type="text" id="password" name="password"><br><br>
  <input type="submit" value="Submit">
</form> 
"""


@app.route("/", methods=["GET"])
def home():
    return HOME_HTML


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
