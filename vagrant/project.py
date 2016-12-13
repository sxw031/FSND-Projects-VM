from flask import Flask, render_template, url_for, request, redirect, flash, jsonify # first we import the Flask class from the flask library
app = Flask(__name__) # and we create a object/instance for this Flask class passing with one parameter "__name__", which "name" is the name of the running application.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()

#Making an API Endpoint(GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItem=[i.serialize for i in items])

# Another JSON Endpoint 
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)

# decorator is the function starts with "@", it wraps the function inside the route function that flask has already created. So the function defined inside the decotors will be called if the browser into that route
@app.route('/')
@app.route('/restaurants/')
def restaurantMenu():
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
    	newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
    	session.add(newItem)
    	session.commit()
    	flash("new menu item created!")
    	return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
    	return render_template('newmenuitem.html', restaurant_id = restaurant_id)
    #return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
    	    editedItem.name = request.form['name']
    	session.add(editedItem)
    	session.commit()
    	flash("menu item changed!")
    	return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
    	return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=editedItem)
    #return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("menu item deleted!")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', item = itemToDelete) 

    # return "page to delete a menu item. Task 3 complete!"

# The application run by the Python interpreter gets a name variable set to __main__ whereas all the other imported Python files get a double underscore name underscore variable set to the actual name of the Python file. 
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	# '0.0.0.0' tell vagrants server to listening all the IP addresses
	app.run(host = '0.0.0.0', port = 8888)
