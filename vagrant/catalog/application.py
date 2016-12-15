from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItems
app = Flask(__name__)


engine = create_engine('sqlite:///catelogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Making a API Endpoint (GET request)
@app.route('/catelog/JSON')
def categoryJSON():
	catelog = session.query(Category).all()
	return jsonify(Category=[i.serialize for i in catelog])

@app.route('/catelog/<int:category_id>/items/JSON')
def categoryItemsJSON(category_id):
	category = session.query(Category).filter_by(id = category_id).one()
	items = session.query(CategoryItems).filter_by(category_id = category_id).all()
	return jsonify(CategoryItems=[i.serialize for i in items])

# Route for landing page, the main page
@app.route('/')
@app.route('/catelog')
def categoryShow():
    category = session.query(Category).all()
    return render_template('main.html', category=category)

# Route for catelog modification
@app.route('/catelog/new', methods=['GET','POST'])
def newCategory():
	"""Page to create a new category."""
	if request.method == 'POST':
		newCat = Category(name = request.form['name'])
		session.add(newCat)
		session.commit()
		flash("%s category is added!" % newCat.name)
		return redirect(url_for('categoryShow'))
	else:
		return render_template('newcategory.html')


@app.route('/catelog/<int:category_id>/edit', methods=['GET','POST'])
def editCategory(category_id):
	editedCategory = session.query(Category).filter_by(id = category_id).one()
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

@app.route('/catelog/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):
	"""Page to delete a category. Task complete"""
	deletedCategory = session.query(Category).filter_by(id = category_id).one()
	if request.method == 'POST':
		session.delete(deletedCategory)
		session.commit()
		flash("%s category is deleted!" % deletedCategory.name)
		return redirect(url_for('categoryShow'))
	else:
		return render_template('deletecategory.html', category_id = category_id, category = deletedCategory)

# Route for Items modification
@app.route('/catelog/<int:category_id>')
def itemPage(category_id):
	category = session.query(Category).all()
	items = session.query(CategoryItems).filter_by(category_id = category_id).all()
	return render_template('itempage.html', category = category, category_id=category_id, items=items)

@app.route('/catelog/<int:category_id>/new', methods = ['GET','POST'])
def newItem(category_id):
	"""Page to add a new item to the specific category"""
	category = session.query(Category).filter_by(id = category_id).one()
	if request.method == 'POST':
		newItem = CategoryItems(name = request.form['name'], description = request.form['description'],category_id=category_id)
		session.add(newItem)
		session.commit()
		flash("'%s' is added to %s category!" % (newItem.name, category.name))
		return redirect(url_for('itemPage', category_id=category_id))
	else:
		return render_template('newitem.html', category_id=category_id)

@app.route('/catelog/<int:category_id>/<int:item_id>/')
def itemDetail(category_id, item_id):
	category = session.query(Category).filter_by(id = category_id).one()
	item = session.query(CategoryItems).filter_by(id = item_id).one()
	return render_template('itemDetail.html', category_id = category_id, item_id = item_id, item = item)

@app.route('/catelog/<int:category_id>/<int:item_id>/usage/edit', methods=['GET','POST'])
def detailEdit(category_id, item_id):
	editedItem = session.query(CategoryItems).filter_by(id = item_id).one()
	if request.method == 'POST':
		if request.form['usage']:
			editedItem.name = request.form['usage']
		session.add(editedItem)
		session.commit()
		flash("%s usage has been successfully modified" % editedItem.name)
		return redirect(url_for('itemDetail', category_id=category_id, item_id=item_id))
	else:
		return render_template('editdetail.html', category_id = category_id, item_id = item_id, item = editedItem)

@app.route('/catelog/<int:category_id>/<int:item_id>/edit', methods=['GET','POST'])
def editItem(category_id, item_id):
	editedItem = session.query(CategoryItems).filter_by(id = item_id).one()
	if request.method == 'POST':
		if request.form['name']:
			oldname = editedItem.name
			editedItem.name = request.form['name']
			editedItem.description = request.form['description']
		session.add(editedItem)
		session.commit()
		flash("%s has been modified to %s!" % (oldname, editedItem.name))
		return redirect(url_for('itemPage', category_id=category_id))
	else:
		return render_template('edititem.html', category_id = category_id, item_id = item_id, item = editedItem)

@app.route('/catelog/<int:category_id>/<int:item_id>/delete', methods=['GET','POST'])
def deleteItem(category_id, item_id):
	"""Page to delete a item."""
	category = session.query(Category).filter_by(id=category_id).one()
	deletedItem = session.query(CategoryItems).filter_by(id = item_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("%s is deleted from category %s!" % (deletedItem.name, category.name))
		return redirect(url_for('itemPage', category_id=category_id))
	else:
		return render_template('deleteitem.html', category_id = category_id, item_id = item_id, item = deletedItem)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8888)