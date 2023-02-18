import datetime
import re
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sms import convert_phone_num_to_valid_format

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


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

    _date = [d.strip() for d in _date]

    while _date.count(''):
        _date.remove('')

    if len(_date) != 3:
        return None, None, None

    return int(_date[0]), int(_date[1]), int(_date[2])


def send_email(email):
    # email_text = "ok stvari se desavaju, normalan non robot text, ok, bye."
    html = f'''
        <!DOCTYPE html>
        <html>
          <head>
            <title>Happy Birthday!</title>
          </head>
          <body style="background-color: #f5f5f5; font-family: Arial, sans-serif; font-size: 16px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px;">
              <img src="https://box4you.rs/image/cache/catalog/postcards/sa-zirafom-1-1000x1000.jpg" alt="Happy Birthday!" style="display: block; margin: 0 auto; max-width: 100%;">
              <h1 style="text-align: center; color: #ff8c00; margin: 20px 0;">Happy Birthday!</h1>
              <p>Dear dete u nominativu,</p>
              <p>Wishing you a very happy birthday filled with love, joy, and laughter! May all your wishes come true and may this new year of your life be full of wonderful moments and achievements.</p>
              <p>Thank you for being a part of our community, and we hope this birthday brings you much happiness and many memorable moments. Enjoy your special day!</p>
              <p>Best wishes,</p>
              <p>Activity center Team</p>
              <hr style="border: none; border-top: 1px solid #dcdcdc; margin: 20px 0;">
              <p style="text-align: center; font-size: 14px;">If you would like to unsubscribe from future birthday emails, please click <a href="[unsubscribe link]">here</a>.</p>
            </div>
          </body>
        </html>
        '''

    # Set up the email addresses and password. Please replace below with your email address and password

    # TODO: settings
    password = 'mojfxgachxjuuksm'
    email_message = MIMEMultipart()
    email_message['From'] = 'matijasreckovic97@gmail.com'
    email_message['To'] = email
    email_message['Subject'] = "Test sending emails"

    email_message.attach(MIMEText(html, "html"))
    email_string = email_message.as_string()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_message['From'], password)
        server.sendmail(email_message['From'], email, email_string)
    print("email sent")

    # treba mi 5$ da implementiram unsibscribe link
    # - odvede ih na stranicu, you have been unsubbed
    # - link: https://example.com/unsubscribe?email=john@example.com get email from query


def send_sms(phone):
    print(phone)
    #     cl.messages.create(body="Srecan rodjendan", from_='+12013747421', to=phone)
    # treba pozvati onu kompaniju u njihovo ime sto im je nudila poruku za 1 2 dinara ili kolko vec
    pass


def process_sheet(ws, settings):
    # Get required header cells positions

    phone_header = get_pos_of_val_in_sheet(ws, settings['Phone number column name'])
    if phone_header is None:
        return
    email_header = get_pos_of_val_in_sheet(ws, settings['Email column name'])
    if email_header is None:
        return
    bday_header = get_pos_of_val_in_sheet(ws, settings['Birthday date column name'])
    if bday_header is None:
        return

    # Chk if header cols are on the same row
    if not are_col_headers_on_same_row([email_header, phone_header, bday_header]):
        return

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

        # TODO: remove in production
        print(phone, email, bday)
        if email != "matijasreckovic97@gmail.com":
            continue
        ############################

        curr_date = date.today()
        if curr_date.day == day and curr_date.month == month - settings['Birthday notification advance']:

            if email is not None and EMAIL_REGEX.fullmatch(email):
                send_email(email)

            if phone is not None:
                phone = convert_phone_num_to_valid_format(phone)
                send_sms(phone)
