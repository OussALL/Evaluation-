from flask import Blueprint,redirect,url_for,render_template,session
from models.models import Schools,Students,Classes,Subjects,Profs,db
dashboard_bp=Blueprint('dashboard',__name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'school_username' and 'school_name' in session:
        students=Students.query.join(Students.classes).join(Classes.schools).filter(Schools.name==session['school_name']).all()
        classes=Classes.query.join(Classes.schools).filter(Schools.name==session['school_name']).all()
        profs=Profs.query.join(Profs.schools).filter(Schools.name==session['school_name']).all()
        subjects=Subjects.query.join(Subjects.classes).join(Classes.schools).filter(Schools.name==session['school_name']).all()
        return render_template("dashboard.html",students=students,classes=classes,profs=profs,subjects=subjects)
    else:
        return redirect(url_for("home.home"))
    
