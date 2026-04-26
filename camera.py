import os
import cv2
from deepface import DeepFace
import time
import warnings
warnings.filterwarnings("ignore")
from db_config import mark_attendance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

    print("Starting Camera")
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print("Camera ON")
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if not camera.isOpened():
        raise RuntimeError("Camera not Accessible.")
    
    frame_count: int = 0
    try:
        while True:
            try:
                success, frame = camera.read()
                if not success:
                    time.sleep(0.2)
                    continue
                
                frame = cv2.flip(frame, 1)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                frame_count += 1
                
                if len(faces)>0:
                    (x,y,w,h) = max(faces, key = lambda f: f[2]*f[3])
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (255,221,102), 2)
                    
                    face_img = frame[y:y+h, x:x+w]
                    if face_img.size == 0:
                        continue
                    if frame_count % 60 == 0 and w > 80 and h > 80:
                        try:
                            print("Finding Face")
                            result= DeepFace.find(
                                img_path=face_img,
                                db_path=os.path.join(BASE_DIR, "ImgDatabase"),
                                enforce_detection=False
                                )
                            print("Search finish")
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
                if not ret:
                    continue
                frame = buffer.tobytes()            

                yield ((b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'))
                time.sleep(0.03)
            except GeneratorExit:
                print("Disconnect")
                return
    finally:
        print("Releasing camera")
        camera.release()
        cv2.destroyAllWindows()
