import os
from dotenv import load_dotenv, dotenv_values
import mysql.connector
from cryptography.fernet import Fernet
from app.classes import Teacher,Admin


load_dotenv()


DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_PORT = os.environ.get('DB_PORT')
KEY = dotenv_values()['KEY']


class Database:

    def __init__(self):
        self.connection = self.connection_init()
        self.cursor = self.connection.cursor()
        self.cipher_suite = Fernet(KEY)


    def connection_init(self):
        return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        port=DB_PORT
        )
    

    def encrypt_data(self, data :str):
        return self.cipher_suite.encrypt(data.encode())
    

    def decrypt_data(self, edata :str):
        return self.cipher_suite.decrypt(edata).decode()
        


    def Add_Teacher(self, fname :str, lname :str, email :str, password :str , bdate :str, phone :str):        
        query = """
                INSERT INTO teacher (fname, lname, email, pw, bdate, phone)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
        self.cursor.execute(query, (fname, lname, email, self.encrypt_data(password), bdate, phone))
        self.connection.commit()
        return


    def Get_Teachers(self):
        """
        returns tuple consisting of all teachers + admin
        as objects
        """
        query = """
                SELECT * FROM teacher
            """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return tuple(Teacher(row[0], row[1], row[2],row[3],self.decrypt_data(row[4]),row[5],row[6]) if row[0] != 1 else Admin(row[0], row[1], row[2],row[3],self.decrypt_data(row[4]),row[5],row[6]) for row in rows)    
    
    def Delete_Teacher(self, id :int):
        """
        Deletes a teacher by his id as integer
        """
        query = """
            DELETE FROM teacher 
            WHERE id = %s
        """
        self.cursor.execute(query, [str(id)])
        self.connection.commit()
        return
    
    def Authentificate(self, email : str, password: str):        
        """
        Takes in email and password as strings and return 
        a tuple with first element being True if authentication 
        succeded else False and second element being the object 
        Account or None if authentication failed
        """
        query = f"""
            SELECT * FROM teacher 
            WHERE  email = '{email}'
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()        
        if len(result) != 0:
            row = result[0]        
            Account = Teacher(row[0], row[1], row[2],row[3],self.decrypt_data(row[4]),row[5],row[6]) if row[0] != 1 else Admin(row[0], row[1], row[2],row[3],self.decrypt_data(row[4]),row[5],row[6]) 
            if Account.verify_pw(password):
                return(True, Account)
            else:
                return(False, None)
        else:
            return (False, None)
            
    


TEST = Database()

#TEST.Add_Teacher('ali', 'youcef', 'aliyoucef599@gmail.com', 'benisaf', '2004-03-13', '0549328708')
#acc = TEST.Authentificate('mahdiitahiir@gmail.com', 'mahdim')[1]
#print(acc.to_json())
#print(TEST.Get_Teachers())
#TEST.Delete_Teacher(3)
#for i in range():
#    TEST.Add_Teacher('ali', 'youcef', 'aliyoucef599@gmail.com', 'benisaf', '2004-03-13', '0549328708')


