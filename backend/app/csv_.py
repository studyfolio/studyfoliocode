import csv
from .db import Database
from io import StringIO
from .utils import send_email
def add_csv(file,group_id=None):
    db =Database()
    file_str = file.stream.read().decode("utf-8")
    file_obj = StringIO(file_str)
    csv_reader = csv.DictReader(file_obj)
    student= []
    subject="StudyFolio Account"
    html = f"""
    <html>
    <head>

    </head>
    <body>
        <div class="content">
            <div class="header">
                <h1>StudyFolio Account Information</h1>
            </div>
            
            <div style="font-size:20px;">
            <h4>Hello,</h4>
            <h5>Email :<b>{email}</b></h5>
            <h5>Password :<b>{password}</b></h5>
            </div>
            <div class="footer">
                <p>&copy; 2024 study folio</p>
            </div>
        </div>
    </body>
    </html>
    """     
    for row in csv_reader:
        firstname = row["First Name"]
        lastname = row["Last Name"]
        email = row["Email"]
        password = row["Password"]
        birthday = row["Bdate"]
        phone = row["Phone"]
        data= db.Add_Student(firstname, lastname, email,password,birthday,phone,group_id)
        send_email(subject,message='',to_email=email,html=html)
        student.append(data.to_json())
    return student
