from flask import Flask,Blueprint,request,redirect,url_for,render_template,session
from models.models import *
from utils.graphs import make_graph 
classes_bp=Blueprint('classes',__name__)



@classes_bp.route("/classes")
def classes():
    if 'school_username' and 'school_name' in session:
        classes=Classes.query.join(Classes.schools).filter(Schools.name==session['school_name']).all()
        return render_template("classes.html",classes=classes)
    else:
        return redirect(url_for("home"))
    
@classes_bp.route('/edit_classe/<int:id>',methods=['POST','GET'])
def edit_classe(id):
    if 'school_username' and 'school_name' in session:
        classe=Classes.query.get(id)
        classes=Classes.query.join(Classes.schools).filter(Schools.name==session['school_name']).all()
        if classe in classes:
            if request.method=="POST":
                name=request.form.get("nom").strip()
                classe.name=name
                db.session.commit()
                return render_template("edit_classe.html",classe=classe)    
            else:
                return render_template("edit_classe.html",classe=classe)    
        else:
            return render_template("error_page.html")
    else:
        return redirect(url_for("home"))

@classes_bp.route('/delete_classe/<int:id>')
def delete_classe(id):
    if 'school_username' and 'school_name' in session:
        classe=Classes.query.get(id)
        classes=Classes.query.join(Classes.schools).filter(Schools.name==session['school_name']).all()
        if classe in classes:
            for student in classe.students:
                student.classe_id=None
                db.session.flush()
            Classes.query.filter_by(id=id).delete()
            db.session.commit()
            return redirect(url_for('classes'))
        else:
            return render_template("error_page.html")
    else:
        return redirect(url_for("home"))
    
@classes_bp.route('/add_classe',methods=['POST','GET'])
def add_classe():
        if request.method=="POST":
            school=Schools.query.join(Schools.user).filter(Users.username==session['school_username']).first()
            name=request.form.get("nom").strip()
            new_classe=Classes(name=name,students_nbrs=0,school_id=school.id)
            db.session.add(new_classe)
            db.session.commit()
            db.session.close()
            return redirect(url_for('classes'))
        else: 
            return redirect(url_for('classes'))


@classes_bp.route('/start_eval/<int:id>')
def start_eval(id):
    if 'school_username' and 'school_name' in session:
        classe=Classes.query.get(id)
        if classe.eval==0:
            classe.eval=1
            db.session.flush()
            for student in classe.students:
                new_student_eval=Student_Eval(student_id=student.id)
                db.session.add(new_student_eval)
        elif classe.eval==1:
            classe.eval=0
            db.session.flush()
            for student in classe.students:
                Student_Eval.query.filter_by(student_id=student.id).delete()
                db.session.flush()

        db.session.commit()
        return redirect(url_for('classes'))
    else:
        return redirect(url_for("home"))

@classes_bp.route('/rapport/<int:id>')
def rapport(id):
    classe=Classes.query.filter_by(id=id).first()
    return render_template("subjects_rapport.html",classe=classe,qt=QuestionsTrack)

@classes_bp.route('/rapport/<int:classe_id>/<int:subject_id>')
def rapport_details(classe_id,subject_id):
    classe=Classes.query.filter_by(id=classe_id).first()
    subject=Subjects.query.filter_by(id=subject_id).first()
    qt=QuestionsTrack.query.filter((QuestionsTrack.classe_id==classe_id)&(QuestionsTrack.subject_id==subject_id))
    valeurs_q1=[qt.filter(QuestionsTrack.q1==1).count()
                ,qt.filter(QuestionsTrack.q1==2).count()
                ,qt.filter(QuestionsTrack.q1==3).count()
                ,qt.filter(QuestionsTrack.q1==4).count()
                ,qt.filter(QuestionsTrack.q1==5).count()]
    make_graph(valeurs_q1,1,subject_id,classe_id)
    valeurs_q2=[qt.filter(QuestionsTrack.q2==1).count()
                ,qt.filter(QuestionsTrack.q2==2).count()
                ,qt.filter(QuestionsTrack.q2==3).count()
                ,qt.filter(QuestionsTrack.q2==4).count()
                ,qt.filter(QuestionsTrack.q2==5).count()]
    make_graph(valeurs_q2,2,subject_id,classe_id)
    valeurs_q3=[qt.filter(QuestionsTrack.q3==1).count()
                ,qt.filter(QuestionsTrack.q3==2).count()
                ,qt.filter(QuestionsTrack.q3==3).count()
                ,qt.filter(QuestionsTrack.q3==4).count()
                ,qt.filter(QuestionsTrack.q3==5).count()]
    make_graph(valeurs_q3,3,subject_id,classe_id)
    valeurs_q4=[qt.filter(QuestionsTrack.q4==1).count()
                ,qt.filter(QuestionsTrack.q4==2).count()
                ,qt.filter(QuestionsTrack.q4==3).count()
                ,qt.filter(QuestionsTrack.q4==4).count()
                ,qt.filter(QuestionsTrack.q4==5).count()]
    make_graph(valeurs_q4,4,subject_id,classe_id)
    c1=qt.all()
    c2=qt.all()
    return render_template("rapport.html",c1=c1,c2=c2,classe=classe,subject=subject,classe_id=str(classe_id),subject_id=str(subject_id))