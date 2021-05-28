from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from sqlalchemy.orm.exc import NoResultFound

engine = create_engine('postgresql://postgres:12345678@localhost/curso_bd')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(), default=datetime.now())
    courses = relationship('Course', backref='user')

    def __str__(self):
        return self.username


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False, unique=True)
    user_id = Column(ForeignKey('users.id'))
    created_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.title


Session = sessionmaker(engine)
session = Session()

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    user1 = User(username='User1', email='emil1@mail.com')
    user2 = User(username='User2', email='emil2@mail.com')

    user1.courses.append(
        Course(title='Curso de Postgres')
    )

    user1.courses.append(
        Course(title='Curso de Django')
    )

    user1.courses.append(
        Course(title='Curso de Laravel')
    )

    session.add(user1)
    session.add(user2)
    session.commit()