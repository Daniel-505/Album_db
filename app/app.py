from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = '123456'

# Función para obtener conexión a la base de datos
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='10.9.120.5', 
            database='realdata',
            user='realdata',
            password='realdata111'
        )
        return connection
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# Función para ejecutar una consulta SQL y devolver los resultados
def fetch_data(query, params=None):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return jsonify({"error": "Error en la consulta SQL"}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta principal con un enlace a las demás secciones
@app.route("/")
def home():
    return render_template('index.html')

# ------------------------- Rutas para obtener listas de datos ---------------------------

@app.route("/albums")
def listar_albums():
    query = "SELECT * FROM Albums"
    albums = fetch_data(query)
    return render_template('albums.html', albums=albums)

@app.route("/artistas")
def listar_artistas():
    query = "SELECT * FROM Artistas"
    artistas = fetch_data(query)
    return render_template('artistas.html', artistas=artistas)

@app.route("/canciones")
def listar_canciones():
    query = "SELECT * FROM Canciones"
    canciones = fetch_data(query)
    return render_template('canciones.html', canciones=canciones)

@app.route("/miembros")
def listar_miembros():
    query = "SELECT * FROM Miembros"
    miembros = fetch_data(query)
    return render_template('miembros.html', miembros=miembros)

@app.route("/roles")
def listar_roles():
    query = "SELECT * FROM Roles"
    roles = fetch_data(query)
    return render_template('roles.html', roles=roles)

# ------------------------- Rutas para crear nuevos registros ---------------------------

@app.route("/api/albums", methods=["POST"])
def crear_album():
    data = request.get_json()
    nombre = data.get("nombre")
    artista_id = data.get("artista_id")
    fecha_lanzamiento = data.get("fecha_lanzamiento")

    query = """
        INSERT INTO Albums (nombre, artista_id, fecha_lanzamiento)
        VALUES (%s, %s, %s)
    """
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    cursor = connection.cursor()
    try:
        cursor.execute(query, (nombre, artista_id, fecha_lanzamiento))
        connection.commit()
        return jsonify({"resultado": "ok", "nombre": nombre})
    except Error as e:
        print(f"Error al crear álbum: {e}")
        return jsonify({"error": "Error al crear álbum"}), 500
    finally:
        cursor.close()
        connection.close()

# ------------------------- Rutas para eliminar registros ---------------------------

@app.route("/albums/<int:id>", methods=["DELETE"])
def borrar_album(id):
    query = "DELETE FROM Albums WHERE id_album = %s"
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    cursor = connection.cursor()
    try:
        cursor.execute(query, (id,))
        connection.commit()
        return jsonify({"resultado": "ok", "id": id})
    except Error as e:
        print(f"Error al borrar álbum: {e}")
        return jsonify({"error": "Error al borrar álbum"}), 500
    finally:
        cursor.close()
        connection.close()

# ------------------------- Rutas para modificar registros ---------------------------

@app.route("/albums/<int:id>", methods=["PUT"])
def modificar_album(id):
    data = request.get_json()
    nombre = data.get("nombre")
    artista_id = data.get("artista_id")
    fecha_lanzamiento = data.get("fecha_lanzamiento")

    query = """
        UPDATE Albums
        SET nombre = %s, artista_id = %s, fecha_lanzamiento = %s
        WHERE id_album = %s
    """
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    cursor = connection.cursor()
    try:
        cursor.execute(query, (nombre, artista_id, fecha_lanzamiento, id))
        connection.commit()
        return jsonify({"resultado": "ok", "id": id})
    except Error as e:
        print(f"Error al modificar álbum: {e}")
        return jsonify({"error": "Error al modificar álbum"}), 500
    finally:
        cursor.close()
        connection.close()

# ------------------------- Otras Rutas de CRUD ---------------------------

# Similar para las tablas Artistas, Canciones, Miembros y Roles:
# Asegúrate de definir las rutas de **POST**, **DELETE**, **PUT** para cada tabla.
# Puedes seguir el patrón mostrado en las rutas anteriores.


@app.route('/api/albums', methods=['GET'])
def albumsss():
    query = "SELECT * FROM Albums"
    albums = fetch_data(query)
    return jsonify(albums)

@app.route('/albumss', methods=['GET', 'POST'])
def albums_POST():
    if request.method == 'POST':
        # Obtener los valores del formulario
        titulo = request.form.get('titulo')
        Año_lanzamiento = request.form.get('Año_lanzamiento')
        genero = request.form.get('genero')

        # Validar que los campos no estén vacíos
        if not titulo or not Año_lanzamiento or not genero:
            flash('Es obligatorio llenar todos los campos')
            return redirect(url_for('albums_POST'))  # Redirige de nuevo al formulario para corregirlo

        # Validar que el año de lanzamiento sea un número entero
        try:
            Año_lanzamiento = int(Año_lanzamiento)  # Intenta convertir a entero
        except ValueError:
            flash('El año de lanzamiento debe ser un número entero válido.')
            return redirect(url_for('albums_POST'))  # Redirige al formulario si la conversión falla

        # Conectar a la base de datos y ejecutar la consulta de inserción
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO Albums (titulo, Año_lanzamiento, genero) VALUES (%s, %s, %s)', 
                (titulo, Año_lanzamiento, genero)
            )
            connection.commit()  # Confirmar los cambios en la base de datos
        except Error as e:
            flash(f'Error al agregar el álbum: {e}')
            return redirect(url_for('albums_POST'))
        finally:
            cursor.close()  # Cerrar el cursor
            connection.close()  # Cerrar la conexión

        # Redirigir a la página de listado de álbumes después de la inserción
        flash('Álbum creado exitosamente')
        return redirect(url_for('index'))  # Redirige a la página donde se muestran los álbumes

    # Si la petición es GET, mostrar el formulario para agregar álbum
    return render_template('POST-album.html')



@app.route('/album-db')
def index():
    # Conectar a la base de datos y obtener los álbumes
    connection = get_db_connection()
    albums = []
    if connection:
        cursor = connection.cursor()
        try:
            # Ejecutar la consulta para obtener los álbumes
            cursor.execute('SELECT titulo, Año_lanzamiento, genero FROM Albums')
            albums = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener los álbumes: {e}")
        finally:
            cursor.close()
            connection.close()

    # Pasar los álbumes a la plantilla
    return render_template('db-albums.html', albums=albums)

@app.route('/borar/int<int>', methods=['DELETE'])
def borrar(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Albums WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash('usuario eliminado correctamente')
    return redirect(url_for('formulario'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        if not nombre or not email:
            flash('Completa los campos.')
            return redirect(url_for('editar_usuario', id=id))
        cursor.execute('UPDATE usuario SET titulo = %s, Año_lanzamiento = %s, genero = %s WHERE id = %s', (nombre, email, id))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Usuario actualizado correctamente.')
        return redirect(url_for('formulario'))
    
    # Recuperar los datos del usuario a editar
    cursor.execute('SELECT * FROM usuario WHERE id = %s', (id,))
    usuario = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('editar.html', usuario=usuario)


if __name__ == "__main__":
    app.run(debug=True)
