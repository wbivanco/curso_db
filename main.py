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

        print("Conexión realizada de forma exitosa")
    except pymysql.err.OperationalError as err:
        print('No fue posible realizar la conexión')
        print(err)
    finally:
        connect.close()

        print("Conexión finalizada de forma exitosa")