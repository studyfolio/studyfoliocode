import os
from dotenv import load_dotenv, dotenv_values
import mysql.connector
from cryptography.fernet import Fernet
from classes import *


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
    
    def check_connection(self):
        try:
            self.connection.ping(reconnect=True, attempts=3, delay=2)
            return True
        except:
            return False
    

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
                return ("Already Registered")
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
    

    def Get_Teacher_By_ID(self, id_teacher):

        query = """
                SELECT * FROM teacher
                WHERE id = %s
            """
        self.cursor.execute(query, [id_teacher])
        row = self.cursor.fetchall()[0]
        return Teacher(row[0], row[1], row[2],row[3],self.decrypt_data(row[4]),row[5],row[6])  

    
    def Delete_Teachers(self, teachers : list):
        """
        Deletes a list of teachers by thier ids as str
        """
        teachers.remove('1') if '1' in teachers else None
        placeholder = ', '.join(['%s'] * len(teachers))
        query1 = f"""
            DELETE FROM role 
            WHERE id_teacher IN ({placeholder})
        """
        query2 = f"""
            DELETE FROM teacher 
            WHERE id IN ({placeholder})
        """
        self.cursor.execute(query1, tuple(teachers))
        self.cursor.execute(query2, tuple(teachers))
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
                return ("Already Registered")
        query = """
                INSERT INTO student (fname, lname, email, pw, bdate, phone, id_group)                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        self.cursor.execute(query, (fname, lname, email, self.encrypt_data(password), bdate, phone, id_groupe))
        self.connection.commit()
        return        

    def Modify_Group(self, students : list, new_group : str):
        """
        Set the group of a number of studetns to a commun new group
        """
        placeholder = ', '.join(['%s'] * len(students))
        query = f"""
            UPDATE student SET id_group = %s
            WHERE id in ({placeholder})
        """                
        self.cursor.execute(query, (new_group, *students))
        self.connection.commit()

    def Delete_Students(self, students : list):
        """
        Deletes a list of students by thier ids as str
        """
        students.remove('1') if '1' in students else None
        placeholder = ', '.join(['%s'] * len(students))
        query = f"""
            DELETE FROM student 
            WHERE id IN ({placeholder})
        """
        self.cursor.execute(query, tuple(students))
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
        return self.Get_Promo_By_ID(self.Get_Promo_ID_By_Year(year)).id
    
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
                SELECT id_promo FROM promo WHERE promo_year = %s
            """
        self.cursor.execute(query, [str(year)])
        row = self.cursor.fetchall()
        return(row[0][0])
    

    def Delete_Promo(self, id_promo : str):
        query1 = """
                DELETE from student
                WHERE id_group IN (
                    SELECT id_group from groupe
                        WHERE id_promo = %s
                )                
            """
        query2 = """
                DELETE from groupe
                WHERE id_promo = %s
            """
        query3 = """
                DELETE from promo 
                WHERE id_promo = %s
            """
        
        self.cursor.execute(query1, [id_promo])
        print('1')        
        self.cursor.execute(query2, [id_promo])
        print('2')
        self.cursor.execute(query3, [id_promo])
        self.connection.commit()
        
     
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
     

    def Add_Module(self, name : str, acronym : str, description : str, coefficient : str, img_link : str):
        query = """
                INSERT INTO module (name, acronym, description, coefficient, img_link)
                VALUES (%s, %s, %s, %s, %s)
            """
        
        self.cursor.execute(query, (name, acronym, description, coefficient, img_link))
        self.connection.commit()

    def Load_Modules(self):
        query = """
                SELECT * FROM module
            """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return (tuple(Module(row[0], row[1],row[2], row[3], row[4], row[5]) for row in rows))
    
    def Get_Module_By_ID(self, id_module):
        query = """
                SELECT * FROM module
                WHERE id = %s
            """
        self.cursor.execute(query, [id_module])
        row = self.cursor.fetchall()[0]
        return Module(row[0], row[1],row[2], row[3], row[4], row[5])


    def Assign(self, id_teacher :str, id_module :str, type_charge :str, permission : str):
        """
        Gives a role to a teacher in a certain module
        type charge can be : 'COURS' or 'TD'
        permission can be : 'R' for read only and 'W' for both read and write
        """
        query = """
                INSERT into role (id_teacher, id_module, type_charge, permission)
                VALUES (%s, %s, %s, %s)
            """
        self.cursor.execute(query, (id_teacher, id_module, type_charge, permission))
        self.connection.commit()


    def Get_Teacher_Roles(self, id_teacher: str):
        query = """
                SELECT * FROM role
                WHERE id_teacher = %s
            """
        self.cursor.execute(query, [id_teacher])
        rows = self.cursor.fetchall()
        return(tuple(Assignement(self.Get_Teacher_By_ID(row[0]), self.Get_Module_By_ID(row[1]), row[2], row[3]) for row in rows))

    

    
    


    
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

TEST.Delete_Teachers(['21'])