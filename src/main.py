import models.models as _models
from configs.database import SessionLocal, engine
from configs.variables import APP_NAME, VERSION
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import collection
from services.cloudinary import createTransformation, getAssetInfo, uploadImage
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(collection.router)

@app.get("/")
def main_function():
    return RedirectResponse(url="/docs/")