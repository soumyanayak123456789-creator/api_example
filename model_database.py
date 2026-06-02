from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__="posts"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    user_id=Column(Integer,ForeignKey("user_details.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("UserDetails")

class UserDetails(Base):
    __tablename__="user_details"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False, unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Votes(Base):
    __tablename__="votes"    
    user_id=Column(Integer,ForeignKey("user_details.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)