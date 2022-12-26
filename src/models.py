from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from src.utils.dbUtil import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)
    password = Column(String, default='pswd')
    role = Column(String, default='user')
    is_active = Column(Boolean, default=False)
    tfa_enabled = Column(Boolean, default=False)
    tfa_secret = Column(String)
    created_on = Column(DateTime(timezone=False), default=datetime.now())
    updated_on = Column(DateTime(timezone=False), default=datetime.now())

class Blacklists(Base):
    __tablename__ = 'blacklists'

    token = Column(String, primary_key=True)
    email = Column(String)

class Codes(Base):
    __tablename__ = 'codes'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    reset_code = Column(String)
    status = Column(Boolean, default=True)
    expired_in = Column(DateTime(timezone=False), default=datetime.now())