import os

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


if os.getenv("APP_ENV") == "development":
    from livereload import Server

    server = Server(app.wsgi_app)
    server.watch("page_analyzer/templates/")
    server.watch("page_analyzer/static/")
    server.serve(port=5000, debug=True)
