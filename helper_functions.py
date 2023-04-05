import re
from datetime import datetime


def digits_only(string_with_non_digits):
    """
    Accepts a string and returns a new string containing only the digits
    from the input string.

    Args:
        string_with_non_digits (str): The input string containing digits and non-digits.

    Returns:
        str: A new string containing only the digits from the input string.
    """
    return ''.join([char for char in string_with_non_digits if char.isdigit()])


def trim_non_digit_chars(string):
    """
    Removes all leading and trailing non-digit characters from a string.

    Args:
        string (str): The string to remove non-digit characters from.

    Returns:
        str: The input string with leading and trailing non-digit characters removed.
    """
    # Remove leading non-digit characters
    start_index = 0
    while start_index < len(string) and not string[start_index].isdigit():
        start_index += 1

    # Remove trailing non-digit characters
    end_index = len(string) - 1
    while end_index >= 0 and not string[end_index].isdigit():
        end_index -= 1

    # Return the trimmed string
    return string[start_index:end_index + 1]


def format_date(date_string):
    """
    Formats a date string into a tuple of day and month integers.

    Args:
    - date_string (str or datetime): A string representing a date or a datetime object.

    Returns:
    - Tuple of day (int) and month (int) if the input is a valid date string.

    Raises:
    - ValueError: If the input string cannot be parsed into a valid date format.

    The function first checks if the input is already a datetime object. If not, it removes any non-digit characters
    from the input string using the 'trim_non_digit_chars' function.

    The function uses a regular expression to match valid date strings. The regular expression pattern is:
    r"\b(?P<day>\d{1,2})[\./,-]\s*(?P<month>\d{1,2})\b"

    This pattern matches strings that start and end with a word boundary, and contain two named groups: 'day' and 'month'.
    The 'day' group matches one or two digits separated by a forward slash, period or comma followed by an optional space character.
    The 'month' group matches one or two digits separated by a forward slash, period or comma.
    """

    # Check if input is already a datetime object
    if isinstance(date_string, datetime):
        return date_string.day, date_string.month

    # Remove non-digit characters from input string
    date_string = trim_non_digit_chars(str(date_string))

    # Regular expression to match valid date strings
    # pattern = r"\b(?P<day>\d{1,2})[\./,-]\s*(?P<month>\d{1,2})\s*\.[\./,-]?\s*\d{2,4}\b"
    pattern = r"\b(?P<day>\d{1,2})[\./,-]\s*(?P<month>\d{1,2})\b"

    match = re.search(pattern, str(date_string))

    if match:
        day, month = int(match.group("day")), int(match.group("month"))
        if 1 <= day <= 31 and 1 <= month <= 12:
            return day, month

    # Raise an exception if date cannot be parsed
    raise ValueError(f"Invalid date format: {date_string}")


def get_pos_of_val_in_sheet(ws, val):
    """Finds the first occurrence of a value in a read-only worksheet and returns its position.

    This function searches for a value in a read-only worksheet by iterating over all the cells in
    the worksheet. It returns the position of the first cell containing the value.

    Args:
        ws (openpyxl.worksheet.worksheet.Worksheet): The read-only worksheet to search.
        val (any): The value to find.

    Returns:
        Tuple[int, int] or Tuple[None, None]: The column and row indices of the cell containing
        the value, or None values if the value is not found.
    """
    for row in ws.iter_rows():
        for cell in row:
            if cell.value == val:
                return cell.column, cell.row

    return None, None


def are_col_headers_on_same_row(headers):
    """Checks if the headers of multiple columns are on the same row.

    Args:
        headers (List[Tuple[str, int]]): A list of tuples containing the column header name
        and its row index.

    Raises:
        ValueError: If the headers are not all on the same row.

    Returns:
        bool: True if all headers are on the same row, False otherwise.
    """
    rows = set(h[1] for h in headers)
    if len(rows) == 1:
        return True
    else:
        raise ValueError("Required columns headings not aligned on the same row")
