import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    secret_key='eval_project'
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT=465
    MAIL_USERNAME="isgaprojet@gmail.com"
    MAIL_PASSWORD="odim sjkt zayx erpe"
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True
    