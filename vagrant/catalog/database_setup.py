import os, sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship 

from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):

	__tablename__ = 'category'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)

class CategoryItems(Base):

	__tablename__ = 'category_item'

	name = Column(String(80), nullable = False)
	description = Column(String(250), nullable = False)

	id = Column(Integer,primary_key = True)

	category_id = Column(Integer, ForeignKey('category.id'))

	category = relationship(Category)

####  insert at the end of file ####

engine = create_engine('sqlite:///catelogitems.db')

Base.metadata.create_all(engine)
 