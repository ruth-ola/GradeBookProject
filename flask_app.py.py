
"""@app.route('/')
def hello_world():
    return 'Hello from Flask!'"""
"""
Routes and views for the flask application.
"""
# A very simple Flask Hello World app for you to get started with...
from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, flash, jsonify, session, abort
from flask_login import login_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship, backref


app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://rutola:is6682020@rutola.mysql.pythonanywhere-services.com/rutola$isgradebook".format(
    username="rutola",
    password="is6682020",
    hostname="rutola.mysql.pythonanywhere-services.com",
    databasename="rutola$isgradebook",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "Nothing Lasts Forever"
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

class Student(db.Model):

    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(4096))
    last_name = db.Column(db.String(4096))
    email = db.Column(db.String(4096))
    major = db.Column(db.String(4096))
    course = db.Column(db.String(4096))
    t_grade = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user = relationship("User", backref=backref("student", uselist=False))


    def get_id(self):
        return self.student_id

class Faculty(db.Model):

    __tablename__ = "faculty"

    professor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(4096))
    last_name = db.Column(db.String(4096))
    email = db.Column(db.String(4096))
    course = db.Column(db.String(4096))

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user = relationship("User", backref=backref("faculty", uselist=False))

class Administration(db.Model):

    __tablename__ = "admin"

    admin_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(4096))
    last_name = db.Column(db.String(4096))
    email = db.Column(db.String(4096))

class Assignment(db.Model):

    __tablename__ = "assignment"

    assgn_id = db.Column(db.Integer, primary_key=True)
    assgn_title = db.Column(db.String(4096))
    course = db.Column(db.String(4096))
    grade  = db.Column(db.Integer)

    def get_id(self):
        return self.assgn_id

"""class Grades(db.Model):

    __tablename__ = "grade"

    grade_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    assgn_id = db.Column(db.Integer)
    grades = db.Column(db.Integer)

    #student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))
    #student = relationship("Students", backref=backref("grade", uselist=False))

    #assign_id = db.Column(db.Integer, db.ForeignKey("assignment.assign_id"))
    #assignment = relationship("Assignent", backref=backref("grade", uselist=False))"""

#from GradeBookProject import app

#Route for homePage
@app.route('/')
@app.route('/home', methods=["GET", "POST"])
def home():
    """Renders the home page."""
    session["user_id"] = None
    if request.method == "GET":
         return render_template(
        'index.html',
        title='Home Page',
        error=False
     )

    user = load_user(request.form["username"])
    if user is None:
        return render_template("index.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("index.html", error=True)

    login_user(user)
    session["user_id"] = user.user_id
    if user.username == 'testUser':
        return redirect(url_for('Admin'))
    elif user.username == 'professor':
        return redirect(url_for('faculty'))
    else:
        return redirect(url_for('student'))



#route for student
@app.route('/student/', methods=["GET"])
def student():
    #Renders the student page.
    #students = Student.query.all()

    current_user_id = session["user_id"]
    if not current_user_id:
        abort(401)
    print(current_user_id)
    current_user = User.query.filter_by(user_id=current_user_id).one()
    student = current_user.student
    return render_template(
        'student.html',
        title='Student',
        student=student,
        Assignment = Assignment.query.all(),
        Student = Student.query.all()
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About'
    )


@app.route('/faculty', methods=["GET","POST"])
def faculty():
    """Renders the faculty page."""
    if request.method == 'POST':
      if not request.form['txtAssignment'] or not request.form['txtGrade']:
         flash('Please enter all the fields', 'error')
      else:
         assignment = Assignment(assgn_title=request.form['txtAssignment'], grade=request.form['txtGrade'])

         db.session.add(assignment)
         db.session.commit()
         flash('Record was successfully added')

    current_user_id = session["user_id"]
    if not current_user_id:
        abort(403)
    current_user = User.query.filter_by(user_id=current_user_id).one()
    faculty = current_user.faculty

    return render_template(
        'faculty.html',
        title='Faculty',
        faculty=faculty,
        #Assignment = Assignment.query.all()
        Student = Student.query.all(),
        Assignment = Assignment.query.all()

    )

@app.route('/faculty/deletea/<int:assgn_id>', methods=['DELETE'])
def deletea(assgn_id):
    assignment = Assignment.query.get(assgn_id)
    db.session.delete(assignment)
    db.session.commit()
    return jsonify(success=True)


@app.route('/Admin', methods=["GET","POST"])
def Admin():
    """Renders the Admin page."""

    if request.method == 'POST':
      if not request.form['first_name'] or not request.form['last_name'] or not request.form['student_id'] or not request.form['email'] or not request.form['major'] or not request.form['course']:
         flash('Please enter all the fields', 'error')
      else:
         student = Student(first_name=request.form['first_name'], last_name=request.form['last_name'],student_id=request.form['student_id'], email=request.form['email'], major = request.form['major'], course = request.form['course'])

         db.session.add(student)
         db.session.commit()
         flash('Record was successfully added')
    return render_template(
        'Admin.html',
        title='Administration',
        Student = Student.query.all()
    )


@app.route('/Admin/delete/<int:student_id>', methods=['DELETE'])
def delete(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify(success=True)



