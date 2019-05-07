from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

myFirstCategory = Category(name = 'Soccer')

session.add(myFirstCategory)
session.commit()

categoryItem = CategoryItem(name="Soccer guayos", description="Adidas ball",
                     price="$7.50", category=myFirstCategory)
session.add(categoryItem)
session.commit()

