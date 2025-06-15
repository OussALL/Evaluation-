from flask import Flask,Blueprint,request,redirect,url_for,render_template,session
from models.models import *
home_bp=Blueprint('home',__name__)

@home_bp.route('/')
def home():
    if 'school_username' and 'school_name' in session:
        return redirect(url_for("dashboard"))
    elif 'student_username' and 'student_name' in session:
        return redirect(url_for("student_home"))
    else:
        return render_template("login.html")


