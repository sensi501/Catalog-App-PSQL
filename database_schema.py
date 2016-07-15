from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True) 
    name = Column(String(250), nullable=False) 
    email = Column(String(250), nullable=False) 
    picture = Column(String(250)) 

    
    
class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    
    
class Item(Base):
    __tablename__ = 'item'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
        
    @property
    def serialize(self):
        return {
            'description': self.description,
            'name': self.name,
            'id': self.id,
        }
    
    
engine = create_engine('postgresql://catalog:Catalog1@localhost/catalog')

Base.metadata.create_all(engine)
