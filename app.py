from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with a fixed key in production

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define models
class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    program = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marks = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('marks', lazy=True))

@app.route('/')
def index():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # Example check
            flash('Login successful!', 'success')
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
            return redirect(url_for('admin_login_page'))
    return render_template('login.html')

@app.route('/login')
def admin_login_page():
    return render_template('login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin' in session:
        return render_template('admin_dashboard.html')
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login_page'))

@app.route('/edit-questions', methods=['GET', 'POST'])
def edit_questions():
    if 'admin' in session:
        if request.method == 'POST':
            question_text = request.form['question']
            new_question = Question(question=question_text)
            db.session.add(new_question)
            db.session.commit()
            flash('Question added successfully!', 'success')
            return redirect(url_for('edit_questions'))
        questions = Question.query.all()
        return render_template('edit_questions.html', questions=questions)
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login_page'))

@app.route('/delete-question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    if 'admin' in session:
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        flash('Question deleted successfully!', 'success')
        return redirect(url_for('edit_questions'))
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login_page'))

@app.route('/update-question', methods=['POST'])
def update_question():
    if 'admin' in session:
        question_id = request.form['question_id']
        question_text = request.form['question']
        question = Question.query.get_or_404(question_id)
        question.question = question_text
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('edit_questions'))
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login_page'))

@app.route('/evaluate-students', methods=['GET', 'POST'])
def evaluate_students():
    if 'admin' in session:
        if request.method == 'POST':
            student_id = request.form['student_id']
            marks = request.form['marks']
            new_mark = Mark(student_id=student_id, marks=marks)
            db.session.add(new_mark)
            db.session.commit()
            flash('Marks added successfully!', 'success')
            return redirect(url_for('evaluate_students'))
        students = Student.query.all()
        return render_template('evaluate_students.html', students=students)
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login_page'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
