import uuid
import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, SmallInteger, String, Time, \
    create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    address = Column(String(255))
    contact_no = Column(String(15))
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=False)


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
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    restaurant = relationship('Restaurant')


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    restaurant_id = Column(ForeignKey('restaurant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    status = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    restaurant = relationship('Restaurant')


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
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    menu = relationship('Menu')
    restaurant = relationship('Restaurant')
    user = relationship('User')


class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    restaurant_id = Column(ForeignKey('restaurant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    date = Column(Date, nullable=False)
    from_time = Column(Time, nullable=False)
    to_time = Column(Time, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    description = Column(Integer)

    restaurant = relationship('Restaurant')
    user = relationship('User')


engine = create_engine('postgresql://postgres:1234@localhost/hm1')
Base.metadata.create_all(engine)
