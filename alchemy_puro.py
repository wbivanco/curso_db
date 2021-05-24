from datetime import datetime
from sqlalchemy import create_engine

from sqlalchemy import MetaData # Catalogo de tablas, puente entre la tabla y el gestor
from sqlalchemy import Table, Column, Integer, String, DateTime # Permite manipular las tablas

engine = create_engine('postgresql://postgres:12345678@localhost/curso_bd')
metadata = MetaData()

# Defino el nombre de la tabla: users
users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(), index=True, nullable=False),
    Column('email', String(), nullable=False),
    Column('created_at', DateTime(), default=datetime.now),
)

if __name__ == '__main__':
    metadata.drop_all(engine) # Borra todas las tablas
    metadata.create_all(engine) # Crea todas las tablas

    print(users) # Muetsra el nombre de la tabla
    print(users.c) # Muestra el nombre de los campos de la tabla
    print(users.c.id) # Muestra el campo id de tabla