import json
from sqlalchemy import create_engine

from sqlalchemy import MetaData # Catalogo de tablas, puente entre la tabla y el gestor
from sqlalchemy import Table, Column, Integer, String, DateTime # Permite manipular las tablas

from sqlalchemy import select # Permite hacer consultas personalizadas
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy import and_, or_, not_

from sqlalchemy import asc, desc

engine = create_engine('postgresql://postgres:12345678@localhost/curso_bd')
metadata = MetaData()

# Defino el nombre de la tabla: users
users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('age', Integer),
    Column('country', String(20), nullable=False),
    Column('email', String(50), nullable=False),
    Column('gender', String(6), nullable=False),
    Column('name', String(50), nullable=False),
)

if __name__ == '__main__':
    metadata.drop_all(engine) # Borra todas las tablas
    metadata.create_all(engine) # Crea todas las tablas

    with engine.connect() as connection:

        query_insert = users.insert()

        with open('users.json') as file:
            usuarios= json.load(file)
            connection.execute(query_insert, usuarios)

            ## Forma 1
            # query_delete = users.delete(users.c.id==1)

            ## Forma 2
            query_delete = delete(users).where(users.c.id==1)

            result = connection.execute(query_delete)
            print(result.rowcount)

            query_select = select([users.c.id, users.c.name]).where(users.c.id==1)
            result = connection.execute(query_select)
            user = result.fetchone()
            if user:
                print(user.name)
            else:
                print("No fue posible obtener el usuario!")