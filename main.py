import pymysql
from decouple import config

DROP_TABLE_USERS = "DROP TABLE IF EXISTS users"

USERS_TABLE = """ CREATE TABLE users(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) """


""" 
Creo variables de entorno con la consola del sistema operativo escribiendo:
export USER_MYSQL=root
export PASSWORD_MYSQL=
export DB_MYSQL=pythondb
"""

users = [
    ("usuario1", "clave1", "mail1@mail.com"),
    ("usuario2", "clave2", "mail2@mail.com"),
    ("usuario3", "clave3", "mail3@mail.com"),
    ("usuario4", "clave4", "mail4@mail.com"),
]


if __name__ == '__main__':
    try:
        connect = pymysql.Connect(host='localhost',
                                  port=3306,
                                  user=config('USER_MYSQL'),
                                  passwd=config('PASSWORD_MYSQL'),
                                  db=config('DB_MYSQL'))

        with connect.cursor() as cursor:
            cursor.execute(DROP_TABLE_USERS)
            cursor.execute(USERS_TABLE)

            ##### Forma1 #####
            # query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            # values = ("walter", "clave123", "mail@mail.com")
            # cursor.execute(query, values)

            ##### Forma 2 #####
            # query = "INSERT INTO users (username, password, email) VALUES ('walter', 'clave123', 'mail@mail.com')"

            ##### Forma 3 #####
            # query = "INSERT INTO users (username, password, email) VALUES ('{}', '{}', '{}')".format(
            #     "walter",
            #     "clave123",
            #     "mail@mail.com"
            # )

            ##### Forma 4 #####
            # username = "walter"
            # password = "clave123"
            # email = "mail@mail.com"
            # query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')"

            ##### Clase 8 #####
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"

            ##### Clase 8 - forma 1 #####
            # for user in users:
            #     cursor.execute(query, users)

            ##### Clase 8 - Forma 2 #####
            cursor.executemany(query, users)

            # El metodo commit se llama solo cuando se desea hacer modificaciones en la BD, para los SELECT no
            connect.commit()

            query = "SELECT * FROM users WHERE id >= 3"
            rows = cursor.execute(query)
            print(rows) # Devuelve un número
            for user in cursor.fetchall():  # Fetchall devuelve una tupla con tuplas que son los registros
                print(user)

            ##### Limitar forma 1 #####
            query = "SELECT * FROM users LIMIT 3"
            rows = cursor.execute(query)
            for user in cursor.fetchall():
                print(user)

            ##### Limitar forma 2 #####
            query = "SELECT * FROM users"
            rows = cursor.execute(query)
            for user in cursor.fetchmany(3):
                print(user)

            ##### Limitar forma 3 #####
            query = "SELECT * FROM users"
            rows = cursor.execute(query)
            user = cursor.fetchone()
            print(user)

            query = "UPDATE users SET username = %s WHERE id = %s"
            values = ("Cambio de nombre", 1)
            cursor.execute(query, values)
            connect.commit()

        print("Conexión realizada de forma exitosa")
    except pymysql.err.OperationalError as err:
        print('No fue posible realizar la conexión')
        print(err)
    finally:
        connect.close()

        print("Conexión finalizada de forma exitosa")