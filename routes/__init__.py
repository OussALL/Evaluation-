from .auth import auth_bp
from .students import students_bp
from .dashboard import dashboard_bp
from .classes import classes_bp
from .home import home_bp
from .subjects import subjects_bp
from .profs import profs_bp
from students_routes.student_eval import student_eval_bp


all_blueprints = [auth_bp, students_bp, dashboard_bp,classes_bp,home_bp,subjects_bp,profs_bp,student_eval_bp]