import sys

import openpyxl

from google.oauth2 import service_account
from googleapiclient.discovery import build

from common import get_file_path_in_curr_working_dir
from configurtion import load_settings
from google_drive_library.discovery import list_files_shared_with_service_acc, filter_files_by_mimeType
from google_drive_library.get import download_file_with_service_acc
from service_one_sheet import process_sheet

# Get credentials & create service
creds = service_account.Credentials.from_service_account_file(
    get_file_path_in_curr_working_dir("credentials.json"),
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)
service = build('drive', 'v3', credentials=creds)

# List xlsx files that were shared with the service account
files = list_files_shared_with_service_acc(service)
xlsx_mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
xlsx_files = filter_files_by_mimeType(files, xlsx_mimeType)
print('Excel files shared with service account: ', xlsx_files)

# Read settings file
settings = load_settings(service, xlsx_files)
if settings is None:
    exit(1)

# Process files
for f in xlsx_files:

    # Download file
    file = download_file_with_service_acc(service, f['id'])
    print(f"Downloaded {f['name']}: {sys.getsizeof(file) / (1 << 10):,.0f} KB")

    # Go through file sheets and process them
    wb = openpyxl.load_workbook(file, read_only=True)
    for sheet_name in wb.sheetnames:
        print("Processing sheet: ", sheet_name)
        process_sheet(wb[sheet_name], settings)
