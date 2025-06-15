from flask import Flask,Blueprint,request,redirect,url_for,render_template,session
from models.models import *
auth_bp=Blueprint('auth',__name__)



@auth_bp.route("/signup",methods=['POST','GET'])
def signup():
    if 'school_username' and 'school_name' in session:
                return redirect(url_for('dashboard'))
    else:
        if request.method=="POST":
            name=request.form.get("name")
            abbr=request.form.get("abbr")
            email=request.form.get("email")
            username=request.form.get("username")
            password=request.form.get("password")
            already_exist=Users.query.filter(or_(Users.username==username,Users.email==email)).first()
            if already_exist:
                return "g"
            if name and abbr and email and username and password:
                new_user=Users(username=username,email=email,password=password,role="school")
                db.session.add(new_user)
                db.session.flush()
                new_school=Schools(name=name,abbr=abbr,user_id=new_user.id)
                db.session.add(new_school)
                db.session.commit()
                session['school_username']=new_user.username
                session['school_name']=new_school.name
                return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('home'))


@auth_bp.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user_exist=Users.query.filter((Users.username==username)&(Users.password==password)).first()
        if user_exist:
            if user_exist.role=="school":
                session['school_username']=user_exist.username
                session['school_name']=user_exist.schools.name
                return redirect(url_for('dashboard'))
            elif user_exist.role=="student":
                session['student_username']=user_exist.username
                session['student_name']=user_exist.students.fname+" "+user_exist.students.lname
                return redirect(url_for('student_home'))
    else:
        return redirect(url_for('home'))
    
@auth_bp.route('/logout')
def logout():
        session.clear()
        return redirect(url_for('home'))

