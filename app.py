from flask import Flask,render_template,request,session,redirect,url_for
from config import Config
from models.models import db
from routes import all_blueprints
from flask_mail import Mail
mail=Mail()
def create_app():
    app= Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app

if __name__=="__main__":
    app=create_app()
    app.run(debug=True)