from src.models.models import Student, Subject, Attendance 
from src.configs.database import SessionLocal, engine
from src.configs.variables import APP_NAME, VERSION
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import collection
from src.services.cloudinary import createTransformation, getAssetInfo, uploadImage
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

# This will create the tables in the database
Student.metadata.create_all(bind=engine)
Subject.metadata.create_all(bind=engine)
Attendance.metadata.create_all(bind=engine)

# FastAPI app setup
app = FastAPI(title=APP_NAME, version=VERSION)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Include routes
app.include_router(collection.router)


@app.get("/")
def main_function():
    return RedirectResponse(url="/docs/")
