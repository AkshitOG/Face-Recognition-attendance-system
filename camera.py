import os
import cv2
from deepface import DeepFace
import time
import warnings
warnings.filterwarnings("ignore")
from db_config import mark_attendance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

#https://github.com/opencv/opencv/tree/4.x/data/haarcascades
cascade_path = os.path.join(
    BASE_DIR,
    'static',
    'cascades',
    'haarcascade_frontalface_default.xml'
)
face_cascade = cv2.CascadeClassifier(cascade_path)

last_marked_present = {}
last_known_name: str = ""
def camera_on(flaskapp):
    global last_known_name
    if not camera.isOpened():
        raise RuntimeError("Camera not Accessible.")
    
    frame_count: int = 0
    try:
        while True:
            success, frame = camera.read()
            if not success:
                continue
            
            frame = cv2.flip(frame, 1)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            frame_count += 1
            
            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255,221,102), 2)
                
                face_img = frame[y:y+h, x:x+w]
                if frame_count%30 == 0 and w > 80 and h > 80:
                    try:
                        result= DeepFace.find(
                            img_path=face_img,
                            db_path=os.path.join(BASE_DIR, "ImgDatabase"),
                            enforce_detection=False
                            )
                        if len(result[0]) > 0 and face_img.shape[1]>0:
                            last_known_name = os.path.basename(result[0].iloc[0]['identity']).split('.')[0]
                            #kept 60 for 1 minute, just for testing later it will be changed.
                            if last_known_name not in last_marked_present or time.time()-last_marked_present[last_known_name] > 60:
                                mark_attendance(last_known_name, app=flaskapp)
                                last_marked_present[last_known_name] = time.time()
                        else:
                            last_known_name = "unknown"
                            
                    except Exception as e:
                        print(f"Error: {e}")
                    
                cv2.putText(frame, last_known_name, (x,y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,221,102),2)
            

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()            

            yield ((b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'))
            time.sleep(0.03)
    finally:
        camera.release()