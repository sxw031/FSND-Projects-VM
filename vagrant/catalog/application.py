from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

engine = create_engine('sqlite:///catalogitems.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

# CRUD CREATE
# myFirstCategory = Category(name = 'Snowboarding')
# session.add(myFirstCategory)
# session.commit()
# session.query(Category).all()

# helmet = CategoryItem(name = "Helmet", description = "It is a must have equipment to protect you from injury", category = myFirstCategory)
# session.add(helmet)
# session.commit()
# session.query(CategoryItem).all()

# CRUD READ
session.query(Category).first()
Result = session.query(Category).all()
print Result

cats = session.query(Category).all()
for cat in cats:
	print cat.name

items = session.query(CategoryItem).all()
for item in items:
	print item.name

# CRUD UPDATE
# 1. find entry.
# 2. reset values.
# 3. add to session
# 4. session commit

# find entry
balls = session.query(CategoryItem).filter_by(name='Ball')
for ball in balls:
	print ball.id
	print ball.description
	print ball.category.name
	print "\n"

soccerball = session.query(CategoryItem).filter_by(id = 1).one() # .one() makes sqlalchemy only gives me one object
print soccerball.description

# reset value, add to session and commit
soccerball.description = 'black and white, sometimes it various'
session.add(soccerball)
session.commit()


# CRUD DELETE
# 1. find the entry
# 2. session.delete(entry)
# 4. session.commit()

# socks = session.query(CategoryItem).filter_by(name='Socks').one()
# print socks.description
# session.delete(socks)
# session.commit()







