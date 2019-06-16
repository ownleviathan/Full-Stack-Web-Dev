from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User

engine = create_engine('postgresql://catalog:password@localhost/catalog')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(name="Edwin Perez", email="edwinperez@gmail.com")
session.add(User1)
session.commit()

myFirstCategory1 = Category(user_id=1, name='Soccer')

session.add(myFirstCategory1)
session.commit()

categoryItem = CategoryItem(name="Two shinguards", description="Shinguards",
                            price="$10.50", category=myFirstCategory1)
session.add(categoryItem)
session.commit()


myFirstCategory2 = Category(user_id=1, name='Basketball')

session.add(myFirstCategory2)
session.commit()

categoryItem1 = CategoryItem(name="Basketall Ball", description="Adidas ball",
                             price="$7.50", category=myFirstCategory2)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(name="Jersey", description="XL Size",
                             price="$15.00", category=myFirstCategory2)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Soccer Cleats", description="Cleast Adidas",
                             price="$20.00", category=myFirstCategory2)
session.add(categoryItem3)
session.commit()

myFirstCategory3 = Category(user_id=1, name='Baseball')

session.add(myFirstCategory3)
session.commit()

myFirstCategory4 = Category(user_id=1, name='Frisbee')

session.add(myFirstCategory4)
session.commit()

myFirstCategory5 = Category(user_id=1, name='Snowboarding')

session.add(myFirstCategory5)
session.commit()

myFirstCategory6 = Category(user_id=1, name='Rock Climbing')

session.add(myFirstCategory6)
session.commit()

myFirstCategory7 = Category(user_id=1, name='Foosball')

session.add(myFirstCategory7)
session.commit()

myFirstCategory8 = Category(user_id=1, name='Skating')

session.add(myFirstCategory8)
session.commit()

myFirstCategory9 = Category(user_id=1, name='Hockey')

session.add(myFirstCategory9)
session.commit()

print("added Categories and Items for Soccer!")
