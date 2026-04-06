from flask import Flask, request, render_template, Response
# from flask import SQLAlchemy
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import cv2
from deepface import DeepFace

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

#https://github.com/opencv/opencv/tree/4.x/data/haarcascades
cascade_path = os.path.join(
    app.root_path,
    'static',
    'cascades',
    'haarcascade_frontalface_default.xml'
)
face_cascade = cv2.CascadeClassifier(cascade_path)

last_known_name: str = ""
def camera_on():
    global last_known_name
    if not camera.isOpened():
        raise RuntimeError("Camera not Accessible.")
    
    frame_count = 0
    while True:
        success, frame = camera.read()
        if not success:
            continue
        
        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        frame_count += 1
        
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            
            face_img = frame[y:y+h, x:x+w]
            if frame_count%10 == 0 and w > 80 and h > 80:
                try:
                    result= DeepFace.find(
                        img_path=face_img,
                        db_path="ImgDatabase",
                        enforce_detection=False
                        )
                    if len(result[0]) > 0 and face_img.shape[1]>0:
                        last_known_name = os.path.basename(result[0].iloc[0]['identity']).split('.')[0]
                        
                except:
                    pass
                
            cv2.putText(frame, last_known_name, (x,y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,2),2)
        

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()            

        yield ((b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'))
        time.sleep(0.03)

@app.route('/video')
def video():
    return Response(camera_on(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/")
def Homepage():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=6969, debug=False)
