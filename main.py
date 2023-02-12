import os

import openpyxl

from google.oauth2 import service_account
from googleapiclient.discovery import build

from get_xlsx_file import list_files_in_drive, download_file, get_file_from_local
from service_one_sheet import service_sheet

script_directory = os.path.dirname(os.path.abspath(__file__))
credentials = os.path.join(script_directory, "credentials.json")
print(credentials)

creds = service_account.Credentials.from_service_account_file(credentials,
                                                              scopes=['https://www.googleapis.com/auth/drive'])

service = build('drive', 'v3', credentials=creds)

# ID of the file to be downloaded
file_id = '1U6GT1M01m1MvTvR7pQCIdm-z-rF0nESB'

list_files_in_drive(service)

wb = openpyxl.load_workbook(download_file(service, file_id), read_only=True)
# wb = openpyxl.load_workbook(get_file_from_local("ExampleXLSX.xlsx"), read_only=True)

print(wb.sheetnames)
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    service_sheet(ws)
    # TODO: remove in production
    break
