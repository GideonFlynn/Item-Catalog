import random
import string

from itsdangerous import BadSignature, Serializer, SignatureExpired
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, ForeignKey, Integer, \
    NVARCHAR, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
secret_key = ''.join(random.choice(
        string.ascii_uppercase +
        string.digits)
                     for x in range(32))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(NVARCHAR, index=True)
    email = Column(NVARCHAR, index=True)
    picture = Column(NVARCHAR)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id

    @property
    def serialize(self):
        return {
            'name':        self.name,
            'picture':     self.picture,
            'description': self.description
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR, nullable=False)
    description = Column(NVARCHAR, nullable=False)
    up_file = Column(NVARCHAR)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object in easily serializable format"""
        return {
            'name':           self.name,
            'description':    self.description,
            'image filename': self.up_file,
            'unique id':      self.id
        }


class Manufacturer(Base):
    __tablename__ = 'manufacturer'
    name = Column(NVARCHAR, primary_key=True, index=True)
    description = Column(NVARCHAR, nullable=False)
    up_file = Column(NVARCHAR)
    id = Column(Integer, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object in easily serializable format"""
        return {
            'name and unique id': self.name,
            'description':        self.description,
            'image filename':     self.up_file,
        }


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR, nullable=False, index=True)
    description = Column(NVARCHAR, nullable=False)
    up_file = Column(NVARCHAR)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object in easily serializable format"""
        return {
            'unique id':      self.id,
            'name':           self.name,
            'description':    self.description,
            'image filename': self.up_file,
        }


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR, nullable=False, index=True)
    description = Column(NVARCHAR, nullable=False)
    category = Column(Integer, ForeignKey('category.id'), nullable=False)
    ingredients = Column(NVARCHAR)
    up_file = Column(NVARCHAR)
    m_id = Column(Integer, ForeignKey('manufacturer.id'), nullable=False)
    s_id = Column(Integer, ForeignKey('shop.id'), nullable=False)
    # Make relationships so the tables know each other or something like that.
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    Category_id = relationship(Category)
    Manufacturer_id = relationship(Manufacturer)
    Shop_id = relationship(Shop)

    @property
    def serialize(self):
        """Return object in easily serializable format"""
        return {
            'name':            self.name,
            'category':        self.category,
            'description':     self.description,
            'image filename':  self.up_file,
            'shop id':         self.s_id,
            'manufacturer id': self.m_id,
            'unique id':       self.id,
        }


# Make the database and call it something
engine = create_engine('sqlite:///models.db')

Base.metadata.create_all(engine)
