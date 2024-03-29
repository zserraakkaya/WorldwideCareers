from flask import Flask, render_template, jsonify, redirect, request, url_for

from database import save_user_to_db, get_user_from_db, save_recruiter_to_db, get_recruiter_from_db, load_jobs_from_db, insert_job_to_db, load_job_from_db, insert_job_application_to_db

# to hash the passwords
from werkzeug.security import generate_password_hash, check_password_hash

# to mail cv
from flask_mail import Mail, Message

# to use env. var.s
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

@app.route("/")
def hello_world():
    jobs = load_jobs_from_db()
    return render_template("home.html", jobs=jobs)

#navbar links
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')

# go to recruiter sign in and sign up pages
@app.route('/recruitersignin')
def recruitersignin():
    return render_template('recruitersignin.html')
@app.route('/recruitersignup')
def recruitersignup():
    return render_template('recruitersignup.html')

# go to signin and signup pages
@app.route('/signin')
def signin():
    return render_template('signin.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')

# user sign up
@app.route('/db-signup', methods=['POST'])
def db_signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_again = request.form.get('password_again')

        if password != password_again:
            return render_template('signup.html', error='Passwords do not match')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        save_user_to_db(first_name, last_name, email, hashed_password)

        return redirect(url_for('signin'))

# user sign in
@app.route('/db-signin', methods=['GET', 'POST'])
def db_signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_from_db(email)

        if user and check_password_hash(user['password'], password):
            return redirect(url_for('home'))
        else:
            return render_template('signin.html', error='Invalid email or password')

    return render_template('signin.html')

# recruiter sign up
@app.route('/db-recruitersignup', methods=['POST'])
def db_recruitersignup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_again = request.form.get('password_again')

        if password != password_again:
            return render_template('recruitersignup.html', error='Passwords do not match')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        save_recruiter_to_db(name, email, hashed_password)

        return redirect(url_for('recruitersignin'))

# recruiter sign in
@app.route('/db-recruitersignin', methods=['GET', 'POST'])
def db_recruitersignin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_recruiter_from_db(email)

        if user and check_password_hash(user['password'], password):
            return redirect(url_for('home'))
        else:
            return render_template('recruitersignin.html', error='Invalid email or password')

    return render_template('recruitersignin.html')


# 
@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)

# to go to apply-job.html
@app.route('/apply-job')
def apply_job():
    return render_template('apply-job.html')
# to go to apply-job.html
@app.route('/go-to-apply-job', methods=['POST'])
def go_to_apply_job():
    return redirect(url_for('apply_job'))

# when "apply job" button clicked on apply-job.html:
@app.route('/post-job-application-to-db', methods=['POST'])
def post_job_application_to_db_route():
    first_name = request.form.get('fname')
    last_name = request.form.get('lname')
    date_of_birth = request.form.get('dob')
    email = request.form.get('email')

    cv_file = request.files['cv']

    if cv_file:
        msg = Message('New CV Submission', sender='zserraakkaya2@gmail.com', recipients=['zserraakkaya2@gmail.com'])
        msg.body = 'A new CV has been submitted.'
        msg.attach(cv_file.filename, 'application/pdf', cv_file.read())
        mail.send(msg)

    return insert_job_application_to_db(first_name, last_name, date_of_birth, email)

# to go to post-job.html
@app.route('/post-job')
def post_job():
    return render_template('post-job.html')
# to go to post-job.html
@app.route('/go-to-post-job', methods=['POST'])
def go_to_post_job():
    return redirect(url_for('post_job'))

# when "post job" button clicked on post-job.html:
@app.route('/post-job-to-db', methods=['POST'])
def post_job_to_db_route():
    title = request.form.get('title')
    location = request.form.get('location')
    description = request.form.get('description')
    salary = request.form.get('salary')
    currency = request.form.get('currency')
    email = request.form.get('email')

    return insert_job_to_db(title, location, description, salary, currency, email)

# when "see job details" button clicked on home.html:
@app.route('/job-details/<int:id>')
def show_job_details(id):
    job = load_job_from_db(id)
    return render_template('job-details.html', job=job)

if __name__ == "__main__":
    app.run(debug=True)