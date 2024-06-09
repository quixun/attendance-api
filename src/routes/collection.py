import base64
import csv
import os
import uuid
import zipfile
from io import BytesIO
from typing import Optional

import cv2
import numpy as np
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

from decorators.tag_router import tag_router
from services.cloudinary import uploadImage

router = APIRouter()

@tag_router("collection-data")
def setup_router(router):
    @router.post("/upload/")
    async def upload_image_on_cloud(data_image: Optional[str] = Form(None), folder_name: Optional[str] = Form(None)):     
        image_bytes = base64.b64decode(data_image)
        
        img_np = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        # Tạo thư mục nếu chưa tồn tại
        
        if len(faces) == 0:
            return JSONResponse(content={"success": False, "message": "No faces detected"}, status_code=400)
    
        (x, y, w, h) = faces[0]
        
        folder_path = os.path.join("data", folder_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face_roi = img[y:y+h, x:x+w]
        face_resized = cv2.resize(face_roi, (160, 160))
        _, img_encoded = cv2.imencode('.jpg', face_resized)
        img_base64 = img_encoded.tobytes()
        
        # Lưu ảnh vào folder
        random_id = uuid.uuid4()
        filename = os.path.join(folder_path, f"{folder_name}_{random_id}.jpg")
        with open(filename, "wb") as file:
            file.write(img_base64)
            
          # Kiểm tra và tạo file dataset.csv nếu nó chưa tồn tại
        if not os.path.exists('dataset.csv'):
            with open('dataset.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["IMAGE_ID", "LABEL"])
        
        # Ghi dữ liệu vào file dataset.csv
        with open('dataset.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([f"{folder_name}_{random_id}.jpg", folder_name])
            
        return JSONResponse(content={"success": True, "message": "Image processed successfully", "folder": folder_name}, status_code=200)
    
    return router

router = setup_router(router)
