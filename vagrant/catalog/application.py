from flask import Flask, render_template
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
def CategoryShow():
    category = session.query(Category).all()
    return render_template('main.html', category = category)


@app.route('/catelog/<int:category_id>/new')
def newCategory(category_id):
	return "Page to create a new category. Task complete"

@app.route('/catelog/<int:category_id>/edit')
def editCategory(category_id):
	return "Page to rename a category. Task complete"

@app.route('/catelog/<int:category_id>/delete')
def deleteCategory(category_id):
	return "Page to delete a category. Task complete"

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