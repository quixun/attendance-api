import base64

import cv2
import numpy as np
import pandas as pd
from src.npwriter import f_name
from pydantic import BaseModel
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors = 5)

class ImagePredictRequest(BaseModel):
    photo: str
    
def train_model():
    data = pd.read_csv(f_name).values

    X, Y = data[:, 1:-1], data[:, -1]
    
    model.fit(X, Y)
    
def predict(photo: str):
    image_bytes = base64.b64decode(photo)
    X_test = []
    img_np = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.5, minNeighbors=5)
    for face in faces: 
        x, y, w, h = face 
        im_face = img[y:y + h, x:x + w] 
        im_face = cv2.resize(im_face, (100, 100)) 
        X_test.append(im_face.reshape(-1)) 

    if len(faces)>0: 
        response = model.predict(np.array(X_test)) 
    else:
        return False
    

    response = model.predict(np.array(X_test))
    
    return response[0]

