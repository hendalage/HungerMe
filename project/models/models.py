import uuid
import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import BigInteger, Column, Float, Date, DateTime, ForeignKey, Integer, SmallInteger, String, Time, \
    create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
# metadata = Base.metadata
# engine = create_engine('postgresql://postgres:1234@localhost/hm1')
# Base.metadata.create_all(engine)
# db_session = scoped_session(sessionmaker())
# Session = sessionmaker()
# session = Session.configure(bind=engine)
# Base.query = session.query_property()

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost/hm1'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = scoped_session(Session)
Base = declarative_base()
# Note the line below
Base.query = session.query_property()



class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    address = Column(String(255))
    contact_no = Column(String(15))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    @staticmethod
    def get_schema():
        """
        method to get schema
        """
        schema = {
            "type": "object",
            "required": ["name", "address"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Restaurant name",
            "type": "string"
        }
        props["address"] = {
            "description": "Restaurant address",
            "type": "string"
        }
        return schema

    def serialize(self):
        role = {
            "name": self.name,
            "address": self.address,
            "contact_no": self.contact_no,
            "created_at": self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
            "updated_at": self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z")
        }
        return role


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(ForeignKey('restaurant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                           index=True)
    name = Column(String(255), nullable=False)
    nic = Column(String(15), nullable=False)
    salary = Column(Integer, nullable=False)
    contact_no = Column(String(15), nullable=False)
    status = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    restaurant = relationship('Restaurant')


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(ForeignKey('restaurant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    qty = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    restaurant = relationship('Restaurant')

    @staticmethod
    def get_schema():
        """
        method to get schema
        """
        schema = {
            "type": "object",
            "required": ["name"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Item name",
            "type": "string"
        }
        props["description"] = {
            "description": "Item description",
            "type": "string"
        }
        props["restaurant_id"] = {
            "description": "Restaurant id",
            "type": "string"
        }
        return schema

    def serialize(self):
        role = {
            "name": self.name,
            "description": self.description,
            "qty": self.qty,
            "restaurant_name": self.restaurant.name,
            "restaurant_address": self.restaurant.address,
            "restaurant_contact_no": self.restaurant.contact_no
        }
        return role


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    restaurant_id = Column(ForeignKey('restaurant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    price = Column(Float, nullable=True)
    status = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    restaurant = relationship('Restaurant')

    @staticmethod
    def get_schema():
        """
        method to get schema
        """
        schema = {
            "type": "object",
            "required": ["name", "restaurant_id"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Menu name",
            "type": "string"
        }
        props["description"] = {
            "description": "Menu description",
            "type": "string"
        }
        props["restaurant_id"] = {
            "description": "Restaurant id",
            "type": "string"
        }
        return schema

    def serialize(self):
        role = {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "restaurant_name": self.restaurant.name,
            "restaurant_address": self.restaurant.address,
            "restaurant_contact_no": self.restaurant.contact_no,
            "restaurant_id": str(self.restaurant_id)
        }
        return role


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    email = Column(String(255), nullable=False)
    contact_no = Column(String(15))
    password = Column(String(255))
    address = Column(String(255))
    type = Column(SmallInteger, nullable=False)
    status = Column(SmallInteger, nullable=False)
    restaurant_id = Column(ForeignKey('restaurant.id', ondelete='CASCADE', onupdate='CASCADE'))
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    restaurant = relationship('Restaurant')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    restaurant_id = Column(ForeignKey('restaurant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    menu_id = Column(ForeignKey('menu.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    status = Column(SmallInteger, nullable=False)
    total = Column(Integer)
    qty = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    menu = relationship('Menu')
    restaurant = relationship('Restaurant')
    user = relationship('User')

    @staticmethod
    def get_schema():
        """
        method to get schema
        """
        schema = {
            "type": "object",
            "required": ["user_id", "restaurant_id"]
        }
        props = schema["properties"] = {}
        props["user_id"] = {
            "description": "Ordered user ID",
            "type": "string"
        }
        props["restaurant_id"] = {
            "description": "Order placed restaurant",
            "type": "string"
        }
        props["menu_id"] = {
            "description": "Ordered menu ID",
            "type": "string"
        }
        props["status"] = {
            "description": "Order status",
            "type": "string"
        }
        return schema

    # @staticmethod
    # def get_schema():
    #     """
    #     method to get schema
    #     """
    #     schema = {
    #         "type": "object"
    #         # "required": ["user_id"]
    #     }
    #     props = schema["properties"] = {}
    #     props["user_id"] = {
    #         "description": "User_id",
    #         "type": "string"
    #     }
    #     # props["restaurant_id"] = {
    #     #     "description": "Restaurant id",
    #     #     "type": "string"
    #     # }
    #     props["menu_id"] = {
    #         "description": "Menu id",
    #         "type": "string"
    #     }
    #     props["qty"] = {
    #         "description": "Quantity",
    #         "type": "string"
    #     }
    #     return schema

    def serialize(self):
        role = {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "restaurant_id": str(self.restaurant_id),
            "menu_id": str(self.menu_id),
            "quantity": self.qty,
            "status": self.status
        }
        return role


class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    restaurant_id = Column(ForeignKey('restaurant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    date = Column(Date, nullable=False)
    from_time = Column(Time, nullable=False)
    to_time = Column(Time, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    description = Column(Integer)

    restaurant = relationship('Restaurant')
    user = relationship('User')

    @staticmethod
    def get_schema():
        """
        method to get schema
        """
        schema = {
            "type": "object",
            "required": ["user_id", "date", "from_time", "to_time"]
        }
        props = schema["properties"] = {}
        props["user_id"] = {
            "description": "Reserved user ID",
            "type": "string"
        }
        props["date"] = {
            "description": "Reserved date",
            "type": "string"
        }
        props["from_time"] = {
            "description": "Reservation start time",
            "type": "string"
        }
        props["to_time"] = {
            "description": "Reservation end time",
            "type": "string"
        }
        props["description"] = {
            "description": "Reservation description",
            "type": "string"
        }
        return schema

    def serialize(self):
        role = {
            "name": self.user.name,
            "contact_no": self.user.contact_no,
            "date": self.date.strftime("%m/%d/%Y"),
            "from_time": self.from_time.strftime("%H:%M:%S"),
            "to_time": self.to_time.strftime("%H:%M:%S"),
            "restaurant_name": self.restaurant.name,
            "restaurant_address": self.restaurant.address,
            "restaurant_contact_no": self.restaurant.contact_no
        }
        return role


