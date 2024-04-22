
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

    def __init__(self, id, number, nb_st, promo = None):
        self.id = id
        self.number = number
        self.nb_students = nb_st
        self.promo = promo

    def to_json(self):
        return {
            'number' : self.number,
            'nb_students' : self.nb_students,
            'promo' : self.promo.to_json()
        }
    
class Promo:

    def __init__(self, id, year, nb_st, avg_sc, avg_m, avg_tm):
        self.id = id
        self.year = year
        self.nb_students = nb_st
        self.avg_sc = avg_sc
        self.avg_tm = avg_tm
        self.avg_m = avg_m


    def to_json(self):
        return{
            'year': self.year,
            'nb_students' : self.nb_students,
            'avg_sc' : self.avg_sc,
            'avg_tm' : self.avg_tm,
            'avg_m' : self.avg_m
        }
    

class Student(Account):

    def __init__(self, id, fname, lname, email, pw, bdate, phone, promo = None, group = None):
        super().__init__(id, fname, lname, email, pw, bdate, phone)
        self.promo = promo
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
            'promo' : self.promo.to_json(),
            'group' : self.group.to_json()
        }

    
    

