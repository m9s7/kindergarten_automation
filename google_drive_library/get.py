import io


# To download Google Docs, Sheets, and Slides use files.export instead
def download_file_with_service_acc(service, file_id):
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO(request.execute())

    return file
