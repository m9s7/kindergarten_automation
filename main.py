import logging
import openpyxl
import pathlib
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build

from configuration import load_settings
from drive_access.discovery import list_files_shared_with_service_acc, filter_files_by_mimeType
from drive_access.get import download_file_as_bytes
from service_one_sheet import process_sheet

DEBUG = True


def get_drive_service():
    """
    Returns a service object for the Google Drive API, authenticated with the
    credentials found in a file named 'credentials.json' in the current working
    directory.

    Raises:
    - FileNotFoundError: if the credentials file is not found
    - google.auth.exceptions.TransportError: if there is an error connecting to
      the authentication server
    - googleapiclient.errors.HttpError: if there is an error calling the Drive
      API
    - ValueError: if the credentials file is not in the correct format
    """
    try:
        credentials_file = pathlib.Path.cwd() / 'credentials.json'
        creds = service_account.Credentials.from_service_account_file(
            str(credentials_file),
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=creds)
    except FileNotFoundError:
        logging.error("credentials.json file not found.")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


def main():
    """
    Downloads and processes Excel files from Google Drive.

    This function lists all Excel files shared with a service account and downloads each file using the
    Google Drive API. It then processes each sheet in each file using the `process_sheet()` function.

    Returns:
    None
    """

    # Set up the logger with the desired level and format
    log_level = logging.DEBUG
    log_format = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(level=log_level, format=log_format)

    # Create a file handler with the desired log level and format
    log_file = 'my_app.log'
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Add the file handler to the logger
    logging.getLogger().addHandler(file_handler)

    service = get_drive_service()

    # List xlsx files that were shared with the service account
    files = list_files_shared_with_service_acc(service)
    xlsx_mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    xlsx_files = filter_files_by_mimeType(files, xlsx_mimeType)
    logging.info(f"{len(xlsx_files)} excel files shared with the service account.")
    # TODO: remove in production
    # for f in xlsx_files:
    #     logging.info(f'{f["name"]} ({f["id"]})')

    # Read settings file
    settings = load_settings(service, xlsx_files)
    if settings is None:
        sys.exit(1)

    # Process files
    for f in xlsx_files:

        # TODO: remove in production
        # Check for specific table
        # if DEBUG and f['name'] != 'Copy of Tabela ČUK VESELJKO - Nikola Kostić.xlsx':
        #     continue

        # Download file
        with download_file_as_bytes(service, f['id']) as file:
            logging.info(f"Downloaded {f['name']}: {sys.getsizeof(file) / (1 << 10):,.0f} KB")

            # Go through file sheets and process them
            wb = openpyxl.load_workbook(file, read_only=True)
            for sheet_name in wb.sheetnames:
                process_sheet(wb[sheet_name], settings)


if __name__ == '__main__':
    main()
