from model import db,app
from routes.public import public_bp 
from routes.admin import admin_bp
from config import hosting,porting,secret_key

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.secret_key = secret_key 
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp,url_prefix="/admin")
    app.run(debug=True,host=hosting,port=porting)
