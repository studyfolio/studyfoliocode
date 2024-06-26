
class Account:
    def __init__(self, id, fname, lname, email, pw, bdate, phone, profile_pic=None):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = pw
        self.bdate = bdate
        self.phone = phone
        self.profile_pic = profile_pic

    def verify_pw(self, pw):
        return (pw == self.password)

class Teacher(Account):

    def __init__(self, id, fname, lname, email, pw, bdate, phone, profile_pic=None):
        super().__init__(id, fname, lname, email, pw, bdate, phone, profile_pic)
    
    def to_json(self):
        return{
            'state' : 'teacher',
            'id' :self.id,
            'fname' : self.fname,
            'lname' : self.lname,
            'email' : self.email,
            'bdate' : str(self.bdate),
            'phone' : self.phone,  
            'profile_pic' : self.profile_pic
        }

    def complete_json(self, roles):
        return list((role.to_json() for role in roles))
    
class Admin(Account):

    def __init__(self, id, fname, lname, email, pw, bdate, phone, profile_pic=None):
        super().__init__(id, fname, lname, email, pw, bdate, phone, profile_pic)
    
    def to_json(self):
        return{
            'state' : 'admin',
            'id' :self.id,
            'fname' : self.fname,
            'lname' : self.lname,
            'email' : self.email,
            'bdate' : str(self.bdate),
            'phone' : self.phone,            
            'profile_pic' : self.profile_pic
        }
    
    

class Group:

    def __init__(self, id, number, promo):
        self.id = id
        self.number = number
        self.promo = promo

    def to_json(self):
        return {
            'id' : self.id,
            'number' : self.number,
            'promo' : self.promo.to_json()
        }
    
class Promo:

    def __init__(self, id, name, year):
        self.id = id
        self.name = name
        self.year = year       


    def to_json(self):
        return{
            'id' : self.id,
            'name' : self.name,
            'year': self.year,
            
        }
    

class Student(Account):

    def __init__(self, id, fname, lname, email, pw, bdate, phone, profile_pic=None, group = None):
        super().__init__(id, fname, lname, email, pw, bdate, phone, profile_pic)
        self.group = group
    
    def to_json(self):
        return{
            'state' : 'student',
            'id' :self.id,
            'fname' : self.fname,
            'lname' : self.lname,
            'email' : self.email,
            'bdate' : str(self.bdate),
            'phone' : self.phone, 
            'group' : None if self.group is None else self.group.to_json(),
            'profile_pic' : self.profile_pic
        }
    
class Module:

    def __init__(self, id, name, acronym, description, coefficient, img_link):
        self.id = id
        self.name = name
        self.acronym = acronym
        self.description = description
        self.coefficient = coefficient
        self.img_link = img_link

    def to_json(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'acronym' : self.acronym,
            'description' : self.description,
            'coefficient' : self.coefficient,
            'image_link' : self.img_link
        }
    
class Assignement:
    def __init__(self, teacher, module, type_charge, permission):
        self.teacher = teacher
        self.module = module
        self.type_charge = type_charge
        self.permission = permission

    def to_json(self):
        return {
            'teacher' : self.teacher.to_json(),
            'module' : self.module.to_json(),
            'type_charge' : self.type_charge,
            'permission' : self.permission
        }
    
class Studying:
    def __init__(self, promo, module, shown, semester):
        self.promo = promo
        self.module = module
        self.shown = shown
        self.semester = semester

    def to_json(self):
        return {
            'promo' : self.promo.to_json(),
            'module' : self.module.to_json(),
            'shown' : self.shown,
            'semester' : self.semester
        }

class Section:
    def __init__(self, id, name, module):
        self.id = id
        self.name = name
        self.module = module

    def to_json(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'module' : self.module.to_json()
        }
    
class Ressource:
    def __init__(self, id, name, type, extension, drive_link, id_teacher, id_section):
        self.id = id
        self.type = type
        self.drive_link = drive_link
        self.name = name
        self.id_teacher = id_teacher
        self.id_section = id_section
        self.extension = extension

    def to_json(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'extension' : self.extension,
            'type' : self.type,
            'drive_link' : self.drive_link,
            'teacher' : self.id_teacher.to_json(),
            'section' : self.id_section.to_json()
        }
    
class Activity:
    def __init__(self, id, name, description, type, drive_link, section, end_date):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.drive_link = drive_link
        self.section = section
        self.end_date = end_date

    def to_json(self):
        return{
            'id' : self.id,
            'name' : self.name,
            'description' : self.description,
            'type' : self.type,
            'drive_link' : self.drive_link,
            'section' : self.section.to_json(),
            'end_date' : self.end_date
        }
    
class Submission:
    def __init__(self, student, activity, drive_link, mark, observation):
        self.mark = mark
        self.observation = observation
        self.student = student
        self.activity = activity
        self.drive_link = drive_link

    def to_json(self):
        return{
            'mark' : self.mark,
            'observation' : self.observation,
            'student' : self.student.to_json(),
            'activity' : self.activity.to_json(),
            'drive_link' : self.drive_link
        }