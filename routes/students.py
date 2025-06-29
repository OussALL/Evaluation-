from flask import Blueprint,request,redirect,url_for,render_template,session,flash
from models.models import Users,Schools,Student_Eval,Students,Classes,db
from utils.send_mail import send_mail
from extensions import mail 
students_bp=Blueprint('students',__name__)

@students_bp.route("/student",methods=['POST','GET'])
def student_home():
    if 'student_username' and 'student_name' in session:
        student=Students.query.join(Students.user).filter(Users.username==session["student_username"]).first()
        classe=Classes.query.filter_by(id=student.classe_id).first()
        recent_subject=Student_Eval.query.filter_by(student_id=student.id).first()
        if request.method=="POST":
            type=request.form.get("button").strip()
            prof_id=request.form.get("teacher").strip()
            if type=="skip":
                recent_subject.subjects_counts+=1
                db.session.commit()
                return redirect(url_for('students.student_home'))
            elif type=="start":
                return redirect(url_for('student_eval.questions',subject_id=student.classes.subjects[recent_subject.subjects_counts].id
                                                    ,prof_id=int(prof_id)
                                                    ,classe_id=classe.id))
        else:
            if student.classes.eval==1:
                if recent_subject.subjects_counts<len(student.classes.subjects):
                    subject=student.classes.subjects[recent_subject.subjects_counts]
                    return render_template('index.html',student=student,subject=subject)
                else:
                    return render_template("done.html")
            else:
                return render_template('noevaluation.html',student=student)
    else:
        return redirect(url_for("home.home"))
    
@students_bp.route('/students')
def students():
    if 'school_username' and 'school_name' in session:
        students=Students.query.join(Students.classes).join(Classes.schools).filter(Schools.name==session['school_name']).all()
        classes=Classes.query.join(Classes.schools).filter(Schools.name==session['school_name']).all()
        return render_template("etudiants.html",students=students,classes=classes)
    else:
        return redirect(url_for('home.home'))
    



@students_bp.route('/edit_student/<int:id>',methods=['POST','GET'])
def edit_student(id):
    if 'school_username' and 'school_name' in session:
        student=Students.query.get(id)
        classes=Classes.query.join(Classes.schools).filter(Schools.name==session['school_name']).all()
        students=Students.query.join(Students.classes).join(Classes.schools).join(Schools.user).filter(Users.username==session['school_username']).all()
        if student in students:
            if request.method=="POST":
                lname=request.form.get('nom').strip()
                fname=request.form.get('prenom').strip()
                email=request.form.get('email').strip()
                classe=request.form.get('classe').strip()
                student.fname=fname
                student.lname=lname
                student.user.email=email
                student.classe_id=Classes.query.join(Classes.schools).filter((Schools.name==session['school_name'])&(Classes.name==classe)).first().id
                db.session.commit()
                flash("Student updated successfully.", "success")
                return redirect(url_for('students.students'))
            else:   
                return render_template("edit_student.html",student=student,classes=classes)
        else:
            return render_template("error_page.html")
    else:
            return redirect(url_for('home.home'))
    

@students_bp.route('/delete_student/<int:id>')
def delete_student(id):
    if 'school_username' and 'school_name' in session:
        student=Students.query.get(id)
        students=Students.query.join(Students.classes).join(Classes.schools).join(Schools.user).filter(Users.username==session['school_username']).all()
        if student in students:
            Students.query.filter_by(id=id).delete()
            db.session.commit()
            flash("student deleted successfully.", "success")
            return redirect(url_for('students.students'))
        else:
            return render_template("error_page.html")
    else:
        return redirect(url_for("home.home"))
    
@students_bp.route('/add_student',methods=['POST','GET'])
def add_student():
    if 'school_username' and 'school_name' in session:
        if request.method=="POST":
            lname=request.form.get("nom").strip()
            fname=request.form.get("prenom").strip()
            email=request.form.get("email").strip()
            student_exist=Students.query.join(Students.user).filter(Users.email==email).first()
            if student_exist:
                flash("Student already exist.", "failed")
                return redirect(url_for('students.students'))
            if request.form.get("classe"):
                classe=request.form.get("classe").strip()
            username=lname+str(Users.query.count())
            password=username+"_"+str(Students.query.count())
            new_user=Users(username=username,email=email,password=password,role="student")
            db.session.add(new_user)
            db.session.flush()
            new_student=Students(fname=fname,
                                lname=lname, 
                                classe_id=Classes.query.join(Classes.schools).filter((Schools.name==session['school_name'])&(Classes.name==classe)).first().id,
                                user_id=new_user.id)
            db.session.add(new_student)
            db.session.flush()
            if new_student.classes.eval==1:
                new_student_eval=Student_Eval(student_id=new_student.id)
                db.session.add(new_student_eval)
            db.session.commit()
            flash("Student added successfully.", "success")
        return redirect(url_for('students.students'))
    else:
        return redirect(url_for("home.home"))

@students_bp.route('/reset_password/<int:id>')
def reset_password(id):
    if 'school_username' and 'school_name' in session:
        student=Students.query.get(id)
        students=Students.query.join(Students.classes).join(Classes.schools).filter(Schools.name==session['school_name']).all()
        if student in students:
            student.user.password=student.user.username+"_"+str(Students.query.count())
            db.session.commit()
            send_mail(mail,student.user.email,student.fname,student.lname,student.user.username,student.user.password)
            flash("Password reset successfully.", "success")
            return redirect(url_for('students.students'))
        else:
            return render_template("error_page.html")
    else:
        return redirect(url_for("home.home"))