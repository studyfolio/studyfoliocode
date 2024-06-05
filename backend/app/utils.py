import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
import config

def generate_code(length=6):
    characters = string.digits + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


def send_email(subject, message, to_email,html):
    from_email = config.MAIL_USERNAME
    smtp_server = config.MAIL_SERVER
    smtp_port = config.MAIL_PORT
    smtp_username = config.MAIL_USERNAME
    smtp_password = config.MAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    

    msg.attach(MIMEText(message, 'plain'))
    msg.attach(MIMEText(html,'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email:", e)


