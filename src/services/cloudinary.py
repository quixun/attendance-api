import json

from src.configs.cloudinary import CloudinaryImage, cloudinary


async def uploadImage(image, folder):
    try:
        response = cloudinary.uploader.upload(
            image,
            folder="Attendance",
            upload_preset="dnsmcvztb",
            unique_filename=False,
            overwrite=True,
        )
        srcURL = CloudinaryImage(response["public_id"]).build_url()
        return srcURL
    except Exception as e:
        print(f"Error uploading image: {str(e)}")
        return None


def getAssetInfo():
    try:
        image_info = cloudinary.api.resource("quickstart_butterfly")
        print(f"Image Info: {image_info}")  # Log the response for debugging

        if image_info.get("width", 0) > 900:
            update_resp = cloudinary.api.update("quickstart_butterfly", tags="large")
        elif image_info.get("width", 0) > 500:
            update_resp = cloudinary.api.update("quickstart_butterfly", tags="medium")
        else:
            update_resp = cloudinary.api.update("quickstart_butterfly", tags="small")

        print(f"Update Response: {update_resp}")  # Log the response for debugging
        return update_resp
    except Exception as e:
        print(f"Error retrieving asset info: {str(e)}")
        return None


def createTransformation():
    try:
        transformedURL = CloudinaryImage("quickstart_butterfly").build_url(
            width=100, height=150, crop="fill"
        )
        return transformedURL
    except Exception as e:
        print(f"Error creating transformation: {str(e)}")
        return None
