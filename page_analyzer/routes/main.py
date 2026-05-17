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
from ..utils.check_site import check_site
from ..utils.normalize_url import normalize_url
from ..utils.validators import validate_url

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template("index.html")


@main_bp.get("/urls")
def get_urls():
    try:
        urls = URLModel.get_urls()
        urls_data = [{**url, "last_check": CheckModel.get_last_check(url["id"])} for url in urls]
    except Exception:
        flash(
            "Произошла ошибка при получении списка сайтов. Попробуйте перезагрузить страницу",
            "error",
        )
        urls_data = []
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
            url_id = existing_url["id"]
            flash("Страница уже существует", "info")
        else:
            url_id = URLModel.save_url(normalized)
            flash("Страница успешно добавлена", "success")
        return redirect(url_for("main.get_url", id=url_id))
    except Exception:
        flash("Ошибка добавления страницы", "error")
        return render_template("index.html", url=url)


@main_bp.get("/urls/<int:id>")
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
        result = check_site(url["name"])
        check_data = {**result, "url_id": id}
        CheckModel.save_check(check_data)
        flash("Страница успешно проверена", "success")
    except Exception:
        flash("Произошла ошибка при проверке", "error")

    return redirect(url_for("main.get_url", id=id))
