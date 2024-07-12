from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with a fixed key in production

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add your authentication logic here
        if username == 'admin' and password == 'password':  # Example check
            flash('Login successful!', 'success')
            session['admin'] = True  # Set admin session
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

@app.route('/edit-questions')
def edit_questions():
    if 'admin' in session:
        return render_template('edit_questions.html')
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login_page'))

@app.route('/evaluate-students')
def evaluate_students():
    if 'admin' in session:
        return render_template('evaluate_students.html')
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login_page'))

if __name__ == '__main__':
    app.run(debug=True)
