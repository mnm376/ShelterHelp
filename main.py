#Import Flask Library
from __future__ import print_function
import sys
import time
from flask import Flask, render_template, request, session, url_for, redirect, flash
#from models import db
from models import *
from forms import *
#from forms import SignupForm, LoginForm

#Initialize the app from Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/ShelterHelp'
db.init_app(app)

#This is a placeholder for the session variable org id.
#For now pretend that org 1 is logged in
sessionOrganization = 1


#Define a route to root of application function
@app.route('/home')
@app.route('/')
def index():
	session.clear() 
	return render_template('index.html')

@app.route('/logout')
def logout():
	session.pop('user', None)
	session.pop('userType', None)
	return redirect(url_for('index'))

@app.route('/registerType')
def registerType():
	return render_template('registerType.html')


#Define route for login
#This route is hit on logging in for employees
@app.route('/employeeLogin', methods=['GET', 'POST'])
def employeeLogin():
	orgs = [(o.Organization_id, o.Name) for o in db.session.query(Organization).order_by('Name').all()]
	form = LoginFormEmployee(request.form)
	form.organization_id.choices = orgs
	loginError = ''
	if request.method == 'POST':
		postData = request.form
		if form.validateEmp(postData['username'],postData['password'],postData['organization_id']):
			session['user'] = postData['organization_id']
			session['userType'] = 'Employee'
			return redirect(url_for('employeeHome'))
		else:
			loginError = 'Incorrect username or password'
			return render_template('employeeLogin.html', error=loginError, form=form)
	else:
		return render_template('employeeLogin.html', form=form)




#test code for the time being
#WILL BE REMOVED ONCE GETTERS ARE CREATED
#DO NOT USE THIS CODE ANYWHERE ELSE BESIDES ITS CURRENT USAGE
class Animal:
	def __init__(self, Id, Name, Age, Breed):
		self.Id = Id
		self.Name = Name
		self.Age = Age
		self.Breed = Breed


#Test Route
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
	form = TransferButton()
	subquery = db.session.query(Transfers.Animal_id)
	myAnimals = (db.session.query(Animals,Organization)\
		.filter(Animals.Organization_id == Organization.Organization_id)\
		.filter(Organization.Organization_id == session['user'])\
		.filter(~Animals.Animal_id.in_(subquery))
		.all())
	return render_template('transfer.html', animals = myAnimals, form=form)

@app.route('/transferAnimal', methods=['GET', 'POST'])
def transferAnimal():
	orgs = [(o.Organization_id, o.Name) for o in db.session.query(Organization).filter(Organization.Organization_id != session['user']).order_by('Name').all()]
	for orgID,orgName in orgs:
		if orgID == session['user']:
			orgs.remove(orgID)
			break
	form = TransferAnimalForm(request.form)
	form.organization_id.choices = orgs
	postData = request.form
	if request.method == 'POST':
		if str(postData['postID']) == 'preTransfer':
			anID = postData['aID']
		else:
			locationQuery = db.session.query(Organization).filter(Organization.Organization_id == session['user']).first()
			postData['organization_id']
			transfer = Transfers(postData['anID'], postData['location'], 'uber', 'time', postData['organization_id'], 'Pending')
			db.session.add(transfer)
			db.session.commit()
			return redirect(url_for('employeeHome'))
	
	return render_template('transferAnimal.html', form=form, anID = anID)


@app.route('/employeeHome', methods=['GET', 'POST'])
def employeeHome():
# we do a join here to get the org name
	if 'user' not in session or len(session['user']) == 0:
		return redirect(url_for('index'))
	form = YesB()
	form1 = NoB()
	form2 = YesB()
	form3 = YesB()
	form4 = NoB()
	myAnimals = (db.session.query(Animals,Organization)\
		.filter(Animals.Organization_id == Organization.Organization_id)\
		.filter(Organization.Organization_id == session['user'])\
		.all())
	mySupplies = (db.session.query(Supplies)\
		.filter(Supplies.Organization_id == session['user'])\
		.all())
	myInfo = (db.session.query(Organization)\
		.filter(Organization.Organization_id == session['user'])\
		.all())
	transTo_alias = db.aliased(Organization)
	transFrom_alias = db.aliased(Organization)
	myTransfers = (db.session.query(Transfers,Animals,Organization, transTo_alias)\
		.filter(Transfers.Animal_id == Animals.Animal_id)\
		.filter(Transfers.Transfer_to == transTo_alias.Organization_id)\
		.filter(Animals.Organization_id == Organization.Organization_id)\
		.filter(transTo_alias.Organization_id == session['user'])\
		.filter(Transfers.Status == 'Pending')
		.all())
	incomingTransfers = (db.session.query(Transfers,Animals,Organization, transFrom_alias)\
		.filter(Transfers.Animal_id == Animals.Animal_id)\
		.filter(Transfers.Transfer_to == transFrom_alias.Organization_id)\
		.filter(Animals.Organization_id == Organization.Organization_id)\
		.filter(Organization.Organization_id == session['user'])\
		.filter(Transfers.Status == 'Approved')
		.all())
	adoptions = (db.session.query(Adoptions,Animals,Organization,Adopter)\
		.filter(Adoptions.Animal_id == Animals.Animal_id)\
		.filter(Adoptions.Adopter_id == Adopter.Adopter_id)\
		.filter(Animals.Organization_id == Organization.Organization_id)\
		.filter(Organization.Organization_id == session['user'])\
		.filter(Adoptions.Status == 'Requested')
		.all())
	if request.method == 'POST':
		postD = request.form
		if postD['postID'] == 'Incoming':
			if postD['decision'] == 'Yes':
				changeStatus = db.session.query(Transfers).filter(Transfers.Transaction_id == postD['transID']).first()
				changeStatus.Status = 'Approved'
				db.session.commit()
				return redirect(url_for('employeeHome'))
			else:
				changeStatus = db.session.query(Transfers).filter(Transfers.Transaction_id == postD['transID']).first()
				db.session.delete(changeStatus)
				db.session.commit()
				return redirect(url_for('employeeHome'))
		elif postD['postID'] == 'Outgoing':
			statusApproved = db.session.query(Transfers).filter(Transfers.Transaction_id == postD['transID']).first()
			statusApproved.Status = 'Completed'
			changeAnimalHome = db.session.query(Animals).filter(Animals.Animal_id == postD['animalID']).first()
			changeAnimalHome.Organization_id = postD['orgToID']
			db.session.commit()
			return redirect(url_for('employeeHome'))
		else:
			if postD['decision'] == 'Yes':
				changeStatusAdopt = db.session.query(Adoptions).filter(Adoptions.Adopter_id == postD['adoptID']).filter(Adoptions.Animal_id == postD['animID']).first()
				changeStatusAdopt.Status = 'Approved'
				db.session.commit()
				return redirect(url_for('employeeHome'))
			else:
				changeStatusAdopt = db.session.query(Adoptions).filter(Adoptions.Adopter_id == postD['adoptID']).filter(Adoptions.Animal_id == postD['animID']).first()
				db.session.delete(changeStatusAdopt)
				db.session.commit()
				return redirect(url_for('employeeHome'))
	return render_template('employeeHome.html', myAnimals = myAnimals, mySupplies=mySupplies, myInfo=myInfo, myTransfers=myTransfers, incoming = incomingTransfers,adoptions=adoptions, form=form, form1=form1, form2=form2, form3=form3, form4=form4)

@app.route('/stats')
def stats():
	aList = []
	myOrganizations = (db.session.query(Organization)\
		.all())
	return render_template('stats.html', data = myOrganizations)

@app.route('/adoptAnimal',methods=['GET', 'POST'])
def adoptAnimal():
	animal = []
	form = AdoptButton()
	form1 = FavButton()
	if request.method == 'POST':
		postData = request.form
		if postData['postID'] == 'MI':
			a_id = postData['aID']
			o_id = postData['oID']
			user = db.session.query(Adopter).filter_by(Username = session['user']).first()
			query = db.session.query(Animals)
			query2 = db.session.query(Organization).filter_by(Organization_id = o_id).first()
			animals = query.all()
			for a in animals:
				if int(a.Animal_id) == int(a_id):
					animal = a
			return render_template('adoptAnimal.html', animal = animal, orgname = query2.Name, user=user, form=form, form1=form1)
		elif postData['postID'] == 'Adopt':
			an_id = postData['anID']
			o_id = postData['oID']
			ad_id = postData['adID']
			adoption = Adoptions(an_id,ad_id,'Requested')
			db.session.add(adoption)
			db.session.commit()
			return redirect(url_for('adoptAnimalMessage'))
		else:
			an_id = postData['anID']
			o_id = postData['oID']
			ad_id = postData['adID']
			fav = Favorites(an_id,ad_id)
			db.session.add(fav)
			db.session.commit()
			return redirect(url_for('userFavorites'))
	else:
		return render_template('adoptAnimal.html')

#Test for adding a transfer button to a table, linking it 
# to that table's row and having it do something.
#DONT DELETE
#@app.route('/transferFunc', methods=['POST'])
#def handleTransfer():
#	#query = db.session.query(Animals)
#	db.session.add(
#		Supplies (
#			"Noticable String",
#			"Purina Puppy Chow",
#			"30 pounds",
#			"Puppy food",
#			"1"
#		)
#	)
#
#	db.session.commit()
#
#	return redirect('animals')

@app.route('/loginType')
def loginType():
	return render_template('loginType.html')

@app.route('/adoptAnimalMessage')
def adoptAnimalMessage():
	return render_template('adoptAnimalMessage.html')

@app.route('/userLogin',methods=['GET', 'POST'])
def userLogin():
	form = LoginFormUser()
	loginError = ''
	if request.method == 'POST':
		postData = request.form
		if form.validateUser(postData['username'],postData['password']):
			session['user'] = str(postData['username'])
			session['userType'] = 'Adopter'
			return redirect(url_for('userHome'))
		else:
			loginError = 'Incorrect username or password'
			return render_template('userLogin.html', error=loginError, form=form)
	else:
		return render_template('userLogin.html', form=form)


@app.route('/recommendedAnimals', methods=['GET'])
def recommendedAnimals():
		form = MoreButton()
		query = db.session.query(Adopter, Animals).filter(Adopter.Username == session['user'])\
		.filter(func.lower((Animals.Temperament)) == func.lower(Adopter.Personality))\
		.filter(Adopter.Age_min <= Animals.Age).filter(Animals.Age <= Adopter.Age_max)
		allAnimals = query.all()
		return render_template('recommendedAnimals.html', animals = allAnimals, form=form)






@app.route('/userHome')
def userHome():
	if 'user' not in session or len(session['user']) == 0:
		return redirect(url_for('index'))
	form = MoreButton()
	if 'user' in session:
		subquery = db.session.query(Adoptions.Animal_id)
		query = (db.session.query(Animals)\
			.filter(~Animals.Animal_id.in_(subquery)))
		allAnimals = query.all()
		return render_template('cards.html', animals = allAnimals, form=form)
	else:
		return redirect(url_for('userLogin'))


@app.route('/userAdoptions', methods=['GET','POST'])
def userAdoptions():
	form = YesB()
	myAdoptions = (db.session.query(Adopter,Animals,Organization,Adoptions)\
		.filter(Adoptions.Animal_id == Animals.Animal_id)\
		.filter(Animals.Organization_id == Organization.Organization_id)\
		.filter(Adopter.Adopter_id == Adoptions.Adopter_id)\
		.filter(Adoptions.Status != 'Completed')\
		.filter(Adopter.Username == session['user'])\
		.all())
	if request.method == 'POST':
		postData = request.form
		changeAdoption = db.session.query(Adoptions).filter(Adoptions.Adopter_id == postData['adoptID']).filter(Adoptions.Animal_id == postData['animalID']).first()
		db.session.delete(changeAdoption)
		remTrans = db.session.query(Transfers).filter(Transfers.Animal_id == postData['animalID']).all()
		if len(remTrans) >= 1:
			db.session.delete(remTrans)
		remFavs = db.session.query(Favorites).filter(Favorites.Animal_id == postData['animalID']).all()
		if len(remFavs) >= 1:
			db.session.delete(remFavs)
		remAnimal = db.session.query(Animals).filter(Animals.Animal_id == postData['animalID']).first()
		db.session.delete(remAnimal)
		db.session.commit()
		return redirect(url_for('userAdoptions'))
	return render_template('userAdoptions.html',adoptions=myAdoptions,form=form)

@app.route('/userFavorites',methods=['GET', 'POST'])
def userFavorites():
	myFavorites = (db.session.query(Adopter,Animals,Organization,Favorites)\
		.filter(Favorites.Animal_id == Animals.Animal_id)\
		.filter(Animals.Organization_id == Organization.Organization_id)\
		.filter(Adopter.Adopter_id == Favorites.Adopter_id)\
		.filter(Adopter.Username == session['user'])\
		.all())
	form = RemoveFavButton()
	if request.method == 'POST':
		postData = request.form
		anID = postData['anID']
		adID = postData['adID']
		fav = (db.session.query(Favorites)\
		.filter(Favorites.Animal_id == anID)\
		.filter(Favorites.Adopter_id == adID)\
		.first())
		db.session.delete(fav)
		db.session.commit()
		return redirect(url_for('userFavorites'))
	return render_template('userFavorites.html',favorites=myFavorites, form=form)

@app.route('/organizationLogin')
def organizationLogin():
	return render_template('organizationLogin.html')


@app.route('/employeeRegister',methods=['GET', 'POST'])
def employeeRegister():
	orgs = [(o.Organization_id, o.Name) for o in db.session.query(Organization).order_by('Name').all()]
	form = EmployeeSignupForm(request.form)
	form.organization_id.choices = orgs
	empError = ''
	if request.method == 'POST' and form.validate():
		postData = request.form
		empUsername = postData['username']
		if not form.checkUnique(empUsername):
			empError = 'This employee already exists!'
		else:
			employee=Employee(empUsername,postData['password'],postData['organization_id'])
			db.session.add(employee)
			db.session.commit()
			session['user'] = postData['organization_id']
			session['userType'] = 'Employee'
			return redirect(url_for('employeeHome'))
	return render_template('employeeRegister.html', error=empError, form=form)


@app.route('/organizationRegister',methods=['GET', 'POST'])
def organizationRegister():
	form = OrganizationSignupForm()
	orgError = ''
	if request.method == 'POST' and form.validate():
		postData = request.form
		orgUser = postData['username']
		if not form.checkUnique(orgUser):
			orgError = 'This organization already exists!'
		else:
			org = Organization(postData['location'],postData['phone_number'],postData['capacity'],postData['username'],postData['name'],postData['password'])
			db.session.add(org)
			db.session.commit()
			return redirect(url_for('employeeRegister'))
	return render_template('organizationRegister.html', error=orgError, form=form)

@app.route('/userRegister',methods=['GET', 'POST'])
def userRegister():
	form = UserSignupForm()
	Usererror = ''
	if request.method == 'POST' and form.validate():
		postData = request.form
		username = postData['username']
		if not form.checkUnique(username):
			Usererror = 'Username already exists!'
			return render_template('userRegister.html', error=Usererror, form=form)
		if not form.checkAgeRange(postData['age_min'], postData['age_max']): 
			Usererror = 'Minimum age must be less than Maximum age'
			return render_template('userRegister.html', error=Usererror, form=form)
		else:
			user = Adopter(username,postData['password'],postData['personality'],postData['space'],postData['age_min'], postData['age_max'])
			db.session.add(user)
			db.session.commit()
			Usererror = ''
			session['user'] = username
			session['userType'] = 'User'
			return redirect(url_for('userHome'))
	return render_template('userRegister.html', error=Usererror, form=form)

app.secret_key = 'YxoCSYSLOJ/UpoFapq0V9Fy2M6L5pHVPqDQKNAYuoD4M2kwqmo5xVqIGLIBvpaMy3/8kMHVyh36aguTLjM8V6+VF6IYDHHEPSO1TZR8DdBz3WocfQVcYLH7pWQpdvitSnNMFBlJrO8sST0UbcJBBTYzWBrPot1e4MtkMovFVc/vFVx6zkBTaZGT7qGpq7a8o+BGoRymYjNtwaJZDLXAa5M5ycAQn50/u9L3'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
