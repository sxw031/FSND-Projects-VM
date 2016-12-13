import os
import sys

# handly for mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# import declarative base which we will use in the configuration and class code.
from sqlalchemy.ext.declarative import declarative_base

# in order to create foreign key relationship, also used in mapper
from sqlalchemy.orm import relationship

# import creat_engine class
from sqlalchemy import create_engine

# make an instance of the declarative_base class we just imported and call it Base, for short.
Base = declarative_base()


class Restaurant(Base):
	__tablename__ = 'restaurant'

	id = Column(Integer, primary_key = True)

	name = Column(String(250), nullable = False)	

class MenuItem(Base):

	__tablename__ = 'menu_item'

	# each restaurant, each menu item needs to have a name, nullable = False make sure that no one can create a manu item without a name.
	name = Column(String(80),nullable = False)
	# create id for each menu item which is set to the primary key
	id = Column(Integer, primary_key = True)

	# create variables and set them to strings
	description = Column(String(250))
	price = Column(String(8))
	course = Column(String(250))

	# this will create the foreign key relationship between my menu item class and my restaurant class.
	# retrieve the ID number whenever I ask for restauran_id
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
		# Return object data in easily serializeable format
		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'price': self.price,
			'course': self.course, 
		}

#######insert at end of file##########

# we create an instance of our create_engine class and point to the database we will use.
engine = create_engine('sqlite:///restaurantmenu.db')

# it goes into the database and adds the classes we will soon create as new tables in our database.
Base.metadata.create_all(engine)


