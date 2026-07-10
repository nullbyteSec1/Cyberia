from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Topics(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    posts = db.relationship(
        "Posts",
        backref="topic",
        lazy=True,
        cascade="all, delete-orphan"
    )

class Posts(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    post_content = db.Column(db.String(1000), nullable=True)
    image_path = db.Column(db.String(100), nullable=True)
    topic_id = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=False
    )

class Reports(db.Model):
    __tablename__ = "reports"
    id = db.Column(db.Integer,primary_key=True)
    report_header = db.Column(db.String(100),nullable=True)
    report_body = db.Column(db.String(200),nullable=True)

class moderator_accounts(db.Model):
    __tablename__ = "moderator_accounts"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),nullable=True)
    password = db.Column(db.String(300),nullable=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
        if not Topics.query.filter_by(name="general").first():
            topic_general = Topics(name="general")
            topic_programming = Topics(name="programmimg")
            topic_memes = Topics(name="memes")

            db.session.add_all([topic_general,topic_programming,topic_memes])
            db.session.commit()
            print("Tópicos criados com sucesso!")
        else:
            print("Tópicos já existem no banco de dados.")
