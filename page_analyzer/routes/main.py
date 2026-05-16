from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from ..models.check_model import CheckModel
from ..models.url_model import URLModel
from ..utils.normalize_url import normalize_url
from ..utils.validators import validate_url

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.get("/urls")
def get_urls():
    urls_data = []
    try:
        urls = URLModel.get_urls()
        for url in urls:
            last_check = CheckModel.get_last_check(url["id"])
            urls_data.append({**url, "last_check": last_check["created_at"] if last_check else ""})
    except Exception:
        flash(
            "Произошла ошибка при получении списка сайтов. Попробуйте перезагрузить страницу",
            "error",
        )
    return render_template("urls.html", urls=urls_data)


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


@main_bp.route("/urls/<int:id>")
def get_url(id):
    try:
        url = URLModel.get_url(id)
        if not url:
            abort(404)
    except Exception:
        abort(404)

    try:
        checks = CheckModel.get_checks(id)
    except Exception:
        flash("Произошла ошибка при загрузке результатов проверок", "error")
        checks = []
    return render_template("url.html", url=url, checks=checks)


@main_bp.post("/urls/<int:id>/checks")
def add_check_for_url(id):
    try:
        url = URLModel.get_url(id)
    except Exception:
        url = ""

    try:
        CheckModel.save_check(id)
        flash("Страница успешно проверена", "success")
    except Exception:
        flash("Произошла ошибка при проверке", "error")

    try:
        checks = CheckModel.get_checks(id)
    except Exception:
        flash("Произошла ошибка при загрузке результатов проверок", "error")
        checks = []
    return render_template("url.html", url=url, checks=checks)
