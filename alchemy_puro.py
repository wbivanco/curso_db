import json
from datetime import datetime

from sqlalchemy import create_engine

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, DateTime, Float, ForeignKey

from sqlalchemy import select

engine = create_engine('postgresql://postgres:12345678@localhost/curso_bd')
metadata = MetaData()

orders = Table(
    'orders',
    metadata,
    Column('id', Integer(), primary_key=True),
)

products = Table(
    'products',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('title', String()),
    Column('price', Float(5,2)),
    Column('order_id', ForeignKey('orders.id'))
)

if __name__ == '__main__':
    metadata.drop_all(engine)
    metadata.create_all(engine)

    with engine.connect() as connection:

        # Orden
        query_insert = orders.insert()
        connection.execute(query_insert)

        # Productos
        query_insert = products.insert().values(
            title='IPhone',
            price=500.50,
            order_id=1
        )
        connection.execute(query_insert)

        query_insert = products.insert().values(
            title='IPad',
            price=800.00,
            order_id=1
        )
        connection.execute(query_insert)

        query_insert = products.insert().values(
            title='MacBook',
            price=2000.50,
            order_id=1
        )
        connection.execute(query_insert)

        query_select = select(
            [
                products.c.title,
                products.c.price
            ]
        ).select_from(
            orders.join(products)
        ).where(
            orders.c.id == 1
        )

        print(query_select)

        result = connection.execute(query_select)

        for product in result.fetchall():
            print(product.title, product.price)