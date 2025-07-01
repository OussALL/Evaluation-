from flask import Flask,render_template,request,session,redirect,url_for
from config import Config
from routes import all_blueprints
from extensions import mail,db



def create_app():
    app= Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    for bp in all_blueprints:
        app.register_blueprint(bp)
    app.secret_key='eval_project'
    return app
    
app = create_app()
if __name__=="__main__":
    app=create_app()
    with app.app_context():
        db.create_all()
    