from flask import Flask, request, render_template, Response
# from flask import SQLAlchemy
import os
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)

#https://github.com/opencv/opencv/tree/4.x/data/haarcascades
cascade_path = os.path.join(
    app.root_path,
    'static',
    'cascades',
    'haarcascade_frontalface_default.xml'
)
face_cascade = cv2.CascadeClassifier(cascade_path)

def camera_on():
    if not camera.isOpened():
        raise RuntimeError("Camera not Accessible.")
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        

        ret, buffer = cv2.imencode('.jpg', frame)
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
