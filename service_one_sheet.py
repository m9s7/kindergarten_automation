import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from openpyxl_data_manipulation import get_column_positions, Column, has_columns, are_col_headers_on_same_row
from sms import cl, convert_phone_num_to_valid_format, format_date


def service_sheet(worksheet):
    phone_number_col = Column(name="KONTAKT")
    email_col = Column(name="MAILADRESA")
    birthday_col = Column(name="RODJENDAN")

    required_columns = [phone_number_col, email_col, birthday_col]

    get_column_positions(worksheet, required_columns)
    if not has_columns(worksheet.title, required_columns):
        return False
    if not are_col_headers_on_same_row(required_columns):
        return False

    # Do work for each row
    min_row = required_columns[0].header_row + 1
    for phone, email, bday in zip(
            worksheet.iter_rows(min_col=phone_number_col.header_col, max_col=phone_number_col.header_col,
                                values_only=True, min_row=min_row),
            worksheet.iter_rows(min_col=email_col.header_col, max_col=email_col.header_col, values_only=True,
                                min_row=min_row),
            worksheet.iter_rows(min_col=birthday_col.header_col, max_col=birthday_col.header_col, values_only=True,
                                min_row=min_row)
    ):
        phone = phone[0]
        email = email[0]
        bday = bday[0]

        if bday is None:
            continue
        # TODO: separate, don't skip but do here
        if email is None and phone is None:
            continue

        phone = convert_phone_num_to_valid_format(phone)

        day, month, year = format_date(bday)
        if day is None or month is None or year is None:
            print(f"Invalid date format for ({email}, {phone})")
            continue

        print(phone, email, format_date(bday))

        # TODO: remove in production
        if email != "matijasreckovic97@gmail.com":
            continue

        # Script will run once a day, I maintain the server, I change the time when they ask for it, that's maintenance 20e a month

        # TODO: settings
        number_of_months_before_bday = 2

        # SEND EMAIL MARKETING
        curr_date = date.today()
        if curr_date.day == day and curr_date.month == month - number_of_months_before_bday:
            # send email
            # choose gmail acc -> acc manager -> security -> turn on 2 step ver..
            #                                             -> app passwords -> custom name

            email_text = "ok stvari se desavaju, normalan non robot text, ok, bye."
            html = f'''
                <html>
                    <body>
                        <h1>Hello happy bday in 2 months</h1>
                        <p>{email_text}</p>
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

            # send text
            print("send text")
            cl.messages.create(body="Srecan rodjendan", from_='+12013747421', to=phone)

        # CONGRATULATE KID ON BDAY same just sent on the exact day
        # na ovaj dan rodjen je Matija Sreckovic, Srecan Rodjendan ta neka fora zbog nominativa
