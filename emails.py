import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "Activity Sportski Rođendan"
html = f'''
        <!DOCTYPE html>
        <html>
          <head>
            <title>Activity Sportski Rođendan</title>
          </head>
          <body style="background-color: #f5f5f5; font-family: Arial, sans-serif; font-size: 16px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px;">
              <img src="https://box4you.rs/image/cache/catalog/postcards/sa-zirafom-1-1000x1000.jpg" alt="Happy Birthday!" style="display: block; margin: 0 auto; max-width: 100%;">
              <h1 style="text-align: center; color: #ff8c00; margin: 20px 0;">Proslavite sa nama svoj NAJBOLJI SPORTSKI ROĐENDAN prilagođen uzrastu uz sportske igre, survivor poligone i Pena žurku!</h1>
              <p>+381642748571 www.activitycentar.com </p>
              <hr style="border: none; border-top: 1px solid #dcdcdc; margin: 20px 0;">
            </div>
          </body>
        </html>
        '''


# <h1 style="text-align: center; color: #ff8c00; margin: 20px 0;">Happy Birthday!</h1>
#               <p>Proslavite sa nama svoj NAJBOLJI SPORTSKI ROĐENDAN prilagođen uzrastu uz sportske igre, survivor poligone i Pena žurku!</p>

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
