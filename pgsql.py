import psycopg2

DROP_TABLE_USERS = "DROP TABLE IF EXISTS users"

USERS_TABLE = """ CREATE TABLE users(
    id SERIAL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) """

users = [
    ("usuario1", "clave1", "mail1@mail.com"),
    ("usuario2", "clave2", "mail2@mail.com"),
    ("usuario3", "clave3", "mail3@mail.com"),
    ("usuario4", "clave4", "mail4@mail.com"),
    ("usuario5", "clave5", "mail5@mail.com"),
]

if __name__ == '__main__':
    try:
        connect = psycopg2.connect("dbname='curso_bd' user='postgres' password='12345678' host='127.0.0.1' ")

        with connect.cursor() as cursor:
            cursor.execute(DROP_TABLE_USERS)
            cursor.execute(USERS_TABLE)

            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.executemany(query, users)
            connect.commit()

            query = "DELETE FROM users WHERE id = 3"
            cursor.execute(query, (3,))
            connect.commit()

            query = "SELECT * FROM users"
            cursor.execute(query)

            for user in cursor.fetchall():
                print(user)

    except psycopg2.OperationalError as err:
        print('No fue posible realizar la conexión')
        print(err)
    finally:
        connect.close()
        print("Conexión finalizada de forma exitosa")