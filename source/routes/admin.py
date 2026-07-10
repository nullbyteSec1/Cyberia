from flask import Blueprint, session, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Length,NumberRange
from functools import wraps
from config import upload_folder
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


@admin_bp.route("/",methods=["GET","POST"])
@login_required
def homepage():
    class DeletePostForm(FlaskForm):
        target_id_post = IntegerField("post_target_id",validators=[DataRequired(),NumberRange(min=1,max=999)])
        submit = SubmitField("delete")

    form = DeletePostForm()

    if request.method == "GET":
       reports = Reports.query.all()
       data = [
       {
            "id": r.id,
            "report_header": r.report_header,
            "report_body": r.report_body,
         }
         for r in reports
       ]
       return render_template("./admin/painel.html",reports=data,form=form)
    if request.method == "POST" and form.validate_on_submit():
       post_target_id = form.target_id_post.data
       post = Posts.query.get_or_404(post_target_id)
       os.remove(Path(upload_folder) / post.image_path)
       db.session.delete(post)
       db.session.commit()
       return render_template("alert.html",alert_mensagem="post Deleted")
    
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    class LoginForm(FlaskForm):
        username = StringField("username",validators=[DataRequired(),Length(min=3,max=50)])
        password = PasswordField("password",validators=[DataRequired()])
        submit = SubmitField("login")
    form = LoginForm()
    if request.method == "GET":
        return render_template("./admin/login.html",form=form)

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if not username or not password:
           return  render_template("warning.html",error_text="invalid credential")
    
        user = moderator_accounts.query.filter_by(username=username).first()

        if user is None:
           return render_template("warning.html",error_text="Invalid credential")
        if bcrypt.checkpw(password.encode("utf-8"),user.password.encode("utf-8")):
           session["logged_in"] = True
           return redirect(url_for("admin.homepage"))
    return render_template("warning.html",error_text="Invalid credential")
