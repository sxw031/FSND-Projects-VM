from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItems, User

# imports for Google Authentication login
# login_session is a dictionary
from flask import session as login_session
import random, string

# import for Gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']
APPLICATION_NAME = "Fun Catalog Application"

engine = create_engine('sqlite:///catalogitemswithuser.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a state token to prevent request foregry.
# Store it in the session for later validation
@app.route('/login')
@app.route('/catalog/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	# return "The current session state is %s" % login_session['state']
	return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain authorization code	
	code = request.data

	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)

	# Submit request, parse request - Python3 compatible
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])

	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
	    	json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_access_token = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
	login_session['credentials'] = access_token
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	# see if user exists, if it doesn't, make a new one.
	user_id = getUserID(login_session['email'])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print "done!"
	return output
 
# The User helper function
def createUser(login_session):
	newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email = login_session['email']).one()
	return user.id

def getUserInfo(user_id):
	user = session.query(User).filter_by(id = user_id).one()
	return user

def getUserID(email):
	try:
		user = session.query(User).filter_by(email = email).one()
		return user.id
	except:
		return None   

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    # print 'In gdisconnect access token is %s', access_token
    # print 'User name is: ' 
    # print login_session['username']
    if access_token is None:
 	# print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # print 'result is '
    # print result
    if result['status'] == '200':
    # reset the user's session.
    	del login_session['access_token']
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']

    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    else:
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response

# Making a API Endpoint (GET request), JSON APIs to view category information

@app.route('/catalog/users/JSON')
def userJSON():
	users = session.query(User).all()
	return jsonify(User=[i.serialize for i in users])

@app.route('/catalog/JSON')
def categoryJSON():
	catalog = session.query(Category).all()
	return jsonify(Category=[i.serialize for i in catalog])

@app.route('/catalog/<int:category_id>/items/JSON')
def categoryItemsJSON(category_id):
	category = session.query(Category).filter_by(id = category_id).one()
	items = session.query(CategoryItems).filter_by(category_id = category_id).all()
	return jsonify(CategoryItems=[i.serialize for i in items])

# Show all categories
@app.route('/')
@app.route('/catalog')
def categoryShow():
    """Route for landing page, the main page"""
    category = session.query(Category).order_by(asc(Category.name))  
    if 'username' not in login_session and 'user_id' != login_session['user_id']:
    	return render_template('publicmain.html', category = category)
    else:
    	return render_template('main.html', category = category)

# Route for category modification
@app.route('/catalog/new', methods=['GET','POST'])
def newCategory():
	"""Page to create a new category."""
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newCat = Category(name = request.form['name'], user_id=login_session['user_id'])
		session.add(newCat)
		session.commit()
		flash("New category %s is added!" % newCat.name)
		return redirect(url_for('categoryShow'))
	else:
		return render_template('newcategory.html')


@app.route('/catalog/<int:category_id>/edit', methods=['GET','POST'])
def editCategory(category_id):
	"""Page to edit the category name."""
	editedCategory = session.query(Category).filter_by(id = category_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if editedCategory.user_id != login_session['user_id']:
		return "<script>function myFunction() { alert('You are not authrorized to edit this category. Please edit the category which created by yourself. If there is none, you can add a new category to edit.');window.location = '/catalog/%s'}</script><body onload='myFunction()''>" % category_id	
	if request.method == 'POST':
		if request.form['name']:
			oldname = editedCategory.name
			editedCategory.name = request.form['name']
			session.add(editedCategory)
			session.commit()
			flash("%s is changed to %s!" % (oldname, editedCategory.name))
			return redirect(url_for('categoryShow'))
	else:
		return render_template('editcategory.html', category_id = category_id, category = editedCategory)

@app.route('/catalog/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):
	"""Page to delete a category. Task complete"""
	deletedCategory = session.query(Category).filter_by(id = category_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if deletedCategory.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authrorized to delete the category, which is created by other owner.');window.location = '/catalog/%s';}</script><body onload='myFunction()''>" % category_id
	if request.method == 'POST':
		session.delete(deletedCategory)
		session.commit()
		flash("%s category is deleted!" % deletedCategory.name)
		return redirect(url_for('categoryShow'))
	else:
		return render_template('deletecategory.html', category_id = category_id, category = deletedCategory)

# Route for Items modification
@app.route('/catalog/<int:category_id>')
def itemPage(category_id):
	"""Route for category display with its item lists"""
	category = session.query(Category).order_by(asc(Category.name))
	# creator = getUserInfo(category.user_id)
	items = session.query(CategoryItems).filter_by(category_id = category_id).all()
	if 'username' not in login_session and 'user_id' != login_session['user_id']:
		return render_template('publicitempage.html', category = category, category_id=category_id, items = items) # creator = creator
	else:
		return render_template('itempage.html', category = category, category_id = category_id, items = items) # creator = creator

@app.route('/catalog/<int:category_id>/new', methods = ['GET','POST'])
def newItem(category_id):
	"""Page to add a new item to the specific category"""
	category = session.query(Category).filter_by(id = category_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if category.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authrorized to add a item. Please create your own catalog in order to add.');window.location = '/catalog/%s'}</script><body onload='myFunction()''>"	% category_id
	if request.method == 'POST':
		newItem = CategoryItems(name = request.form['name'], description = request.form['description'],category_id=category_id, user_id=category.user_id)
		session.add(newItem)
		session.commit()
		flash("'%s' is added to %s category!" % (newItem.name, category.name))
		return redirect(url_for('itemPage', category_id=category_id))
	else:
		return render_template('newitem.html', category_id=category_id)

@app.route('/catalog/<int:category_id>/<int:item_id>/edit', methods=['GET','POST'])
def editItem(category_id, item_id):
	category = session.query(Category).filter_by(id=category_id).one()
	editedItem = session.query(CategoryItems).filter_by(id = item_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if category.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authrorized to edit this item. Please create your own catalog in order to edit.');window.location = '/catalog/%s/%s'}</script><body onload='myFunction()''>" % (category_id, item_id)
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		session.add(editedItem)
		session.commit()
		flash("Item Successfuly Edited!")
		return redirect(url_for('itemPage', category_id=category_id))
	else:
		return render_template('edititem.html', category_id = category_id, item_id = item_id, item = editedItem)

@app.route('/catalog/<int:category_id>/<int:item_id>/delete', methods=['GET','POST'])
def deleteItem(category_id, item_id):
	"""Page to delete a item."""
	category = session.query(Category).filter_by(id=category_id).one()
	deletedItem = session.query(CategoryItems).filter_by(id = item_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if category.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authrorized to delete this item. Please create your own catalog in order to delete.');window.location = '/catalog/%s/<%s'}</script><body onload='myFunction()''>" % (category_id, item_id)
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("%s is deleted from category %s!" % (deletedItem.name, category.name))
		return redirect(url_for('itemPage', category_id=category_id))
	else:
		return render_template('deleteitem.html', category_id = category_id, item_id = item_id, item = deletedItem)

@app.route('/catalog/<int:category_id>/<int:item_id>/')
def itemDetail(category_id, item_id):
	category = session.query(Category).order_by(asc(Category.name))
	item = session.query(CategoryItems).filter_by(id = item_id).one()
	if 'username' not in login_session and 'username' != login_session['user_id']:
		return render_template('publicitemdetail.html',category = category, category_id = category_id, item = item)
	return render_template('itemdetail.html', category = category, category_id = category_id, item = item)

@app.route('/catalog/<int:category_id>/<int:item_id>/usage/edit', methods=['GET','POST'])
def detailEdit(category_id, item_id):
	editedItem = session.query(CategoryItems).filter_by(id = item_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if editedItem.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authrorized to edit this item. Please create your own catalog in order to edit.');window.location = '/catalog/%s/%s'}</script><body onload='myFunction()''>" % (category_id, item_id)
	if request.method == 'POST':
		if request.form['usage']:
			editedItem.name = request.form['usage']
		session.add(editedItem)
		session.commit()
		flash("%s usage has been successfully modified" % editedItem.name)
		return redirect(url_for('itemDetail', category_id=category_id, item_id=item_id))
	else:
		return render_template('editdetail.html', category_id = category_id, item_id = item_id, item = editedItem)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8888)