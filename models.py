from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, func

import sqlalchemy
from sqlalchemy import create_engine, ForeignKey

db = SQLAlchemy()
Base = declarative_base()

class Adopter(Base):
    __tablename__ = 'Adopter'

    Personality = Column(String)
    Space       = Column(String)
    Age_min     = Column(Integer)
    Age_max     = Column(Integer)
    Adopter_id  = Column(Integer, primary_key=True, autoincrement=True)
    Username    = Column(String, unique = True)
    Password    = Column(String)

#    def __init__(self):
#        pass

    def __init__(self, user, password, personality, space, age_min, age_max):
#        self.Adopter_id  = "`DEFAULT`"
        self.Username    = user
        self.Password    = password
        self.Personality = personality
        self.Space       = space
        self.Age_min     = age_min
        self.Age_max     = age_max

#    @staticmethod
#    def validate_form(form):
#        username = form['username']
#        if len(str(username)) < 1 or len(str(form['password'])) < 1:
#            return False
#        query = db.session.query(Adopter)
#        adopters = query.all()
#        for a in adopters:
#            if a.Username == username:
#                return False
#        user = Adopter(str(username),str(form['password']),str(form['personality']),str(form['space']),str(form['age_r']))
#        db.session.add(user)
#        db.session.commit()
#        return True


class Favorites(Base):
    __tablename__ = 'Favorites'

    Animal_id  = Column(Integer, ForeignKey('Animals.Animal_id'), primary_key=True, nullable = False)
    Adopter_id = Column(Integer, ForeignKey('Adopter.Adopter_id'), primary_key=True, nullable = False)

    def __init__ (self, aId, uId):
        self.Animal_id  = aId
        self.Adopter_id = uId

class Animals(Base):
    __tablename__ = 'Animals'

    Medical_history = Column(String)
    Age             = Column(Integer)
    Type            = Column(String)
    Breed           = Column(String)
    Temperament     = Column(String)
    Color           = Column(String)
    Size            = Column(String)
    Name            = Column(String)
    Animal_id       = Column(Integer, primary_key=True, autoincrement=True)
    Organization_id = Column(Integer, ForeignKey('Organization.Organization_id'), nullable = False)
    img_path        = Column(String)


    def __init__(self, med_hist, age, temperament, name, oId, img_path, typ, breed, color, size):
        self.Medical_history = med_hist
        self.Age             = age
        self.Temperament     = temperament
        self.Name            = name
        self.Organization_id = oId
        self.img_path        = img_path
        self.Breed           = breed
        self.Type            = typ
        self.Color           = color
        self.Size            = size 

class Employee(Base):
    __tablename__ = 'Employee'

    Username        = Column(String, unique=True)
    Password        = Column(String)
    Employee_id     = Column(Integer, primary_key=True, autoincrement=True)
    #Email           = Column(String, unique=True)
    Organization_id = Column(Integer, ForeignKey('Organization.Organization_id'), nullable = False)

    def __init__(self, username, password, orgId):
        self.Username        = username
        self.Password        = password
        self.Organization_id = orgId
        #self.email           = email

class Organization(Base):
    #Add a name and a description
    __tablename__ = 'Organization'

    Location        = Column(String)
    Phone_number    = Column(String)
    Capacity        = Column(Integer)
    Organization_id = Column(Integer, primary_key=True, autoincrement = True)
    Username        = Column(String, unique = True)
    Name            = Column(String)
    Password        = Column(String)
    MaxCap          = Column(Integer)

    def __init__(self, loc, pn, cap, user, name, passw, MAX=100):
        #self.Organization_id = oID
        self.Location     = loc
        self.Phone_number = pn
        self.Capacity     = cap
        self.Username     = user
        self.Name         = name
        self.Password     = passw
        self.MaxCap       = MAX

class Supplies(Base):
    __tablename__ = 'Supplies'

    Description     = Column(String)
    Title           = Column(String)
    Amount          = Column(String)
    Type            = Column(String)
    Organization_id = Column(Integer, ForeignKey('Organization.Organization_id'), nullable = False)
    Supply_id       = Column(Integer,primary_key=True, autoincrement = True)

    def __init__(self, desc, title, amnt, typ, orgId):
        self.Description     = desc
        self.Title           = title
        self.Amount          = amnt
        self.Type            = typ
        self.Organization_id = orgId



class Transfers(Base):
    __tablename__ = 'Transfers'

    Animal_id           = Column(Integer, ForeignKey('Animals.Animal_id'), nullable = False)
    MeetUp_Location     = Column(String)
    Transportation_type = Column(String)
    Time                = Column(String)
    Transaction_id      = Column(Integer,primary_key=True, autoincrement = True)
    Transfer_to         = Column(Integer, ForeignKey('Organization.Organization_id'), nullable = False)
    Status              = Column(String)

    def __init__(self, aId, loc, trans, time, oId, status):
        self.Animal_id           = aId
        self.MeetUp_Location     = loc
        self.Transportation_type = trans
        self.Time                = time
        self.Transfer_to         = oId
        self.Status              = status

class Adoptions(Base):
    __tablename__ = 'Adoptions'

    Animal_id  = Column(Integer, ForeignKey('Animals.Animal_id'), primary_key=True, nullable = False)
    Adopter_id = Column(Integer, ForeignKey('Adopter.Adopter_id'), primary_key=True, nullable = False)
    Status     = Column(String)

    def __init__ (self, aId, uId, status):
        self.Animal_id  = aId
        self.Adopter_id = uId
        self.Status     = status
