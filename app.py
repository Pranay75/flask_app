from flask import Flask, render_template, request, redirect, url_for, flash, session , jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime, timezone , timedelta
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "safeisnotsafe")
app.config.update(
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # Set to True if using HTTPS
    SESSION_COOKIE_SAMESITE='Lax'
)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define models
class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Student(db.Model):
    student_id = db.Column(db.String(20), primary_key=True)  
    name = db.Column(db.String(100), nullable=False)
    program = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marks = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False, default=datetime.now(timezone.utc).year)
    student_id = db.Column(db.String(20), db.ForeignKey('student.student_id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('marks', lazy=True))

class Solved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.String(500), nullable=True)
    marks = db.Column(db.Integer, nullable=False)
    link1 = db.Column(db.String(200), nullable=True)
    link2 = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    questions = Question.query.filter_by(is_active=True).order_by(Question.question_id.desc()).all()
    return render_template('index.html', questions=questions)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == os.getenv("ADMIN_USERNAME", "admin") and password == os.getenv("ADMIN_PASSWORD","password"):  #password can be changed
            flash('Login successful!', 'success')
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
            return redirect(url_for('admin_login_page'))
    return render_template('login.html')

@app.route('/login')
def admin_login_page():
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin' in session:
        return render_template('admin_dashboard.html')
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login_page'))

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/edit-questions', methods=['GET', 'POST'])
def edit_questions():
    if 'admin' in session:
        if request.method == 'POST':
            question_text = request.form['question']
            new_question = Question(question=question_text, is_active=True)
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
    
@app.route('/deactivate_question/<int:question_id>', methods=['POST'])
def deactivate_question(question_id):
    if 'admin' in session:
        question = Question.query.get_or_404(question_id)
        question.is_active = not (question.is_active)
        db.session.commit()
        return redirect(url_for('edit_questions'))
    flash('Please log in first.', 'danger')
    return render_template('login.html')
    

@app.route('/evaluate_students', methods=['GET', 'POST'])
def evaluate_students():
    if 'admin' in session:
        if request.method == 'POST':
            student_id = request.form['student_id']
            name = request.form['name']
            program = request.form['program']
            branch = request.form['branch']
            marks = int(request.form['marks'])
            question = request.form['question']
            remarks = request.form['remarks']
            date = request.form['date']
            link1 = request.form['link1']
            link2 = request.form['link2']
            
            date = datetime.strptime(date, '%Y-%m-%d')
            year = date.year  # Set the year from the date
            
            student = Student.query.filter_by(student_id=student_id).first()
            if student:
                mark = Mark.query.filter_by(student_id=student_id, year=year).first()
                if mark:
                    mark.marks += marks
                else:
                    new_mark = Mark(student_id=student_id, marks=marks, year=year)
                    db.session.add(new_mark)
                
                solved = Solved(
                    student_id=student_id, 
                    student_name=name, 
                    question=question,
                    remarks=remarks,
                    marks=marks,
                    link1=link1,
                    link2=link2,
                    date=date
                )
                db.session.add(solved)
            else:
                new_student = Student(student_id=student_id, name=name, program=program, branch=branch)
                db.session.add(new_student)
                
                new_mark = Mark(student_id=student_id, marks=marks, year=year)
                db.session.add(new_mark)
                
                solved = Solved(
                    student_id=student_id, 
                    student_name=name, 
                    question=question,
                    remarks=remarks,
                    marks=marks,
                    link1=link1,
                    link2=link2,
                    date=date
                )
                db.session.add(solved)
            
            db.session.commit()
            flash('Evaluation recorded successfully!', 'success')
            return redirect(url_for('evaluate_students'))

        questions = Question.query.filter_by(is_active=True).all()
        return render_template('evaluate_students.html', questions=questions)
    flash('Please log in first.', 'danger')
    return render_template('login.html')

@app.route('/view_solved', methods=['GET'])
def view_solved():
    if 'admin' in session:
        solved_questions = Solved.query.all()
        return render_template('view_solved.html', solved_questions=solved_questions)
    flash('Please log in first.', 'danger')
    return render_template('login.html')

@app.route('/view_all_questions')
def view_all_questions():
    if 'admin' in session:
        questions = Question.query.all()
        return render_template('view_all_questions.html', questions=questions)
    flash('Please log in first.', 'danger')
    return render_template('login.html')

@app.route('/honor-board', defaults={'year': None})
@app.route('/honor-board/<int:year>')
def honor_board(year):
    if year is None:
        year = datetime.now(timezone.utc).year

    query = db.session.query(
        Student.student_id, Student.name, Student.program, Student.branch, db.func.sum(Mark.marks).label('total_marks')
    ).join(Mark).filter(Mark.year == year).group_by(Student.student_id).order_by(db.func.sum(Mark.marks).desc())

    students = query.all()

    ranked_students = []
    for index, student in enumerate(students):
        student_dict = {
            'student_id': student.student_id,
            'name': student.name,
            'program': student.program,
            'branch': student.branch,
            'total_marks': student.total_marks,
            'rank': index + 1
        }
        ranked_students.append(student_dict)

    # Get available years for the honor board
    available_years = db.session.query(Mark.year).distinct().order_by(Mark.year.desc()).all()
    available_years = [year[0] for year in available_years]

    return render_template('honor_board.html', students=ranked_students, year=year, available_years=available_years)

@app.route('/get_student_details', methods=['GET'])
def get_student_details():
    if 'admin' in session:
        student_id = request.args.get('student_id')
        student = Student.query.filter_by(student_id=student_id).first()
        if student:
            student_data = {
                'name': student.name,
                'program': student.program,
                'branch': student.branch,
            }
            return jsonify(student_data)
        else:
            return jsonify({})
    flash('Please log in first.', 'danger')
    return render_template('login.html')
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
