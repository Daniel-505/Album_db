from flask import Flask, redirect, url_for, flash, request, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = '123456'

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


@app.route('/', methods=['GET', 'POST'])
def formulario():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        Año_lanzamiento = request.form.get('Año_lanzamiento')
        genero = request.form.get('genero')

        if not titulo or not Año_lanzamiento or not genero:
            flash('Completa todos los campos.')
            return redirect(url_for('formulario'))
        
        cursor.execute('INSERT INTO Albums (titulo, Año_lanzamiento, genero) VALUES (%s, %s, %s)', (titulo, Año_lanzamiento, genero))

        connection.commit()
        flash('Álbum agregado exitosamente.')
    
    cursor.execute('SELECT * FROM Albums')
    albums = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', albums=albums)


@app.route('/eliminar_album/<int:id_album>', methods=['POST'])
def eliminar_album(id_album):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Primero eliminar las canciones asociadas al álbum
        cursor.execute('DELETE FROM Canciones WHERE id_album = %s', (id_album,))
        connection.commit()
        
        # Ahora eliminar el álbum
        cursor.execute('DELETE FROM Albums WHERE id_album = %s', (id_album,))
        connection.commit()
        
        flash('Álbum y sus canciones relacionadas eliminados exitosamente.')
    except Error as e:
        flash(f'Error al eliminar el álbum: {e}')
    
    cursor.close()
    connection.close()
    return redirect(url_for('formulario'))



@app.route('/editar_album/<int:id_album>', methods=['GET', 'POST'])
def editar_album(id_album):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        nuevo_titulo = request.form.get('nuevo_titulo')
        nuevo_Año_lanzamiento = request.form.get('nuevo_Año_lanzamiento')
        nuevo_genero = request.form.get('nuevo_genero')

        if not nuevo_titulo or not nuevo_Año_lanzamiento or not nuevo_genero:
            flash('Completa todos los campos.')
            return redirect(url_for('editar_album', id_album=id_album))
        
        cursor.execute(
            'UPDATE Albums SET titulo = %s, Año_lanzamiento = %s, genero = %s WHERE id_album = %s',
            (nuevo_titulo, nuevo_Año_lanzamiento, nuevo_genero, id_album)
        )
        connection.commit()
        flash('Álbum actualizado exitosamente.')
        cursor.close()
        connection.close()
        return redirect(url_for('formulario'))

    cursor.execute('SELECT * FROM Albums WHERE id_album = %s', (id_album,))
    album = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('editar.html', album=album)


@app.route('/canciones/<int:id_album>', methods=['GET', 'POST'])
def gestionar_canciones(id_album):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        duracion = request.form.get('duracion')
        numero_pista = request.form.get('numero_pista')
        fecha_lanzamiento = request.form.get('fecha_lanzamiento')

        if not titulo or not duracion or not numero_pista or not fecha_lanzamiento:
            flash('Completa todos los campos.')
            return redirect(url_for('gestionar_canciones', id_album=id_album))

        cursor.execute(
            'INSERT INTO Canciones (id_album, titulo, duracion, numero_pista, fecha_lanzamiento) VALUES (%s, %s, %s, %s, %s)',
            (id_album, titulo, duracion, numero_pista, fecha_lanzamiento)  # Aquí pasamos id_album correctamente
        )
        connection.commit()
        flash('Canción agregada exitosamente.')

    cursor.execute('SELECT * FROM Canciones WHERE id_album = %s', (id_album,))
    canciones = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('canciones.html', canciones=canciones, id_album=id_album)


@app.route('/eliminar_cancion/<int:id_cancion>', methods=['POST'])
def eliminar_cancion(id_cancion):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Canciones WHERE id_cancion = %s', (id_cancion,))
    connection.commit()
    flash('Canción eliminada exitosamente.')
    cursor.close()
    connection.close()
    return redirect(request.referrer)


if __name__ == '__main__':
    app.run(debug=True)
