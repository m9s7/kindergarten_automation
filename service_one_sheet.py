import logging
import re
from datetime import date

from configuration import BDAY_NOTIFICATION_ADVANCE, PHONE_COL_NAME, EMAIL_COL_NAME, BDAY_COL_NAME
from emails import send_emails
from helper_functions import get_pos_of_val_in_sheet, are_col_headers_on_same_row, format_date
from sms import format_phone_number, send_sms_messages


# This regular expression is used to match email addresses. It matches any character that is not an "@" symbol, one or more times,
# followed by an "@" symbol, followed by any character that is not an "@" symbol, one or more times, followed by a literal "." character,
# followed by any character that is not an "@" symbol, one or more times.
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def process_sheet(ws, settings):
    """Process the worksheet to find birthdays and send notifications.

    Args:
        ws (openpyxl.Worksheet): The worksheet to process.
        settings (dict): A dictionary of configuration settings.

    Returns:
        None: If the required headers are not found, or if there is an error in processing the worksheet.

    """

    # Get required header cells positions
    phone_header_pos = get_pos_of_val_in_sheet(ws, settings[PHONE_COL_NAME])
    if phone_header_pos[0] is None:
        return
    email_header_pos = get_pos_of_val_in_sheet(ws, settings[EMAIL_COL_NAME])
    if email_header_pos[0] is None:
        return
    bday_header_pos = get_pos_of_val_in_sheet(ws, settings[BDAY_COL_NAME])
    if bday_header_pos[0] is None:
        return

    try:
        are_col_headers_on_same_row([email_header_pos, phone_header_pos, bday_header_pos])
    except ValueError as e:
        logging.error(f"Skipping sheet {ws.title} - {str(e)}")
        return

    recipient_emails = []
    recipient_phones = []

    # Do work for each row
    min_row = email_header_pos[1] + 1
    for phone, email, bday in zip(
            ws.iter_rows(min_col=phone_header_pos[0], max_col=phone_header_pos[0], values_only=True, min_row=min_row),
            ws.iter_rows(min_col=email_header_pos[0], max_col=email_header_pos[0], values_only=True, min_row=min_row),
            ws.iter_rows(min_col=bday_header_pos[0], max_col=bday_header_pos[0], values_only=True, min_row=min_row),
    ):
        phone = phone[0]
        email = email[0]
        bday = bday[0]

        if bday is None:
            continue

        try:
            day, month = format_date(bday)
        except ValueError as e:
            logging.info(f"{email}, {phone}: {str(e)}")
            continue

        # If date condition is fulfilled add them to recipients list
        curr_date = date.today()
        if curr_date.day == day and curr_date.month == month - settings[BDAY_NOTIFICATION_ADVANCE]:

            logging.info(f"Birthday today: {email} ({phone}) in {ws.title}")

            if email is not None and EMAIL_REGEX.fullmatch(email):
                recipient_emails.append(email)

            if phone is not None:
                phone = format_phone_number(phone)
                recipient_phones.append(phone)

    # if len(recipient_emails) != 0:
    #     send_emails(recipient_emails, settings)
    #
    # if len(recipient_phones) != 0:
    #     send_sms_messages(recipient_phones)
