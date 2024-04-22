
class Account:
    def __init__(self, id, fname, lname, email, pw, bdate, phone):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = pw
        self.bdate = bdate
        self.phone = phone

    def verify_pw(self, pw):
        return (pw == self.password)

class Teacher(Account):

    def __init__(self, id, fname, lname, email, pw, bdate, phone):
        super().__init__(id, fname, lname, email, pw, bdate, phone)

    def __repr__(self) -> str:
        return('TEACHER || ID : '+str(self.id) + ' Name : '+self.fname+' '+self.lname+' Email : '+self.email+" "+self.password)
    
    def to_json(self):
        return{
            'state' : 'teacher',
            'id' :self.id,
            'fname' : self.fname,
            'lname' : self.lname,
            'email' : self.email,
            'bdate' : str(self.bdate),
            'phone' : self.phone,            
        }

class Admin(Account):

    def __init__(self, id, fname, lname, email, pw, bdate, phone):
        super().__init__(id, fname, lname, email, pw, bdate, phone)

    def __repr__(self) -> str:
        return('ADMIN || ID : '+str(self.id) + ' Name : '+self.fname+' '+self.lname+' Email : '+self.email+' '+self.password)

    def to_json(self):
        return{
            'state' : 'admin',
            'id' :self.id,
            'fname' : self.fname,
            'lname' : self.lname,
            'email' : self.email,
            'bdate' : str(self.bdate),
            'phone' : self.phone,            
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

    def __init__(self, id, fname, lname, email, pw, bdate, phone, group = None):
        super().__init__(id, fname, lname, email, pw, bdate, phone)
        self.group = group

    def __repr__(self) -> str:
        return('Student || ID : '+str(self.id) + ' Name : '+self.fname+' '+self.lname+' Email : '+self.email+" "+self.password)
    
    def to_json(self):
        return{
            'state' : 'student',
            'id' :self.id,
            'fname' : self.fname,
            'lname' : self.lname,
            'email' : self.email,
            'bdate' : str(self.bdate),
            'phone' : self.phone, 
            'group' : self.group.to_json()
        }

    
    

