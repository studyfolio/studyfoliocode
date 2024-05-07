import cloudinary
from cloudinary.uploader import upload


cloudinary.config(
    cloud_name = "dikcbn5dw",
    api_key = "541363273917361",
    api_secret = "3FZY1W5NCCHIJy6oIgvWkTyo3kQ"
)

def upload_file(image):
    try:
        result = upload(image)["secure_url"]
        return result
    except Exception as e:
        return None
