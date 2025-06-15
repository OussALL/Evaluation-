from flask import Flask,Blueprint,request,redirect,url_for,render_template,session
from models.models import *
subjects_bp=Blueprint('subjects',__name__)

    
@subjects_bp.route("/subjects")
def subjects():
    if 'school_username' and 'school_name' in session:
        subjects=Subjects.query.join(Subjects.classes).join(Classes.schools).filter(Schools.name==session['school_name']).all()
        classes=Classes.query.join(Classes.schools).filter(Schools.name==session['school_name']).all()
        profs=Profs.query.join(Profs.schools).filter(Schools.name==session['school_name']).all()

        return render_template("subjects.html",subjects=subjects,classes=classes,profs=profs)
    else:
        return redirect(url_for("home"))
      
@subjects_bp.route("/edit_subject/<int:id>",methods=['POST','GET'])
def edit_subject(id):
    if 'school_username' and 'school_name' in session:
        subject=Subjects.query.get(id)
        subjects=Subjects.query.join(Subjects.classes).join(Classes.schools).filter(Schools.name==session['school_username']).all()
        if subject in subjects: 
            if request.method=="POST":
                name=request.form.get("nom")
                form_classes=request.form.get("selectedClasses")
                form_profs=request.form.get("selectedProfs")
                if name:
                    subject.name=name 
                id_classes=[]
                id_profs=[]
                for i in form_classes.split(","):
                    id_classes.append(int(i.strip("[]").strip()))
                for i in form_profs.split(","):
                    id_profs.append(int(i.strip("[]").strip()))
                classes=Classes.query.filter(Classes.id.in_(id_classes)).all()
                subject.classes=classes
                profs=Profs.query.filter(Profs.id.in_(id_profs)).all()
                subject.profs=profs
                db.session.commit()
                return redirect(url_for('subjects'))
            else:   
                classes=Classes.query.join(Classes.schools).filter(Schools.name==session['school_name']).all()
                profs=Profs.query.join(Profs.schools).filter(Schools.name==session['school_name']).all()
                selected_classes=[{'id':classe.id,'name':classe.name} for classe in subject.classes]
                selected_profs=[{'id':prof.id,'name':prof.fname+" "+prof.lname} for prof in subject.profs]
                return render_template("edit_subject.html",subject=subject,classes=classes,profs=profs,selected_classes=selected_classes,selected_profs=selected_profs)
        else:
                return render_template("error_page.html")

    else:
            return redirect(url_for("home")) 
    
@subjects_bp.route('/delete_subject/<int:id>')
def delete_subject(id):
    if 'school_username' and 'school_name' in session:
        subject=Subjects.query.get(id)
        subjects=Subjects.query.join(Subjects.classes).join(Classes.schools).filter(Schools.name==session['school_username']).all()
        if subject in subjects:
            Subjects.query.filter_by(id=id).delete()
            db.session.commit()
            return redirect(url_for('subjects'))
        else:
            return render_template("error_page.html")
    else:
        return redirect(url_for("home"))


@subjects_bp.route('/add_subject', methods=['POST', 'GET'])
def add_subject():
    if 'school_username' in session and 'school_name' in session:
        if request.method == 'POST':
            name = request.form.get("name", "").strip()
            form_classes = request.form.get("selectedClasses", "")
            form_profs = request.form.get("selectedProfs", "")

            id_classes = [int(i.strip()) for i in form_classes.strip("[]").split(",") if i.strip().isdigit()]
            id_profs = [int(i.strip()) for i in form_profs.strip("[]").split(",") if i.strip().isdigit()]

            classes = Classes.query.filter(Classes.id.in_(id_classes)).all() if id_classes else []
            profs = Profs.query.filter(Profs.id.in_(id_profs)).all() if id_profs else []

            if name and classes and profs:
                new_subject = Subjects(name=name, profs=profs, classes=classes)
                db.session.add(new_subject)
                db.session.commit()

            return redirect(url_for('subjects'))
        else:
            return redirect(url_for('subjects'))
    else:
        return redirect(url_for("home"))