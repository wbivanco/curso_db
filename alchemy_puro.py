import json
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
    Column('age', Integer),
    Column('country', String(20), nullable=False),
    Column('email', String(50), nullable=False),
    Column('gender', String(6), nullable=False),
    Column('name', String(50), nullable=False),
)

if __name__ == '__main__':
    metadata.drop_all(engine) # Borra todas las tablas
    metadata.create_all(engine) # Crea todas las tablas

    # print(users) # Muetsra el nombre de la tabla
    # print(users.c) # Muestra el nombre de los campos de la tabla
    # print(users.c.id) # Muestra el campo id de tabla

    with engine.connect() as connection:

        query_insert = users.insert()

        with open('users.json') as file:
            usuarios= json.load(file)
            ## Forma optima de hacer el insert, hace un batch con los usuarios uan sola vez
            connection.execute(query_insert, usuarios)

            query_select = users.select()
            result = connection.execute(query_select) # ResultProxy
            for user in result.fetchall():
                print(user.name) # RowProxy

            ## Forma no tan correcta porque hacer un insert por cada usuario
            # for user in users:
            #     query = query_insert.values(**user)
            #     connection.execute(query)
