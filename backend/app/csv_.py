import csv
from db import Database

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

DB = Database()

def save_csv(file_path, year):
    csv_data = read_csv_file(file_path)
    for row in csv_data[1:]:
        DB.Add_Student(row[0], row[1], row[2], row[3], row[4], row[5], DB.Get_Promo_ID_By_Year(year), None)


