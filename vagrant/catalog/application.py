from flask import Flask
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
    categories = session.query(Category).all()
    output = ""
    for category in categories:
    	output += category.name
    	output += "</br>"
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8888)