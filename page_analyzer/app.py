import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

from .routes.main import main_bp  # noqa: E402

app.register_blueprint(main_bp)

if os.getenv("APP_ENV") == "development":
    from livereload import Server

    server = Server(app.wsgi_app)
    server.watch("page_analyzer/templates/")
    server.watch("page_analyzer/static/")
    server.serve(port=5000, debug=True)
