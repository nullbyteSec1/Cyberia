from flask import Blueprint,request,render_template,redirect,send_from_directory,url_for
from model import Posts,Topics,Reports,db
from config import upload_folder
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField,FileAllowed
from werkzeug.utils import secure_filename
from PIL import Image
import uuid
import os


public_bp = Blueprint("main_routes", __name__)

@public_bp.route("/")
def homepage():
    return redirect("/board/general")

@public_bp.route("/rules")
def rules():
   return render_template("rules.html")

@public_bp.route("/board/<request_topic>",methods=["GET","POST"])
def render_board(request_topic):
    class PostForm(FlaskForm):
        post_body = StringField("content",validators=[DataRequired(), Length(min=3, max=50)])
        image = FileField("image",validators=[FileAllowed(["jpg", "jpeg"])])
        submit = SubmitField("enter")
    form = PostForm()

    topic = Topics.query.filter_by(name=request_topic).first()
    if request.method == "GET":
       if not request_topic:
           request_topic = "general"   
       topics_list = Topics.query.all()
       posts = list(topic.posts) if topic.posts else [] 
       if not topic:
          return recirect("warning.html",error_text="The topic you selected does not exist")
       return render_template("index.html", posts=posts,topic_list=topics_list,form=form)

    if request.method == "POST" and form.validate_on_submit():
        post_body = form.post_body.data
        image = form.image.data
        image_filename = secure_filename(image.filename)
        image_path = os.path.join(upload_folder,image_filename)
        post_obj = Posts(post_content=post_body,image_path=image_filename,topic_id=topic.id)
        image.save(image_path)
        img = Image.open(image)
        clean = Image.new(img.mode, img.size)
        clean.putdata(list(img.getdata()))
        clean.save(image_path)
        db.session.add(post_obj)
        db.session.commit()
        return redirect("/")

@public_bp.route("/view/<filename>")
def view_image(filename):
    return send_from_directory(upload_folder,filename)

@public_bp.route("/reports",methods=["GET","POST"])
def reports():
    class ReportForm(FlaskForm):
        report_header = StringField("report_header",validators=[DataRequired(), Length(min=3, max=30)])
        report_body = StringField("report_body",validators=[DataRequired(), Length(min=3, max=50)])    
        submit = SubmitField("enter")
    form = ReportForm()

    if request.method == "GET":
        return render_template("reports.html",form=form)

    if request.method == "POST" and form.validate_on_submit():
        report_header = form.report_header.data
        report_body = form.report_body.data
        if not all([report_header,report_body]):
           return render_template("warning.html",error_text="One of the fields was left blank")
        new_report = Reports(report_header=report_header,report_body=report_body)
        db.session.add(new_report)
        db.session.commit()
        return redirect("/reports") 
