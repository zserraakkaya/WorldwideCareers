from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
    {
        'id': 1,
        'title': 'Information Technology Support Technician',
        'location': 'Novara, Piedmont, Italy'
    },
    {
        'id': 2,
        'title': 'DevOps Engineer',
        'location': 'Vienna, Austria'
    }
]

@app.route("/")
def hello_world():
    return render_template("home.html", jobs=JOBS)

@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)

if __name__ == "__main__":
    app.run(debug=True)