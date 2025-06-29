from flask import Blueprint,request,redirect,url_for,render_template,session,flash
from models.models import Users,Schools,Classes,Subjects,Profs
from sqlalchemy import func

subjects_bp=Blueprint('subjects',__name__)

    

@subjects_bp.route("/subjects")
def subjects():
    if 'school_username' and 'school_name' in session:
        school=Schools.query.join(Schools.user).filter(Users.username==session['school_username']).first()
        subjects=Subjects.query.filter_by(school_id=school.id).all()
        classes=Classes.query.join(Classes.schools).filter(Schools.name==session['school_name']).all()
        profs=Profs.query.join(Profs.schools).filter(Schools.name==session['school_name']).all()
        return render_template("subjects.html",subjects=subjects,classes=classes,profs=profs)
    else:
        return redirect(url_for("home.home"))
      
@subjects_bp.route("/edit_subject/<int:id>",methods=['POST','GET'])
def edit_subject(id):
    if 'school_username' and 'school_name' in session:
        school=Schools.query.join(Schools.user).filter(Users.username==session['school_username']).first()
        subject=Subjects.query.get(id)
        subjects=Subjects.query.filter_by(school_id=school.id).all()
        all_school_classes=Classes.query.join(Classes.schools).join(Schools.user).filter(Users.username==session['school_username']).all()
        all_school_profs=Profs.query.join(Profs.schools).join(Schools.user).filter(Users.username==session['school_username']).all()
        if subject in subjects: 
            if request.method=="POST":
                name=request.form.get("nom")
                form_classes=request.form.get("selectedClasses")
                form_profs=request.form.get("selectedProfs")
                if name:
                    subject.name=name 
                id_classes=[]
                id_profs=[]
                for i in form_classes:
                    if i.isdigit():
                        id_classes.append(int(i))
                for i in form_profs:
                    if i.isdigit():
                        id_profs.append(int(i))
                classes=Classes.query.filter(Classes.id.in_(id_classes)).all()
                subject.classes=classes
                profs=Profs.query.filter(Profs.id.in_(id_profs)).all()
                subject.profs=profs
                db.session.commit()
                flash("Subject updated successfully.", "success")
                return redirect(url_for('subjects.subjects'))
            else:   
                classes=Classes.query.join(Classes.schools).join(Schools.user).filter(Users.username==session['school_username']).all()
                profs=Profs.query.join(Profs.schools).join(Schools.user).filter(Users.username==session['school_username']).all()
                selected_classes=[{'id':classe.id,'name':classe.name} for classe in subject.classes if classe in all_school_classes]
                selected_profs=[{'id':prof.id,'name':prof.fname+" "+prof.lname} for prof in subject.profs if prof in all_school_profs]
                return render_template("edit_subject.html",subject=subject,classes=classes,profs=profs,selected_classes=selected_classes,selected_profs=selected_profs)
        else:
                return render_template("error_page.html")

    else:
            return redirect(url_for("home.home")) 
    
@subjects_bp.route('/delete_subject/<int:id>')
def delete_subject(id):
    if 'school_username' and 'school_name' in session:
        school=Schools.query.join(Schools.user).filter(Users.username==session['school_username']).first()
        subject=Subjects.query.get(id)
        subjects=Subjects.query.filter_by(school_id=school.id).all()
        if subject in subjects:
            Subjects.query.filter_by(id=id).delete()
            db.session.commit()
            flash("Subject deleted successfully.", "success")
            return redirect(url_for('subjects.subjects'))
        else:
            return render_template("error_page.html")
    else:
        return redirect(url_for("home.home"))


@subjects_bp.route('/add_subject', methods=['POST', 'GET'])
def add_subject():
    if 'school_username' in session and 'school_name' in session:
        school=Schools.query.join(Schools.user).filter(Users.username==session['school_username']).first()   
        if request.method == 'POST':
            name = request.form.get("name", "").strip()
            form_classes = request.form.get("selectedClasses", "")
            form_profs = request.form.get("selectedProfs", "")
            id_classes = [int(i.strip()) for i in form_classes.strip("[]").split(",") if i.strip().isdigit()]
            id_profs = [int(i.strip()) for i in form_profs.strip("[]").split(",") if i.strip().isdigit()]
            if name:
                subject_exist=Subjects.query.join(Subjects.classes).join(Classes.schools).join(Schools.user).filter(
                    (func.lower(Subjects.name)==name.lower())&(Users.username==session['school_username'])
                ).first()
                if subject_exist:
                    for prof_id in id_profs:
                        prof=Profs.query.get(prof_id)
                        if prof in subject_exist.profs:
                            id_profs.remove(prof_id)
                    for classe_id in id_classes:
                        classe=Classes.query.get(classe_id)
                        if classe in subject_exist.classes:
                            id_classes.remove(classe_id)
                    if not id_profs and not id_classes:
                        flash("Subject already exist.", "failed")
                        return redirect(url_for('subjects.subjects'))
                    if not id_classes:
                        for prof_id in id_profs:
                            prof=Profs.query.get(prof_id)
                            subject_exist.profs.append(prof)
                            db.session.commit()  
                        flash("Subject added successfully.", "success")
                        return redirect(url_for('subjects.subjects'))
                        
                classes = Classes.query.filter(Classes.id.in_(id_classes)).all() if id_classes else []
                profs = Profs.query.filter(Profs.id.in_(id_profs)).all() if id_profs else []
                new_subject = Subjects(name=name, profs=profs, classes=classes,school_id=school.id)
                db.session.add(new_subject)
                db.session.commit()
                flash("Subject added successfully.", "success")
                
            else:
                flash("Please fill in all required fields.", "failed")
            return redirect(url_for('subjects.subjects'))
    else:
        return redirect(url_for("home.home"))