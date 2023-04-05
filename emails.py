import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from configuration import SENDER_EMAIL, SENDER_EMAIL_APP_PASSWORD

SUBJECT = "Activity Sportski Rođendan"
HTML_TEMPLATE = '''
        <!DOCTYPE html>
        <html>
          <head>
            <title>Activity Sportski Rođendan</title>
          </head>
          <body style="background-color: #f5f5f5; font-family: Arial, sans-serif; font-size: 16px;">
            <div style="max-width: 600px; text-align: center; margin: 0 auto; background-color: #ffffff; padding: 20px;">
              <img src="https://raw.githubusercontent.com/m9s7/kindergarten_automation/main/assets/images/SRE%C4%86AN%20RO%C4%90ENDAN%20MEJL.png" alt="Happy Birthday!" style="display: block; margin: 0 auto; max-width: 100%;">
              <h1 style="text-align: center; color: #2EA3F2; margin: 20px 0;">Proslavite sa nama svoj NAJBOLJI SPORTSKI ROĐENDAN prilagođen uzrastu uz sportske igre, survivor poligone i Pena žurku!</h1>
              <h2 style="color: #741B64;">
              <a href="https://www.youtube.com/@skolicasportaactivity">
                <img src="https://raw.githubusercontent.com/m9s7/kindergarten_automation/main/assets/images/yt.png" alt="YouTube Icon" width="64" height="64">
                <br> Pogledajte na YouTube-u
              </a>
            </h2>
            <h2 style="display: inline-block; color: #741B64; margin-right: 20px;">+381642748571</h2>
            <h2 style="display: inline-block; color: #741B64;"><a href="http://www.activitycentar.com">www.activitycentar.com</a></h2>
            </div>
          </body>
        </html>
        '''


def send_email(recipient_email, settings):
    """
    Sends an email to the specified recipient using the provided settings.

    Args:
        recipient_email (str): The email address of the recipient.
        settings (dict): A dictionary containing the sender's email and app password.
    """
    email_message = MIMEMultipart()
    email_message['Subject'] = SUBJECT
    email_message['From'] = settings[SENDER_EMAIL]
    email_message['To'] = recipient_email

    email_message.attach(MIMEText(HTML_TEMPLATE, "html"))
    email_string = email_message.as_string()

    with smtplib.SMTP_SSL('activitycentar.com', 465) as server:
        server.login(
            settings[SENDER_EMAIL],
            settings[SENDER_EMAIL_APP_PASSWORD]
        )
        server.sendmail(email_message['From'], recipient_email, email_string)

    logging.info(f"Email to {email_message['To']} sent")


def send_emails(recipients, settings):
    """
    Sends emails to all recipients in the provided list.

    Args:
        recipients (list): A list of email addresses for the recipients.
        settings (dict): A dictionary containing the sender's email and app password.
    """
    for recipient in recipients:
        # TODO: remove in production
        if recipient != 'matijasreckovic97@gmail.com':
            continue
        send_email(recipient, settings)
