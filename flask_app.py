#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------



app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Catalogo:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        print(host)
        print(user)
        print(database)
        print(input"mostrar los datos")
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
            print(input"una tecla")

        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS opcion_menu (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL
            )''')
        self.conn.commit()



        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    #----------------------------------------------------------------
    def agregar_menu(self, descripcion, precio):

        sql = "INSERT INTO opcion_menu (descripcion, precio) VALUES (%s, %s)"
        valores = (descripcion, precio)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid

    #----------------------------------------------------------------
    def consultar_menu(self, codigo):
        # Consultamos un menu a partir de su código
        self.cursor.execute(f"SELECT * FROM opcion_menu WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def modificar_menu(self, codigo, nueva_descripcion, nuevo_precio):
        sql = "UPDATE opcion_menu SET descripcion = %s, precio = %s WHERE codigo = %s"
        valores = (nueva_descripcion, nuevo_precio, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def listar_menu(self):
        self.cursor.execute("SELECT * FROM opcion_menu")
        opcion_menu = self.cursor.fetchall()
        return opcion_menu

    #----------------------------------------------------------------
    def eliminar_menu(self, codigo):
        # Eliminamos un menu de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM opcion_menu WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def mostrar_menu(self, codigo):
        # Mostramos los datos del menu a partir de su código
        menu = self.consultar_menu(codigo)
        if menu:
            print("-" * 40)
            print(f"Código.....: {menu['codigo']}")
            print(f"Descripción: {menu['descripcion']}")
            print(f"Precio.....: {menu['precio']}")
            print("-" * 40)
        else:
            print("Menu no encontrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
#const URL = "https://andreag.pythonanywhere.com/"
#Database host address:andreag.mysql.pythonanywhere-services.com
#Username:andreag
#Name:andreag$default
#catalogo = Catalogo(host='localhost', user='root', password='', database='menu')

catalogo = Catalogo(host='andreag.mysql.pythonanywhere-services.com', user='andreag', password='pampa2024', database='andreag$menu')


# Carpeta para guardar las imagenes.
#RUTA_DESTINO = './static/imagenes/'

#Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
RUTA_DESTINO = '/home/andreag/cafeteria22/static/imagenes'


#--------------------------------------------------------------------
# Listar todos los menues
#--------------------------------------------------------------------
#La ruta Flask /menu con el método HTTP GET está diseñada para proporcionar los detalles de todos los menues almacenados en la base de datos.
#El método devuelve una lista con todos los menues en formato JSON.
@app.route("/menu", methods=["GET"])
def listar_menu():
    opcion_menu = catalogo.listar_menu()
    return jsonify(opcion_menu)


#--------------------------------------------------------------------
# Mostrar un sólo menu según su código
#--------------------------------------------------------------------
#La ruta Flask /menu/<int:codigo> con el método HTTP GET está diseñada para proporcionar los detalles de un menu específico basado en su código.
#El método busca en la base de datos el menu con el código especificado y devuelve un JSON con los detalles del menu si lo encuentra, o None si no lo encuentra.
@app.route("/menu/<int:codigo>", methods=["GET"])
def mostrar_menu(codigo):
    menu = catalogo.consultar_menu(codigo)
    if menu:
        return jsonify(menu), 201
    else:
        return "Menu no encontrado", 404


#--------------------------------------------------------------------
# Agregar un menu
#--------------------------------------------------------------------
@app.route("/menu", methods=["POST"])
#La ruta Flask `/menues` con el método HTTP POST está diseñada para permitir la adición de un nuevo menu a la base de datos.
#La función menu se asocia con esta URL y es llamada cuando se hace una solicitud POST a /menues.
def agregar_menu():
    #Recojo los datos del form
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    nombre_imagen=""



    nuevo_codigo = catalogo.agregar_menu(descripcion, precio)
    if nuevo_codigo:


        #Si el menu se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "Menu agregado correctamente.", "codigo": nuevo_codigo}), 201
    else:
        #Si el menu no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar el menu."}), 500


#--------------------------------------------------------------------
# Modificar un menu según su código
#--------------------------------------------------------------------
@app.route("/menu/<int:codigo>", methods=["PUT"])
#La ruta Flask /menu/<int:codigo> con el método HTTP PUT está diseñada para actualizar la información de un menu existente en la base de datos, identificado por su código.
#La función menu se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /menues/ seguido de un número (el código del menu).
def modificar_menu(codigo):
    #Se recuperan los nuevos datos del formulario
    nueva_descripcion = request.form.get("descripcion")
    nuevo_precio = request.form.get("precio")





    # Se llama al método modificar_menu pasando el codigo del menu y los nuevos datos.
    if catalogo.modificar_menu(codigo, nueva_descripcion, nuevo_precio):

        #Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Menu modificado"}), 200
    else:
        #Si el menu no se encuentra (por ejemplo, si no hay ningún menu con el código dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Menu no encontrado"}), 404



#--------------------------------------------------------------------
# Eliminar un menu según su código
#--------------------------------------------------------------------
@app.route("/menu/<int:codigo>", methods=["DELETE"])
#La ruta Flask /menu/<int:codigo> con el método HTTP DELETE está diseñada para eliminar un menu específico de la base de datos, utilizando su código como identificador.
#La función eliminar_menu se asocia con esta URL y es llamada cuando se realiza una solicitud DELETE a /menu/ seguido de un número (el código del menu).
def eliminar_menu(codigo):
    # Busco el menu en la base de datos
    menu = catalogo.consultar_menu(codigo)
    if menu: # Si el menu existe, verifica si hay una imagen asociada en el servidor.
            # Luego, elimina el menu del catálogo
        if catalogo.eliminar_menu(codigo):
            #Si el menu se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Menu eliminado"}), 200
        else:
            #Si ocurre un error durante la eliminación (por ejemplo, si el menu no se puede eliminar de la base de datos por alguna razón), se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar el menu"}), 500
    else:
        #Si el menu no se encuentra (por ejemplo, si no existe un menu con el codigo proporcionado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Menu no encontrado"}), 404

#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)