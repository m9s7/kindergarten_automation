def list_files_shared_with_service_acc(service):
    """
    Retrieves a list of files that are shared with a particular service account, using the Google Drive API.

    Parameters:
    - service: The Google Drive API service object, obtained through authentication.

    Returns:
    - A list of files that are shared with the specified service account. Each file is represented as a dictionary with the following keys:
        - id: The unique identifier for the file.
        - name: The name of the file.
        - mimeType: The MIME type of the file.

    Example usage:
    ```
    # Authenticate and create a Google Drive API service object
    service = build('drive', 'v3', credentials=creds)

    # Call the list_files_shared_with_service_acc() function to retrieve the list of shared files
    shared_files = list_files_shared_with_service_acc(service)

    # Print the list of shared files
    for file in shared_files:
        print(file['name'])
    ```

    Notes:
    - This function uses the `files().list()` method of the Google Drive API to retrieve the list of shared files.
    - The function retrieves up to 1000 files per API call, using a `pageToken` to keep track of where it left off in the list of results.
    - The function searches for files across all drives that the specified service account has access to.
    - The function only retrieves the file ID, name, and MIME type for each file, as specified by the `fields` parameter.
    """
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
    """
    Filters a list of files by MIME type.

    Parameters:
    - files: A list of files, where each file is represented as a dictionary with the following keys:
        - id: The unique identifier for the file.
        - name: The name of the file.
        - mimeType: The MIME type of the file.
    - mime_type: The MIME type to filter by.

    Returns:
    - A filtered list of files that match the specified MIME type. Each file is represented as a dictionary with the following keys:
        - id: The unique identifier for the file.
        - name: The name of the file.

    Example usage:
    ```
    # Call the filter_files_by_mimeType() function to filter the list of files by MIME type
    filtered_files = filter_files_by_mimeType(files, 'application/pdf')

    # Print the list of filtered files
    for file in filtered_files:
        print(file['name'])
    ```

    Notes:
    - This function filters the list of files by the specified MIME type, using a list comprehension.
    - The function removes the `mimeType` key from each file in the filtered list before returning it.
    """
    filtered = [f for f in files if f['mimeType'] == mime_type]

    for f in filtered:
        del f['mimeType']

    return filtered
