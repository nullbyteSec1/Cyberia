from flask import Blueprint, session, redirect, url_for, render_template, request
from functools import wraps
import os
from pathlib import Path
import bcrypt
from model import Posts, Reports, moderator_accounts, db

admin_bp = Blueprint("admin", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/")
@login_required
def homepage():
    reports = Reports.query.all()
    data = [
        {
            "id": r.id,
            "report_header": r.report_header,
            "report_body": r.report_body,
        }
        for r in reports
    ]
    return render_template("./admin/painel.html",reports=data)

@admin_bp.route("/api/delete", methods=["POST"])
@login_required
def delete_post():
    target_post_id = request.form.get("post_id")

    if target_post_id is None:
        return render_template("warning.html",error_text="post id not define")

    post = Posts.query.get_or_404(int(target_post_id))
    os.remove(Path("uploads") / post.image_path)
    db.session.delete(post)
    db.session.commit()
    return render_template("alert.html",alert_mensagem="post deleted",page_return="/admin")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("./admin/login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return  render_template("warning.html",error_text="invalid credential")

    user = moderator_accounts.query.filter_by(username=username).first()

    if user is None:
        return render_template("warning.html",error_text="Invalid credential")
    if bcrypt.checkpw(password.encode("utf-8"),user.password.encode("utf-8")):
        session["logged_in"] = True
        return redirect(url_for("admin.homepage"))

    return render_template("warning.html",error_text="Invalid credential")
