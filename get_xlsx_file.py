import io
import sys


def list_files_in_drive(service):
    fileList = []
    pageToken = ""
    while pageToken is not None:

        # mimeType='application/vnd.google-apps.spreadsheet' or
        res = service.files().list(
            q="mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' and trashed=false",
            fields="nextPageToken, files(id,name,mimeType)", pageSize=1000, pageToken=pageToken, corpora="allDrives",
            includeItemsFromAllDrives=True, supportsAllDrives=True).execute()

        for e in res.get("files", []):
            del e["mimeType"]
            fileList.append(e)
        pageToken = res.get("nextPageToken")

    return fileList


def download_file(service, file_id):
    file = service.files().get(fileId=file_id, fields='*').execute()
    file_name = file['name']
    mimetype = file['mimeType']

    # add support for Google sheets if they need it, because that needs to be downloaded with .export not .get
    if mimetype != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        print("Not an excel file")
        return

    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO(request.execute())
    print(f"{file_name}: {sys.getsizeof(file) / (1 << 10):,.0f} KB")

    return file


def get_file_from_local(filename):
    with open(filename, "rb") as f:
        in_mem_file = io.BytesIO(f.read())

    return in_mem_file
