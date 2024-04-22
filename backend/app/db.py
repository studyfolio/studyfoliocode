import os
from dotenv import load_dotenv, dotenv_values
import mysql.connector
from cryptography.fernet import Fernet
from classes import Teacher, Admin, Student, Promo, Group


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
                SELECT pw FROM teacher 
                where email = %s
            """     
        self.cursor.execute(query, [email])
        rows = self.cursor.fetchall()
        for row in rows:
            if self.decrypt_data(row[0]) == password:
                return("Already Registered")
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
        if id == 1:
            return
        query = """
            DELETE FROM teacher 
            WHERE id = %s
        """
        self.cursor.execute(query, [str(id)])
        self.connection.commit()
        return
    
    def Add_Student(self, fname :str, lname :str, email :str, password :str , bdate :str, phone :str, id_groupe : str):        
        query = """
                SELECT pw FROM student 
                where email = %s
            """     
        self.cursor.execute(query, [email])
        rows = self.cursor.fetchall()
        for row in rows:
            if self.decrypt_data(row[0]) == password:
                print("Already Registered")
                return("Already Registered")
        query = """
                INSERT INTO student (fname, lname, email, pw, bdate, phone, id_group)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        self.cursor.execute(query, (fname, lname, email, self.encrypt_data(password), bdate, phone, id_groupe))
        self.connection.commit()
        return
    
    def Get_Students(self):
        """
        returns tuple consisting of all students
        as objects
        """
        query = """
                SELECT * FROM student
            """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        return tuple(Student(row[0], row[1], row[2],row[3],self.decrypt_data(row[4]),row[5],row[6], self.Get_Group_By_ID(row[7])) for row in rows)  
    
    def Add_Promo(self, name :str, year : str):        

        query = """
                INSERT INTO promo (promo_name, promo_year)
                VALUES (%s, %s)
            """
        self.cursor.execute(query, (name, year))
        self.connection.commit()
        return (self.Get_Promo_By_ID(self.Get_Promo_ID_By_Year(year)))
    
    def Add_Group(self, number : str, id_promo : str):        

        query = """
                INSERT INTO groupe (group_number, id_promo)
                VALUES (%s, %s)
            """
        self.cursor.execute(query, (number, id_promo))
        self.connection.commit()
        return
    
    
    def Get_Promos(self):
        """
        returns tuple consisting of all promos
        as objects
        """
        query = """
                SELECT * FROM promo
            """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return tuple(Promo(row[0], row[1], row[2]) for row in rows)  
    
    def Get_Promo_By_ID(self, id):
        """
        returns selected promo by id
        """
        query = """
                SELECT * FROM promo WHERE id_promo = %s
            """
        self.cursor.execute(query, [str(id)])
        rows = self.cursor.fetchall()
        for row in rows:
            return Promo(row[0], row[1], row[2])
        return None 
    
    def Get_Promo_ID_By_Year(self, year):
        """
        returns selected promo id by year
        """
        query = """
                SELECT id FROM promo WHERE promo_year = %s
            """
        self.cursor.execute(query, [str(year)])
        row = self.cursor.fetchall()
        return(row[0][0])
        
     
    def Get_Groups(self):
        """
        returns tuple consisting of all groups
        as objects
        """
        query = """
                SELECT * FROM groupe
            """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return tuple(Group(row[0], row[1], self.Get_Promo_By_ID(row[2])) for row in rows)  
    
    def Get_Group_By_ID(self, id):
        """
        returns selected promo by id
        """
        query = """
                SELECT * FROM groupe WHERE id_group = %s
            """
        self.cursor.execute(query, [str(id)])
        rows = self.cursor.fetchall()
        for row in rows:
            return Group(row[0], row[1], self.Get_Promo_By_ID(row[2]))
        return None
     
    
    


    
    def Authentificate_TA(self, email : str, password: str):        
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
        
    def Authentificate_ST(self, email : str, password: str):        
        """
        Takes in email and password as strings and return 
        a tuple with first element being True if authentication 
        succeded else False and second element being the object 
        Account or None if authentication failed
        """
        query = f"""
            SELECT * FROM student 
            WHERE  email = '{email}'
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()        
        if len(result) != 0:
            row = result[0]        
            Account = Student(row[0], row[1], row[2],row[3],self.decrypt_data(row[4]),row[5],row[6], self.Get_Group_By_ID(row[7]))
            if Account.verify_pw(password):
                return(True, Account)
            else:
                return(False, None)
        else:
            return (False, None)
        
    
    def Authentificate(self, email : str, password : str):

        attempt = self.Authentificate_TA(email, password)
        if not attempt[0]:
            return self.Authentificate_ST(email, password)
        else:
            return attempt
                        
    


TEST = Database()
#TEST.Add_Student('tahir', 'abderrahmane', 'am.tahir@esi-sba.dz', 'relizane48', '2004-10-19', '0798113634', '1')
result = TEST.Get_Students()
for res in result:
    print(res.to_json())