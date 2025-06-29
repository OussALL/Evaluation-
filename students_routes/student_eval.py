from flask import Flask,Blueprint,request,redirect,url_for,render_template,session
from models.models import *
student_eval_bp=Blueprint('student_eval',__name__)

@student_eval_bp.route('/questions/<int:subject_id>_<int:prof_id>_<int:classe_id>>',methods=['POST','GET'])
def questions(subject_id,prof_id,classe_id):
    if 'student_username' and 'student_name' in session:
        if request.method=="POST":
            student=Students.query.join(Students.user).filter(Users.username==session["student_username"]).first()
            q1=int(request.form.get("radio1").strip())
            q2=int(request.form.get("radio2").strip())
            q3=int(request.form.get("radio3").strip())
            q4=int(request.form.get("radio4").strip())
            q5=request.form.get("commentaire1").strip()
            q6=request.form.get("commentaire2").strip()
            newQT=QuestionsTrack(student_id=student.id,classe_id=classe_id,prof_id=prof_id,subject_id=subject_id,
                                q1=q1,q2=q2,q3=q3,q4=q4,c1=q5,c2=q6)
            db.session.add(newQT)
            recent_subject=Student_Eval.query.filter_by(student_id=student.id).first()
            recent_subject.subjects_counts+=1
            db.session.commit()
            return redirect(url_for('students.student_home'))
        else:
            subject=Subjects.query.filter_by(id=subject_id).first()
            prof=Profs.query.filter_by(id=prof_id).first()
            classe=Classes.query.filter_by(id=classe_id).first()
            return render_template('questions.html',subject=subject,prof=prof,classe=classe)

    else:
        return redirect(url_for("home.home"))