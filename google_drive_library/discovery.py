# List files in the Google dive

def list_files_shared_with_service_acc(service):
    fileList = []

    pageToken = ""
    while pageToken is not None:

        res = service.files().list(
            fields="nextPageToken, files(id,name,mimeType)",
            pageSize=1000, pageToken=pageToken, corpora="allDrives",
            includeItemsFromAllDrives=True, supportsAllDrives=True
        ).execute()

        for e in res.get("files", []):
            fileList.append(e)

        pageToken = res.get("nextPageToken")

    return fileList


def filter_files_by_mimeType(files, mime_type):
    filtered = [f for f in files if f['mimeType'] == mime_type]

    for f in filtered:
        del f['mimeType']

    return filtered
