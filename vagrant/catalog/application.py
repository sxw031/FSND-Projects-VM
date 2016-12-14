from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItems
app = Flask(__name__)


engine = create_engine('sqlite:///catelogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catelog')
def categoryShow():
    category = session.query(Category).all()
    return render_template('main.html', category=category)

@app.route('/catelog/new', methods=['GET','POST'])
def newCategory():
	"""Page to create a new category."""
	if request.method == 'POST':
		newCat = Category(name = request.form['name'])
		session.add(newCat)
		session.commit()
		return redirect(url_for('categoryShow'))
	else:
		return render_template('newcategory.html')


@app.route('/catelog/<int:category_id>/edit', methods=['GET','POST'])
def editCategory(category_id):
	editedCategory = session.query(Category).filter_by(id = category_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedCategory.name = request.form['name']
		session.add(editedCategory)
		session.commit()
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
		return redirect(url_for('categoryShow'))
	else:
		return render_template('deletecategory.html', category_id = category_id, category = deletedCategory)

@app.route('/catelog/<int:catelog_id>/<int:item_id>/new')
def newCategoryItem(category_id, item_id):
	return "Page to add a new item into the category. Task complete"

@app.route('/catelog/<int:catelog_id>/<int:item_id>/edit')
def editCategoryItem(category_id, item_id):
	return "Page to edit an item into the category. Task complete"

@app.route('/catelog/<int:category_id>/<int:item_id>/delete')
def deleteCategoryItem(category_id, item_id):
	return "Page to delete an item. Task complete"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8888)