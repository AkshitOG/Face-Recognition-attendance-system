from flask import Flask, render_template, Response, request
from db_config import db, daily_total_count
from camera import camera_on
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route('/video')
def video():
    return Response(camera_on(app), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/history')
def historypage(): 
    return render_template('history.html')

@app.route('/test')
def test():
    from models import Person
    data = Person.query.all()
    return str(data)

@app.route("/total", methods=["GET"])
def day_total():
    return f"{daily_total_count()}"

@app.route("/")
def Homepage():
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
