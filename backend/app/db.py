import os
from dotenv import load_dotenv, dotenv_values
import mysql.connector
from cryptography.fernet import Fernet
from .classes import *
import secrets
import string

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
    
    def Generate_ID(self):
        numeric_id = ''.join(secrets.choice(string.digits) for _ in range(10))
        return numeric_id
        


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
        self.cursor.execute("SELECT * FROM teacher WHERE id = LAST_INSERT_ID()")
        row = self.cursor.fetchone()
        return Teacher(row[0], row[1], row[2],row[3],self.decrypt_data(row[4]),row[5],row[6])
        
    

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
            DELETE FROM ressource
            WHERE id_teacher IN ({placeholder})
        """
        query3 = f"""
            DELETE FROM teacher 
            WHERE id IN ({placeholder})
        """
        self.cursor.execute(query1, tuple(teachers))
        self.cursor.execute(query2, tuple(teachers))
        self.cursor.execute(query3, tuple(teachers))
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
        self.cursor.execute("SELECT * FROM student WHERE id = LAST_INSERT_ID()")
        row = self.cursor.fetchone()
        return Student(row[0], row[1], row[2],row[3],self.decrypt_data(row[4]),row[5],row[6], self.Get_Group_By_ID(row[7]))       

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
        return self.Get_Students()

    def Delete_Students(self, students : list):
        """
        Deletes a list of students by thier ids as str
        """
        students.remove('1') if '1' in students else None
        placeholder = ', '.join(['%s'] * len(students))
        query1 = f"""
            DELETE FROM notation 
            WHERE id_student IN ({placeholder})
        """
        query2 = f"""
            DELETE FROM student 
            WHERE id IN ({placeholder})
        """
        self.cursor.execute(query1, tuple(students))
        self.cursor.execute(query2, tuple(students))
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
    

    def Get_Student_By_ID(self, id_student : str):        
        query = """
                SELECT * FROM student
                WHERE id = %s
            """
        self.cursor.execute(query, [id_student])
        row = self.cursor.fetchone()
        
        return Student(row[0], row[1], row[2],row[3],self.decrypt_data(row[4]),row[5],row[6], self.Get_Group_By_ID(row[7]))
    
    
    def Add_Promo(self, name :str, year : str):        

        query = """
                INSERT INTO promo (promo_name, promo_year)
                VALUES (%s, %s)
            """
        self.cursor.execute(query, (name, year))
        self.connection.commit()
        self.cursor.execute("SELECT * FROM promo WHERE id_promo = LAST_INSERT_ID()")
        row = self.cursor.fetchone()
        return Promo(row[0], row[1], row[2])
    
    def Add_Group(self, number : str, id_promo : str):        

        query = """
                INSERT INTO groupe (group_number, id_promo)
                VALUES (%s, %s)
            """
        self.cursor.execute(query, (number, id_promo))
        self.connection.commit()
        self.cursor.execute("SELECT * FROM groupe WHERE id_group = LAST_INSERT_ID()")
        row = self.cursor.fetchone()
        return Group(row[0], row[1], self.Get_Promo_By_ID(row[2]))
    
    
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
                DELETE from study
                WHERE id_promo = %s
            """
        query4 = """
                DELETE from promo 
                WHERE id_promo = %s
            """
        
        self.cursor.execute(query1, [id_promo])
        self.cursor.execute(query2, [id_promo])
        self.cursor.execute(query3, [id_promo])
        self.cursor.execute(query4, [id_promo])
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
        self.cursor.execute("SELECT * FROM module WHERE id = LAST_INSERT_ID()")
        row = self.cursor.fetchone()
        return Module(row[0], row[1],row[2], row[3], row[4], row[5])

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
    
    def Delete_Module(self, id_module : str):
        query1 = """
                DELETE FROM role 
                WHERE id_module = %s
            """
        query2 = """
                DELETE FROM study 
                WHERE id_module = %s
            """
        query3 = """
                DELETE FROM ressource                 
                WHERE id_section IN 
                    ( SELECT id FROM section
                        WHERE id_module = %s 
                        )   
            """
        query4 = """
                DELETE FROM notation                 
                WHERE id_activity IN 
                    ( SELECT id FROM activity
                        WHERE id_section IN
                         (
                            SELECT id FROM section
                            WHERE id_module = %s
                         ) 
                        )   
            """
        query5 = """
                DELETE FROM activity                 
                WHERE id_section IN 
                    ( SELECT id FROM section
                        WHERE id_module = %s 
                        )   
            """
        query6 = """
                DELETE FROM section 
                WHERE id_module = %s
            """
        query7 = """
                DELETE FROM module 
                WHERE id = %s
            """
        self.cursor.execute(query1, [id_module])
        self.cursor.execute(query2, [id_module])
        self.cursor.execute(query3, [id_module])
        self.cursor.execute(query4, [id_module])
        self.cursor.execute(query5, [id_module])
        self.cursor.execute(query6, [id_module])
        self.cursor.execute(query7, [id_module])

        self.connection.commit()
        return


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
        return


    def Get_Teacher_Roles(self, id_teacher: str):
        """
        Returns a tuple containing all roles for a given teacher
        """
        query = """
                SELECT * FROM role
                WHERE id_teacher = %s
            """
        self.cursor.execute(query, [id_teacher])
        rows = self.cursor.fetchall()
        return(tuple(Assignement(self.Get_Teacher_By_ID(row[0]), self.Get_Module_By_ID(row[1]), row[2], row[3]) for row in rows))
    

    def Get_Roles_By_Module(self, id_module : str):   
        """
        Returns a tuple containing all roles for a given module
        """     
        query = """
                SELECT * FROM role
                WHERE id_module = %s
            """
        self.cursor.execute(query, [id_module])
        rows = self.cursor.fetchall()
        return(tuple(Assignement(self.Get_Teacher_By_ID(row[0]), self.Get_Module_By_ID(row[1]), row[2], row[3]) for row in rows))
    
    def Get_Roles(self):   
        """
        Returns a tuple containing all roles for all modules
        """     
        query = """
                SELECT * FROM role                
            """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return(tuple(Assignement(self.Get_Teacher_By_ID(row[0]), self.Get_Module_By_ID(row[1]), row[2], row[3]) for row in rows))
    

    def Delete_Role(self, id_teacher : str, id_module : str, charge : str):
        query = """
            DELETE FROM role 
            WHERE id_teacher = %s AND id_module = %s AND type_charge = %s
            """
        self.cursor.execute(query, (id_teacher, id_module, charge))
        self.connection.commit()
        return

     
        
    
    def Add_Study_Link(self, id_promo : str, id_module : str, shown : str, semester : str):  
        """
        Adds a module to a promo with shown taking '0' or '1' and semenster 
        being either '1' or '2'
        """      
        query = """
                INSERT INTO study (id_promo, id_module, shown, semester)
                VALUES (%s, %s, %s, %s)
            """
        self.cursor.execute(query, (id_promo, id_module, shown, semester))
        self.connection.commit()
        self.cursor.execute("SELECT * FROM study WHERE id_module = %s AND id_promo = %s", (id_module, id_promo))
        row = self.cursor.fetchone()
        return Studying(self.Get_Promo_By_ID(row[1]), self.Get_Module_By_ID(row[0]), row[2], row[3])
    

    def Show_Module(self, id_module : str, id_promo : str):
        """
        Makes a module visible for a promo
        """
        query = """
            UPDATE study SET shown = 1
            WHERE id_promo = %s AND id_module = %s
            """
        self.cursor.execute(query, (id_promo, id_module))
        self.connection.commit()
        return (self.Get_Studies())

    def Hide_Module(self, id_module : str, id_promo : str):
        """
        Makes a module non visible for a promo
        """
        query = """
            UPDATE study SET shown = 0
            WHERE id_promo = %s AND id_module = %s
            """
        self.cursor.execute(query, (id_promo, id_module))
        self.connection.commit()     
        return (self.Get_Studies())   

    def Remove_Study_Link(self, id_promo : str, modules : list):
        placeholder = ','.join(['%s'] * len(modules))
        query = f"""
            DELETE FROM study 
            WHERE id_promo = {'%s'} AND id_module IN ({placeholder})
            """
        self.cursor.execute(query, (id_promo, *modules))
        self.connection.commit()

    def Get_Promo_Modules(self, id_promo):
        query = """
                SELECT * FROM study
                WHERE id_promo = %s
            """
        self.cursor.execute(query, [id_promo])
        rows = self.cursor.fetchall()
        return(tuple(Studying(self.Get_Promo_By_ID(row[1]), self.Get_Module_By_ID(row[0]), row[2], row[3]) for row in rows))

    def Get_Studies(self):
        query = """
                SELECT * FROM study
            """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return(tuple(Studying(self.Get_Promo_By_ID(row[1]), self.Get_Module_By_ID(row[0]), row[2], row[3]) for row in rows))
        

    def Add_Section(self, name : str, id_module : str):
        query = """
            INSERT INTO section (name, id_module)
            VALUES (%s, %s)
        """
        self.cursor.execute(query, (name, id_module))
        self.connection.commit()
        self.cursor.execute("SELECT * FROM section WHERE id = LAST_INSERT_ID()")
        row = self.cursor.fetchone()
        return Section(row[0], row[1], self.Get_Module_By_ID(row[2]))


    def Remove_Sections(self, sections : list):
        placeholder = ','.join(['%s'] * len(sections))
        query1 = f"""
            DELETE FROM ressource 
            WHERE id_section IN ({placeholder})
            """
        query2 = f"""
            DELETE FROM notation 
            WHERE id_activity IN
             (
                SELECT id FROM activity
                WHERE id_section IN ({placeholder})
             ) 
            """
        query3 = f"""
            DELETE FROM activity 
            WHERE id_section IN ({placeholder})
            """
        query4 = f"""
            DELETE FROM section 
            WHERE id IN ({placeholder})
            """
        self.cursor.execute(query1, tuple(sections))
        self.cursor.execute(query2, tuple(sections))
        self.cursor.execute(query3, tuple(sections))
        self.cursor.execute(query4, tuple(sections))    
        self.connection.commit()
        return

    
    def Get_Module_Sections(self, id_module):
        query = """
            SELECT * FROM section
            WHERE id_module = %s
        """
        self.cursor.execute(query, [id_module])
        rows = self.cursor.fetchall()
        return(tuple(Section(row[0], row[1], self.Get_Module_By_ID(row[2])) for row in rows))
    
    def Get_Section_By_ID(self, id_section):
        query = """
            SELECT * FROM section
            WHERE id = %s
        """
        self.cursor.execute(query, [id_section])
        rows = self.cursor.fetchall()
        return(tuple(Section(row[0], row[1], self.Get_Module_By_ID(row[2])) for row in rows)[0])
    
    

    def Add_Ressource(self,name : str, extension : str, type : str, drive_link : str, id_teacher : str, id_section : str):       
        query = """
            INSERT INTO ressource (name, extension, type, drive_link, id_teacher, id_section)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (name, extension, type, drive_link, id_teacher, id_section))
        self.connection.commit()
        self.cursor.execute("SELECT * FROM ressource WHERE id = LAST_INSERT_ID()")
        row = self.cursor.fetchone()
        return Ressource(row[0], row[1], row[2], row[3], row[4], self.Get_Teacher_By_ID(row[5]), self.Get_Section_By_ID(row[6]))
    


    def Delete_Ressource(self, ressources : list):
        placeholder = ','.join(['%s'] * len(ressources))
        query = f"""
            DELETE FROM ressource 
            WHERE id  IN ({placeholder})
            """
        self.cursor.execute(query, tuple(ressources))
        self.connection.commit()
        return

    def Get_Ressources_By_Section(self, id_section):
        query = """
            SELECT * FROM ressource
            WHERE id_section = %s
            """
        self.cursor.execute(query, [id_section])
        rows = self.cursor.fetchall()
        return (tuple(Ressource(row[0], row[2], self.Get_Teacher_By_ID(row[4]), self.Get_Section_By_ID(row[3]), row[1]) for row in rows))

    def Add_Activity(self,name : str, description : str, type : str, drive_link : str, id_section : str, end_date : str):       
        query = """
            INSERT INTO activity (name, description, type, drive_link, id_section, end_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (name, description, type, drive_link, id_section, end_date))
        self.connection.commit()
        self.cursor.execute("SELECT * FROM activity WHERE id = LAST_INSERT_ID()")
        row = self.cursor.fetchone()
        return  Activity(row[0], row[1], row[2], row[3], row[4], self.Get_Section_By_ID(row[5]), row[6])
    

    def Get_Activities(self):
        query = """
            SELECT * FROM activity            
            """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return(tuple(Activity(row[0], row[1], row[2], row[3], row[4], self.Get_Section_By_ID(row[5]), row[6]) for row in rows))
    
    def Get_Activity_By_ID(self, id_activity : str):
        query = """
            SELECT * FROM activity            
            WHERE id = %s
            """
        self.cursor.execute(query, [id_activity])
        row = self.cursor.fetchone()
        return(Activity(row[0], row[1], row[2], row[3], row[4], self.Get_Section_By_ID(row[5]), row[6]))
    

    def Get_Section_Activities(self, id_section : str):
        query = """
            SELECT * FROM activity   
            WHERE id_section = %s         
            """
        self.cursor.execute(query, [id_section])
        rows = self.cursor.fetchall()
        return(tuple(Activity(row[0], row[1], row[2], row[3], row[4], self.Get_Section_By_ID(row[5]), row[6]) for row in rows))
    
    def Delete_Activity(self, id_activity : str):
        query1 = """
            DELETE FROM notation 
            WHERE id_activity = %s
            """
        query2 = """
            DELETE FROM activity 
            WHERE id = %s
            """
        self.cursor.execute(query1, [id_activity])
        self.cursor.execute(query2, [id_activity])
        self.connection.commit()

    def Give_Notation(self, id_student : str, id_activity : str, mark : str, observation : str):
        query = """
            INSERT INTO notation (mark, observation, id_student, id_activity)
            VALUES (%s, %s, %s, %s)
            """
        self.cursor.execute(query, (mark, observation, id_student, id_activity))
        self.connection.commit()
        self.cursor.execute("SELECT * FROM notation WHERE id_student = %s AND id_activity = %s", (id_student, id_activity))
        row = self.cursor.fetchone()
        return Notation(row[0], row[1], self.Get_Student_By_ID(row[2]), self.Get_Activity_By_ID(row[3]))
    

    def Delete_Notaion(self, id_student : str, id_activity : str):
        query = """"
            DELETE FROM notation 
            WHERE id_student = %s AND id_activity = %s
            """
        self.cursor.execute(query, (id_student, id_activity))
        self.connection.commit()

    
    def Get_Students_Notations(self, id_student : str):
        query = """
            SELECT * FROM notation
            WHERE id_student = %s
            """
        self.cursor.execute(query, [id_student])
        rows = self.cursor.fetchall()
        return (tuple(Notation(row[0], row[1], self.Get_Student_By_ID(row[2]), self.Get_Activity_By_ID(row[3])) for row in rows))
        
    def Get_Activity_Notations(self, id_activity : str):
        query = """
            SELECT * FROM notation
            WHERE id_activity = %s
            """
        self.cursor.execute(query, [id_activity])
        rows = self.cursor.fetchall()
        return (tuple(Notation(row[0], row[1], self.Get_Student_By_ID(row[2]), self.Get_Activity_By_ID(row[3])) for row in rows))
        
    


    
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
                if Account.id == 1:
                    return(True, Account)
                else:
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
                        


""" TEST = Database()
TEST.Modify_Group(['174'], '100') """