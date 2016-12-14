from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, CategoryItem

engine = create_engine('sqlite:///catelogitems.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Items for Category1 - Soccer
category1 = Category(name="Soccer")

session.add(category1)
session.commit()

catItem1 = CategoryItem(name="Ball", description="black and white", category=category1)

session.add(catItem1)
session.commit()

catItem2 = CategoryItem(name="Sock", description="beautiful and long", category=category1)

session.add(catItem2)
session.commit()

catItem3 = CategoryItem(name="Shoes", description="specialized design for running on grass", category=category1)

session.add(catItem3)
session.commit()

# Items for Category2 - Basketball

category2 = Category(name="Basketball")

session.add(category2)
session.commit()

catItem1 = CategoryItem(name="Ball", description="orange color with grips for better handling", category=category2)

session.add(catItem1)
session.commit()

catItem2 = CategoryItem(name="Sock", description="comfort and fit for better cushion and feeling", category=category2)

session.add(catItem2)
session.commit()

catItem3 = CategoryItem(name="Shoes", description="specialized design for make movement on different floor, such as jump or stop", category=category2)

session.add(catItem3)
session.commit()

# Items for Category3 - Snowboarding
category3 = Category(name="Snowboarding")

session.add(category3)
session.commit()

catItem1 = CategoryItem(name="Board", description="demension, shape and material matters", category=category3)

session.add(catItem1)
session.commit()

catItem2 = CategoryItem(name="Boots", description="Fit and comfort is very important", category=category3)

session.add(catItem2)
session.commit()

catItem3 = CategoryItem(name="goggle", description="Viewing better and looking better", category=category3)

session.add(catItem3)
session.commit()

# Items for Category4 - Rock Climbing
category4 = Category(name="Rock Climbing")

session.add(category4)
session.commit()

catItem1 = CategoryItem(name="Harness", description="bucket it correctly and tightly, please", category=category4)

session.add(catItem1)
session.commit()

catItem2 = CategoryItem(name="Rope", description="various way to climbing, and always take a company with you", category=category4)

session.add(catItem2)
session.commit()

catItem3 = CategoryItem(name="shoe", description="some people prefer not wearing shoes", category=category4)

session.add(catItem3)
session.commit()

# Items for Category5 - Swimming
category5 = Category(name="Swimming")

session.add(category5)
session.commit()

catItem1 = CategoryItem(name="Suits", description="buy with hi-tech suits if you are affordable", category=category5)

session.add(catItem1)
session.commit()

catItem2 = CategoryItem(name="Goggle", description="viewing nicely under water, another scenery of world", category=category5)

session.add(catItem2)
session.commit()

catItem3 = CategoryItem(name="earplug", description="my must have item, maybe it's not yours", category=category5)

session.add(catItem3)
session.commit()

print "added menu items!"