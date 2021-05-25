import json
from datetime import datetime
from sqlalchemy import create_engine

from sqlalchemy import MetaData # Catalogo de tablas, puente entre la tabla y el gestor
from sqlalchemy import Table, Column, Integer, String, DateTime # Permite manipular las tablas
from sqlalchemy import select # Permite hacer consultas personalizadas

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

            ## Primer método para select, método select hace sobre *(todos los campos)
            ## SELECT * FROM users WHERE country = 'Argentina'
            query_select = users.select(users.c.country == "Argentina")

            ## Segundo método para hacer select, funcción select hace sobro los campos que quiero
            ## SELECT id, email, nam FORM users WHERE country = 'Argentina'
            # query_select = select([
            #     users.c.id,
            #     users.c.email,
            #     users.c.name
            # ]).where(
            #     users.c.country == "Argentina"
            # )

            print(query_select) # Imprimo la consulta

            result = connection.execute(query_select)
            for user in result.fetchall():
                print(user.name)