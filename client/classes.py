
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
    
    

