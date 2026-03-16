from flask import Flask, jsonify
from dotenv import load_dotenv
import os


load_dotenv()


#initialise flask

app = Flask(__name__)

#base route
@app.route("/")
def hello():
    return "<p>Hello, World!</p>"

#dynamic route
@app.route("/<name>")
def hello_person(name):
    #greeting string 
    return f"<p>Hello, {name}!</p>"

#Json API route
@app.route("/api/tasks")
def tasks():
    return jsonify({
        "wednesdays_tasks":["learn docker", "learn flask", "dots of tech lesson"],
        "thursdays_tasks": ["continue with docker", "continue with flask", "recieve orthopaedic kneeling chair"]})



if __name__ == "__main__":

    app.run(host = os.getenv("HOST"), port = os.getenv("PORT"))