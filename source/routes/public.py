from flask import Blueprint, request, render_template, jsonify, redirect, send_from_directory, make_response
from model import Posts,Topics,Reports,db
import uuid

public_bp = Blueprint("main_routes", __name__)

@public_bp.route("/")
def homepage():
    return redirect("/board/general")

@public_bp.route("/rules")
def rules():
    return render_template("rules.html")

@public_bp.route("/board/<topic>")
def render_board(topic):
    if not topic:
        topic = "general"
    
    topic_obj = Topics.query.filter_by(name=topic).first()
    topics_list = Topics.query.all()
    if not topic_obj:
        return recirect("/")
    posts = list(topic_obj.posts) if topic_obj.posts else []
    
    resp = make_response(render_template("index.html", posts=posts,topic_list=topics_list))
    resp.set_cookie("topic_name", topic)
    return resp

@public_bp.route("/view/<filename>")
def view_image(filename):
    return send_from_directory("./uploads", filename)

@public_bp.route("/reports",methods=["GET","POST"])
def reports():
    if request.method == "GET":
        return render_template("reports.html")

    report_header = request.form.get("report_header")
    report_body = request.form.get("report_body")

    if not all([report_header,report_body]):
        return render_template("warning.html",error_text="One of the fields was left blank")

    new_report = Reports(report_header=report_header,report_body=report_body)
    db.session.add(new_report)
    db.session.commit()
    return redirect("/reports")
    
@public_bp.route("/send/post", methods=["POST"])
def send_post():
    post_content = request.form.get("content")
    image_to_post = request.files.get("image")
    topic_post = request.cookies.get("topic_name")

    if not post_content or not image_to_post or not topic_post:
        return render_template("warning.html",error_text="Please fill in all the fields")

    try:
        filename = f"{uuid.uuid4().hex}.jpg"
        image_to_post.save(f"./uploads/{filename}") 
        topic_obj = Topics.query.filter_by(name=topic_post).first()
        if not topic_obj:
            return redirect("/")
        
        new_post = Posts(post_content=post_content, image_path=filename, topic_id=topic_obj.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/")
    
    except Exception as e:
        print(e)
        return render_template("warning.html","Internal server error. Please try again.")
