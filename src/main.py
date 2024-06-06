from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from configs.variables import APP_NAME, VERSION
from routes import collection
from services.cloudinary import createTransformation, getAssetInfo, uploadImage

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

# Redirect / -> Swagger-UI documentation
@app.get("/")
def main_function():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    uploadImage()
    getAssetInfo()
    createTransformation()
    return RedirectResponse(url="/docs/")