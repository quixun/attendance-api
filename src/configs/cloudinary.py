from dotenv import load_dotenv

load_dotenv()

import cloudinary
import cloudinary.api
import cloudinary.uploader
from cloudinary import CloudinaryImage

config = cloudinary.config(secure=True)
