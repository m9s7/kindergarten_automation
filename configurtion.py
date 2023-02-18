import openpyxl

from google_drive_library.get import download_file_with_service_acc


def load_default_settings():
    print('Excel file "configurations.xlsx" ne postoji ili nije podeljen sa programom')
    print('Bice koriscena podrazumevana podesavanja:')

    default_settings = {
        "Email column name": "MAILADRESA",
        "Phone number column name": "KONTAKT",
        "Birthday date column name": "RODJENDAN",
        "Birthday notification advance": 2,
    }
    print(default_settings)

    return default_settings


def load_settings(service, files):
    # Find configuration.xlsx file
    config_file = [f for f in files if f['name'] == 'configuration.xlsx']

    # If it's not there, load defaults
    if len(config_file) != 1:
        return load_default_settings()

    # Remove config file from files that will be searched
    files.remove(config_file[0])

    # Download config file
    file = download_file_with_service_acc(service, config_file[0]['id'])

    # Load settings from file
    wb = openpyxl.load_workbook(file, read_only=True)
    ws = wb.worksheets[0]

    settings = {
        "Email column name": ws["e5"].value,
        "Phone number column name": ws["e6"].value,
        "Birthday date column name": ws["e7"].value,
        "Birthday notification advance": int(ws["e8"].value),
    }

    return settings


def get_required_columns_names(settings):

    required_fields = [
        settings['Email column name'],
        settings['Phone number column name'],
        settings['Birthday date column name'],
    ]

    return required_fields
