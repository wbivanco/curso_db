from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime

engine = create_engine('postgresql://postgres:12345678@localhost/curso_bd')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.username

# Para poder relacionar una modelo con una conexion se usa sesiones
Session = sessionmaker(engine)
session = Session()

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    user1 = User(username='User1', email='user1@mail.com')
    user2 = User(username='User2', email='user2@mail.com')
    user3 = User(username='User3', email='user3@mail.com')

    session.add(user1)
    session.add(user2)
    session.add(user3)

    session.commit()

    # SELECT * FROM users
    # users = session.query(User).all()

    # SELECT * FROM users WHERE id >=2 AND username = 'User3', utilizo en query una clase y me devuelve una
    # instancia de la clase
    # users = session.query(User).filter(
    #     User.id >= 2
    # ).filter(
    #     User.username == 'User3'
    # )

    # SELECT id, username, email FROM users WHERE id >=2, utilizo en query argumentos y me devuelve tuplas
    # instancia de la clase
    users = session.query(User.id, User.username, User.email).filter(
        User.id >= 2
    )

    for user in users:
        print(user)