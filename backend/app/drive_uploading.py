from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
import io
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'app/service_account.json'



def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_file(file, name : str, Folder : str):
    
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': name,
        'parents': [Folder]
    }
    media_body = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype='application/pdf', resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media_body
    ).execute()

def upload_image(file, name : str):
    upload_file(file, name, "1_I9uUqXfsUz4d1G5gUBLpXcTIB4UX5p8")

def upload_ressource(file, name : str):
    upload_file(file, name, "1YbY2WkCgfvOltgIdmwiRwN_v-oGBfagP")

