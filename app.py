from flask import Flask, request, render_template, Response
# from flask import SQLAlchemy
# import os
import cv2


app = Flask(__name__)

def camera_on():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            ret, buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
            
            yield ((b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'))

@app.route('/video')
def video():
    return Response(camera_on(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/")
def Homepage():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=6969, debug=True)
