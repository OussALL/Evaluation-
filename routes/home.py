from flask import Blueprint,redirect,url_for,render_template,session
home_bp=Blueprint('home',__name__)

@home_bp.route('/')
def home():
    if 'school_username' and 'school_name' in session:
        return redirect(url_for("dashboard.dashboard"))
    elif 'student_username' and 'student_name' in session:
        return redirect(url_for("students.student_home"))
    else:
        return render_template("login.html")


