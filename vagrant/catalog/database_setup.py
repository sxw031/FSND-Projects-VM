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

	@property
	def serialize(self):
		"""return object data in easily serializable format"""
		return {
			'id':self.id,
			'name': self.name,
		}


class CategoryItems(Base):

	__tablename__ = 'category_item'

	id = Column(Integer,primary_key = True)
	name = Column(String(80), nullable = False)
	description = Column(String(250), nullable = False)

	category_id = Column(Integer, ForeignKey('category.id'))

	category = relationship(Category)

	@property
	def serialize(self):
		"""return object data in easily serializable format"""
		return {
			'id': self.id,
			'description': self.description,
			'name': self.name,
		}

####  insert at the end of file ####

engine = create_engine('sqlite:///catelogitems.db')

Base.metadata.create_all(engine)
 