import psycopg2

DROP_USERS_TABLE = "DROP TABLE IF EXISTS users"

USERS_TABLE = """ CREATE TABLE users(
    id SERIAL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""

def create_user(connect, cursor):
    """ A) Crear Usario"""

    username = input("Ingrese un username: ")
    email = input("Ingrese un email: ")

    query = "INSERT INTO users(username, email)  VALUES(%s, %s)"
    values = (username, email)

    cursor.execute(query, values)
    connect.commit()

    print("Usuario creado")

def list_users(connect, cursor):
    """ B) Listar usuarios"""

    print("Listado de usuarios")

def update_user(connect, cursor):
    """ C) Actualizar Usuario"""

    print("Usuario modificado")

def delete_user(connect, cursor):
    """ D) Eliminar usuario"""

    print("Usuario eliminado")

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
            cursor.execute(DROP_USERS_TABLE)
            cursor.execute(USERS_TABLE)
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
