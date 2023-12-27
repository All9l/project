from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.declarative import declarative_base

db_url = "postgresql://Alla:2002@localhost:5432/Exam"
engine = create_engine(db_url)
Base = declarative_base()

class MySession(Base):
    __tablename__ = "session"
    id = Column(Integer, Sequence('less_id_seq'), primary_key=True)
    Professor = Column(String(50))
    DateSession = Column(Date)
    ControlType = Column(String)
    GroupId = Column(Integer, ForeignKey('groups.id'))
    Group = relationship('Group', back_populates='sessions')
    SubId = Column(Integer, ForeignKey('subjects.id'))
    Subject = relationship('Subject', back_populates='sessions')

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, Sequence('group_id_seq'), primary_key=True)
    Faculty = Column(String(50))
    GroupCode = Column(String(50))
    Course = Column(Integer)
    StudentsNum = Column(Integer)
    sessions = relationship('MySession', back_populates='Group')

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, Sequence('sub_id_seq'), primary_key=True)
    Name = Column(String(50))
    Hours = Column(Integer) 
    Department = Column(String(50))
    sessions = relationship('MySession', back_populates='Subject')

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
