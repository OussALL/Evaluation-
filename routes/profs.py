from flask import Flask,Blueprint,request,redirect,url_for,render_template,session,flash
from models.models import *
profs_bp=Blueprint('profs',__name__)

@profs_bp.route("/profs")
def profs():
    if 'school_username' and 'school_name' in session:
        profs=Profs.query.join(Profs.schools).join(Schools.user).filter(Users.username==session['school_username']).all()
        return render_template("profs.html",profs=profs)
    else:
        return redirect(url_for("home.home"))

@profs_bp.route("/edit_prof/<int:id>",methods=['POST','GET'])
def edit_prof(id):
        if 'school_username' and 'school_name' in session:
            school=Schools.query.join(Schools.user).filter(Users.username==session['school_username']).first()
            prof=Profs.query.get(id)
            if prof in school.profs:
                if request.method=="POST":
                        lname=request.form.get("nom").strip()
                        fname=request.form.get("prenom").strip()
                        prof.fname=fname
                        prof.lname=lname
                        db.session.commit()
                        flash("Prof updated successfully.", "success")
                        return redirect(url_for('profs.profs'))
                else:
                        return render_template("edit_prof.html",prof=prof)
            else:
                return render_template("error_page.html")
        else:
            return redirect(url_for("home.home")) 

@profs_bp.route('/delete_prof/<int:id>')
def delete_prof(id):
    if 'school_username' and 'school_name' in session:
        school=Schools.query.join(Schools.user).filter(Users.username==session['school_username']).first()
        prof=Profs.query.get(id)
        if prof in school.profs:
            Profs.query.filter_by(id=id).delete()
            db.session.commit()
            flash("Prof deleted successfully.", "success")
            return redirect(url_for('profs.profs'))
        else:
            return render_template("error_page.html")
    else:
        return redirect(url_for("home.home"))
    
@profs_bp.route('/add_prof',methods=['POST','GET'])
def add_prof():
    if 'school_username' and 'school_name' in session:
        if request.method=="POST":
            lname=request.form.get("nom").strip()
            fname=request.form.get("prenom").strip()
            immatriculation=request.form.get("immatriculation").strip()
            already_exist=Profs.query.join(Profs.schools).join(Schools.user).filter(Users.username==session['school_username'],Profs.immatriculation==immatriculation).first()
            if already_exist:
                flash("Prof / immaatriculation already exist.", "failed")
                return redirect(url_for('profs.profs'))
            new_prof=Profs(fname=fname,lname=lname,immatriculation=immatriculation)
            db.session.add(new_prof)
            school=Schools.query.join(Schools.user).filter(and_(Users.username==session["school_username"],Schools.name==session['school_name'])).first()
            school.profs.append(new_prof)
            db.session.commit()
            flash("Prof added successfully.", "success")
        return redirect(url_for('profs.profs'))
    else:
        return redirect(url_for("home.home"))