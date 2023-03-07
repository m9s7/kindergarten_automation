import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "Test sending emails"
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


def send_email(email, settings):
    # Email initialization
    email_message = MIMEMultipart()
    email_message['Subject'] = subject
    email_message['From'] = settings['Sender email']
    email_message['To'] = email
    password = settings['Sender email app password']

    # Finalize and send
    email_message.attach(MIMEText(html, "html"))
    email_string = email_message.as_string()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_message['From'], password)
        server.sendmail(email_message['From'], email, email_string)
    print("email to " + email_message['To'] + "sent")

    # treba mi 5$ da implementiram unsibscribe link
    # - odvede ih na stranicu, you have been unsubbed
    # - link: https://example.com/unsubscribe?email=john@example.com get email from query
    # ko je unsubbed dodas u jedan excel sheet jelte i provers kad saljes da li osoba nije na listi,
    # apsolutno neefikasno ali sta da se radi


def send_emails(recipients, settings):
    for recipient in recipients:
        # TODO: remove in production
        if recipient != 'matijasreckovic97@gmail.com' and recipient != "activity_client_acc@proton.me":
            continue
        send_email(recipient, settings)
