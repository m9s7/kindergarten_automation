import re
from datetime import date

from configurtion import email_col_name, phone_col_name, bday_col_name, bday_notification_advance
from emails import send_emails
from helper_functions import get_pos_of_val_in_sheet, are_col_headers_on_same_row, format_date
from sms import convert_phone_num_to_valid_format, send_sms_messages

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def process_sheet(ws, settings):
    # Get required header cells positions

    phone_header = get_pos_of_val_in_sheet(ws, settings[phone_col_name])
    if phone_header is None:
        return
    email_header = get_pos_of_val_in_sheet(ws, settings[email_col_name])
    if email_header is None:
        return
    bday_header = get_pos_of_val_in_sheet(ws, settings[bday_col_name])
    if bday_header is None:
        return

    # Chk if header cols are on the same row
    if not are_col_headers_on_same_row([email_header, phone_header, bday_header]):
        return

    recipient_emails = []
    recipient_phones = []

    # Do work for each row
    min_row = email_header[1] + 1
    for phone, email, bday in zip(
            ws.iter_rows(min_col=phone_header[0], max_col=phone_header[0], values_only=True, min_row=min_row),
            ws.iter_rows(min_col=email_header[0], max_col=email_header[0], values_only=True, min_row=min_row),
            ws.iter_rows(min_col=bday_header[0], max_col=bday_header[0], values_only=True, min_row=min_row),
    ):
        phone = phone[0]
        email = email[0]
        bday = bday[0]

        if bday is None:
            continue

        day, month, year = format_date(bday)
        if day is None or month is None or year is None:
            print(f"Invalid date format for ({email}, {phone})")
            continue

        # If date condition is fulfilled add them to recipients list
        curr_date = date.today()
        if curr_date.day == day and curr_date.month == month - settings[bday_notification_advance]:

            if email is not None and EMAIL_REGEX.fullmatch(email):
                recipient_emails.append(email)

            if phone is not None:
                phone = convert_phone_num_to_valid_format(phone)
                recipient_phones.append(phone)

    if len(recipient_emails) != 0:
        send_emails(recipient_emails, settings)

    if len(recipient_phones) != 0:
        send_sms_messages(recipient_phones)
