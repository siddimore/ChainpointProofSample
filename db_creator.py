from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///documents.db', echo=True)
Base = declarative_base()

#
# class Artist(Base):
#     __tablename__ = "artists"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#
#     def __repr__(self):
#         return "{}".format(self.name)


class Document(Base):
    """"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    ownerName = Column(String)
    title = Column(String)


# create tables
Base.metadata.create_all(engine)
