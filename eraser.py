import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests
import sys

# Initialize Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_DIR = 'keys'
SERVICE_ACCOUNT_FILES = [f'{i}.json' for i in range(1, 3)]
SERVICE_ACCOUNT_INDEX = 0
USED_SERVICE_ACCOUNTS = set()

def get_next_service_account_credentials():
    global SERVICE_ACCOUNT_INDEX
    service_account_file = os.path.join(SERVICE_ACCOUNT_DIR, SERVICE_ACCOUNT_FILES[SERVICE_ACCOUNT_INDEX])
    USED_SERVICE_ACCOUNTS.add(service_account_file)
    SERVICE_ACCOUNT_INDEX = (SERVICE_ACCOUNT_INDEX + 1) % len(SERVICE_ACCOUNT_FILES)
    return Credentials.from_service_account_file(service_account_file, scopes=SCOPES)

def get_drive_service():
    credentials = get_next_service_account_credentials()
    return build('drive', 'v3', credentials=credentials)

def list_files(drive_service):
    files = []
    page_token = None
    while True:
        response = drive_service.files().list(q="trashed=false", spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files

def delete_file(drive_service, file_id):
    drive_service.files().delete(fileId=file_id).execute()
    print(f"File with ID {file_id} deleted successfully.")

def delete_all_data():
    while True:
        if len(USED_SERVICE_ACCOUNTS) >= len(SERVICE_ACCOUNT_FILES):
            print("All service accounts have been used. Terminating.")
            break

        drive_service = get_drive_service()
        
        # Check storage quota
        about = drive_service.about().get(fields="storageQuota").execute()
        quota_usage = int(about['storageQuota']['usage'])
        quota_limit = int(about['storageQuota']['limit'])
        quota_percentage = (quota_usage / quota_limit) * 100
        print(f"Storage quota percentage: {quota_percentage}%")
        
        if quota_percentage < 0.2:
            print("Storage quota is less than 0.2%. Switching to the next service account.")
            continue  # Skip the current service account and switch to the next one
            
        files = list_files(drive_service)
        if files:  # Check if there are any files to delete
            for file in files:
                delete_file(drive_service, file['id'])
        else:
            print("All files deleted from this service account.")



def send_message(user, password, sender, phone, text, priority, params):
    api_url = "https://bhashsms.com/api/sendmsg.php"
    payload = {
        'user': user,
        'pass': password,
        'sender': sender,
        'phone': phone,
        'text': text,
        'priority': priority,
        'stype': 'normal',
        'Params': params
    }
    response = requests.get(api_url, params=payload)
    return response.text

def main():
    # Placeholder values for message parameters
    user = "PastelFrames"
    password = "123456"
    sender = "BUZWAP"
    phone_number = "7708196973"  # Replace with the actual phone number
    text = "cloud_deletion"
    priority = "wa"
    dynamic_params = "PastelFrames Ai."  # Replace with actual dynamic parameters

    # Sending message
    response = send_message(user, password, sender, phone_number, text, priority, dynamic_params)
    print(f"Message sent to {phone_number} with response: {response}")

if __name__ == '__main__':
    delete_all_data()
    main()
