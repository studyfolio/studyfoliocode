from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config 

SECRET_KEY = config.SECRET_KEY

serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_reset_token(user_id):
    return serializer.dumps(user_id)

def verify_reset_token(token, expiration=3600):
    try:
        user_id = serializer.loads(token, max_age=expiration)
        return user_id
    except Exception as e:
        return None
    

def send_email(subject, message, to_email):
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

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email:", e)


