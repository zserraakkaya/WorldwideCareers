from flask import Flask, render_template, jsonify, redirect, request, url_for

from database import load_jobs_from_db, insert_job_to_db

app = Flask(__name__)

@app.route("/")
def hello_world():
    jobs = load_jobs_from_db()
    return render_template("home.html", jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)

@app.route('/post-job')
def post_job():
    return render_template('post-job.html')

@app.route('/go-to-post-job', methods=['POST'])
def go_to_post_job():
    return redirect(url_for('post_job'))

@app.route('/post-job-to-db', methods=['POST'])
def post_job_to_db_route():
    title = request.form.get('title')
    location = request.form.get('location')
    description = request.form.get('description')
    salary = request.form.get('salary')
    currency = request.form.get('currency')

    return insert_job_to_db(title, location, description, salary, currency)

if __name__ == "__main__":
    app.run(debug=True)