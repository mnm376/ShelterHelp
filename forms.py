from __future__ import print_function
import sys
from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField, SelectField, validators, IntegerField
from models import *

#this file will be hosting all forms regarding our web application


#Form for registration 
#For now assume they are an adoptor with no Organization_id
class OrganizationSignupForm(Form):
    name         = StringField('Organization name',[validators.DataRequired(message='Organization name required')])
    username     = StringField('Organization username',[validators.DataRequired(message='Username required')])
    password     = PasswordField('Password',[validators.DataRequired(message='Password required')])
    location     = StringField('Location',[validators.DataRequired(message='Location required')])
    phone_number = StringField('Phone Number',[validators.DataRequired(message='Phone number required')])
    capacity     = IntegerField('Animal Capacity Integer',[validators.DataRequired(message='Animal capacity description required')])
    submit       = SubmitField('Register Organization')

    def checkUnique(self, potUsername):
        query = db.session.query(Organization)
        orgs = query.all()
        for o in orgs:
            if o.Username == potUsername:
                return False
        return True

class EmployeeSignupForm(Form):
    organization_id = SelectField(u'Select Organization', choices=[], coerce=int)
    username     = StringField('Employee Username',[validators.DataRequired(message='Username required')])
    password     = PasswordField('Password',[validators.DataRequired(message='Password required')])
    submit       = SubmitField('Register Employee')

    def checkUnique(self, potUsername):
        query = db.session.query(Employee)
        emps = query.all()
        for e in emps:
            if e.Username == potUsername:
                return False
        return True


class UserSignupForm(Form):
    username    = StringField('Username',[validators.DataRequired(message='Username required')])
    password    = PasswordField('Password',[validators.DataRequired(message='Password required')])
    personality = StringField('Describe what animal personality types you like')
    space       = StringField('Describe the type of space you have (apt./house)')
    age_min     = IntegerField('What is minimum age of an animal you would be interested in?')
    age_max     = IntegerField('What is maximum age of an animal you would be interested in?')
    submit      = SubmitField('Register User')

    def checkUnique(self, potUsername):
    	query = db.session.query(Adopter)
    	adopters = query.all()
    	for a in adopters:
    		if a.Username == potUsername:
    			return False
    	return True

    def checkAgeRange(self, age_min, age_max):
        return int(age_min) < int(age_max)

#Form for logging into website
class LoginForm(Form):
	username     = StringField('Username')
	password     = PasswordField('Password')
	submit       = SubmitField('Sign in')


class LoginFormEmployee(Form):
    organization_id = SelectField(u'Select Organization', choices=[], coerce=int)
    username     = StringField('Username')
    password     = PasswordField('Password')
    submit       = SubmitField('Sign in')

    def validateEmp(self, user, passw, org):
        query = db.session.query(Employee)
        emps = query.all()
        for e in emps:
            if ((str((e.Username).strip()) == str(user.strip())) and (str((e.Password).strip()) == str(passw.strip())) and (int(e.Organization_id) == int(org))):
                return True
        return False

class LoginFormUser(Form):
    username     = StringField('Username')
    password     = PasswordField('Password')
    submit       = SubmitField('Sign in')

    def validateUser(self, user, passw):
        query = db.session.query(Adopter)
        users = query.all()
        for u in users:
            if ((str((u.Username).strip()) == str(user.strip())) and (str((u.Password).strip()) == str(passw.strip()))):
                return True
        return False

class TransferAnimalForm(Form):
    organization_id = SelectField(u'Select Organization', choices=[], coerce=int)   
    location = StringField('Meet up location')
    submit = SubmitField('Transfer')

class MoreButton(Form):
    submit = SubmitField('More Info')

class AdoptButton(Form):
    submit = SubmitField('Adopt')

class FavButton(Form):
    submit = SubmitField('Favorite Animal')

class RemoveFavButton(Form):
    submit = SubmitField('Remove')

class NoB(Form):
    submit = SubmitField('No')

class YesB(Form):
    submit = SubmitField('Yes')

class TransferButton(Form):
    submit = SubmitField('Transfer')