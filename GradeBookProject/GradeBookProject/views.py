"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, url_for, request 
from GradeBookProject import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('index.html', error=error)

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
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/student')
def student():
    """Renders the student page."""
    return render_template(
        'student.html',
        title='Student',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/faculty')
def faculty():
    """Renders the faculty page."""
    return render_template(
        'faculty.html',
        title='Faculty',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/Admin')
def Admin():
    """Renders the Admin page."""
    return render_template(
        'Admin.html',
        title='Administration',
        year=datetime.now().year,
        message='Your application description page.'
    )
