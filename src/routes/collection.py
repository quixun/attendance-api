import base64
import os
import uuid
from typing import List

import cv2
import models.models as _models
import npwriter
import numpy as np
from configs.database import db_dependency
from decorators.tag_router import tag_router
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.schema import StudentSchema
from pydantic import BaseModel
from services.model import model, train_model

router = APIRouter()
class ImageUploadRequest(BaseModel):
    photos: List[str]
    folder_name: str
class ImagePredictRequest(BaseModel):
    photo: str

@tag_router("collection-data")
def setup_router(router):
    @router.post("/upload/")
    async def upload_image_on_cloud(request: ImageUploadRequest):
        f_list = []
        for data_image in request.photos:
            image_bytes = base64.b64decode(data_image)
            
            img_np = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(img, scaleFactor=1.5, minNeighbors=5)
            faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
            if len(faces) == 0:
                print("No faces detected")
        
            (x, y, w, h) = faces[0]
            
            folder_path = os.path.join("data", request.folder_name)
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face_roi = img[y:y+h, x:x+w]
            face_resized = cv2.resize(face_roi, (100, 100))
            _, img_encoded = cv2.imencode('.jpg', face_resized)
            img_base64 = img_encoded.tobytes()
            f_list.append(face_resized.reshape(-1))

            random_id = uuid.uuid4()
            filename = os.path.join(folder_path, f"{request.folder_name}_{random_id}.jpg")
            with open(filename, "wb") as file:
                file.write(img_base64)
                
        npwriter.write(request.folder_name, np.array(f_list))
        
        return JSONResponse(content={"success": True, "message": "Image processed successfully", "folder": request.folder_name}, status_code=200)
    
    @router.post("/attendance")
    async def attendance(request: ImagePredictRequest):
        train_model()

        image_bytes = base64.b64decode(request.photo)
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
            return JSONResponse(content={"success": False, "message": "No faces detected"}, status_code=400)
        

        response = model.predict(np.array(X_test))

        return JSONResponse(content={"success": True, "message": "Predict successfully!!!", "name": response[0]}, status_code=200)
    
    @router.post("/test-db", response_model=StudentSchema)
    async def test(student: StudentSchema, db: db_dependency):
        db_student = _models.Student(id=student.id, email=student.email, name=student.name)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        print(db_student)
        return JSONResponse(content={"success": True, "message": "Save into database successfully!!!"}, status_code=200)
    return router

router = setup_router(router)
