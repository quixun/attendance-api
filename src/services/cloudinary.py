import json

from configs.cloudinary import CloudinaryImage, cloudinary


async def uploadImage(image, folder):
    response = cloudinary.uploader.upload(
        image,
        folder=folder,
        upload_preset="snvlqaav",
        unique_filename=False,
        overwrite=True
    )
    srcURL = CloudinaryImage(response['public_id']).build_url()
    return srcURL
  
def getAssetInfo():
  image_info=cloudinary.api.resource("quickstart_butterfly")

  if image_info["width"]>900:
    update_resp=cloudinary.api.update("quickstart_butterfly", tags = "large")
  elif image_info["width"]>500:
    update_resp=cloudinary.api.update("quickstart_butterfly", tags = "medium")
  else:
    update_resp=cloudinary.api.update("quickstart_butterfly", tags = "small")

  
def createTransformation():
  transformedURL = CloudinaryImage("quickstart_butterfly").build_url(width = 100, height = 150, crop = "fill")
