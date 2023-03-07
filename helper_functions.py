import datetime


def format_date(date_string):
    if isinstance(date_string, datetime.datetime):
        return int(date_string.day), int(date_string.month), int(date_string.year)

    date_string = date_string.strip()

    _date = []
    # chk various delimiters
    if date_string.find('.') != -1:
        _date = date_string.split('.')
    elif date_string.find('/') != -1:
        _date = date_string.split('.')
    elif date_string.find('\\') != -1:
        _date = date_string.split('.')
    elif date_string.find('-') != -1:
        _date = date_string.split('.')
    else:
        print(date_string, " is invalid date format")

    _date = [d.strip() for d in _date]

    while _date.count(''):
        _date.remove('')

    if len(_date) != 3:
        return None, None, None

    return int(_date[0]), int(_date[1]), int(_date[2])


def get_pos_of_val_in_sheet(ws, val):
    for row in ws.iter_rows():
        for cell in row:
            if cell.value == val:
                return cell.column, cell.row

    return None


def are_col_headers_on_same_row(headers):
    first_header_row = headers[0][1]

    for h in headers[1:]:
        if h[1] != first_header_row:
            print("Required columns headings not aligned on the same row")
            return False
    return True
