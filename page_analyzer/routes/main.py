from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from ..models.url_model import URLModel
from ..utils.normalize_url import normalize_url
from ..utils.validators import validate_url

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.get("/urls")
def get_urls():
    try:
        urls = URLModel.get_urls()
    except Exception:
        flash(
            "Произошла ошибка при получении списка сайтов. Попробуйте перезагрузить страницу",
            "error",
        )
        urls = []
    return render_template("urls.html", urls=urls)


@main_bp.post("/urls")
def add_url():
    url = request.form.to_dict().get("url")
    normalized = normalize_url(url)
    error = validate_url(normalized)
    if error:
        flash(error, "error")
        return render_template("index.html", url=url), 422

    try:
        existing_url = URLModel.find_url_by_name(normalized)
        if existing_url:
            id = existing_url["id"]
        else:
            id = URLModel.save_url(normalized)
            flash("Страница успешно добавлена", "success")
        return redirect(url_for("main.get_url", id=id))
    except Exception:
        flash("Ошибка добавления страницы", "error")
        return render_template("index.html", url=url)


@main_bp.route("/urls/<id>")
def get_url(id):
    try:
        url = URLModel.get_url(id)
        url["created_at"] = url["created_at"].strftime("%Y-%m-%d")
        if url:
            return render_template("url.html", url=url)
        abort(404)
    except Exception:
        abort(404)
