from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
import io
import json
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "app\\service_account.json"



def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_file(file, name: str, folder: str):
    creds = authenticate()  
    service = build('drive', 'v3', credentials=creds)

    if file.filename.endswith('.pdf'):
        mimetype = 'application/pdf'
    elif file.filename.lower().endswith(('.jpg', '.jpeg')):
        mimetype = 'image/jpeg'
    elif file.filename.lower().endswith('.png'):
        mimetype = 'image/png'
    elif file.filename.lower().endswith('.gif'):
        mimetype = 'image/gif'
    else:
        raise ValueError("Unsupported file format")

    file_metadata = {
        'name': name,
        'parents': [folder]
    }
    media_body = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=mimetype, resumable=True)
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media_body,
        fields='webViewLink, id'
    ).execute()

    file_id = uploaded_file.get('id')
    webViewLink = uploaded_file.get('webViewLink')
    service.permissions().create(
        fileId=file_id,
        body={'role': 'reader', 'type': 'anyone'},
        fields='id'
    ).execute()

    return webViewLink

def upload_image(file, name : str):
    return upload_file(file, name, "1_I9uUqXfsUz4d1G5gUBLpXcTIB4UX5p8")

def upload_ressource(file, name : str):
    return upload_file(file, name, "1YbY2WkCgfvOltgIdmwiRwN_v-oGBfagP")

def upload_json(json_data, name: str):
    creds = authenticate()  
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {
        'name': name,
        'parents': ["1Es2NprUtHTzYIwnmbCkBYGEgxxqiKRMi"]
    }
    
    json_bytes = json.dumps(json_data).encode('utf-8')
    
    media_body = MediaIoBaseUpload(io.BytesIO(json_bytes), 'application/json', resumable=True)
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media_body,
        fields='webViewLink, id'
    ).execute()

    file_id = uploaded_file.get('id')
    webViewLink = uploaded_file.get('webViewLink')
    service.permissions().create(
        fileId=file_id,
        body={'role': 'reader', 'type': 'anyone'},
        fields='id'
    ).execute()
    

    return webViewLink



def download_json(file_link):
    creds = authenticate()  
    service = build('drive', 'v3', credentials=creds)

    file_id = file_link.split('/')[-2]

    request = service.files().get_media(fileId=file_id)
    downloaded_file = io.BytesIO()
    downloader = MediaIoBaseDownload(downloaded_file, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()

    downloaded_file.seek(0)

    json_data = json.loads(downloaded_file.read().decode('utf-8'))

    return json_data


