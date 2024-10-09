import smtplib

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(subject: str, text: str, settings: dict):
    sender_email = settings['MAIL_USR']
    app_password = settings['MAIL_PASS']
    recipient_email = settings['MAIL_TO']
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(text, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully!")
        logging.info(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Unsuccessful sent email to {recipient_email}")