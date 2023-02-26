from constant import CLOUDINARY_NAME,CLOUDINARY_API_KEY,CLOUDINARY_API_SECRET
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="CLOUDINARY CLOUD NAME",
    api_key="CLOUDINARY API KEY",
    api_secret="CLOUDINARY API SECRET"
)