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
    @router.get("/upload/")
    async def upload_image_on_cloud():
        # image: UploadFile = File(...), cloudinary_folder: Optional[str] = Form(None)
        print("image:::")
        print("cloudinary_folder:::")
        # image_bytes = await image.read()
        
        # img_np = np.frombuffer(image_bytes, np.uint8)
        # img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        
        # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # for (x, y, w, h) in faces:
        #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        #     face_roi = img[y:y+h, x:x+w]
        #     face_resized = cv2.resize(face_roi, (160, 160))
        #     _, img_encoded = cv2.imencode('.jpg', face_resized)
        #     img_base64 = img_encoded.tobytes()
        #     cloudinary_url = await uploadImage(img_base64, cloudinary_folder)

        # return JSONResponse(content={"success": True, "message": "Image uploaded successfully", "cloudinary_url": cloudinary_url}, status_code=200)
    
    return router

router = setup_router(router)
