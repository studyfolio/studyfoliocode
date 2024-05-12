from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
import io
import json
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
current_directory = os.path.dirname(os.path.abspath(__file__))
service_account_path = os.path.join(current_directory, 'service_account.json')
SERVICE_ACCOUNT_FILE = service_account_path



def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def get_mimetype(file_extension):
    mime_types = {
        '.pdf': 'application/pdf',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.rar': 'application/zip',
        '.zip': 'application/zip',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
        '.html': 'text/html',
        '.htm': 'text/html',
        '.json': 'application/json',
        '.gz': 'application/gzip',
        '.tar': 'application/x-tar',
        '.xml': 'application/xml',
        '.7z': 'application/x-7z-compressed'
    }
    return mime_types.get(file_extension.lower(), None)


def upload_file(file, name: str, folder: str):
    creds = authenticate()  
    service = build('drive', 'v3', credentials=creds)
    file_extension = os.path.splitext(file.filename)[1]
    mimetype = get_mimetype(file_extension)
    if mimetype is None:
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


