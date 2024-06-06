import csv
from .db import Database
from io import StringIO
def add_csv(file,group_id=None):
    db =Database()
    file_str = file.stream.read().decode("utf-8")
    file_obj = StringIO(file_str)
    csv_reader = csv.DictReader(file_obj)
    student= []   
    for row in csv_reader:
        firstname = row["First Name"]
        lastname = row["Last Name"]
        email = row["Email"]
        password = row["Password"]
        birthday = row["Bdate"]
        phone = row["Phone"]
        data= db.Add_Student(firstname, lastname, email,password,birthday,phone,None,None)
        student.append(data.to_json())
    return student
