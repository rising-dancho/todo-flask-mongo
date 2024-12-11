from flask import Flask, render_template, request, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
import logging

logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# # MongoDB connection URI from environment variables
# uri = os.getenv("MONGO_URI")
# print(f"Mongo URI: {os.getenv('MONGO_URI')}")

uri = "mongodb+srv://josealejoperezjr:denden123@cluster0.uaaav.mongodb.net/flask_database?retryWrites=true&w=majority&appName=Cluster0"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# MongoDB database and collection
db = client.flask_database  # Database name
todos = db.todos  # Collection name


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form["content"]
        degree = request.form["degree"]
        todos.insert_one({"content": content, "degree": degree})
        return redirect(url_for("index"))
    all_todos = todos.find()
    return render_template("index.html", todos=all_todos)


# Delete Route
@app.post("/<id>/delete/")
def delete(id):  # delete function by targeting a todo document by its own id
    todos.delete_one(
        {"_id": ObjectId(id)}
    )  # deleting the selected todo document by its converted id
    return redirect(url_for("index"))  # again, redirecting you to the home page


if __name__ == "__main__":
    from os import environ

    app.run(host="0.0.0.0", port=int(environ.get("PORT", 8080)))
