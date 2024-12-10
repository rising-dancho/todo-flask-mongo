from flask import Flask, render_template, request, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB connection URI from environment variables
uri = os.getenv("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

# Test connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

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
    app.run(debug=True)
