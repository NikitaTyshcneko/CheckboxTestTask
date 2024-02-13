from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, JSON
from sqlalchemy.ext.mutable import MutableDict
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


users = User.__table__


class Receipt(Base):
    __tablename__ = "receipts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    rest = Column(Float, nullable=False)
    payment_type = Column(String, nullable=False)
    payment_amount = Column(Float, nullable=False)
    products = Column(JSON)


receipts = Receipt.__table__
