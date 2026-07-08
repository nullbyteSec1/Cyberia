from model import db,app
from routes.public import public_bp 
from routes.admin import admin_bp
import json

with open("config.json","r",encoding="utf-8") as config:
    data = json.load(config) 


hosting = data["hosting"]
porting = data["porting"]
secret_key = data["secret_key"]

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.secret_key = secret_key 
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp,url_prefix="/admin")
    app.run(debug=True,host=hosting,port=porting)
