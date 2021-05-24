import os
import psycopg2

DROP_USERS_TABLE = "DROP TABLE IF EXISTS users"

USERS_TABLE = """ CREATE TABLE users(
    id SERIAL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""

def system_clear(function):
    def wrapper(connect, cursor):
        os.system("clear")
        function(connect, cursor)
        input("")
        os.system("clear")
    wrapper.__doc__ = function.__doc__
    return wrapper

def user_exists(function):
    def wrapper(connect, cursor):
        id = input("Ingrese el id del usuario a actualizar: ")

        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (id,))
        user = cursor.fetchone()

        if user:
           function(id, connect, cursor)
        else:
            print("no existe un usuario con ese id, intenta de nuevo.")

    wrapper.__doc__ = function.__doc__
    return wrapper

@system_clear
def create_user(connect, cursor):
    """ A) Crear Usario"""

    username = input("Ingrese un username: ")
    email = input("Ingrese un email: ")

    query = "INSERT INTO users(username, email)  VALUES(%s, %s)"
    values = (username, email)

    cursor.execute(query, values)
    connect.commit()

    print(">>>> Usuario creado exitosamente")

@system_clear
def list_users(connect, cursor):
    """ B) Listar usuarios"""

    query = "SELECT id, username, email FROM users"
    cursor.execute(query)

    for id, username, email in cursor.fetchall():
        print(id, '-', username, '-', email)

    print(">>>> Listado de usuarios")

@system_clear
@user_exists
def update_user(id, connect, cursor):
    """ C) Actualizar Usuario"""

    username = input("Ingresa un nuevo username: ")
    email = input("Inrese un nuevo email: ")

    query = "UPDATE users SET username = %s, email = %s WHERE id = %s "
    values = (username, email, id)
    cursor.execute(query, values)
    connect.commit()
    print(">>>> Usuario actualizado exitosamente!")

@system_clear
@user_exists
def delete_user(id, connect, cursor):
    """ D) Eliminar usuario"""

    query = "DELETE FROM users WHERE id = %s "
    cursor.execute(query, (id, ))
    connect.commit()
    print(">>>> Usuario eliminado exitosamente!")

def default(*args):
    print("Opción no valida!")

if __name__ == '__main__':
    options = {
        'a': create_user,
        'b': list_users,
        'c': update_user,
        'd': delete_user
    }

    try:
        connect = psycopg2.connect("postgresql://postgres:12345678@127.0.0.1/curso_bd")

        with connect.cursor() as cursor:
            # cursor.execute(DROP_USERS_TABLE)
            # cursor.execute(USERS_TABLE)
            connect.commit()

            while True:
                for function in options.values():
                    print(function.__doc__)

                print("quit para salir")

                option = input("Seleccione una opción válida: ").lower()

                if option == "quit" or option == "q":
                    break

                function = options.get(option, default)
                function(connect, cursor)

    except psycopg2.OperationalError as err:
        print("No fue posible realizar la conexion")
        print(err)
