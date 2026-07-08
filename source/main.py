from model import db,app
from routes.public import public_bp 
from routes.admin import admin_bp

hosting = "localhost"
porting = 8080

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.secret_key = "3905ed174eca6e6d443ccfb4b9b1c77b430ea2b800ccec9c5a3c2ae3e9378b5e"
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp,url_prefix="/admin")
    app.run(debug=True,host=hosting,port=porting)
