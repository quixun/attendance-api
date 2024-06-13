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
from dto.index import LoginDto, MarkAttendanceDto, RegisterStudentDto
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.schema import StudentSchema, SubjectSchema
from pydantic import BaseModel
from services.attendance import get_attended_students_by_subject_id
from services.attendance import mark_attendance as mark_attendance_service
from services.model import predict, train_model
from services.subject import (get_subject_by_id, get_subjects_service,
                              save_subject)
from services.users import get_students_service, login_service, save_user

router = APIRouter()
class ImageUploadRequest(BaseModel):
    photos: List[str]
    folder_name: str
class ImagePredictRequest(BaseModel):
    photo: str

@tag_router("collection-data")
def setup_router(router):
    @router.post("/register/")
    async def register(request: RegisterStudentDto, db: db_dependency):
        folder_name = f'{request.student_id}_{request.name}'
        f_list = []
        for data_image in request.photos:
            image_bytes = base64.b64decode(data_image)
            
            img_np = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(img, scaleFactor=1.5, minNeighbors=5)
            faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
            if (len(faces) <= 0):
                print("No faces detected!!!")
                raise HTTPException(status_code=400, detail="No faces detected")
            
            (x, y, w, h) = faces[0]
            
            folder_path = os.path.join("data", folder_name)
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face_roi = img[y:y+h, x:x+w]
            face_resized = cv2.resize(face_roi, (100, 100))
            _, img_encoded = cv2.imencode('.jpg', face_resized)
            img_base64 = img_encoded.tobytes()
            f_list.append(face_resized.reshape(-1))

            random_id = uuid.uuid4()
            filename = os.path.join(folder_path, f"{folder_name}_{random_id}.jpg")
            with open(filename, "wb") as file:
                file.write(img_base64)
                
        npwriter.write(folder_name, np.array(f_list))
        student = StudentSchema(student_id=request.student_id, name=request.name, email=request.email)
        
        await save_user(student, db)
        
        return JSONResponse(content={"success": True, "message": "Registered successfully!!"}, status_code=200)
    
    @router.post("/attendance")
    async def attendance(request: ImagePredictRequest):
        train_model()
        result = predict(request.photo)
        if result == False:
            return JSONResponse(content={"success": False, "message": "No faces detected"}, status_code=400)
        
        print(result)
                        
        return JSONResponse(content={"success": True, "message": "Predict successfully!!!", "name": result}, status_code=200)
    
    @router.post("/add-subject")
    async def add_subject(subject: SubjectSchema, db: db_dependency):
        await save_subject(subject, db)
        return JSONResponse(content={"success": True, "message": "Save subject into database successfully!!!"}, status_code=200)
    
    @router.get("/get-subjects")
    async def get_subjects(db: db_dependency):
        subjects = await get_subjects_service(db)
        return JSONResponse(content={"success": True, "message": "Save subject into database successfully!!!", "subjects": subjects}, status_code=200)
    
    @router.post("/mark-attendance")
    async def mark_attendace(mark_attendance: MarkAttendanceDto, db: db_dependency):
        await mark_attendance_service(mark_attendance, db)
        
        return JSONResponse(content={"success": True, "message": "Attendance successfully!!!"}, status_code=200)
    
    @router.post("/login")
    async def login(login_dto: LoginDto, db: db_dependency):
        result = await login_service(login_dto, db)
        
        return JSONResponse(content={"success": True, "message": "Login successfully!!!", "student": result}, status_code=200)
    
    @router.get("/subjects/{subject_id}")
    async def get_subject(subject_id: str, db: db_dependency):
        return await get_subject_by_id(subject_id, db)
    
    @router.get("/attendances/students/{subject_id}")
    async def get_attended_students(subject_id: str, db: db_dependency):
        return get_attended_students_by_subject_id(subject_id, db)
    
    @router.get("/students")
    async def get_students(db: db_dependency):
        return get_students_service(db)
    
    return router

router = setup_router(router)
