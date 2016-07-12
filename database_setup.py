from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_schema import Base, Category


# Database Session Variable Initialization
engine = create_engine('postgresql://catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Initialization Of Category Types
categories = ['Appliances', 'Auto', 'Baby', 'Clothing', 'Electronics', 
             'Fitness', 'Food', 'Health', 'Home', 
             'Jewlery', 'Music', 'Outdoor', 'Footwear', 'Tools', 
             'Toys', 'Miscellaneous']

for category in categories:
    category_name = Category(name=category)
    session.add(category_name)
    session.commit()

# Database Category Initialization Completion Message
print("Successfully Added Category Names To catalog.db Database!")