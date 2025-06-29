from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_
from extensions import db

school_prof=db.Table('school_prof',
                     db.Column('school_id',db.Integer,db.ForeignKey('schools.id', ondelete="CASCADE"),primary_key=True),
                     db.Column('prof_id',db.Integer,db.ForeignKey('profs.id', ondelete="CASCADE"),primary_key=True))
subject_prof=db.Table('subject_prof',
                     db.Column('subject_id',db.Integer,db.ForeignKey('subjects.id', ondelete="CASCADE"),primary_key=True),
                     db.Column('prof_id',db.Integer,db.ForeignKey('profs.id', ondelete="CASCADE"),primary_key=True))
subject_classe=db.Table('subject_classe',
                     db.Column('subject_id',db.Integer,db.ForeignKey('subjects.id', ondelete="CASCADE"),primary_key=True),
                     db.Column('classe_id',db.Integer,db.ForeignKey('classes.id', ondelete="CASCADE"),primary_key=True))

class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(1000),unique=True)
    email=db.Column(db.String(1000),unique=True)
    password=db.Column(db.String(1000))
    role=db.Column(db.String(1000))
    schools=db.relationship('Schools',back_populates='user',uselist=False,passive_deletes=True)
    students=db.relationship('Students',back_populates='user',uselist=False,passive_deletes=True)
# uselist : each User can only be linked to one School / Student
class Schools(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(1000),unique=True)
    abbr=db.Column(db.String(1000))
    profs=db.relationship('Profs',secondary=school_prof,back_populates='schools',passive_deletes=True)
    classes=db.relationship('Classes',back_populates='schools')
    subjects=db.relationship('Subjects',back_populates='schools')
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),unique=True,nullable=False)
    user=db.relationship('Users',back_populates='schools',passive_deletes=True)
#passive_deletes=True : let the database handle cascading deletes via ON DELETE CASCADE
# ==> which improves performance by reducing application-side SQL queries.


class Student_Eval(db.Model):
    student_id=db.Column(db.Integer,db.ForeignKey('students.id', ondelete="CASCADE"),primary_key=True)
    students=db.relationship('Students',back_populates='eval')
    subjects_counts=db.Column(db.Integer,default=0)

class Students(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(200))
    lname=db.Column(db.String(200))
    classe_id=db.Column(db.Integer,db.ForeignKey('classes.id'))
    classes=db.relationship('Classes',back_populates='students',passive_deletes=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),unique=True,nullable=False)
    user=db.relationship('Users',back_populates='students',passive_deletes=True)
    eval=db.relationship('Student_Eval',back_populates='students',passive_deletes=True)
    questionstrack=db.relationship('QuestionsTrack',back_populates='students',passive_deletes=True)


class Classes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(1000))
    students_nbrs=db.Column(db.Integer)
    school_id=db.Column(db.Integer,db.ForeignKey('schools.id'))
    schools=db.relationship('Schools',back_populates='classes',passive_deletes=True)
    students=db.relationship('Students',back_populates='classes',passive_deletes=True)
    subjects=db.relationship('Subjects',secondary=subject_classe,back_populates='classes',passive_deletes=True)
    eval=db.Column(db.Integer,default=0)
    questionstrack=db.relationship('QuestionsTrack',back_populates='classes',passive_deletes=True)

class Subjects(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(1000))
    profs=db.relationship('Profs',secondary=subject_prof,back_populates='subjects',passive_deletes=True)
    classes=db.relationship('Classes',secondary=subject_classe,back_populates='subjects',passive_deletes=True)
    questionstrack=db.relationship('QuestionsTrack',back_populates='subjects',passive_deletes=True)
    school_id=db.Column(db.Integer,db.ForeignKey('schools.id'))
    schools=db.relationship('Schools',back_populates='subjects',passive_deletes=True)

class Profs(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(200))
    lname=db.Column(db.String(200))
    immatriculation=db.Column(db.Integer,unique=True)
    schools=db.relationship('Schools',secondary=school_prof,back_populates='profs',passive_deletes=True)
    subjects=db.relationship('Subjects',secondary=subject_prof,back_populates='profs',passive_deletes=True)
    questionstrack=db.relationship('QuestionsTrack',back_populates='profs',passive_deletes=True)


class QuestionsTrack(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey('students.id',ondelete="CASCADE"))
    students=db.relationship('Students',back_populates='questionstrack',passive_deletes=True)
    classe_id=db.Column(db.Integer,db.ForeignKey('classes.id',ondelete="CASCADE"))
    classes=db.relationship('Classes',back_populates='questionstrack',passive_deletes=True)
    prof_id=db.Column(db.Integer,db.ForeignKey('profs.id',ondelete="CASCADE"))
    profs=db.relationship('Profs',back_populates='questionstrack',passive_deletes=True)
    subject_id=db.Column(db.Integer,db.ForeignKey('subjects.id',ondelete="CASCADE"))
    subjects=db.relationship('Subjects',back_populates='questionstrack',passive_deletes=True)
    q1=db.Column(db.Integer)
    q2=db.Column(db.Integer)
    q3=db.Column(db.Integer)
    q4=db.Column(db.Integer)
    c1=db.Column(db.String(9000))
    c2=db.Column(db.String(9000))


#### this code below : This code enables foreign key constraints in SQLite on every connection
# ensuring that rules like `ON DELETE CASCADE` are properly enforced, as SQLite disables them by default.
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
