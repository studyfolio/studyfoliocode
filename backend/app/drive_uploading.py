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

def upload_file(file, name: str, folder):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': name,
        'parents': [folder]
    }
    media_body = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype='application/pdf', resumable=True)
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media_body,
        fields='webViewLink, id'
    ).execute()

    file_id = uploaded_file.get('id')
    webViewLink = uploaded_file.get('webViewLink')
    
    return webViewLink


def upload_image(file, name : str):
    return upload_file(file, name, "1_I9uUqXfsUz4d1G5gUBLpXcTIB4UX5p8")

def upload_ressource(file, name : str):
    return upload_file(file, name, "1YbY2WkCgfvOltgIdmwiRwN_v-oGBfagP")


